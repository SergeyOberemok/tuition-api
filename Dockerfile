FROM ubuntu:22.04

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y python3 python3-pip

COPY ./arithmetical-tuition-api/requirements.txt .
RUN pip install -r requirements.txt

COPY ./arithmetical-tuition-api ./

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["assessment_flask_app.py"]