FROM python:2.7
RUN apt-get update
RUN apt-get install nodejs npm -y
RUN mkdir /app
WORKDIR /app
COPY ./ /app
RUN pip install virtualenv
RUN virtualenv env
RUN make
ENTRYPOINT /bin/bash