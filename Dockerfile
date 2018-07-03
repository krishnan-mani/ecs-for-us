FROM python:3.6-alpine

WORKDIR /app

COPY requirements.txt /app
COPY example.py /app

RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["/app/example.py"]
