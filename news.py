#!/home/ec2-user/newsengine/venv/bin python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 10:34:42 2017

@author: cammilligan
"""

#AWS DYNAMO TEST CONNECTION

import boto3
import requests
import time
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import datetime
from dateutil import tz
import hashlib

import uuid

from credentials import *

#innitialize reddit
import praw
reddit = praw.Reddit(client_id=cid[0],
                     client_secret=csecret[0],
                     user_agent=uagent[0],
                     username=uname[0],
                     password=pword)
subreddit = reddit.subreddit('thenewsrightnow')

#home or away
home = '/Users/cammilligan/Dropbox/Projects/News-Reddit-DynamoDB/warehouse.txt'
away = '/home/ec2-user/newsengine/scripts/warehouse.txt'

#unhash below if on AWS
home = away


##initalize dynamodb connection
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
table = dynamodb.Table(tname)


#innitialize newsapi requests & session
sources = ['the-verge','the-wall-street-journal','the-washington-post','time','usa-today','the-new-york-times','the-huffington-post','the-guardian-uk','techcrunch','techradar','the-economist','reuters','national-geographic','new-scientist','new-york-magazine','ign','independent','hacker-news','google-news','fortune','financial-times','engadget','bloomberg','business-insider','cnbc','cnn','daily-mail','associated-press','bbc-news']
apiKey = apik
sortBy = 'top'
link = 'https://newsapi.org/v1/articles?'
s = requests.Session()

#Initialize the warehouse & lists
warehouse =[]
warehousetitles = []
freshdump = []
freshdumptitles = []

def initializewh():
    print('initializing warehouse')
    with open(home, 'r') as wh:
        x = json.loads(wh.read())
        x = json.loads(x)
        for article in x:
            warehouse.append(article)
            warehousetitles.append(article['title'])
        wh.close()
    print('warehouse initialized with',len(warehouse),'articles in the warehosue')

initializewh()

def getcurrentdt():
    currentdt = datetime.datetime.now().replace(microsecond=0)
    currentdt = currentdt.replace(tzinfo=tz.tzlocal())
    currentdt = currentdt.isoformat()
    return currentdt

def runit():
    print(getcurrentdt())
    for i in sources:
        print(i)
        payload = {'source': i, 'apiKey': apiKey,'sortBy': sortBy}
        req = requests.Request('GET', link, params=payload)
        r = req.prepare()
        raw_data = s.send(r)
        raw_data = raw_data.json()
        try:
            raw_data = raw_data['articles']
        except:
            continue
        for article in raw_data:
            article.update({'source':i})
            article.update({'capturedat':getcurrentdt()})
            freshdump.append(article)
            freshdumptitles.append(article['title'])
    prunewarehouse(freshdump,freshdumptitles)
    cleanupwarehouse()

def cleanupwarehouse():
    with open(home, 'w+') as whc:
        x = json.dumps(freshdump)
        json.dump(x,whc)
        whc.close()
    print('Cleanup complete')



def prunewarehouse(freshdump,freshdumptitles):
    for warehousedarticle in warehouse:
        if warehousedarticle['title'] not in freshdumptitles:
            publish(warehousedarticle)
    print('publishing complete')


def publish(warehousedarticle):
    try:
        x = reddit.subreddit('thenewsrightnow').submit(warehousedarticle['title'], url=warehousedarticle['url'],resubmit=False)
        warehousedarticle.update({'redditid':x.id})
        warehousedarticle.update({'redditurl':x.url})
    except:
        print(warehousedarticle['capturedat'])
        print('error during reddit posting')
        print(warehousedarticle['title'])
    try:        
        warehousedarticle.update({'lastseenat':getcurrentdt()})
        author = warehousedarticle['author']
        capturedat = warehousedarticle['capturedat']
        lastseenat = warehousedarticle['lastseenat']
        description = warehousedarticle['description']
        publishedAt = warehousedarticle['publishedAt']
        source = warehousedarticle['source']
        title = warehousedarticle['title']
        url = warehousedarticle['url']
        urlToImage = warehousedarticle['urlToImage']
        redditid = warehousedarticle['redditid']
        redditurl = warehousedarticle['redditurl']
    except:
        print('error during warehousedarticle updating')
    try:
        articleid = str(uuid.uuid4())
    except:
        print('error during hashing')
        
    try:
        z.append(warehousedarticle)
    except:
        print("couldn't append to z")

    try:
        print("Publishing article:", source, title)
        table.put_item(
                Item={
                    'author': author,
                    'capturedat': capturedat,
                    'lastseenat': lastseenat,
                    'description': description,
                    'publishedAt': publishedAt,
                    'source': source,
                    'title': title,
                    'url': url,
                    'urlToImage': urlToImage,
                    'redditid': redditid,
                    'redditurl': redditurl,
                    'articleid': articleid,
                }
            )
    except:
        print('error during dynamodb publishing')
        print()


runit()
