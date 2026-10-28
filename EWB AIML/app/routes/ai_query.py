from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/ai", tags=["Local AI (Ollama)"])

# Local, offline model served by `ollama serve`
llm = ChatOllama(model="llama3.2", temperature=0)

# Structured prompt template (system rules + user input)
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant. Use ONLY the following database records "
     "to answer user questions accurately and professionally. "
     "If the answer is not in the records, say you don't know.\n\n"
     "Database records:\n{db_records}"),
    ("human", "{question}"),
])

chain = prompt | llm


def format_records(students) -> str:
    if not students:
        return "No records found."
    return "\n".join(
        f"ID={s.id}, Name={s.name}, Email={s.email}, "
        f"Course={s.course}, Marks={s.marks}"
        for s in students
    )


@router.post("/query-ai")
def query_local_ai(body: schemas.AIQuery, db: Session = Depends(get_db)):
    """Answer a question using live records from the database."""
    records = format_records(db.query(models.Student).all())
    try:
        response = chain.invoke({"db_records": records,
                                 "question": body.question})
    except Exception as e:
        raise HTTPException(
            503,
            "Could not reach Ollama. Make sure `ollama serve` is running "
            f"and `ollama pull llama3.2` is done. Details: {e}",
        )
    return {"status": "success", "response": response.content}
