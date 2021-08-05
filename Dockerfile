FROM python:3.7

WORKDIR /usr/src/fastapi

COPY ./app ./app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
#EXPOSE 8080

#CMD [ "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8080"]

#CMD ["python", "app/main.py"]