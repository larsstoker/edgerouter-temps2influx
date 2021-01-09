FROM python:3.7-alpine
RUN mkdir /app
COPY app.py /app
COPY requirements.txt /app
WORKDIR /app
RUN apk update
RUN pip install -r requirements.txt
CMD python -u app.py