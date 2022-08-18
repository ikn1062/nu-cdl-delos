from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def home(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


@app.get("/initiate")
def initiate():
    return {"Microservice is successfully triggered"}
