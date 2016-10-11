FROM debian:wheezy
MAINTAINER jj
RUN DBEIAN_FRONTEND=noninteractive apt-get update && \
   apt-get install python python-pip -y && \
   apt-get clean autoclean && apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
VOLUME /results/
RUN mkdir /app/
ADD . /app/
WORKDIR /app/
RUN pip install -r /app/requirements.txt && chmod +x /app/test.py
CMD /app/test.py dummy 10 100 >> /results/result.txt && \
    /app/test.py neo 10 100 >> /results/result.txt &&  \
    /app/test.py mongo 10 100 >> /results/result.txt
