FROM python:3
ENV PYTHONUNBUFFERED 1
RUN apt-get install -y default-libmysqlclient-dev
RUN mkdir /code
RUN mkdir /code/requirements
WORKDIR /code
COPY requirements/* /code/requirements/
RUN pip install --upgrade pip
RUN pip install -r requirements/base.txt
COPY . /code/
