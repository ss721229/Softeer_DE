FROM ubuntu:20.04

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV PATH=$PATH:$JAVA_HOME/bin:/hadoop-3.4.1/bin:/hadoop-3.4.1/sbin
ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /

RUN apt update && \
    apt install -y openjdk-8-jdk curl rsync && \
    apt install -y ssh sudo

RUN mkdir -p /root/.ssh && \
    ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa && \
    cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && \
    chmod 0600 /root/.ssh/authorized_keys && \
    service ssh start

RUN curl -O https://downloads.apache.org/hadoop/common/hadoop-3.4.1/hadoop-3.4.1.tar.gz && \
    tar -xzvf hadoop-3.4.1.tar.gz && \
    rm hadoop-3.4.1.tar.gz && \
    echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64" >> /hadoop-3.4.1/etc/hadoop/hadoop-env.sh

# 파일 복사
COPY core-site.xml /hadoop-3.4.1/etc/hadoop/core-site.xml
COPY hdfs-site.xml /hadoop-3.4.1/etc/hadoop/hdfs-site.xml
COPY mapred-site.xml /hadoop-3.4.1/etc/hadoop/mapred-site.xml

EXPOSE 9870

ENTRYPOINT bash -c "\
  if [ ! -d /tmp/hadoop-root/dfs/name ]; then \
    hdfs namenode -format -force; \
  fi && \
  service ssh start && \
  start-dfs.sh && \
  sleep 5 && \
  hdfs dfs -mkdir -p /user/root && \
  hdfs dfs -mkdir -p /upload && \
  tail -f /dev/null"
