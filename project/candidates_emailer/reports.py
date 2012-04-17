import odesk

from candidates_emailer.odesk_settings import ODESK_KEY, ODESK_SECRET

def get_client(key=ODESK_KEY, secret=ODESK_SECRET,
               user=None, oauth_access_token=None, oauth_access_token_secret=None):
    if user:
        oauth_access_token = user.access_token
        oauth_access_token_secret = user.access_token_secret

    client = odesk.Client(key, secret, auth="oauth")
    client.oauth_access_token = oauth_access_token
    client.oauth_access_token_secret = oauth_access_token_secret
    
    return client


