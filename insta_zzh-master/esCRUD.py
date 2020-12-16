from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
import random
import numpy as np
import django
if django.VERSION >= (1, 7):
    django.setup()


es = Elasticsearch(['127.0.0.1'], port = 9200)
csvFile = open(os.path.join(os.getcwd(),"static\\flickr_dataset\\flickr30k_images\\results.csv"), "r", encoding = "utf-8")
result = {}
uuid = 0
for line in csvFile:    
    if line.startswith('image_name'):
        continue
    item = [x.strip() for x in line.split('|')]
    if item[0] not in result:
        result[item[0]] = item[2]
    else:
        result[item[0]] += item[2]
csvFile.close()
dataset = []

    data = {}
    data['filename'] = key
    data['description'] = result[key]
    dataset.append(data)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
 

