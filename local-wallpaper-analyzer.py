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

def uploadToS3(post):
    url = post["data"]["url"]

    if "i.redd.it" in url:
        """

        If the link is a i.redd.it link then the image is downloaded and uploaded to an S3 bucket for unprocessed images.
        The files are saved locally and then deleted.

        """    

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
    sub_top_posts = requests.get("https://www.reddit.com/r/%s/top/.json" % SUBREDDIT).json()

    p = Pool(len(sub_top_posts["data"]["children"]))

    p.map(uploadToS3, sub_top_posts["data"]["children"])

    

    




