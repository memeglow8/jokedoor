import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
CHANNEL_ID = os.getenv('CHANNEL_ID')
PROJECT_NAME = os.getenv('PROJECT_NAME', 'JokeCoin')
VERIFY_URL = os.getenv('VERIFY_URL')
