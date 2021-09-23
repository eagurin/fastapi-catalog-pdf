FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /app

CMD gunicorn app.main:api -c config.py
