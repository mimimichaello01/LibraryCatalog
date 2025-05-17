from fastapi import FastAPI

from src.library_catalog.api.routers import book_router

app = FastAPI()
app.include_router(book_router)
