FROM bamos/openface
RUN apt-get update && apt-get install -y \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ADD . /root/ffod
RUN pip3 install -r /root/ffod/requirements.txt
