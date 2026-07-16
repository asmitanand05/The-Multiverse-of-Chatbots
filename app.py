import streamlit as st
from google import genai
import os 
from dotenv import load_dotenv

# ==========================================
# 1. PAGE CONFIGURATION (Must be first!)
# ==========================================
st.set_page_config(
    page_title="Multiverse Chat",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. CUSTOM CSS FUNCTION (Theming)
# ==========================================
def add_custom_css(theme):
    if theme == "Dark":
        st.markdown(
            """
            <style>
            .stApp { background: linear-gradient(135deg, #0f2027, #203a43, #2c5364) !important; color: white !important; }
            [data-testid="stSidebar"] { background-color: rgba(15, 32, 39, 0.8) !important; border-right: 1px solid #4ffafc !important; color: white !important;}
            h1 { color: #4ffafc !important; text-align: center !important; font-family: 'Courier New', Courier, monospace !important; text-shadow: 2px 2px 4px #000000 !important; }
            .stTextInput input { background-color: #1e3c4a !important; color: white !important; border: 1px solid #4ffafc !important; border-radius: 10px !important; }
            p, .stMarkdown, .stText { color: white !important; }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .stApp { background: linear-gradient(135deg, #fdfbfb, #ebedee) !important; color: #1a1a1a !important; }
            [data-testid="stSidebar"] { background-color: rgba(253, 251, 251, 0.9) !important; border-right: 1px solid #005f73 !important; color: #1a1a1a !important;}
            h1 { color: #005f73 !important; text-align: center !important; font-family: 'Courier New', Courier, monospace !important; text-shadow: 1px 1px 2px #cccccc !important; }
            .stTextInput input { background-color: #ffffff !important; color: #1a1a1a !important; border: 1px solid #005f73 !important; border-radius: 10px !important; }
            p, .stMarkdown, .stText { color: #1a1a1a !important; }
            </style>
            """,
            unsafe_allow_html=True
        )

# ==========================================
# 3. API SETUP
# ==========================================
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ==========================================
# 4. SIDEBAR SETTINGS & THEME TOGGLE
# ==========================================
st.sidebar.title("App Settings")

personalities = [
    "An expert Hacker",
    "An angry Ravi Shastri",
    "A crazy Ronaldo fan",
    "Donald Trump",
    "A panicked college student at 3 AM",
    "A 1920s Mafia Boss",
    "A highly sarcastic fitness coach"
]

personality = st.sidebar.selectbox("Who do you want to talk to?", personalities)
intensity = st.sidebar.slider("Intensity Level", min_value=1, max_value=10, value=5)

st.sidebar.divider()
st.sidebar.markdown("**Note:** The intensity slider affects how strongly the chatbot embodies the persona.")

# Theme Selector
selected_theme = st.sidebar.segmented_control("Choose a theme", options=["Light", "Dark"], default="Dark", key="theme_selector")

# Apply the selected theme immediately
add_custom_css(selected_theme)

# ==========================================
# 5. DYNAMIC AVATARS
# ==========================================
if personality == "An expert Hacker":
    bot_avatar = "💻"
elif personality == "An angry Ravi Shastri":
    bot_avatar = "🏏"
elif personality == "A crazy Ronaldo fan":
    bot_avatar = "⚽"
elif personality == "Donald Trump":
    bot_avatar = "🇺🇸"
elif personality == "A panicked college student at 3 AM":
    bot_avatar = "☕"
elif personality == "A 1920s Mafia Boss":
    bot_avatar = "🕴️"
elif personality == "A highly sarcastic fitness coach":
    bot_avatar = "🏋️‍♂️"
else:
    bot_avatar = "🤖"

# ==========================================
# 6. MAIN APP LAYOUT & CHAT
# ==========================================
st.markdown("<h1>THE MULTIVERSE OF CHATBOTS</h1>", unsafe_allow_html=True)
st.divider()

# Welcome Message (Empty State)
with st.chat_message("assistant", avatar="🌌"):
    st.write(f"Welcome to the Multiverse! I am currently attuned to the mind of **{personality}**. Adjust my intensity in the sidebar and say hello!")

# Chat Input
user_message = st.text_input("Say something: ")

if st.button("SEND"):
    if user_message:
        
        # Render the user's message
        with st.chat_message("user"):
            st.write(user_message)
            
        # Prompt Engineering
        ai_instructions = (
            f"You are acting as {personality}. "
            f"Your personality intensity level is {intensity} out of 10. "
            f"Respond to the following message staying completely in character: {user_message}"
        )
        
        # Try-Except block for safe API calls
        try:
            with st.spinner("Connecting to the multiverse!......"):
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=ai_instructions
                )
                
            st.success("Message received!")
            
            # Render the AI's response with dynamic avatar
            with st.chat_message("assistant", avatar=bot_avatar):
                st.write(response.text)
                
        except Exception as e:
            st.error(f"Oops! Something went wrong in the multiverse: {e}")
    
    else:
        st.warning("Please type a message first")