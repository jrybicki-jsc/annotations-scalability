FROM ubuntu:latest
MAINTAINER jj
RUN DBEIAN_FRONTEND=noninteractive apt-get update && \
   apt-get install python python-numpy -y && \
   apt-get clean autoclean && \
   apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
VOLUME /results/
RUN mkdir /app/
ADD ./spliter.sh /app/
ADD ./merger.py /app/
RUN chmod +x /app/spliter.sh /app/merger.py
WORKDIR /results/
CMD /app/spliter.sh
