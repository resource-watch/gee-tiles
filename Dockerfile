FROM python:3.11-bullseye
MAINTAINER info@vizzuality.com

ENV NAME geetiles
ENV USER geetiles

RUN apt-get -y update && apt-get -y upgrade && \
   apt-get install -y bash git \
   libffi-dev gcc python3-dev musl-dev

RUN addgroup $USER && adduser --shell /bin/bash --disabled-login --ingroup $USER $USER

RUN pip install --upgrade pip
RUN pip install gunicorn gevent

RUN mkdir -p /opt/$NAME
WORKDIR /opt/$NAME

COPY tox.ini /opt/$NAME/tox.ini
COPY requirements.txt /opt/$NAME/requirements.txt
COPY requirements_dev.txt /opt/$NAME/requirements_dev.txt
RUN pip install -r requirements.txt
RUN pip install -r requirements_dev.txt

COPY entrypoint.sh /opt/$NAME/entrypoint.sh
COPY main.py /opt/$NAME/main.py
COPY gunicorn.py /opt/$NAME/gunicorn.py

# Copy the application folder inside the container

COPY ./$NAME /opt/$NAME/$NAME
COPY tests /opt/$NAME/tests
RUN chown -R $USER:$USER /opt/$NAME

# Tell Docker we are going to use this ports
EXPOSE 5700
USER $USER

# Launch script
ENTRYPOINT ["./entrypoint.sh"]
