FROM python:3.8

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8080

#CMD [ "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8080"]

CMD ["python", "./app/main.py"]