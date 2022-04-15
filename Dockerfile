FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app /app
COPY ./app/dist /app/
