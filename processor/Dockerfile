FROM busybox:latest
MAINTAINER jj
VOLUME /results/
RUN mkdir /app/
ADD ./spliter.sh /app/
RUN chmod +x /app/spliter.sh
WORKDIR /results/
CMD /app/spliter.sh
