# initalize the image from official elasticsearch image
# the current version we are using is 5.5.0
FROM docker.elastic.co/elasticsearch/elasticsearch:5.5.0
# Add our own elasticsearch config file
ADD elasticsearch.yml /usr/share/elasticsearch/config/
# Grant proper access to the config file
USER root
RUN chown elasticsearch:elasticsearch config/elasticsearch.yml
# install ec2 plugin so that elasticsearch can discover each other in ECS
USER elasticsearch
WORKDIR /usr/share/elasticsearch
RUN bin/elasticsearch-plugin install discovery-ec2
