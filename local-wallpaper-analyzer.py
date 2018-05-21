# This file is intended to test the logic that will be used in the lambda function

import boto3
import requests
import os

SUBREDDIT = "wallpapers"
UNPROCESSED_BUCKET = "cwunprocessedimages"
PROCESSED_BUCKET = "cwprocessedimages"

if __name__ == '__main__':

    s3 = boto3.resource('s3')
    sub_top_posts = requests.get("https://www.reddit.com/r/%s/top/.json" % SUBREDDIT).json()
    i = 0

    for post in sub_top_posts["data"]["children"]:

        url = post["data"]["url"]

        if "i.redd.it" in url:
            """

            If the link is a i.redd.it link then the image is downloaded and uploaded to an S3 bucket for unprocessed images.
            The files are saved locally and then deleted.

            """    

            file_name = "pic" + str(i) + ".jpg"
            with open(file_name,'wb') as f:
                pic = requests.get(url, stream=True)

                for block in pic.iter_content(1024):
                    if not block:
                        break

                    f.write(block)
            
            data = open(file_name, "rb")
            s3.Bucket('cwunprocessedimages').put_object(Key=file_name, Body=data)
            data.close()

            os.remove(file_name)

            i = i + 1

    




