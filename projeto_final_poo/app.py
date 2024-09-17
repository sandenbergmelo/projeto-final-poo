from fastapi import FastAPI

from projeto_final_poo.routers import address, client, schedules, services

app = FastAPI()
app.include_router(client.router)
app.include_router(services.router)
app.include_router(schedules.router)
app.include_router(address.router)


@app.get('/')
def root():
    return {'message': 'Hello, World!'}
