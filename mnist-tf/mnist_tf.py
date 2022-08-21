import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


def train_model():
    """
    Trains model to recognize whether digits are odd and even using mnist data
    - creates model file
    - prints training epochs and initial evaluation of model
    :return: None
    """
    # Loads MNIST data set
    (ds_train, ds_test), ds_info = tfds.load('mnist', split=['train', 'test'], shuffle_files=True, as_supervised=True,
                                             with_info=True, )
    print(ds_info)

    # Prepare the data sets for training
    ds_train = prepare_data(ds_train, "train", ds_info)
    ds_test = prepare_data(ds_test)

    # Create the model using make_model()
    model = make_model()
    print(model.summary())

    # Compile model
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss=tf.keras.losses.BinaryCrossentropy(),
        metrics=["accuracy"],)

    # Model fit and evaluation
    model.fit(ds_train, epochs=5)
    model.evaluate(ds_test, verbose=2)

    # Saving Model
    model.save('mnist-model/')


def rotate(image, label):
    """
    Rotate images
    :param image: image tensor
    :param label: label tensor
    :return: image rotated 180 degrees
    """
    return tf.image.rot90(image, k=2), label


def normalize_img(image, label):
    """
    Normalized image
    :param image: image tensor
    :param label: label tensor
    :return: Normalized image
    """
    return tf.cast(image, tf.float32) / 255., label


def make_model():
    """
    Creates CNN TF model and returns model
    :return: TF Model
    """
    model = keras.Sequential()
    model.add(layers.Input(shape=(28, 28, 1)))
    model.add(layers.Conv2D(28, (3, 3), padding='valid', activation='relu'))  # padding is a hyperparameter
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.25))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(0.25))
    model.add(layers.Dense(1, activation='sigmoid'))
    return model


def prepare_data(dataset, data_type="test", ds_info=None):
    """
    Prepares dataset for binary classification
    :param dataset: mnist dataset (tf dataset object)
    :param data_type: Type of data input
    :param ds_info: dataset info object from tf.tfds
    :return: Dataset for training and evaluation
    """
    # Makes labels binary
    dataset = dataset.map(lambda x, y: (x, tf.cast(y % 2, tf.float32)))

    # Rotates dataset and adds it to the original dataset
    dataset_rotated = dataset.map(rotate)
    dataset = dataset.concatenate(dataset_rotated)

    # Normalizes data and shuffles, uses caching and prefetch for performance
    dataset = dataset.map(normalize_img, num_parallel_calls=tf.data.AUTOTUNE)
    if data_type == "train":
        dataset.shuffle(ds_info.splits['train'].num_examples)
    dataset = dataset.batch(128)
    dataset = dataset.cache()
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    return dataset


def evaluate_model(show_errors=True):
    """
    Loads and evaluates trained model
    - Prints Model evaluation and plots images which resulted in errors
    :param show_errors: Show plot of error images
    :return: None
    """
    # Retrieves and prepares data
    (ds_train, ds_test), ds_info = tfds.load('mnist', split=['train', 'test'], shuffle_files=True, as_supervised=True,
                                             with_info=True, )
    ds_test = prepare_data(ds_test)

    # Loads and evaluates model
    model = keras.models.load_model('mnist-model/')
    model.evaluate(ds_test, verbose=2)

    map_result = {1: "odd", 0: "even"}

    if show_errors:
        # Gets the true and predicted values from test dataset
        y_true, y_pred = [], []
        images = []
        for image_batch, label_batch in ds_test:
            y_true.append(label_batch)
            y_pred.append((model.predict(image_batch) > 0.5).astype("float32"))
            images.append(image_batch)
        images = tf.concat([item for item in images], axis=0)
        true_labels = tf.concat([item for item in y_true], axis=0)
        predicted_labels = tf.concat([item for item in y_pred], axis=0)
        predicted_labels = tf.reshape(predicted_labels, (20000,))

        # Finds locations where true != predicted
        predicted_false = tf.where(true_labels != predicted_labels)

        # Creates list of random indexes for images
        rand_idx = np.random.randint(0, len(predicted_false), 10)

        # Plots images with labels
        f, ax = plt.subplots(1, 10, figsize=(50, 50))
        for ii, i in enumerate(rand_idx):
            idx = predicted_false[i]
            img = tf.reshape(tf.gather(images, idx), (28, 28)).numpy() * 255.0
            y_t = tf.gather(true_labels, idx).numpy()
            y_p = tf.gather(predicted_labels, idx).numpy()
            ax[ii].imshow(img, cmap='gray')
            ax[ii].set_title(f"predicted: {map_result[y_p[0]]}, true: {map_result[y_t[0]]}", fontsize=20)
        # plt.savefig('error_example.png')
        plt.show()


if __name__ == "__main__":
    train = input("Do you want to train the model? [y/n]\n")

    while train != "y" and train != "n":
        print("Invalid input, please write 'y' or 'n'")
        train = input("Do you want to train the model? [y/n]")

    if train == "y":
        train_model()

    evaluate_model(show_errors=True)

