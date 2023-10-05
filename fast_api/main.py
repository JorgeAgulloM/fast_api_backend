from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "¡Hola FastAPI!"}

@app.get("/url")
async def url():
    return {"url_project": "https://github.com/jorgeagullom/fast_api_backend"}
