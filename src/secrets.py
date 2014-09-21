"""API keys for accessing Twitter, and local config"""
import os

class Secrets():
    """API keys for accessing Twitter"""
    consumer_key = os.environ['twemail_api_key']
    consumer_secret = os.environ['twemail_api_secret']
    access_token_key = os.environ['twemail_access_token']
    access_token_secret = os.environ['twemail_access_token_secret']

    local_timezone = os.environ['twemail_local_timezone']
    record_path = os.environ['twemail_record_path']
    email_address = os.environ['twemail_email_address']
