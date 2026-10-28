from fastapi import FastAPI
from .database import Base, engine
from .routes import students, ai_query

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student API with Local LLM (Ollama)")

app.include_router(students.router)
app.include_router(ai_query.router)


@app.get("/")
def root():
    return {"message": "API is running. Open /docs for Swagger UI."} 
