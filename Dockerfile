FROM python:3.9.7

ADD dinning_hall.py .

ADD config.py .

RUN pip install requests flask

EXPOSE 8000

CMD ["python", "-u", "dinning_hall.py"]