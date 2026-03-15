import streamlit as st
import os
import time
from PIL import Image

# Configuration
st.set_page_config(
    page_title="In Loving Memory - A Life Story",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for UI styling, hiding Streamlit default elements
st.markdown("""
<style>
    /* Global Theme */
    .stApp {
        background: linear-gradient(to bottom, #111111, #1e1b24, #0f0f0f);
        color: #e8e8e8;
    }
    
    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebar"] {display: none;}

    /* Typography */
    .hero-title {
        text-align: center;
        font-family: 'Georgia', serif;
        color: #f2e3c6;
        font-size: 3.8rem;
        font-weight: 300;
        margin-top: 3rem;
        margin-bottom: 5px;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
        animation: fadeIn 3s ease-in;
    }
    .hero-subtitle {
        text-align: center;
        font-family: 'Georgia', serif;
        color: #b5a48b;
        font-size: 1.6rem;
        font-style: italic;
        margin-bottom: 15px;
        animation: fadeIn 4s ease-in;
    }
    .hero-dates {
        text-align: center;
        font-family: 'Arial', sans-serif;
        color: #8c7f6d;
        font-size: 1.2rem;
        letter-spacing: 3px;
        margin-bottom: 4rem;
        animation: fadeIn 5s ease-in;
    }
    
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(10px); }
        100% { opacity: 1; transform: translateY(0); }
    }

    .section-header {
        text-align: center;
        font-family: 'Georgia', serif;
        color: #f2e3c6;
        font-size: 2.6rem;
        margin-top: 5rem;
        margin-bottom: 3rem;
        border-bottom: 1px solid #b5a48b;
        padding-bottom: 15px;
        display: inline-block;
    }
    .center-wrapper {
        text-align: center;
    }

    /* Timeline (Roadmap) CSS */
    .timeline {
        position: relative;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px 0;
    }
    .timeline::after {
        content: '';
        position: absolute;
        width: 3px;
        background: linear-gradient(to bottom, rgba(181, 164, 139, 0) 0%, rgba(181, 164, 139, 0.8) 15%, rgba(181, 164, 139, 0.8) 85%, rgba(181, 164, 139, 0) 100%);
        top: 0;
        bottom: 0;
        left: 50%;
        margin-left: -1px;
    }
    .timeline-container {
        padding: 10px 40px;
        position: relative;
        background-color: inherit;
        width: 50%;
    }
    .timeline-container::after {
        content: '';
        position: absolute;
        width: 16px;
        height: 16px;
        right: -8px;
        background-color: #111111;
        border: 3px solid #b5a48b;
        top: 24px;
        border-radius: 50%;
        z-index: 1;
        box-shadow: 0 0 10px rgba(181, 164, 139, 0.5);
    }
    .left { left: 0; }
    .right { left: 50%; }
    .right::after { left: -8px; }
    
    .timeline-content {
        padding: 25px 35px;
        background: rgba(255, 255, 255, 0.03);
        position: relative;
        border-radius: 12px;
        border: 1px solid rgba(181, 164, 139, 0.15);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: all 0.4s ease;
        backdrop-filter: blur(5px);
    }
    .timeline-content:hover {
        transform: scale(1.02);
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(181, 164, 139, 0.4);
        box-shadow: 0 15px 40px rgba(0,0,0,0.7);
    }
    .timeline-year {
        font-size: 1.5rem;
        font-weight: 600;
        color: #d1b88e;
        margin-bottom: 12px;
        font-family: 'Georgia', serif;
    }
    .timeline-text {
        font-size: 1.15rem;
        line-height: 1.7;
        color: #cccccc;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 300;
    }

    /* Quote */
    .emotional-quote {
        text-align: center;
        font-style: italic;
        color: #d1b88e;
        font-size: 1.5rem;
        max-width: 650px;
        margin: 5rem auto;
        line-height: 1.9;
        padding: 30px;
        border-top: 1px solid rgba(209, 184, 142, 0.3);
        border-bottom: 1px solid rgba(209, 184, 142, 0.3);
        background: radial-gradient(circle, rgba(255,255,255,0.03) 0%, rgba(0,0,0,0) 80%);
    }

    /* Footer */
    .footer {
        text-align: center;
        font-family: 'Georgia', serif;
        color: #666666;
        margin-top: 6rem;
        padding-top: 3rem;
        padding-bottom: 3rem;
        font-size: 1rem;
        background: linear-gradient(to top, rgba(0,0,0,0.8), transparent);
    }
    
    /* Login Box */
    .login-container {
        background: rgba(255, 255, 255, 0.02);
        padding: 40px;
        border-radius: 15px;
        border: 1px solid rgba(181, 164, 139, 0.2);
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        text-align: center;
        margin-top: 2rem;
    }

    /* Responsive timeline */
    @media screen and (max-width: 768px) {
        .timeline::after { left: 31px; }
        .timeline-container { width: 100%; padding-left: 70px; padding-right: 25px; }
        .timeline-container::after { left: 23px; }
        .right { left: 0%; }
        .hero-title { font-size: 2.8rem; }
    }

    /* Floating Embers */
    .ember {
        position: fixed;
        bottom: -50px;
        width: 5px;
        height: 5px;
        background: #ffab40;
        border-radius: 50%;
        box-shadow: 0 0 10px 3px #ffab40, 0 0 20px 5px #ff5722;
        opacity: 0.8;
        z-index: 9999;
        pointer-events: none;
        animation: floatUp 15s linear infinite, glow 3s ease-in-out infinite alternate;
    }

    @keyframes floatUp {
        0% { bottom: -50px; transform: translateX(0px) scale(0.8); opacity: 0; }
        10% { opacity: 1; }
        80% { opacity: 0.8; }
        100% { bottom: 110vh; transform: translateX(100px) scale(1.2); opacity: 0; }
    }

    @keyframes glow {
        from { box-shadow: 0 0 5px 1px #ffab40; opacity: 0.6; }
        to { box-shadow: 0 0 15px 6px #ff5722; opacity: 1; }
    }

    /* Force buttons to stretch width without triggering streamlit warning */
    .stButton > button {
        width: 100% !important;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(255, 171, 64, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Embers HTML
EMBERS_HTML = """
<div class="ember" style="left: 10%; animation-delay: 0s; animation-duration: 18s;"></div>
<div class="ember" style="left: 20%; animation-delay: 5s; animation-duration: 25s;"></div>
<div class="ember" style="left: 30%; animation-delay: 2s; animation-duration: 22s;"></div>
<div class="ember" style="left: 45%; animation-delay: 7s; animation-duration: 20s;"></div>
<div class="ember" style="left: 50%; animation-delay: 4s; animation-duration: 19s;"></div>
<div class="ember" style="left: 65%; animation-delay: 1s; animation-duration: 23s;"></div>
<div class="ember" style="left: 70%; animation-delay: 8s; animation-duration: 21s;"></div>
<div class="ember" style="left: 85%; animation-delay: 3s; animation-duration: 24s;"></div>
<div class="ember" style="left: 90%; animation-delay: 6s; animation-duration: 19s;"></div>
"""
st.markdown(EMBERS_HTML, unsafe_allow_html=True)


# Constants
PHOTOS_DIR = "photos"
PASSWORD = "password" 
GRANDFATHER_NAME = "Peter Gopal"
BIRTH_YEAR = "1945"
DEATH_YEAR = "2025"
CYCLE_INTERVAL = 4.0 

STORY_EVENTS = [
    {"year": "1945", "title": "A Beautiful Beginning", "text": "Born into a world of endless possibilities. A quiet dawn that would eventually touch so many lives with unconditional warmth and light."},
    {"year": "1968", "title": "Finding True Love", "text": "A simple glance turned into a lifelong promise. Hand in hand, they built a sanctuary of devotion, weathering every storm with laughter and grace."},
    {"year": "1975", "title": "Building the Foundation", "text": "Years of tireless sacrifice, late nights, and boundless hope. Every drop of sweat was poured into giving us a future he had only dreamed of."},
    {"year": "1998", "title": "The Joy of Grandchildren", "text": "A new chapter of endless smiles, spoiled weekends, and gentle lessons. He became the ultimate guardian, a gentle giant in our adoring eyes."},
    {"year": "2015", "title": "The Golden Years", "text": "Reflecting on a life incredibly well-lived. Tending to his beautiful garden, sharing a lifetime of wisdom, and sitting peacefully with the ones he cherished."},
    {"year": "2025", "title": "A Peaceful Sunset", "text": "He left this world just as he lived in it—with quiet strength, immense dignity, and surrounded by our fierce love. His legacy now echoes in every beat of our hearts."}
]

# Session Initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "photo_index" not in st.session_state:
    st.session_state.photo_index = 0

if "last_update_time" not in st.session_state:
    st.session_state.last_update_time = time.time()

def authenticate():
    # Adding some blank space
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown(f"<h1 class='hero-title'>Remembering {GRANDFATHER_NAME}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-dates'>🌅 {BIRTH_YEAR} — {DEATH_YEAR} 🌇</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<div style='color: #b5a48b; font-size: 1.2rem; font-style: italic; margin-bottom: 20px;'>This sacred space holds his life's most cherished memories.<br>Please enter the password to walk this emotional journey with us.</div>", unsafe_allow_html=True)
        pwd_input = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Enter Password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Unlock His Memory"):
            if pwd_input == PASSWORD:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
        st.markdown("</div>", unsafe_allow_html=True)

def render_timeline():
    st.markdown("<div class='center-wrapper'><h2 class='section-header'>His Journey, Our Roadmap</h2></div>", unsafe_allow_html=True)
    
    timeline_html = "<div class='timeline'>"
    for i, event in enumerate(STORY_EVENTS):
        side = "left" if i % 2 == 0 else "right"
        timeline_html += f"""
        <div class="timeline-container {side}">
            <div class="timeline-content">
                <div class="timeline-year">{event['year']} &mdash; {event['title']}</div>
                <div class="timeline-text">{event['text']}</div>
            </div>
        </div>
        """
    timeline_html += "</div>"
    st.markdown(timeline_html, unsafe_allow_html=True)

def get_photos():
    if not os.path.exists(PHOTOS_DIR):
        os.makedirs(PHOTOS_DIR)
        
    supported_extensions = {".jpg", ".jpeg", ".png", ".webp"}
    photos = []
    
    for filename in os.listdir(PHOTOS_DIR):
        ext = os.path.splitext(filename)[1].lower()
        if ext in supported_extensions:
            photos.append(os.path.join(PHOTOS_DIR, filename))
            
    return sorted(photos)

def render_gallery():
    st.markdown("<div class='center-wrapper'><h2 class='section-header'>Fading Embers: Precious Moments</h2></div>", unsafe_allow_html=True)
    
    photos = get_photos()
    
    if not photos:
        st.info(f"No photos found. Please add image files to the '{PHOTOS_DIR}' folder to watch his beautiful life unfold.")
    else:
        # Time-based exact photo index cycling
        current_time = time.time()
        time_elapsed = current_time - st.session_state.last_update_time
        
        if time_elapsed > CYCLE_INTERVAL:
            st.session_state.photo_index = (st.session_state.photo_index + 1) % len(photos)
            st.session_state.last_update_time = current_time

        # Ensure index safety if photos were deleted
        if st.session_state.photo_index >= len(photos):
            st.session_state.photo_index = 0
            
        current_photo = photos[st.session_state.photo_index]
        
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            # Display active main image
            try:
                image = Image.open(current_photo)
                st.image(image)
                st.markdown(f"<div style='text-align:center; color: #8c7f6d; font-style: italic; margin-top: 15px;'>A glimpse into forever...</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading image: {e}")
                
            # Display controls under the image to be more subtle
            st.write("")
            btn_col1, btn_col2, btn_col3, btn_col4, btn_col5 = st.columns([1, 2, 1, 2, 1])
            with btn_col2:
                if st.button("❮ Go Back in Time"):
                    st.session_state.photo_index = (st.session_state.photo_index - 1) % len(photos)
                    st.session_state.last_update_time = time.time()
                    st.rerun()
            with btn_col4:
                if st.button("Relive Next ❯"):
                    st.session_state.photo_index = (st.session_state.photo_index + 1) % len(photos)
                    st.session_state.last_update_time = time.time()
                    st.rerun()

    # Auto loop triggering
    if photos:
        time.sleep(1)
        st.rerun()

def show_main_content():
    # Hero Section
    st.markdown(f"<h1 class='hero-title'>{GRANDFATHER_NAME}</h1>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>His Story, Our Legacy</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-dates'>🌅 {BIRTH_YEAR} — {DEATH_YEAR} 🌇</div>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='emotional-quote'>
            "Those we love don't go away, they walk beside us every day. <br><br>
            Unseen, unheard, but always near; still loved, still missed and very dear. 
            His light may have faded from this world, but the fire he lit in our hearts will warm us forever."
        </div>
    """, unsafe_allow_html=True)
    
    # Roadmap / Timeline
    render_timeline()
    
    # Breathing room
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Photo Gallery
    render_gallery()
    
    # Footer
    st.markdown("""
        <div class='footer'>
            With tears in our eyes and boundless love in our hearts, we say goodbye.<br>
            <br>
            <span style='font-size: 1.2rem; color: #b5a48b; font-style: italic;'>Forever & Always.</span>
        </div>
    """, unsafe_allow_html=True)

if not st.session_state.authenticated:
    authenticate()
else:
    show_main_content()
