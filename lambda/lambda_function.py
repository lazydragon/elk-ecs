import os
import re
import string
import logging
import urllib
import zlib

import boto3
import redis


REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_DB = os.environ['REDIS_DB']
REDIS_KEY = os.environ['REDIS_KEY']
DEST_BUCKET = os.environ['DEST_BUCKET']
DEST_PREFIX = os.environ['DEST_PREFIX']

def lambda_handler(event, context):
    # connect redis
    r = redis.StrictRedis(host=REDIS_SERVER, port=REDIS_PORT, db=REDIS_DB)

    # get the s3 object
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    
    # generate dest key
    regex = "(?P<prefix>.*)\/(?P<distributionid>.*)\.(?P<year>[0-9]{4})\-(?P<month>[0-9]{2})\-(?P<day>[0-9]{2})\-(?P<hour>[0-9]{2})\.(?P<hash>.*)\.gz"
    replace = "yyyy=\g<year>/mm=\g<month>/dd=\g<day>/hh=\g<hour>/\g<distributionid>.\g<year>-\g<month>-\g<day>-\g<hour>.\g<hash>.gz"
    dest_key = DEST_PREFIX + '/' + re.sub(regex, replace, key)
    
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        data = response['Body'].read()
        # unzip and split logs by line
        logs = string.split(zlib.decompress(data, 16+zlib.MAX_WBITS), '\n')
        # for each log, push it to the redis queue
        for log in logs:
            r.lpush(REDIS_KEY, log)
        
        # partition log file
        s3.copy({'Bucket': bucket, 'Key': key}, DEST_BUCKET, dest_key)
        
    except Exception as e:
        print(e)
        raise e


