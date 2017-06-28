FROM ubuntu:latest
MAINTAINER jj
RUN DBEIAN_FRONTEND=noninteractive apt-get update && \
   apt-get install docker.io docker-compose -y && \
   apt-get clean autoclean && \
   apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
VOLUME /results/
RUN mkdir /app/
ADD . /app/
WORKDIR /results/
