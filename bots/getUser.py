import tweepy
import sys
sys.path.append('..')

from styles import in_color, styled_input


def getUser(api) -> None:
    user_name = styled_input('Enter a username ─ ')

    user = api.get_user(user_name)

    # FIXME: Extract details from response and display beautifully.
    print(user)
    
