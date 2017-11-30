#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 15:56:41 2017

@author: cammilligan
"""

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

from credentials import *


from boto3 import resource
from boto3.dynamodb.conditions import Key

# The boto3 dynamoDB resource
dynamodb_resource = resource('dynamodb')

def get_table_metadata(tname):
    """
    Get some metadata about chosen table.
    """
    table = dynamodb_resource.Table(tname)

    return {
        'num_items': table.item_count,
        'primary_key_name': table.key_schema[0],
        'status': table.table_status,
        'bytes_size': table.table_size_bytes,
        'global_secondary_indices': table.global_secondary_indexes
    }

get_table_metadata(tname)