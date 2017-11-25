#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 09:34:34 2017

@author: cammilligan
"""

from credentials import *
import praw
reddit = praw.Reddit(client_id=cid[0],
                     client_secret=csecret[0],
                     user_agent=uagent[0],
                     username=uname[0],
                     password=pword)
subreddit = reddit.subreddit('thenewsrightnow')

print(reddit.user.me())

x = reddit.subreddit('thenewsrightnow').submit('Jeff Bezos’ net worth surpasses 100 billion dollars', url='https://www.theverge.com/2017/11/24/16697520/jeff-bezos-net-worth-100-billion-dollars-amazon',resubmit=False)


import hashlib
hash_object = hashlib.sha256(b'Hello World')
hex_dig = hash_object.hexdigest()
print(hex_dig)