FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /
RUN pip install -r /requirements.txt
CMD python3 manage.py runserver 0.0.0.0:8000