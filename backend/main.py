from fastapi import FastAPI

import models  # noqa: F401  (registers the tables)
from auth_routes import router as auth_router
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LaserLink")
app.include_router(auth_router)


@app.get("/health")
def health():
    return {"status": "ok"}