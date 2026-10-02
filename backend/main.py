from fastapi import FastAPI

import models  # noqa: F401  (registers the tables)
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="LaserLink")


@app.get("/health")
def health():
    return {"status": "ok"}