FROM python:3

WORKDIR /code

EXPOSE 5000
ENV FLASK_APP=/code/app_stack/app.py
ENV FLASK_RUN_HOST=0.0.0.0
#RUN apk add --no-cache gcc musl-dev linux-headers

RUN /usr/local/bin/pip install --user --no-cache-dir pymongo flask connexion[swagger-ui]

CMD ["python", "app_stack/app.py"]
