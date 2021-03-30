import praw
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv()

configFile = open('config.json')
config = json.load(configFile)

subreddits = "+".join(config["subreddits"])
apiURL = 'https://api.outline.com/v3/parse_article'

reddit = praw.Reddit(
    user_agent="NewsOutlineBot (by u/iamgloriousbastard)",
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

subreddit = reddit.subreddit(subreddits)
for submission in subreddit.stream.submissions(skip_existing=True):
    for url in config["urls"]:
        if url in submission.url:
            response = requests.get(apiURL, params={"source_url": submission.url})
            submission.reply(
                "Paywalls? Cluttered? Here's the Outline URL! https://outline.com/" + response.json()['data'][
                    'short_code'])
            print(response.json()['data']['short_code'])
