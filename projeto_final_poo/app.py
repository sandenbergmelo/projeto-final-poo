from fastapi import FastAPI

from projeto_final_poo.routers import client, services

app = FastAPI()
app.include_router(client.router)
app.include_router(services.router)


@app.get('/')
def root():
    return {'message': 'Hello, World!'}
