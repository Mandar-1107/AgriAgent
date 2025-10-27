import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys - Loaded from environment variables
# If not found in environment, you can set them directly here (not recommended)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")

# Gemini Model Configuration
GEMINI_MODEL = "gemini-2.5-flash-lite"  # Updated to latest model
GEMINI_VISION_MODEL = "gemini-2.5-flash-lite"  # For image analysis

# Response Configuration
MIN_RESPONSE_LENGTH = 150
MAX_RESPONSE_LENGTH = 400
IMAGE_ANALYSIS_MAX_TOKENS = 500
CHAT_MAX_TOKENS = 600

# Temperature settings for different contexts
TEMPERATURE_IMAGE_ANALYSIS = 0.7
TEMPERATURE_CHAT = 0.8

# Weather Configuration
WEATHER_UNITS = "metric"  # Celsius
WEATHER_TIMEOUT = 10  # seconds
WEATHER_CACHE_DURATION = 600  # 10 minutes in seconds

# UI Configuration
MAX_IMAGE_WIDTH = 400
CHAT_MAX_WIDTH = 500
MAX_MESSAGES_DISPLAY = 50  # Prevent memory issues

# Image Processing
SUPPORTED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "webp"]
MAX_IMAGE_SIZE_MB = 10

# Agriculture Focus Areas
AGRICULTURE_FOCUS = [
    "Crop management and cultivation",
    "Soil health and testing",
    "Pest identification and management",
    "Disease identification and treatment",
    "Irrigation optimization",
    "Fertilization strategies",
    "Weather impact analysis",
    "Sustainable farming practices",
    "Crop rotation planning",
    "Yield optimization techniques",
    "Organic farming methods",
    "Market pricing guidance"
]

# Indian Agricultural Context
INDIAN_SEASONS = {
    "Kharif": [6, 7, 8, 9],      # June-September (Monsoon crops)
    "Rabi": [10, 11, 12, 1, 2, 3], # October-March (Winter crops)
    "Zaid": [4, 5]                 # April-May (Summer crops)
}

# Common Indian Crops by Season
SEASONAL_CROPS = {
    "Kharif": ["Rice", "Cotton", "Maize", "Soybean", "Groundnut", "Millet"],
    "Rabi": ["Wheat", "Barley", "Chickpea", "Mustard", "Linseed", "Peas"],
    "Zaid": ["Watermelon", "Cucumber", "Bitter Gourd", "Pumpkin"]
}