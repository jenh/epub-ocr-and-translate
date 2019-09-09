#! /usr/bin/env python2.7

import boto3
import argparse
import sys
import subprocess
from subprocess import call
import os
import time

# Todo: Setup OpenNMT environment

log_file = 'opennmt-train.log'

parser = argparse.ArgumentParser(description='eoat-trains3: Run OpenNMT training and save checkpoints out to s3. Allows worry-free training runs on spot instances')
parser.add_argument('-e','--training_script',help='Path to OpenNMT training script. If using the EOAT AMI, this is /usr/bin/opennmt-train which links to /opt/OpenNMT-py/train.py')
parser.add_argument('-i','--input_data',help='Data to train from (output of OpenNMT preprocess.py',required=True)
parser.add_argument('-m','--model_file',help='Model file prefix to use for completed training models',required=True)
parser.add_argument('-t','--train_from',help='The model file to use if restarting an interrupted training session',required=False)
parser.add_argument('-c','--checkpoint',help='Saves a model every number of specified steps. Default is 5000',required=False)
parser.add_argument('-s','--s3_bucket',help='Specifies the s3 bucket to periodically save training data',required=False)
parser.add_argument('-w','--world_size',help='If GPU-enabled, number of GPUs to use. If not set, we use CPU',required=False)
parser.add_argument('-g','--gpu_ranks',help='If GPU-enabled, list the GPUs in order of use, for example, 0 1 2 3',required=False)
parser.add_argument('-d','--working_dir',help='Directory that holds training and checkpoint files. Defaults to current directory',required=False)
args = parser.parse_args()

if (args.training_script):
    training_script = args.training_script
else:
    training_script = '/usr/bin/opennmt-train'
if (args.input_data):
    input_data = args.input_data
    print ('Found training data file as ' + input_data)
else:
   sys.exit()
if (args.model_file):
    model_file = args.model_file
    print ('Found model file prefix as ' + model_file)
else:
    sys.exit()
if (args.train_from):
    train_from = ' --train_from ' + args.train_from
    print ('Resuming training using ' + train_from)
else:
    train_from = '' 
if (args.checkpoint):
    checkpoint = args.checkpoint
    print ('Saving a checkpoint file every ' + checkpoint + ' steps')
else:
    checkpoint = 5000
if (args.world_size):
    world_size = ' --world_size ' +str(args.world_size)
else:
     world_size = '' 
if (args.gpu_ranks):
    gpu_ranks = ' --gpu_ranks ' + args.gpu_ranks
else:
    gpu_ranks = ''
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
      print ('Found s3 bucket as ' + s3_bucket)
    else:
      print ('Did not find ' + s3_bucket + ' in S3, creating bucket ' + s3_bucket)
      s3.create_bucket(Bucket=s3_bucket,ACL='bucket-owner-full-control')
else:
  print ('\nNo bucket name specified. Found the following existing buckets:\n')
  for bucket in s3.buckets.all():
    print(bucket.name)
  sys.exit()

mycommand = training_script + ' --data ' + input_data + ' --save_model ' + model_file + ' --save_checkpoint ' + checkpoint + train_from + world_size + gpu_ranks + ' &'
print ('Using ' + mycommand + '. \nOutput logged to ' + log_file)

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
