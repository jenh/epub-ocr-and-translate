#! /usr/bin/env python2.7

# Super simple get bucket list

import boto3

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
  print(bucket.name)

