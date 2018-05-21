# This file is intended to test the logic that will be used in the lambda function

import boto3
import requests
import os
import string
import random

from multiprocessing import Pool

SUBREDDIT = "wallpapers"
UNPROCESSED_BUCKET = "cwunprocessedimages"
PROCESSED_BUCKET = "cwprocessedimages"
TOPICS = ["outdoors","outside","tree","leaf","city","building","water","ocean","water","landscape","mountain","grass"]

def uploadToS3(post):
    """

        If the link is a i.redd.it link then the image is downloaded and uploaded to an S3 bucket for unprocessed images.
        The files are saved locally and then deleted.

    """ 
    
    url = post["data"]["url"]

    if "i.redd.it" in url:   

        alpha = string.ascii_uppercase
        num = string.digits
        rand_string = ''.join(random.choice(alpha + num) for _ in range(5))

        file_name = rand_string + ".jpg"
        with open(file_name, 'wb') as f:
            pic = requests.get(url, stream=True)

            for block in pic.iter_content(1024):
                if not block:
                    break

                f.write(block)
        
        s3.Bucket('cwunprocessedimages').upload_file(file_name, file_name)

        os.remove(file_name)

if __name__ == '__main__':

    s3 = boto3.resource('s3')
    r_client = boto3.client('rekognition', 'us-east-1')

    sub_top_posts = requests.get("https://www.reddit.com/r/%s/top/.json" % SUBREDDIT).json()

    p = Pool(len(sub_top_posts["data"]["children"]))

    p.map(uploadToS3, sub_top_posts["data"]["children"])

    objectSummary = s3.Bucket('cwunprocessedimages').objects.all()

    for obs in objectSummary:
        response = r_client.detect_labels(Image={'S3Object':{'Bucket':obs.bucket_name,'Name':obs.key}})
   
        for label in response['Labels']:
            if label['Name'].lower() in TOPICS and label['Confidence'] > 60.0:
                copy_source = {
                    'Bucket': obs.bucket_name,
                    'Key': obs.key
                }
                s3.Bucket('cwprocessedimages').copy(copy_source, obs.key)
                print("Copying to S3")
                break
            elif label['Confidence'] < 60.0:
                break

    s3.Bucket('cwunprocessedimages').objects.delete()
