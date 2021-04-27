FROM python:3.9

ADD source/requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY ./source/ /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["worker.py" ] 

