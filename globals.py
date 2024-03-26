from dotenv import load_dotenv
import os

load_dotenv()

DIRECTORY=os.environ.get('DIRECTORY')
GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY')
REDDIT_CLIENT_ID=os.environ.get('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET=os.environ.get('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT=os.environ.get('REDDIT_USER_AGENT')
GOOGLE_DEV_KEY=os.environ.get('GOOGLE_DEV_KEY')
GOOGLE_CUSTOM_SEARCH_ENGINE_KEY=os.environ.get('GOOGLE_CUSTOM_SEARCH_ENGINE_KEY')
LOG_LEVEL=os.environ.get('LOG_LEVEL', 'DEBUG')
