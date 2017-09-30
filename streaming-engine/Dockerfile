FROM python:2.7.13-alpine3.6

MAINTAINER Imre Nagi <imre.nagi2812@gmail.com>

ADD . /src

WORKDIR /src
ADD requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r /src/requirements.txt

CMD [ "python", "/src/src/StreamingMain.py" ]
