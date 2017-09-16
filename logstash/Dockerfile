FROM docker.elastic.co/logstash/logstash:5.5.0
# drop the default config
RUN rm -f /usr/share/logstash/pipeline/logstash.conf
# add our own configs
ADD pipeline/ /usr/share/logstash/pipeline/
ADD config/ /usr/share/logstash/config/
