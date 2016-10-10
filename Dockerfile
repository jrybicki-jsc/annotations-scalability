FROM debian:wheezy
MAINTAINER jj
RUN useradd tester
RUN DBEIAN_FRONTEND=noninteractive apt-get update && apt-get install wget python python-pip -y && \
   apt-get clean autoclean && apt-get autoremove && \
   rm -rf /var/lib/{apt,dpkg,cache,log}
RUN mkdir /app/
VOLUME /results/
ADD . /app/
WORKDIR /app/
RUN pip install -r /app/requirements.txt && chown -R tester:tester /app/
USER tester
CMD /app/test.py > /results/result.txt
