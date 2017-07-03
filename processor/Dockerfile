FROM ubuntu:latest
MAINTAINER jj
RUN DBEIAN_FRONTEND=noninteractive apt-get update && \
   apt-get install python python-numpy -y && \
   apt-get clean autoclean && \
   apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
VOLUME /results/
RUN mkdir /app/
ADD . /app/
RUN chmod +x /app/spliter.sh /app/merger.py /app/mergeall.sh
WORKDIR /results/
CMD /app/spliter.sh
