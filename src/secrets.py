"""API keys for accessing Twitter, and local config"""
import os

class Secrets():
    """API keys for accessing Twitter"""
    api_key = os.environ['twemail_api_key']
    api_secret = os.environ['twemail_api_secret']
    access_token = os.environ['twemail_access_token']
    access_token_secret = os.environ['twemail_access_token_secret']
    
    username = os.environ['twemail_username']
    password = os.environ['twemail_password']

    record_path = os.environ['twemail_record_path']
    email_address = os.environ['twemail_email_address']
