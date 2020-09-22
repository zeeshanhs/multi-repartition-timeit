#
# Spark Standalone Container
# Apache Spark 2.4.5
#
# Runs a super-tiny, Spark standalone cluster in a container
# Suitable for building test/development containers for spark apps
#
# Usage:
# $ docker build -t uncharted/sparklet:2.4.5 .
# $ docker run -p 8080:8080 -it uncharted/sparklet:2.4.5

FROM anapsix/alpine-java:latest
LABEL author="Sean McIntyre <smcintyre@uncharted.software>"

# spark web admin ports
EXPOSE 4040
EXPOSE 8080

# spark debugging port
EXPOSE 9999

WORKDIR /opt

RUN \
  # update packages
  apk update --update && \
  # grab curl and ssh
  apk add --update openssh vim curl procps && \
  curl -L -k https://apache.mirror.gtcomm.net/spark/spark-2.4.7/spark-2.4.7-bin-hadoop2.7.tgz > spark.tgz && \
  # generate a keypair and authorize it
  mkdir -p /root/.ssh && \
  ssh-keygen -f /root/.ssh/id_rsa -N "" && \
  cat /root/.ssh/id_rsa.pub > /root/.ssh/authorized_keys && \
  # extract spark
  tar -xzf spark.tgz && \
  # cleanup spark tarball
  rm spark.tgz && \
  # s6 overlay
  curl -LS https://github.com/just-containers/s6-overlay/releases/download/v1.17.2.0/s6-overlay-amd64.tar.gz -o /tmp/s6-overlay.tar.gz && \
  tar xvfz /tmp/s6-overlay.tar.gz -C / && \
  rm -f /tmp/s6-overlay.tar.gz


# upload init scripts
ADD includes/services/spark-master-run /etc/services.d/spark-master/run
ADD includes/services/spark-slave-run /etc/services.d/spark-slave/run
ADD includes/services/spark-slave2-run /etc/services.d/spark-slave2/run

ENV PATH /spark-2.4.7-bin-hadoop2.7/bin:$PATH

ENTRYPOINT [ "/init" ]

RUN ls -la

RUN ls -la ./spark-2.4.7-bin-hadoop2.7/bin

WORKDIR /opt/spark-2.4.7-bin-hadoop2.7/bin

RUN ls -la

# CMD ["./spark-2.4.7-bin-hadoop2.7/bin/spark-shell"]
CMD ["spark-shell"]
