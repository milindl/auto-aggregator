import os

__group_id = '433290100027449'
if 'SHARE_AUTO_GROUP_ID' in os.environ:
    __group_id = os.environ['SHARE_AUTO_GROUP_ID']

__token = ''
if 'SHARE_AUTO_ACCESS_TOKEN' in os.environ:
    __token = os.environ['SHARE_AUTO_ACCESS_TOKEN']

__username = 'postgres'
if 'SHARE_AUTO_USERNAME' in os.environ:
    __username = os.environ['SHARE_AUTO_USERNAME']

__password = ''
if 'SHARE_AUTO_PASSWORD' in os.environ:
    __password = os.environ['SHARE_AUTO_PASSWORD']

__host = 'localhost'
if 'SHARE_AUTO_HOST' in os.environ:
    __host = os.environ['SHARE_AUTO_HOST']

__db = 'postgres'
if 'SHARE_AUTO_DATABASE' in os.environ:
    __db = os.environ['SHARE_AUTO_DATABASE']

__sleep_time = 3600
if 'SHARE_AUTO_SLEEP_TIME' in os.environ:
    __sleep_time = os.environ['SHARE_AUTO_SLEEP_TIME']

# Aggregator
graph_api = {
    'GROUP_ID' : __group_id,
    'TOKEN' : __token
    }
postgres = {
    'USERNAME' : __username,
    'PASSWORD' : __password,
    'HOST' : __host,
    'DB' : __db
    }

main = {
    'SLEEP_TIME' : __sleep_time
    }

