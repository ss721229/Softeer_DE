FROM ubuntu:20.04

WORKDIR /root

RUN apt update && \
    apt install -y python3 python3-pip git && \
    pip install --upgrade pip && \
    pip install jupyter && \
    git clone https://github.com/ss721229/Softeer_DE.git missions && \
    find /root/missions -maxdepth 1 -mindepth 1 ! -name missions -exec rm -rf {} + && \
    mv missions/missions/* missions/ && \
    rm -rf missions/missions && \
    apt clean

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]