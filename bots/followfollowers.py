#!/usr/bin/env python
# twitterBot/bots/followfollowers.py

import tweepy
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api):
    while True:
        logger.info("Retrieving and following followers")
        for follower in tweepy.Cursor(api.followers).items():
            if not follower.following:
                logger.info(f"Following {follower.name}")
                follower.follow()
        logger.info("Waiting...")
        time.sleep(60)

