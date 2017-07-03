FROM ubuntu:latest
MAINTAINER jj
RUN DBEIAN_FRONTEND=noninteractive apt-get update && \
   apt-get install docker.io python-pip -y && \
   apt-get clean autoclean && \
   apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
# volumes make no sense in this case
#VOLUME /results/
RUN pip install docker-compose
ADD . /app/
# run tests
RUN chmod +x /app/scripts/workflow.sh && \
   cd /app/ &&  docker-compose build && docker-compose pull && 
   /app/scripts/workflow.sh
# process
RUN docker run --name back -v /results/:/results/ processor:latest && \
   docker run --volumes-from back processor:latest /bin/sh -c '/app/merger.py /results/5000/sql && /app/merger.py /results/10000/sql && /app/merger.py /results/1000/sql' && \
   docker run --volumes-from back processor:latest /bin/sh -c '/app/merger.py /results/5000/mongo && /app/merger.py /results/10000/mongo && /app/merger.py /results/1000/mongo' && \
   docker run --volumes-from back processor:latest /bin/sh -c '/app/merger.py /results/5000/neo && /app/merger.py /results/10000/neo && /app/merger.py /results/1000/neo'
# plots
RUN docker run --volumes-from back visualiser

