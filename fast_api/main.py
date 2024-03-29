from fastapi import FastAPI
from routers import products, users, basic_auth_users, jwt_auth_users, users_db
from fastapi.staticfiles import StaticFiles

# Start server: from uvicorn main:app --reload
# Stop server:  ctrl+c

# Standard server ->     http://127.0.0.1:8000
# Swagger documentation: http://127.0.0.1:8000/docs
# Redocly documentation: http://127.0.0.1:8000/redoc
# API json:              http://127.0.0.1:8000/openapi.json

app = FastAPI()

# routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "¡Hola FastAPI!"}

@app.get("/url")
async def url():
    return {"url_project": "https://github.com/JorgeAgulloM/fast_api_backend"}

# @app.get()
# @app.post()
# @app.put()
# @app.delete()
#
# @app.options()
# @app.head()
# @app.patch()
# @app.trace()