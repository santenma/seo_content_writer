import streamlit as st
import os
from datetime import datetime
import json
from auth import (
    initialize_auth_session, 
    render_enhanced_login, 
    render_user_profile, 
    logout_user
)
from content_input import render_content_input_interface
from content_generator import render_content_generation_interface
from seo_settings import render_complete_seo_settings
from style_customization import render_complete_style_customization
from output_editor import render_complete_output_editor
from download_manager import render_complete_download_manager
from youtube_extractor import render_complete_youtube_extractor

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
    # Initialize authentication first
    initialize_auth_session()
    
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
                "📥 Content Input": "content_input", 
                "🚀 Generate Article": "generate",
                "✏️ Edit Content": "editor",
                "📥 Download & Export": "download",
                "⚙️ SEO Settings": "seo_settings",
                "🎨 Style & Voice": "style_settings",
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
                logout_user()
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
    """Render enhanced login interface"""
    render_enhanced_login()



def render_content_generator():
    """Render enhanced content input interface"""
    render_content_input_interface()

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
        elif st.session_state.current_page == "content_input":
            render_content_generator()
        elif st.session_state.current_page == "generate":
            render_content_generation_interface()
        elif st.session_state.current_page == "editor":
            render_complete_output_editor()
        elif st.session_state.current_page == "download":
            render_complete_download_manager()
        elif st.session_state.current_page == "generator":
            render_content_generator()  # Legacy compatibility
        elif st.session_state.current_page == "seo_settings":
            render_complete_seo_settings()
        elif st.session_state.current_page == "style_settings":
            render_complete_style_customization()
        elif st.session_state.current_page == "bulk":
            st.markdown("## 📊 Bulk Generation") 
            st.info("Bulk content generation will be implemented in Phase 3.")
        elif st.session_state.current_page == "analytics":
            st.markdown("## 📈 Analytics")
            st.info("Analytics dashboard will be implemented in Phase 3.")
        elif st.session_state.current_page == "profile":
            render_user_profile()

if __name__ == "__main__":
    main()
