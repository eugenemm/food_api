FROM python:3.10

RUN mkdir -p /var/lib/food_api

RUN mkdir /var/lib/food_api/logs

COPY ./requirements.txt  /var/lib/food_api

WORKDIR /var/lib/food_api

RUN /bin/bash -c 'pip3 install wheel && pip3 install -r ./requirements.txt'

COPY ./ /var/lib/food_api

RUN cp -rf ./vendor/* /usr/local

EXPOSE 49105

#CMD /bin/bash -c 'gunicorn --worker-class eventlet wsgi:app --timeout 0 --workers=1'

CMD /bin/bash -c 'python3 manage.py db upgrade && python3 apply_seeds.py && python server.py'

