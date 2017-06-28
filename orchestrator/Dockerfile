FROM ubuntu:latest
MAINTAINER jj
RUN DBEIAN_FRONTEND=noninteractive apt-get update && \
   apt-get install docker.io python-virtualenv -y && \
   apt-get clean autoclean && \
   apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
# volumes make no sense in this case
#VOLUME /results/
RUN mkdir /app/ && cd /app/ && \
    virtualenv env && source env/bin/activate && \ 
    pip install docker-compose
ADD . /app/
RUN chmod +x /app/scripts/workflow.sh
CMD /app/scripts/workflow.sh

