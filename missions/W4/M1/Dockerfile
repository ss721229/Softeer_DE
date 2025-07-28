FROM python:3.10-slim

ENV SPARK_HOME=/opt/spark
ENV SPARK_VERSION=4.0.0
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && \
    apt -y update && \
    apt install -y openjdk-17-jdk && \
    apt-get install -y ssh sudo rsync vim curl net-tools iputils-ping procps && \
    rm -rf /var/lib/apt/lists/*

RUN curl -O https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    tar -xzf spark-${SPARK_VERSION}-bin-hadoop3.tgz -C /opt && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop3 $SPARK_HOME && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

COPY start-cmd.sh /usr/local/bin/start-cmd.sh
RUN chmod +x /usr/local/bin/start-cmd.sh

CMD ["./start-cmd.sh"]