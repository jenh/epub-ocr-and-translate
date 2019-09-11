#! /usr/bin/env python

# Super simple get bucket list

import boto3

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
  print(bucket.name)

