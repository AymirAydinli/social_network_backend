FROM python:3.9.19

WORKDIR /Users/Ay/Developer/DevOps/FASTAPI_DOCKER

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "uvicorn", "app.main:app","--host", "0.0.0.0", "--port", "8000"]