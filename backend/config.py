import os

from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 500
REFRESH_TOKEN_EXPIRE_MINUTES = 1000

AVATARS_PATH = "images/avatars"
POST_IMAGES_PATH = "images/posts"


CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)

SESSION_MIDDLEWARE_SECRET = os.environ.get("SESSION_MIDDLEWARE_SECRET", None)
