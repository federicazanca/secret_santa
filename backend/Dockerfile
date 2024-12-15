FROM python:3.9.18-slim-bullseye

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

CMD ["uvicorn", "main:santapp", "--host", "0.0.0.0", "--reload"]