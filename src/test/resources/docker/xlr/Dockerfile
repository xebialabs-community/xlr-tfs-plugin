FROM xebialabs/xlr_dev_run:v6.1.0.1
ADD resources/script.policy /opt/xlr/server/conf/script.policy

WORKDIR /tmp
RUN wget -O tfs.zip https://github.com/Microsoft/team-explorer-everywhere/releases/download/v14.111.1/TFS-SDK-14.111.1.zip \
    && unzip -o /tmp/tfs.zip -d /tmp \
    && mv /tmp/TFS-SDK-14.111.1/redist/lib/* /opt/xlr/server/plugins \
    && mv /tmp/TFS-SDK-14.111.1/redist/native /opt/xlr/server/conf
