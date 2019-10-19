#! /usr/bin/env python3

import boto3
import argparse
import sys
import subprocess
from subprocess import call
import os
import time
import re

# Todo: Setup OpenNMT environment

log_file = 'opennmt-train.log'

parser = argparse.ArgumentParser(description='eoat-trains3: Run OpenNMT training and save checkpoints out to s3. Allows worry-free training runs on spot instances',add_help=False)
parser.add_argument('--training_script',help='Path to OpenNMT training script. If using the EOAT AMI, this is /usr/bin/opennmt-train which links to /opt/OpenNMT-py/train.py')
parser.add_argument('-data',help='Model prefix, we just grab this from training options.',required=True)
parser.add_argument('--s3_bucket',help='Specifies the s3 bucket to periodically save training data',required=False)
parser.add_argument('--working_dir',help='Directory that holds training and checkpoint files. Defaults to current directory',required=False)

args, unknown = parser.parse_known_args()
command = (str(' '.join(unknown)))

if (args.data):
    input_data = args.data
else:
    sys.exit(0)
if (args.training_script):
    training_script = args.training_script
else:
    training_script = '/usr/bin/opennmt-train'
if (args.working_dir):
    working_dir = args.working_dir
else:
    working_dir = os.getcwd()

s3 = boto3.resource('s3')
available_buckets = s3.buckets.all()

checkbuckets = []

for bucket in available_buckets:
    checkbuckets.append(bucket.name)

if (args.s3_bucket):
    s3_bucket = args.s3_bucket
    if s3_bucket in checkbuckets:
      print('Found s3 bucket as ' + s3_bucket)
    else:
      print('Did not find ' + s3_bucket + ' in S3, creating bucket ' + s3_bucket)
      s3.create_bucket(Bucket=s3_bucket,ACL='bucket-owner-full-control')
else:
  print('\nNo bucket name specified. Found the following existing buckets:\n')
  for bucket in s3.buckets.all():
    print(bucket.name)
  sys.exit()

mycommand = "python3 " + training_script + " -data " + input_data + " " + command  + ' &'
print('Using ' + mycommand + '. \nOutput logged to ' + log_file)

log = open(log_file,'a')
call(mycommand,stdout=log,stderr=log,shell=True)

# Initial log copy to S3

data = open(log_file,'rb')
s3.Bucket(s3_bucket).put_object(Key=log_file, Body=data)
data.close()

# Initial training data to S3 
mytrainingfiles = os.popen('ls ' + '|grep ' + input_data + ' |grep .pt').readlines()
for line in mytrainingfiles:
  file2save = line.strip()
  data = open(file2save,'rb')
  s3.Bucket(s3_bucket).put_object(Key=file2save, Body=data)
  data.close()

# Update changed files periodically
def aws_sync():
  s3log = open('s3.log','a')
  synccommand = 'aws s3 sync ' + working_dir + ' s3://' + s3_bucket
  call(synccommand,stdout=s3log,stderr=s3log,shell=True)
  time.sleep(120)

while True:
    aws_sync()
