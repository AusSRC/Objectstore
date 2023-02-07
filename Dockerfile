FROM ubuntu

RUN apt update && apt upgrade -y
RUN apt install curl vim sudo -y
RUN adduser --disabled-password --gecos "" aussrc
RUN usermod -aG sudo aussrc

ARG DEBIAN_FRONTEND=noninteractive 
ENV TZ="Australia/Perth" 
RUN ln -snf "/usr/share/zoneinfo/$TZ" /etc/localtime
RUN echo "$TZ" > /etc/timezone
RUN apt -y install tzdata
RUN apt install python3 python3-scipy python3-pip python3-matplotlib -y
RUN pip3 install astropy corner boto3 requests

ADD example* /home/aussrc/objectstore/
ADD * /usr/local/lib/python3.10/dist-packages/objectstore/
RUN chown -R aussrc:aussrc /home/aussrc
RUN mkdir -p /mnt/config







