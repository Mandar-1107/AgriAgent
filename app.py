# app.py - Fixed UI Layout
import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime
from PIL import Image
from typing import Optional, Dict, Any, List
import re
from config import *

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="AgriAgent - AI Agriculture Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== PROFESSIONAL STYLING ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e3e8ef 100%);
        min-height: 100vh;
        padding-bottom: 200px;
    }
    
    .chat-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 30px 20px;
    }
    
    .message-container {
        display: flex;
        margin-bottom: 24px;
        animation: fadeSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes fadeSlideIn {
        from { 
            opacity: 0; 
            transform: translateY(20px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    .user-message {
        justify-content: flex-end;
    }
    
    .message-bubble {
        max-width: 80%;
        padding: 16px 20px;
        border-radius: 20px;
        word-wrap: break-word;
        line-height: 1.6;
        font-size: 15px;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px 20px 4px 20px;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.25);
    }
    
    .assistant-bubble {
        background: white;
        color: #2d3748;
        border-radius: 20px 20px 20px 4px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.04);
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        padding: 20px;
        box-shadow: 0 -8px 32px rgba(0,0,0,0.12);
        z-index: 1000;
        border-top: 1px solid rgba(0,0,0,0.08);
    }
    
    .input-wrapper {
        max-width: 900px;
        margin: 0 auto;
        display: flex;
        gap: 12px;
        align-items: flex-start;
    }
    
    .stTextInput > div > div > input {
        border-radius: 28px !important;
        padding: 14px 22px !important;
        border: 2px solid #e2e8f0 !important;
        font-size: 15px !important;
        transition: all 0.3s ease !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
    }
    
    .upload-badge {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        font-size: 13px;
        font-weight: 500;
        margin-top: 8px;
    }
    
    .stButton > button {
        border-radius: 24px !important;
        padding: 10px 20px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        border: none !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* File uploader styling */
    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 16px;
        padding: 16px;
        border: 2px dashed #e2e8f0;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .message-bubble {
            max-width: 90%;
        }
        .input-container {
            padding: 16px;
        }
        .input-wrapper {
            flex-direction: column;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
def initialize_session_state():
    defaults = {
        "messages": [],
        "weather_data": None,
        "weather_cache_time": None,
        "last_location": None,
        "processed_input": None,
        "input_counter": 0,
        "current_images": []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# ==================== API CONFIGURATION ====================
def configure_gemini():
    if not GEMINI_API_KEY:
        st.error("⚠️ **Gemini API Key Missing**\n\nPlease add your API key to the `.env` file.")
        st.stop()
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"❌ **API Configuration Failed**\n\n{str(e)}")
        st.stop()

configure_gemini()

# ==================== HELPER FUNCTIONS ====================
def get_indian_season() -> str:
    month = datetime.now().month
    for season, months in INDIAN_SEASONS.items():
        if month in months:
            return season
    return "Transition Period"

def is_simple_greeting(message: str) -> bool:
    greetings = ['hi', 'hello', 'hey', 'namaste', 'namaskar', 'good morning', 'good evening', 'good afternoon']
    casual = ['how are you', 'what is your name', 'who are you', 'whats up', 'sup', 'wassup']
    
    message_lower = message.lower().strip()
    
    if message_lower in greetings:
        return True
    
    for phrase in casual:
        if phrase in message_lower and len(message_lower) < 30:
            return True
    
    return False

def remove_markdown_formatting(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    return text

def get_weather_data(location: str) -> Optional[Dict[str, Any]]:
    if not WEATHER_API_KEY:
        return None
    
    if (st.session_state.weather_data and 
        st.session_state.last_location == location and
        st.session_state.weather_cache_time and
        (datetime.now() - st.session_state.weather_cache_time).seconds < WEATHER_CACHE_DURATION):
        return st.session_state.weather_data
    
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather"
        params = {"q": location, "appid": WEATHER_API_KEY, "units": WEATHER_UNITS}
        response = requests.get(url, params=params, timeout=WEATHER_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.weather_data = data
            st.session_state.weather_cache_time = datetime.now()
            st.session_state.last_location = location
            return data
    except:
        pass
    
    return None

def format_weather_context(weather_data: Dict[str, Any]) -> str:
    if not weather_data:
        return ""
    
    try:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        
        context = f"Weather in {weather_data['name']}: {temp}°C, {humidity}% humidity, {description}."
        
        if temp > 35:
            context += " High heat - extra irrigation needed."
        elif temp < 10:
            context += " Cold conditions - frost protection advised."
        
        if humidity > 80:
            context += " High humidity - disease risk."
        elif humidity < 30:
            context += " Low humidity - increase irrigation."
        
        return context
    except:
        return ""

def resize_image(image: Image.Image, max_size: int = 2048) -> Image.Image:
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return image

def analyze_images_with_gemini(images: List[Image.Image], query: str = "") -> str:
    try:
        model = genai.GenerativeModel(GEMINI_VISION_MODEL)
        season = get_indian_season()
        
        prompt = f"""You are AgriAgent, an agricultural expert.

Season: {season}
Query: "{query}"

Analyze {"these images" if len(images) > 1 else "this image"} and provide:

1. Identification: What crops/plants?
2. Health: Current condition
3. Issues: Diseases, pests, problems
4. Recommendations: Specific actions with product names and dosages

STRICT RULES:
- Maximum {MAX_RESPONSE_LENGTH} words
- No bold formatting (**)
- Simple language
- Practical advice only"""
        
        content_parts = [prompt] + [resize_image(img) for img in images]
        
        response = model.generate_content(
            content_parts,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=IMAGE_ANALYSIS_MAX_TOKENS,
                temperature=TEMPERATURE_IMAGE_ANALYSIS,
            )
        )
        
        result = response.text if response and response.text else "Unable to analyze images."
        return remove_markdown_formatting(result)
    
    except Exception as e:
        return f"Error analyzing images: {str(e)[:100]}"

def get_agriculture_response(user_message: str, weather_context: str = "", image_analysis: str = "") -> str:
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        is_greeting = is_simple_greeting(user_message)
        current_season = get_indian_season()
        seasonal_crops = SEASONAL_CROPS.get(current_season, [])
        
        conversation_history = ""
        if len(st.session_state.messages) > 1:
            recent = st.session_state.messages[-8:]
            history_parts = []
            for msg in recent:
                role = "Farmer" if msg["role"] == "user" else "Agent"
                content = msg['content'][:100]
                history_parts.append(f"{role}: {content}")
            conversation_history = "\n".join(history_parts)
        
        if is_greeting:
            system_prompt = f"""You are AgriAgent, an AI agricultural assistant.

This is a casual greeting.

STRICT RULES:
- Reply in 30-50 words maximum
- Be warm and brief
- Do NOT use bold formatting (**)
- Simply greet and ask how you can help
- Do NOT give agricultural advice yet

Previous conversation:
{conversation_history if conversation_history else "First interaction"}"""
        else:
            system_prompt = f"""You are AgriAgent, expert agricultural consultant for Indian farmers.

Context:
- Season: {current_season}
- Common crops: {', '.join(seasonal_crops[:4])}

CRITICAL RULES:
1. MAXIMUM {MAX_RESPONSE_LENGTH} words - BE STRICT
2. For beginners: Ask 2-3 qualifying questions BEFORE detailed advice
3. Do NOT dump information - have a conversation
4. One topic at a time
5. No bold formatting (**)
6. Simple language
7. Ask follow-up questions to understand context

IMPORTANT: If farmer is a beginner, you MUST ask about:
- Location/state (for crop suitability)
- Soil type (clay, loam, sandy)
- Water availability (irrigation or rain-fed)
- Budget constraints

Only after knowing these, provide specific recommendations.

Previous conversation:
{conversation_history if conversation_history else "First interaction"}"""
        
        context_parts = [system_prompt]
        if weather_context and not is_greeting:
            context_parts.append(f"\nWeather: {weather_context}")
        if image_analysis:
            context_parts.append(f"\nImage Analysis: {image_analysis}")
        
        full_context = "\n\n".join(context_parts)
        
        response = model.generate_content(
            f"{full_context}\n\nFarmer's Query: {user_message}",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=200 if is_greeting else CHAT_MAX_TOKENS,
                temperature=0.9 if is_greeting else TEMPERATURE_CHAT,
            )
        )
        
        result = response.text if response and response.text else "I apologize, but I couldn't generate a response."
        return remove_markdown_formatting(result)
    
    except Exception as e:
        return f"Error: {str(e)[:150]}"

def display_message(role: str, content: str, images: List[Image.Image] = None):
    import html
    safe_content = html.escape(content).replace('\n', '<br>')
    
    if role == "user":
        col1, col2 = st.columns([1, 4])
        with col2:
            st.markdown(f"""
            <div class="message-container user-message">
                <div class="message-bubble user-bubble">
                    {safe_content}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if images and len(images) > 0:
                if len(images) == 1:
                    st.image(images[0], width=400, use_container_width=False)
                else:
                    cols = st.columns(min(len(images), 3))
                    for idx, img in enumerate(images):
                        with cols[idx % 3]:
                            st.image(img, use_container_width=True)
                            st.caption(f"Image {idx + 1}")
    else:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div class="message-container">
                <div class="message-bubble assistant-bubble">
                    {safe_content}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div style="text-align: center; padding: 40px 0 30px 0;">
    <h1 style="font-size: 3em; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; letter-spacing: -1px;">
        🌾 AgriAgent
    </h1>
    <p style="color: #718096; font-size: 1.15em; font-weight: 400;">AI-Powered Agricultural Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ==================== CHAT DISPLAY ====================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

display_messages = st.session_state.messages[-MAX_MESSAGES_DISPLAY:]

for message in display_messages:
    display_message(
        message["role"], 
        message["content"], 
        message.get("images")
    )

st.markdown('</div>', unsafe_allow_html=True)

# ==================== INPUT AREA (FIXED LAYOUT) ====================
st.markdown('<div class="input-container">', unsafe_allow_html=True)

# Main input row
col_input, col_upload, col_location, col_clear = st.columns([5, 2, 2, 1])

with col_input:
    user_input = st.text_input(
        "Message",
        placeholder="Ask about crops, diseases, pests, or upload images...",
        key=f"user_input_{st.session_state.input_counter}",
        label_visibility="collapsed"
    )

with col_upload:
    uploaded_files = st.file_uploader(
        "Upload",
        type=SUPPORTED_IMAGE_FORMATS,
        accept_multiple_files=True,
        key=f"file_upload_{st.session_state.input_counter}",
        label_visibility="collapsed"
    )

with col_location:
    location_input = st.text_input(
        "Location",
        placeholder="City name",
        key=f"location_{st.session_state.input_counter}",
        label_visibility="collapsed"
    )

with col_clear:
    if st.button("🗑️", help="Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.weather_data = None
        st.session_state.processed_input = None
        st.session_state.input_counter += 1
        st.rerun()

# Show upload status below input
if uploaded_files:
    st.markdown(f"""
    <div style="margin-top: 8px; text-align: center;">
        <span class="upload-badge">📷 {len(uploaded_files)} image{'s' if len(uploaded_files) > 1 else ''} ready</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ==================== PROCESS INPUT ====================
if user_input or uploaded_files:
    current_input_id = f"{user_input}_{len(uploaded_files) if uploaded_files else 0}_{st.session_state.input_counter}"
    
    if st.session_state.processed_input != current_input_id:
        st.session_state.processed_input = current_input_id
        
        weather_context = ""
        if location_input:
            with st.spinner(f"🌤️ Getting weather..."):
                weather_data = get_weather_data(location_input)
                if weather_data:
                    weather_context = format_weather_context(weather_data)
        
        image_analysis = ""
        image_objects = []
        
        if uploaded_files:
            try:
                for uploaded_file in uploaded_files:
                    file_size_mb = uploaded_file.size / (1024 * 1024)
                    if file_size_mb <= MAX_IMAGE_SIZE_MB:
                        image_objects.append(Image.open(uploaded_file))
                
                if image_objects:
                    st.session_state.messages.append({
                        "role": "user",
                        "content": user_input if user_input else f"📷 {len(image_objects)} image{'s' if len(image_objects) > 1 else ''}",
                        "images": image_objects.copy()
                    })
                    
                    with st.spinner("🔍 Analyzing..."):
                        query = user_input if user_input else "Analyze these images"
                        image_analysis = analyze_images_with_gemini(image_objects, query)
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        elif user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
        
        query = user_input if user_input else "Analyze the uploaded images."
        
        with st.spinner("🤖 Thinking..."):
            response = get_agriculture_response(query, weather_context, image_analysis)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.session_state.input_counter += 1
        st.rerun()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 16px; color: white; margin-bottom: 24px;">
        <h2 style="margin: 0; font-size: 1.5em; font-weight: 600;">🌾 AgriAgent</h2>
        <p style="margin: 8px 0 0 0; opacity: 0.9; font-size: 0.9em;">AI Agricultural Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Capabilities")
    st.markdown("🌱 Crop health assessment")
    st.markdown("🐛 Pest & disease diagnosis")
    st.markdown("📸 Multi-image analysis")
    st.markdown("🌤️ Weather-based advice")
    st.markdown("💬 Natural conversations")
    
    st.markdown("---")
    
    if st.session_state.weather_data:
        weather = st.session_state.weather_data
        st.markdown("### 🌍 Current Weather")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temp", f"{weather['main']['temp']}°C")
            st.metric("Humidity", f"{weather['main']['humidity']}%")
        with col2:
            st.metric("Wind", f"{weather['wind']['speed']} m/s")
            st.metric("Clouds", f"{weather['clouds']['all']}%")
        
        st.caption(f"📍 {weather['name']}")
        st.markdown("---")
    
    st.markdown("### 📊 Session")
    st.metric("Messages", len(st.session_state.messages))
    
    st.markdown("---")
    st.markdown("### 💡 Quick Tips")
    st.markdown("• Upload multiple images")
    st.markdown("• Be specific about crops")
    st.markdown("• Mention your location")
    st.markdown("• Ask follow-up questions")
