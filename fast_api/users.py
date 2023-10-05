from fastapi import FastAPI

# Start server: from uvicorn users:app --reload
# Stop server:  ctrl+c

app = FastAPI()

@app.get("/usersjson")
async def usersjson():
    return [{"name": "Jorge", "surname": "Agullo", "age": 40, "url": "https://github.com/JorgeAgulloM"},
            {"name": "Yorch", "surname": "Soft", "age": 1, "url": "https://softyorch.com"}]
