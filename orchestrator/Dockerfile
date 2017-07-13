FROM ubuntu:latest
MAINTAINER j.rybicki@fz-juelich.de
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
RUN chmod +x /app/scripts/workflow.sh 
CMD cd /app/ &&  docker-compose build && docker-compose pull && \
   docker pull httpprincess/processor:1.0 && docker pull httpprincess/visualizer:1.0 && \
   /app/scripts/workflow.sh && \
  docker run --name back -v /results/:/results/ httpprincess/processor:1.0 && \
  docker run --volumes-from back httpprincess/processor:1.0 /bin/sh -c '/app/merger.py /results/5000/sql && /app/merger.py /results/10000/sql && /app/merger.py /results/1000/sql' && \
  docker run --volumes-from back httpprincess/processor:1.0 /bin/sh -c '/app/merger.py /results/5000/mongo && /app/merger.py /results/10000/mongo && /app/merger.py /results/1000/mongo' && \
  docker run --volumes-from back httpprincess/processor:1.0 /bin/sh -c '/app/merger.py /results/5000/neo && /app/merger.py /results/10000/neo && /app/merger.py /results/1000/neo' && \
  docker run --volumes-from back httpprincess/visualizer:1.0
