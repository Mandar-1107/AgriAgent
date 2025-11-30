# app.py - AgriAgent (FINAL - All Issues Resolved)
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
    initial_sidebar_state="expanded"
)

# ==================== MODERN CHATBOT UI ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', sans-serif;
    }

    
    .main {
        background: #0f1419;
        min-height: 100vh;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .chat-container {
        max-width: 850px;
        margin: 0 auto;
        padding: 100px 20px 160px 20px;
    }
    
    .welcome-message {
        text-align: center;
        padding: 40px 20px;
        color: #8b98a5;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .welcome-message h2 {
        color: #fff;
        font-size: 1.8em;
        margin-bottom: 12px;
    }
    
    .message-container {
        display: flex;
        margin-bottom: 16px;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        justify-content: flex-end;
    }
    
    .message-bubble {
        max-width: 75%;
        padding: 12px 16px;
        border-radius: 16px;
        word-wrap: break-word;
        line-height: 1.5;
        font-size: 15px;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        border-radius: 16px 16px 2px 16px;
    }
    
    .assistant-bubble {
        background: #1c2128;
        color: #e6edf3;
        border-radius: 16px 16px 16px 2px;
        border: 1px solid #30363d;
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #0f1419;
        padding: 10px 20px 20px 20px;
        border-top: 1px solid #30363d;
        z-index: 1000;
    }
    
    .input-wrapper {
        max-width: 850px;
        margin: 0 auto;
    }
    
    /* Form styling */
    [data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    
    .stTextInput > div > div > input {
        border-radius: 24px !important;
        padding: 10px 20px !important;
        border: 1px solid #30363d !important;
        background: #1c2128 !important;
        color: #e6edf3 !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
    }
    
    /* Send button styling */
    .stButton > button {
        border-radius: 20px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 8px 20px !important;
        font-weight: 600 !important;
        height: auto !important;
        margin-top: 2px !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Compact audio/file uploader */
    .stAudio {
        margin-top: -15px !important;
        height: 40px !important;
    }
    
    /* File Uploader Styling - Simplified */
    [data-testid="stFileUploader"] section {
        background: #1c2128 !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    
    [data-testid="stFileUploader"] section:hover {
        border-color: #667eea !important;
    }
    
    [data-testid="stFileUploader"] button {
        background: transparent !important;
        color: #8b98a5 !important;
        border: none !important;
        font-size: 14px !important;
    }
    
    [data-testid="stFileUploader"] button:hover {
        color: #e6edf3 !important;
    }
    
    /* Hide file size limits */
    [data-testid="stFileUploader"] small {
        display: none !important;
    }

    /* Audio Input Styling */
    [data-testid="stAudioInput"] {
        margin-top: -5px !important;
    }
    
    [data-testid="stAudioInput"] > div {
        background: transparent !important;
        border: none !important;
    }
    
    /* Input Container Layout */
    .input-container {
        padding: 15px 20px !important;
    }
    
    .upload-badge {
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        padding: 8px 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        animation: slideUp 0.3s ease;
        z-index: 1001;
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0; 
            transform: translateX(-50%) translateY(10px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(-50%) translateY(0); 
        }
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    
    [data-testid="stSidebar"] {
        background: #0f1419 !important;
        border-right: 1px solid #30363d !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: #0f1419 !important;
        padding-top: 20px !important;
    }
    
    [data-testid="collapsedControl"] {
        background: #1c2128 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        margin-top: 80px !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: #667eea !important;
        color: #fff !important;
    }
    
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 998;
        background: #0f1419;
        padding: 16px 20px;
        border-bottom: 1px solid #30363d;
        text-align: center;
    }
    
    .app-header h1 {
        font-size: 1.8em;
        font-weight: 700;
        color: #fff;
        margin: 0;
    }
    
    .app-header p {
        color: #8b98a5;
        font-size: 0.9em;
        margin: 4px 0 0 0;
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
        "greeting_done": False,
        "location_asked": False,
        "user_declined_help": False,
        "current_mode": "neutral",  # neutral, advisory, support
        "context": {
            "location": None,
            "soil_type": None,
            "water_source": None,
            "budget": None,
            "experience": None,
            "farm_size": None,
            "active_farming": True,
            "current_crop": None,
            "crop_stage": None
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# ==================== API CONFIGURATION ====================
def configure_gemini():
    if not GEMINI_API_KEY:
        st.error("⚠️ Gemini API Key Missing")
        st.stop()
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        st.stop()

configure_gemini()

# ==================== HELPER FUNCTIONS ====================
def get_indian_season() -> str:
    month = datetime.now().month
    for season, months in INDIAN_SEASONS.items():
        if month in months:
            return season
    return "Transition Period"

def extract_context_from_history():
    context = st.session_state.context.copy()
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            content_lower = msg["content"].lower()
            
            # 1. Check for explicit rejection
            if any(phrase in content_lower for phrase in ["no", "dont want", "don't want", "not interested", "stop asking"]):
                st.session_state.user_declined_help = True
            
            # 2. Check for resting soil (Fallow)
            if any(phrase in content_lower for phrase in ["not growing", "giving time", "break", "replenish", "rest"]):
                context["active_farming"] = False
                st.session_state.current_mode = "support"
            
            # 3. Extract Location (Expanded List)
            location_keywords = [
                # Maharashtra
                "mumbai", "pune", "nagpur", "nashik", "aurangabad", "solapur", "kolhapur", 
                "thane", "amravati", "jalgaon", "satara", "nanded", "akola", "latur", "ahmednagar",
                # States
                "maharashtra", "punjab", "karnataka", "gujarat", "rajasthan", "tamil nadu",
                "uttar pradesh", "madhya pradesh", "west bengal", "telangana", "kerala",
                # Major Cities
                "delhi", "bangalore", "hyderabad", "chennai", "kolkata", "ahmedabad", "surat", 
                "jaipur", "lucknow", "indore", "bhopal", "chandigarh", "patna"
            ]
            
            if not context["location"]:
                for keyword in location_keywords:
                    if keyword in content_lower:
                        context["location"] = keyword.title()
                        break
            
            # 4. Extract Crop (Critical for Context Awareness)
            common_crops = ["orange", "wheat", "rice", "paddy", "cotton", "soybean", "sugarcane", 
                          "maize", "corn", "onion", "potato", "tomato", "chickpea", "gram", 
                          "mustard", "groundnut", "turmeric", "ginger", "banana", "mango", "grape", "pomegranate"]
            
            for crop in common_crops:
                if crop in content_lower:
                    context["current_crop"] = crop.title()
                    st.session_state.current_mode = "support" # Switch to support mode if crop mentioned
                    break

            # 5. Detect Mode based on intent
            if any(word in content_lower for word in ["suggest", "recommend", "what to grow", "best crop", "profitable"]):
                st.session_state.current_mode = "advisory"
            
            # 6. Other details
            if not context["soil_type"] and any(word in content_lower for word in ["clay", "sand", "loam", "soil"]):
                context["soil_type"] = content_lower
            
            if not context["water_source"] and any(word in content_lower for word in ["rain", "irrigation", "well", "borewell"]):
                context["water_source"] = content_lower
            
            if not context["farm_size"] and any(word in content_lower for word in ["acre", "hectare"]):
                numbers = re.findall(r'\d+', content_lower)
                if numbers:
                    context["farm_size"] = f"{numbers[0]} acres"
    
    st.session_state.context = context
    return context

def is_simple_greeting(message: str) -> bool:
    greetings = ['hi', 'hello', 'hey', 'namaste', 'good morning', 'good evening']
    casual = ['how are you', 'what is your name', 'who are you']
    
    message_lower = message.lower().strip()
    if message_lower in greetings: return True
    for phrase in casual:
        if phrase in message_lower and len(message_lower) < 25: return True
    return False

def remove_markdown_formatting(text: str) -> str:
    """Safe string replacement to remove markdown"""
    text = text.replace('**', '')
    text = text.replace('*', '')
    text = text.replace('_', '')
    text = text.replace('#', '')
    return text

def extract_location_from_query(query: str) -> Optional[str]:
    """Expanded location extraction"""
    cities = [
        "mumbai", "pune", "nagpur", "nashik", "aurangabad", "solapur", "amravati", "kolhapur", 
        "thane", "jalgaon", "satara", "nanded", "akola", "latur", "ahmednagar",
        "delhi", "bangalore", "hyderabad", "chennai", "kolkata", "ahmedabad", "surat", 
        "jaipur", "lucknow", "indore", "bhopal", "chandigarh", "patna", "vadodara", "coimbatore"
    ]
    
    states_to_cities = {
        "maharashtra": "mumbai", "punjab": "chandigarh", "karnataka": "bangalore",
        "gujarat": "ahmedabad", "rajasthan": "jaipur", "madhya pradesh": "bhopal",
        "uttar pradesh": "lucknow", "tamil nadu": "chennai", "west bengal": "kolkata",
        "telangana": "hyderabad", "andhra pradesh": "visakhapatnam", "kerala": "kochi"
    }
    
    query_lower = query.lower()
    for city in cities:
        if city in query_lower: return city.title()
    for state, capital in states_to_cities.items():
        if state in query_lower: return capital.title()
    return None

def get_weather_data(location: str) -> Optional[Dict[str, Any]]:
    if not WEATHER_API_KEY: return None
    
    if (st.session_state.weather_data and 
        st.session_state.last_location and
        st.session_state.last_location.lower() == location.lower() and
        st.session_state.weather_cache_time and
        (datetime.now() - st.session_state.weather_cache_time).seconds < WEATHER_CACHE_DURATION):
        return st.session_state.weather_data
    
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": f"{location},IN", "appid": WEATHER_API_KEY, "units": WEATHER_UNITS}
        response = requests.get(url, params=params, timeout=WEATHER_TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            st.session_state.weather_data = data
            st.session_state.weather_cache_time = datetime.now()
            st.session_state.last_location = location
            return data
    except: pass
    return None

def format_weather_context(weather_data: Dict[str, Any]) -> str:
    if not weather_data: return ""
    try:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        return f"Weather: {temp}°C, {humidity}% humidity."
    except: return ""

def resize_image(image: Image.Image, max_size: int = 2048) -> Image.Image:
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return image

def analyze_images_with_gemini(images: List[Image.Image], query: str = "") -> str:
    """Visual Disease Diagnosis"""
    try:
        model = genai.GenerativeModel(GEMINI_VISION_MODEL)
        season = get_indian_season()
        
        prompt = f"""You are an expert plant pathologist and agronomist.
        
        Task: Analyze these agricultural images.
        User Query: "{query}"
        Season: {season}
        
        Provide a structured diagnosis:
        1. **Identification**: What crop/plant is this?
        2. **Diagnosis**: Identify specific disease, pest, or deficiency. Be precise.
        3. **Severity**: Mild, Moderate, or Severe?
        4. **Immediate Action**: Chemical/Organic treatment with dosage.
        5. **Prevention**: How to stop recurrence.
        
        If the image is NOT related to agriculture, politely decline to analyze it.
        Keep response conversational but professional. Max {MAX_RESPONSE_LENGTH} words."""
        
        content_parts = [prompt] + [resize_image(img) for img in images]
        
        response = model.generate_content(
            content_parts,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=IMAGE_ANALYSIS_MAX_TOKENS,
                temperature=0.4, # Lower temperature for more accurate diagnosis
            )
        )
        
        result = response.text if response and response.text else "I couldn't analyze the image clearly. Please try a clearer photo."
        
        # Update context if crop is identified (simple heuristic)
        st.session_state.current_mode = "support" 
        
        return remove_markdown_formatting(result)
    
    except Exception as e:
        return f"Image analysis failed: {str(e)[:100]}"

def get_agriculture_response(user_message: str, weather_context: str = "", image_analysis: str = "") -> str:
    """Smart Context-Aware Response Generation"""
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # 1. Update Context & Mode
        context = extract_context_from_history()
        current_season = get_indian_season()
        is_greeting = is_simple_greeting(user_message)
        
        # 2. Construct System Prompt based on State
        base_prompt = f"""You are AgriAgent, an intelligent agricultural assistant for Indian farmers.
        
        Current Context:
        - Location: {context.get('location', 'Unknown')}
        - Season: {current_season}
        - Weather: {weather_context if weather_context else 'Not available'}
        - Active Crop: {context.get('current_crop', 'None')}
        - Mode: {st.session_state.current_mode.upper()}
        """
        
        # PRIORITY 1: Image Analysis (Visual Diagnosis)
        if image_analysis:
            system_prompt = f"""{base_prompt}
            
            TASK: Explain the image analysis results to the farmer.
            Analysis: {image_analysis}
            
            RULES:
            - Focus on the specific problem identified.
            - Provide clear, step-by-step treatment instructions.
            - Be empathetic but authoritative on the diagnosis.
            - Ask if they need clarification on the treatment."""

        # PRIORITY 2: User Declined Help
        elif st.session_state.user_declined_help and len(st.session_state.messages) > 4:
            system_prompt = f"""{base_prompt}
            User has indicated they don't need more help right now.
            Reply politely, acknowledging their choice. Keep it very brief (under 50 words).
            Do not ask further questions."""

        # PRIORITY 3: Fallow/Resting Soil
        elif not context["active_farming"]:
            system_prompt = f"""{base_prompt}
            User wants to rest their soil (fallow).
            - Commend this sustainable practice.
            - Suggest 2-3 cover crops (like Dhaincha, Sunhemp) to improve soil fertility during the break.
            - Keep it encouraging."""

        # PRIORITY 4: Greeting
        elif is_greeting and not st.session_state.greeting_done:
            st.session_state.greeting_done = True
            system_prompt = f"""{base_prompt}
            First interaction.
            - Warm, friendly Indian-style greeting (Namaste/Hello).
            - Ask: "Where are you farming and what crops are you interested in?"
            - Keep it short and welcoming."""

        # PRIORITY 5: Support Mode (Existing Crop)
        elif st.session_state.current_mode == "support" or context.get("current_crop"):
            system_prompt = f"""{base_prompt}
            MODE: SUPPORT (User has an active crop: {context.get('current_crop')})
            
            User Query: "{user_message}"
            
            RULES:
            - Provide specific advice for {context.get('current_crop')}.
            - Do NOT suggest other crops unless explicitly asked.
            - Focus on care, pest management, irrigation, or harvest for THIS crop.
            - If the query is generic, relate it back to {context.get('current_crop')}.
            - Be practical and actionable."""

        # PRIORITY 6: Advisory Mode (Planning)
        elif st.session_state.current_mode == "advisory":
            system_prompt = f"""{base_prompt}
            MODE: ADVISORY (User is planning new crops)
            
            User Query: "{user_message}"
            
            RULES:
            - Suggest 2-3 suitable crops for {context.get('location', 'their area')} in {current_season}.
            - Consider water: {context.get('water_source', 'unknown')} and soil: {context.get('soil_type', 'unknown')}.
            - Include estimated cost and returns if possible.
            - Ask clarifying questions about their resources if needed."""

        # PRIORITY 7: General/Neutral
        else:
            system_prompt = f"""{base_prompt}
            MODE: GENERAL
            
            User Query: "{user_message}"
            
            RULES:
            - Answer the agricultural question accurately.
            - If they haven't mentioned location or crop, gently ask for it to give better advice.
            - Keep tone helpful and encouraging."""
        
        # 3. Generate Response
        response = model.generate_content(
            f"{system_prompt}\n\nFarmer: {user_message}",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=CHAT_MAX_TOKENS,
                temperature=0.7,
            )
        )
        
        result = response.text if response and response.text else "I'm here to help with your farming questions!"
        return remove_markdown_formatting(result)
    
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)[:150]}"

def display_message(role: str, content: str, images: List[Image.Image] = None):
    import html
    safe_content = html.escape(content).replace('\n', '<br>')
    
    if role == "user":
        st.markdown(f"""
        <div class="message-container user-message">
            <div class="message-bubble user-bubble">
                {safe_content}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if images and len(images) > 0:
            if len(images) == 1:
                st.image(images[0], width=400)
            else:
                cols = st.columns(min(len(images), 3))
                for idx, img in enumerate(images):
                    with cols[idx % 3]:
                        st.image(img, use_container_width=True)
    else:
        st.markdown(f"""
        <div class="message-container">
            <div class="message-bubble assistant-bubble">
                {safe_content}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div class="app-header">
    <h1>🌾 AgriAgent</h1>
    <p>AI Agricultural Assistant</p>
</div>
""", unsafe_allow_html=True)

# ==================== CHAT DISPLAY ====================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-message">
        <h2>👋 Welcome to AgriAgent</h2>
        <p>Your friendly AI agricultural assistant for crop advice, disease diagnosis, and farming guidance.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    display_messages = st.session_state.messages[-MAX_MESSAGES_DISPLAY:]
    for message in display_messages:
        display_message(message["role"], message["content"], message.get("images"))

st.markdown('</div>', unsafe_allow_html=True)

def process_audio_input(audio_file) -> str:
    """Process audio input using Gemini"""
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        # Create a prompt for transcription/translation
        prompt = """
        Listen to this audio. 
        1. Transcribe it exactly as spoken.
        2. If it is in a local Indian language (Hindi, Marathi, etc.), translate it to English.
        3. Return ONLY the English translation (or transcription if already English).
        """
        
        # Create a temporary file for the audio
        # Note: In a real deployment we might handle bytes directly if supported, 
        # but saving to temp is safer for API compatibility
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_file.read())
            tmp_path = tmp_file.name
            
        # Upload to Gemini (using File API if needed, or passing data if supported by SDK version)
        # For simplicity with current SDK, we'll try to use the file API or direct content
        # Assuming genai.upload_file is available or we pass the file object
        
        # Since we can't easily check SDK version capabilities at runtime without docs,
        # we'll use the standard file upload approach which is robust
        uploaded_file = genai.upload_file(tmp_path)
        
        response = model.generate_content([prompt, uploaded_file])
        
        # Cleanup
        os.unlink(tmp_path)
        
        return response.text.strip()
        
    except Exception as e:
        return f"Error processing audio: {str(e)}"

# ==================== INPUT AREA ====================
st.markdown('<div class="input-container"><div class="input-wrapper">', unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    col_text, col_send = st.columns([8, 1])
    
    with col_text:
        user_input = st.text_input(
            "Message", 
            placeholder="Type your message...", 
            label_visibility="collapsed"
        )
    
    with col_send:
        submit_button = st.form_submit_button("Send ➤")
    
    # Media inputs in a compact row below
    col_media1, col_media2, col_spacer = st.columns([3, 3, 2])
    
    with col_media1:
        audio_value = st.audio_input("Record", label_visibility="collapsed")
        
    with col_media2:
        uploaded_files = st.file_uploader(
            "Upload Images", 
            type=SUPPORTED_IMAGE_FORMATS, 
            accept_multiple_files=True,
            label_visibility="collapsed"
        )

st.markdown('</div></div>', unsafe_allow_html=True)

# ==================== PROCESS INPUT ====================
if submit_button and (user_input or audio_value or uploaded_files):
    
    final_query = user_input
    
    # Process Audio
    if audio_value:
        with st.spinner("Processing audio..."):
            transcribed_text = process_audio_input(audio_value)
            if "Error" not in transcribed_text:
                if final_query:
                    final_query += f" {transcribed_text}"
                else:
                    final_query = transcribed_text
                st.toast(f"Audio: {transcribed_text}", icon="🎤")
            else:
                st.error(transcribed_text)
    
    # ... (rest of processing logic same as before) ...
    
    weather_context = ""
    if final_query:
        location = extract_location_from_query(final_query)
        if location:
            weather_data = get_weather_data(location)
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
                    "content": final_query if final_query else f"📷 {len(image_objects)} image{'s' if len(image_objects) > 1 else ''}",
                    "images": image_objects.copy()
                })
                
                with st.spinner("Analyzing images..."):
                    query = final_query if final_query else "Analyze images"
                    image_analysis = analyze_images_with_gemini(image_objects, query)
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    elif final_query:
        st.session_state.messages.append({
            "role": "user",
            "content": final_query
        })
    
    if final_query or image_analysis:
        query = final_query if final_query else "Analyze images"
        
        with st.spinner("Thinking..."):
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
                border-radius: 16px; color: white; margin-bottom: 24px; text-align: center;">
        <h2 style="margin: 0; font-size: 1.5em;">🌾 AgriAgent</h2>
        <p style="margin: 8px 0 0 0; opacity: 0.95; font-size: 0.9em;">AI Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Features")
    st.markdown("""
    - 🌱 Crop recommendations
    - 🐛 Disease diagnosis  
    - 📸 Image analysis
    - 🌤️ Weather insights
    - 💬 Natural conversation
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Session")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Season", get_indian_season()[:8])
    
    if st.session_state.weather_data:
        st.markdown("---")
        weather = st.session_state.weather_data
        st.markdown("### 🌍 Weather")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temp", f"{weather['main']['temp']}°C")
            st.metric("Humidity", f"{weather['main']['humidity']}%")
        with col2:
            st.metric("Wind", f"{weather['wind']['speed']} m/s")
            st.metric("Clouds", f"{weather['clouds']['all']}%")
        
        st.info(f"📍 {weather['name']}")
    
    st.markdown("---")
    st.caption("🌾 Made with ❤️ for farmers")
