# ML Training
## Important Files
The two important files for this project include `mnist_tf.py` and the model files 
within `mnist-model/`. `mnist_tf.py` contains all the main function for training
and testing the tensorflow CNN model for binary classification (odd/even) of digits.
The model is saved, and can be loaded from `mnist-model/'.

## Installation 
To set up the environment to run the files, you can use conda environments, or 
python virtual environments. 

### Conda
To set up a conda environment:
```
conda create -n mnist python=3.10
conda activate mnist

conda install -c conda-forge tensorflow===2.7.0 tensorflow_datasets==1.2.0 matplotlib==3.5.1
```

### Python Venv

Alternatively, you can use the following if you have set up a regular python venv
```angular2html
pip install -r requirements.txt
```

## Running the Files

You can run the files with the following line in terminal

### Running the file
```angular2html
python -m mnist_tf
```

You will then be asked a prompt

### Training the model

```angular2html
Do you want to train the model? [y/n]
```

If you decide to train the model, reply with `y`. The MNIST files will be downloaded and the model
will be trained using the cnn described in `make_model()`. A model will then be created in `mnist-model/`.

The next step will be to evaluate the model, this will also happen if you reply with `n`.

### Evaluating the model

The model evaluation is run using the function `evaluate_model`. 

The model will return with the evaluation data (example shown below)

```angular2html
157/157 - 2s - loss: 0.6018 - accuracy: 0.8284 - 2s/epoch - 13ms/step
```

As well as an output showing examples of errors as a plot. 

