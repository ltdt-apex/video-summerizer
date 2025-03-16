import streamlit as st
import time
import requests
import os
import re
from urllib.parse import urlparse, parse_qs
from typing import Optional

# Get backend URL from environment variable or use default
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

def extract_youtube_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats."""
    if not url:
        return None
        
    # Regular YouTube URL patterns
    patterns = [
        r'^https?://(?:www\.)?youtube\.com/watch\?v=([^&]+)',  # Standard URL
        r'^https?://(?:www\.)?youtube\.com/embed/([^?]+)',      # Embed URL
        r'^https?://youtu\.be/([^?]+)',                         # Short URL
    ]
    
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            return match.group(1)
            
    # Try parsing query parameters for other URL formats
    parsed = urlparse(url)
    if 'youtube.com' in parsed.netloc:
        query = parse_qs(parsed.query)
        if 'v' in query:
            return query['v'][0]
            
    return None

def format_string(input_: str) -> str:
    return input_.replace("\n", "  \n")

def get_video_summary(url: str) -> tuple[int, dict]:
    data = {
        "url": url,
    }
    
    response = requests.post(f"{BACKEND_URL}/api/summarize", json=data)
    
    if response.status_code == 200:
        return response.status_code, response.json()
    else:
        return response.status_code, {}

# Streamed response emulator
def response_generator(response: str):
    # Split text into paragraphs
    paragraphs = response.split('\n')
    for paragraph in paragraphs:
        words = paragraph.split()
        for word in words:
            yield word + " "
            time.sleep(0.02)
        if paragraph!=paragraphs[-1]:
            yield "\n\n"

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'model' not in st.session_state:
    st.session_state.model = None

# Sidebar configuration
st.sidebar.title('Settings')
show_parameter_button = st.sidebar.checkbox("Show Parameters")
selected_option = st.sidebar.selectbox('Select Model:', ["gpt-3.5-turbo", "gpt-4"])
reset_button = st.sidebar.button("Clear Chat History")
test_button = st.sidebar.button("test")

if reset_button:
    st.session_state.messages = []

# Main interface
st.title("Video Summarizer")

if show_parameter_button:
    st.write("Current Configuration:")
    st.json({
        "backend_url": BACKEND_URL,
        "model": selected_option,
    })

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if selected_option == "None":
    with st.chat_message("assistant"):
        st.markdown("Please select a model in the sidebar to begin.")
else:
    # Chat inputww
    url = st.chat_input("Paste YouTube URL here...")
    display_url = url
    if test_button:
        url = "test"
        display_url = "https://www.youtube.com/watch?v=aGokIxrtWrg"

    if url:
        # Display user message
        user_message = f"Please summarize this video: {display_url}"
        video_id = extract_youtube_id(display_url)

        st.session_state.messages.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(user_message)

        if video_id:
            st.video(f"https://youtu.be/{video_id}")

        # Generate response
        status = st.empty()
        with status.status("Generating summary..."):
            response_code, output = get_video_summary(url)
        status.empty()

        if response_code != 200:
            message = "Error: Unable to generate summary. Please try again."
        else:
            message = output["summary"]

        # Display assistant response
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
            
            # Stream the response
            for chunk in response_generator(message):
                full_response += chunk
                # Use markdown to properly render newlines
                response_placeholder.markdown(full_response)
                
        st.session_state.messages.append({"role": "assistant", "content": message})

# Footer
st.markdown("""
<div style="position: fixed; bottom: 0; left: 0; right: 0; text-align: center; padding: 10px; background: rgba(0,0,0,0.5);">
    Video Summarizer AI can make mistakes. Please verify important information.
</div>
""", unsafe_allow_html=True) 