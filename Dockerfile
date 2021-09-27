FROM python:3.7.6

ADD dinning_hall.py .

ADD config.py .

CMD ["python", "./dinning_hall.py"]