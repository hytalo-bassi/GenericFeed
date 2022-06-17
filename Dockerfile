FROM python:3.10.5-buster
WORKDIR /usr/GenericFeed
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "GenericFeed"]

