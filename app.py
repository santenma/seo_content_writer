import streamlit as st
import os
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="SEO Blog Content Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
    
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    
    .warning-message {
        background: #fff3cd;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #ffeaa7;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    if 'generated_content' not in st.session_state:
        st.session_state.generated_content = {}
    if 'seo_settings' not in st.session_state:
        st.session_state.seo_settings = {
            'primary_keyword': '',
            'secondary_keywords': [],
            'content_length': 800,
            'tone': 'professional',
            'content_type': 'blog_post'
        }

def render_sidebar():
    """Render sidebar navigation"""
    with st.sidebar:
        st.markdown("### 🚀 Navigation")
        
        if st.session_state.authenticated:
            st.success(f"Welcome, {st.session_state.username}!")
            
            # Navigation menu
            pages = {
                "🏠 Home": "home",
                "📝 Content Generator": "generator",
                "⚙️ SEO Settings": "seo_settings",
                "📊 Bulk Generation": "bulk",
                "📈 Analytics": "analytics",
                "👤 Profile": "profile"
            }
            
            for page_name, page_key in pages.items():
                if st.button(page_name, key=f"nav_{page_key}"):
                    st.session_state.current_page = page_key
                    st.rerun()
            
            st.markdown("---")
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.username = ""
                st.session_state.current_page = "home"
                st.rerun()
        else:
            st.info("Please login to access all features")

def render_home_page():
    """Render home/landing page"""
    st.markdown('<h1 class="main-header">📝 SEO Blog Content Generator</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Transform Any Content into SEO-Optimized Blog Posts</h3>
            <p>Generate high-quality, search-engine-optimized blog content from various sources including articles, YouTube videos, and audio files.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature highlights
    st.markdown("## ✨ Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📚 Multi-Source Input</h4>
            <ul>
                <li>Text articles & URLs</li>
                <li>YouTube videos</li>
                <li>Audio files</li>
                <li>Manual text input</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🔧 SEO Optimization</h4>
            <ul>
                <li>Keyword density control</li>
                <li>Header structure (H1-H6)</li>
                <li>Meta descriptions</li>
                <li>SEO scoring</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🚀 Advanced Features</h4>
            <ul>
                <li>Bulk content generation</li>
                <li>Custom tone & style</li>
                <li>Interactive editing</li>
                <li>Multiple content types</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick stats or demo
    st.markdown("## 📊 Quick Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Content Types", "5+", "Blog, Review, Landing")
    with col2:
        st.metric("Input Sources", "4", "Text, Video, Audio, URL")
    with col3:
        st.metric("SEO Parameters", "10+", "Keywords, Headers, Meta")
    with col4:
        st.metric("Customization", "High", "Tone, Style, Length")

def render_login_page():
    """Render login interface"""
    st.markdown("## 🔐 Login to Access Premium Features")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.markdown("### Login Credentials")
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                login_submitted = st.form_submit_button("🚀 Login", use_container_width=True)
            
            with col_register:
                register_submitted = st.form_submit_button("📝 Register", use_container_width=True)
            
            if login_submitted:
                # Simple authentication (in production, use proper auth)
                if username and password:
                    if authenticate_user(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")
                else:
                    st.warning("Please enter both username and password.")
            
            if register_submitted:
                if username and password:
                    if register_user(username, password):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Registration failed. Username might already exist.")
                else:
                    st.warning("Please enter both username and password.")

def authenticate_user(username, password):
    """Simple authentication function (replace with proper auth in production)"""
    # For demo purposes - in production, use proper authentication
    demo_users = {
        "demo": "password123",
        "admin": "admin123",
        "user": "user123"
    }
    return demo_users.get(username) == password

def register_user(username, password):
    """Simple registration function (replace with proper auth in production)"""
    # For demo purposes - in production, use proper user management
    return len(username) >= 3 and len(password) >= 6

def render_content_generator():
    """Render content generator page"""
    st.markdown("## 📝 Content Generator")
    st.markdown("Generate SEO-optimized blog content from various sources.")
    
    # Input source selection
    st.markdown("### 📥 Select Input Source")
    
    input_type = st.selectbox(
        "Choose your content source:",
        ["Text Input", "Article URL", "YouTube Video", "Audio File"],
        key="input_type_selector"
    )
    
    # Input interface based on selection
    if input_type == "Text Input":
        content = st.text_area(
            "Enter your content:",
            height=200,
            placeholder="Paste your article, notes, or any text content here..."
        )
    
    elif input_type == "Article URL":
        url = st.text_input(
            "Article URL:",
            placeholder="https://example.com/article"
        )
        if url and st.button("📖 Extract Content"):
            st.info("URL content extraction will be implemented in the next phase.")
    
    elif input_type == "YouTube Video":
        youtube_url = st.text_input(
            "YouTube URL:",
            placeholder="https://youtube.com/watch?v=..."
        )
        if youtube_url and st.button("🎥 Extract Transcript"):
            st.info("YouTube transcript extraction will be implemented in the next phase.")
    
    elif input_type == "Audio File":
        audio_file = st.file_uploader(
            "Upload audio file:",
            type=['mp3', 'wav', 'ogg', 'm4a']
        )
        if audio_file and st.button("🎧 Transcribe Audio"):
            st.info("Audio transcription will be implemented in the next phase.")
    
    # Generation button
    if st.button("🚀 Generate Content", type="primary"):
        if input_type == "Text Input" and content:
            st.info("Content generation will be implemented in the next phase.")
            st.markdown("**Preview of what will be generated:**")
            st.markdown("- SEO-optimized article based on your settings")
            st.markdown("- Proper header structure (H1-H6)")
            st.markdown("- Keyword optimization")
            st.markdown("- Meta description")
        else:
            st.warning("Please provide content input before generating.")

def main():
    """Main application function"""
    initialize_session_state()
    render_sidebar()
    
    # Route to appropriate page
    if not st.session_state.authenticated:
        if st.session_state.current_page == "home":
            render_home_page()
            
            # Login section at bottom of home page
            st.markdown("---")
            render_login_page()
        else:
            st.session_state.current_page = "home"
            st.rerun()
    
    else:
        # Authenticated user pages
        if st.session_state.current_page == "home":
            render_home_page()
        elif st.session_state.current_page == "generator":
            render_content_generator()
        elif st.session_state.current_page == "seo_settings":
            st.markdown("## ⚙️ SEO Settings")
            st.info("SEO configuration interface will be implemented in the next phase.")
        elif st.session_state.current_page == "bulk":
            st.markdown("## 📊 Bulk Generation")
            st.info("Bulk content generation will be implemented in the next phase.")
        elif st.session_state.current_page == "analytics":
            st.markdown("## 📈 Analytics")
            st.info("Analytics dashboard will be implemented in the next phase.")
        elif st.session_state.current_page == "profile":
            st.markdown("## 👤 Profile")
            st.info("User profile management will be implemented in the next phase.")

if __name__ == "__main__":
    main()
