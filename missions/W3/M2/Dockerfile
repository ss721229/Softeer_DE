# 베이스 이미지 선택 (Java 포함)
FROM openjdk:8-jdk

# 환경 변수 설정
ENV HADOOP_VERSION=3.4.1
ENV HADOOP_HOME=/opt/hadoop
ENV JAVA_HOME=/usr/local/openjdk-8
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    ssh \
    sudo \
    rsync \
    vim \
    curl \
    net-tools \
    iputils-ping \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Hadoop 다운로드 및 압축 해제
RUN curl -O https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt && \
    mv /opt/hadoop-${HADOOP_VERSION} $HADOOP_HOME && \
    rm hadoop-${HADOOP_VERSION}.tar.gz

# Hadoop 환경 변수 추가
COPY config/hadoop-env.sh $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# SSH 설정 (Hadoop은 내부에서 SSH 사용)
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys

# Hadoop 설정 파일 복사
COPY config/*.xml $HADOOP_HOME/etc/hadoop/
COPY modify-config/*.xml /modify-config/

# Hadoop 시작용 진입점 스크립트 복사 (마스터/워커에 따라 달라짐)
COPY start-cmd.sh /usr/local/bin/start-cmd.sh
RUN chmod +x /usr/local/bin/start-cmd.sh

COPY modify-config-data.sh /usr/local/bin/modify-config-data.sh
COPY modify-config-name.sh /usr/local/bin/modify-config-name.sh
COPY verify-config.sh /usr/local/bin/verify-config.sh
RUN chmod +x /usr/local/bin/modify-config-data.sh
RUN chmod +x /usr/local/bin/modify-config-name.sh
RUN chmod +x /usr/local/bin/verify-config.sh

RUN ln -s $JAVA_HOME/bin/java /bin/java

# 포트 오픈 (웹 UI 접근을 위해)
EXPOSE 9870 9864 8088

# 시작 명령어
CMD ["/usr/local/bin/start-cmd.sh"]