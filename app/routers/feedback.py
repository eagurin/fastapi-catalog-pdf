import os
import shutil
import uuid

from fastapi import (APIRouter, BackgroundTasks, Depends, File, Form,
                     HTTPException, UploadFile, status)
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from ..database import get_db
from ..models import Feedback
from ..schemas import EmailStr, FeedbackShow


conf = ConnectionConfig(
    MAIL_USERNAME="message@eagurin.ru",
    MAIL_PASSWORD="u0k%WZ3n",
    MAIL_FROM="message@eagurin.ru",
    MAIL_PORT=25,
    MAIL_SERVER="smtp.beget.com",
    MAIL_TLS=True,
    MAIL_SSL=False,
)

router = APIRouter()


@router.post(
    "/feedback/",
    response_model=FeedbackShow,
    status_code=status.HTTP_201_CREATED,
    tags=["Feedback"],
)
async def leave_feedback(
    title: str,
    subtitle: str,
    description: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    email: EmailStr = Form(...),
    db: Session = Depends(get_db),
) -> JSONResponse:

    if not file.filename[-3:].lower() == "pdf":
        raise HTTPException(status_code=415, detail="Unsupported Media Type")

    url = "./static/documents/" + str(uuid.uuid4()) + ".pdf"
    with open(url, "wb") as image:
        shutil.copyfileobj(file.file, image)
        size = os.path.getsize(url)
        if size > 15728640:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )

    new_feedback = Feedback(
        title=title, subtitle=subtitle, description=description, url=url
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)

    message = MessageSchema(
        subject="Feedback: " + title + " - " + subtitle,
        recipients=[email],
        body=description,
        attachments=[file],
    )
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)
    return JSONResponse(
        status_code=200, content={"message": "email has been sent"}
    )
