import argparse
import logging
import tweepy
import time
import os
import sys
import json
import stdiomask

from typing import Any, Dict, List, Optional, Tuple
from styles import in_color, styled_input
from bots.getUser import getUser
from bots.followfollowers import follow_followers
from bots.favRetweet import retweet
from bots.autoreply import check_mentions

auth_keys = {
    'TWITTER_CONSUMER_KEY': '',
    'TWITTER_CONSUMER_SECRET': '',
    'TWITTER_ACCESS_TOKEN': '',
    'TWITTER_ACCESS_TOKEN_SECRET': '',
}

# Basic config needs to be called atleast once, to set the level properly.
logging.basicConfig()
# Set the level to INFO to write all logs with level >= info to stdout.
logging.root.setLevel(logging.INFO)
# Get the logger object
logger = logging.getLogger()


def read_keys_from_env_vars() -> bool:
    global auth_keys
    logger.info(' Searching for Authentication keys in Environment varibales...')
    time.sleep(1)
    for key in auth_keys:
        auth_keys[key] = os.getenv(auth_keys[key])
        if auth_keys[key] is None:
            logger.error(f' Key─ {key} not found in environment variables. Select other method for authentication.\n')
            time.sleep(1)
            return False
    logger.info(' All Authentication keys found.')
    return True

def read_keys_from_user() -> None:
    global auth_keys
    logger.info(' Please Enter the following authentication keys to login...')
    time.sleep(0.5)
    for key in auth_keys:
        if key.endswith('_SECRET'):
            auth_keys[key] = stdiomask.getpass(in_color('blue', f"{key} -> "), mask="*")
        else:
            auth_keys[key] = styled_input(f"{key} -> ")

def read_keys_from_file() -> None:
    global auth_keys
    print('Please ensure that your JSON file is in curent working directory.')
    filename = styled_input('Enter the filename ─ ')
    filename = filename + '.json'
    if os.path.exists(f"./{filename}"):
        file = open(filename)
        db = json.load(file)
        if db.keys() == auth_keys.keys():
            auth_keys = db
            logger.info(' All Authentication keys found.\n')
            return None
        else:
            logger.error(' File missing some keys. Please re-check the file.\n')
            read_keys_from_file()
            return None
    else:
        logger.error('Incorrect path. Please try again.\n')
        read_keys_from_file()
        return None

def get_authentication_method_and_verify() -> Any:
    global auth_keys
    print('Please select an authentication method:')
    print('\t[1] Get authentication keys from my Environment variables.')
    print('\t[2] Get authentication keys from an input file.')
    print('\t[3] Let me input the authentication keys myself.\n')
    auth_method = input('Enter your choice ─ ')
    while auth_method not in ['1', '2', '3']:
        print('You have entered an incorrect input. Please enter a valid choice.')
        auth_method = input('Enter your choice ─ ')

    if auth_method == '1':
        keys = read_keys_from_env_vars()
        if not keys:
            return False
    elif auth_method == '2':
        read_keys_from_file()
    elif auth_method == '3':
        read_keys_from_user()
    else:
        logger.error(' An error occured. Please restart TwiBot.')
        sys.exit(0)

    logger.info(' Authenticating...')

    auth = tweepy.OAuthHandler(auth_keys['TWITTER_CONSUMER_KEY'],
                               auth_keys['TWITTER_CONSUMER_SECRET'])
    auth.set_access_token(auth_keys['TWITTER_ACCESS_TOKEN'],
                          auth_keys['TWITTER_ACCESS_TOKEN_SECRET'])

    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)

    return api


def print_welcome_header(slow: bool=True) -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(in_color('purple', '────────────────────────────────────────────────────────────'))
    print(in_color('purple', '                     Welcome to TwiBot'))
    print(in_color('purple', '────────────────────────────────────────────────────────────\n'))
    if slow:
        time.sleep(1)

def get_feature_choice() -> str:
    print('Twibot can do the following for you. Please select an option:')
    print('\t[1] Search twitter for a user.')
    print('\t[2] Follow-back all your followers.')
    print('\t[3] Search and re-tweet a tweet.')
    print('\t[4] Autoreply to tweets mentioning you, or some keyword.\n')

    choice = input('Enter your choice ─ ')
    while choice not in ['1', '2', '3', '4']:
        print('You have entered an incorrect input. Please enter a valid choice.')
        choice = input('Enter your choice ─ ')

    return choice

def main():
    """
    Launch TwiBot.
    """
    print_welcome_header(slow=True)

    api = get_authentication_method_and_verify()
    while not api:
        api = get_authentication_method_and_verify()

    try:
        response = api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API. Bad Authentication data", exc_info=True)
        sys.exit(0)

    print(in_color('green', "Authentication OK ─ API created...\n"))
    time.sleep(1.5)
    
    print_welcome_header(slow=False)
    choice = get_feature_choice()
    
    if choice == '1':
        getUser(api)
    elif choice == '2':
        follow_followers(api)
    elif choice == '3':
        retweet(api)
    elif choice == '4':
        check_mentions(api)

    
if __name__ == '__main__':
    main()