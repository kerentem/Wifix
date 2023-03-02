from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def func():
    return { "key": "value" }