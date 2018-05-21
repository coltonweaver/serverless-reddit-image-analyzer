# This file is intended to test the logic that will be used in the lambda function

import requests

SUBREDDIT = "wallpapers"

if __name__ == '__main__':

    r = requests.get("https://www.reddit.com/r/%s/top/.json" % SUBREDDIT).json()

    print("Here is what was retrieved:")

    for json_child in r["data"]["children"]:

        print(json_child["data"]["url"])




