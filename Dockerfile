FROM bamos/openface
RUN apt-get update && apt-get install -y \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
RUN pip3 install vk grequests
ADD . /root/ffod
ADD . /root/ffod2
RUN pip3 install -r /root/ffod/requirements.txt && \
    pip2 install -r /root/ffod/requirements.txt