FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN python -m pip install --upgrade pip
RUN pip install netmiko python-multipart fastapi uvicorn aiofiles

COPY ./app /app
COPY ./app/dist /app/
