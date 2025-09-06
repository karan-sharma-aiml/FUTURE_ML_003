import os
from dotenv import load_dotenv

# Load all keys/URIs from .env
load_dotenv()

# OpenAI GPT API key (if using OpenAI)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Hugging Face free-tier token for text-generation
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

# MongoDB connection URI
MONGO_URI = os.getenv("MONGO_URI")

# Redis URL (optional caching/session store)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
