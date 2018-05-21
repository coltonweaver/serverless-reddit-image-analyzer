import boto3
import os
from botocore.vendored import requests

SNS_TOPIC = os.environ['SNS_TOPIC']
SUBREDDIT = os.environ['SUBREDDIT']
IMAGE_TOPIC = os.environ['IMAGE_TOPIC']

sns_topic = boto3.resource('sns').Topic(SNS_TOPIC)

def lambda_handler(event, context):
    
    # First grab the top 100 images from the last 24 hours
    # Then upload all of the images to an S3 bucket for unprocessed photos
    # Then send all to rekognition
    # then add all that have 'topic' as a recognized object to another bucket, processed photos
    # Then empty the unprocessed bucket