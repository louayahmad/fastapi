from database.database import db_dependency
from database.models import Choices, Questions
from endpoints.questions.models.struct import QuestionBase
from fastapi import APIRouter

router = APIRouter()


@router.post("/questions/")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = Choices(
            choice_text=choice.choice_text,
            is_correct=choice.is_correct,
            question_id=db_question.id,
        )
        db.add(db_choice)
    db.commit()
