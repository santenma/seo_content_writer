"""
SEO Blog Content Generator - Main Application
A comprehensive tool for generating SEO-optimized blog content from multiple input sources.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.append(str(src_dir))

# Import configuration
from config.settings import (
    app_settings, 
    render_seo_config_sidebar,
    render_content_config_sidebar,
    render_api_config_sidebar,
    InputType,
    ContentType,
    ToneType
)

# Page configuration
st.set_page_config(
    page_title="SEO Blog Content Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .input-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .output-section {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 1rem 0;
    }
    
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    
    .status-processing {
        color: #ffc107;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 SEO Blog Content Generator</h1>
        <p>Transform any content into SEO-optimized blog articles</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar configuration
    render_sidebar()
    
    # Main content area
    render_main_interface()

def render_sidebar():
    """Render sidebar with configuration options"""
    st.sidebar.title("⚙️ Configuration")
    
    # API Configuration
    render_api_config_sidebar()
    
    st.sidebar.divider()
    
    # SEO Configuration  
    render_seo_config_sidebar()
    
    st.sidebar.divider()
    
    # Content Configuration
    render_content_config_sidebar()
    
    st.sidebar.divider()
    
    # Help section
    render_help_section()

def render_help_section():
    """Render help section in sidebar"""
    st.sidebar.header("❓ Help")
    
    with st.sidebar.expander("How to use"):
        st.write("""
        1. **Configure APIs**: Add your OpenAI or Anthropic API keys
        2. **Set SEO parameters**: Define keywords and target length
        3. **Choose content type**: Select blog post, review, etc.
        4. **Input content**: Paste URL, upload audio, or enter text
        5. **Generate**: Click generate to create optimized content
        6. **Edit & refine**: Use the editor to make adjustments
        7. **Download**: Export your final content
        """)
    
    with st.sidebar.expander("Supported formats"):
        st.write("""
        **Input sources:**
        - 📄 Article URLs (any website)
        - 🎥 YouTube videos (with transcription)
        - 🎵 Audio files (.mp3, .wav, .m4a)
        - 📝 Direct text input
        
        **Content types:**
        - Blog posts
        - Product reviews  
        - Landing pages
        - Tutorials
        - News articles
        """)

def render_main_interface():
    """Render main application interface"""
    
    # Check API configuration
    is_valid, message = app_settings.validate_api_setup()
    if not is_valid:
        st.error(f"⚠️ {message}")
        st.info("Please add your API keys in the sidebar to continue.")
        return
    
    # Input section
    render_input_section()
    
    # Process and generate section
    if st.session_state.get('content_processed', False):
        render_generation_section()
    
    # Output and editing section
    if st.session_state.get('content_generated', False):
        render_output_section()

def render_input_section():
    """Render content input section"""
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.header("📥 Content Input")
    
    # Input type selection
    input_type = st.selectbox(
        "Choose input type:",
        options=[
            InputType.ARTICLE_URL.value,
            InputType.YOUTUBE_URL.value, 
            InputType.AUDIO_FILE.value,
            InputType.TEXT_INPUT.value
        ],
        format_func=lambda x: {
            'article_url': '📄 Article URL',
            'youtube_url': '🎥 YouTube Video',
            'audio_file': '🎵 Audio File',
            'text_input': '📝 Direct Text'
        }[x]
    )
    
    # Input interface based on type
    content_data = None
    
    if input_type == InputType.ARTICLE_URL.value:
        content_data = render_url_input()
    elif input_type == InputType.YOUTUBE_URL.value:
        content_data = render_youtube_input()
    elif input_type == InputType.AUDIO_FILE.value:
        content_data = render_audio_input()
    elif input_type == InputType.TEXT_INPUT.value:
        content_data = render_text_input()
    
    # Process input button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Process Content", type="primary", use_container_width=True):
            if content_data:
                process_input_content(input_type, content_data)
            else:
                st.error("Please provide content to process")
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_url_input():
    """Render URL input interface"""
    url = st.text_input(
        "Enter article URL:",
        placeholder="https://example.com/article",
        help="Enter the URL of the article you want to process"
    )
    
    if url:
        import validators
        if not validators.url(url):
            st.error("Please enter a valid URL")
            return None
        st.success(f"✅ Valid URL: {url}")
        return {'url': url}
    return None

def render_youtube_input():
    """Render YouTube input interface"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        youtube_url = st.text_input(
            "Enter YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=...",
            help="Enter YouTube video URL for transcription"
        )
    
    with col2:
        transcription_option = st.selectbox(
            "Transcription:",
            ["Auto", "Manual"],
            help="Choose automatic transcription or provide your own"
        )
    
    if transcription_option == "Manual":
        manual_transcript = st.text_area(
            "Paste transcript:",
            height=200,
            help="Paste the video transcript manually"
        )
        if manual_transcript:
            return {'transcript': manual_transcript, 'source': 'manual'}
    
    if youtube_url:
        if "youtube.com" in youtube_url or "youtu.be" in youtube_url:
            st.success(f"✅ Valid YouTube URL: {youtube_url}")
            return {'url': youtube_url, 'transcription': transcription_option.lower()}
        else:
            st.error("Please enter a valid YouTube URL")
    
    return None

def render_audio_input():
    """Render audio file input interface"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        audio_file = st.file_uploader(
            "Upload audio file:",
            type=['mp3', 'wav', 'm4a'],
            help=f"Upload audio file (max {app_settings.max_audio_size_mb}MB)"
        )
    
    with col2:
        transcription_service = st.selectbox(
            "Transcription service:",
            ["Whisper (OpenAI)", "Manual"],
            help="Choose transcription method"
        )
    
    if transcription_service == "Manual":
        manual_transcript = st.text_area(
            "Paste transcript:",
            height=200,
            help="Paste the audio transcript manually"
        )
        if manual_transcript:
            return {'transcript': manual_transcript, 'source': 'manual'}
    
    if audio_file:
        # Check file size
        file_size_mb = len(audio_file.getvalue()) / (1024 * 1024)
        if file_size_mb > app_settings.max_audio_size_mb:
            st.error(f"File too large. Maximum size: {app_settings.max_audio_size_mb}MB")
            return None
        
        st.success(f"✅ Audio file uploaded: {audio_file.name} ({file_size_mb:.1f}MB)")
        return {
            'file': audio_file,
            'transcription_service': transcription_service.lower()
        }
    
    return None

def render_text_input():
    """Render direct text input interface"""
    text_content = st.text_area(
        "Enter your content:",
        height=300,
        max_chars=app_settings.max_text_length,
        help=f"Paste your content directly (max {app_settings.max_text_length:,} characters)"
    )
    
    if text_content:
        word_count = len(text_content.split())
        char_count = len(text_content)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Words", word_count)
        with col2:
            st.metric("Characters", char_count)
        
        if word_count < 50:
            st.warning("Content might be too short for effective SEO optimization")
        
        return {'text': text_content}
    
    return None

def process_input_content(input_type, content_data):
    """Process the input content"""
    with st.spinner("Processing content..."):
        try:
            # This is a placeholder - actual processing will be implemented in separate modules
            st.session_state['input_type'] = input_type
            st.session_state['content_data'] = content_data
            st.session_state['processed_content'] = f"Processed content from {input_type}"
            st.session_state['content_processed'] = True
            st.success("✅ Content processed successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error processing content: {str(e)}")

def render_generation_section():
    """Render content generation section"""
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.header("🎯 Content Generation")
    
    # Show processing status
    st.info(f"📋 Ready to generate {app_settings.content_config.content_type.value.replace('_', ' ').title()}")
    
    # Generation options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subfield("Current Configuration:")
        st.write(f"**Content Type:** {app_settings.content_config.content_type.value.replace('_', ' ').title()}")
        st.write(f"**Tone:** {app_settings.content_config.tone.value.title()}")
        st.write(f"**Target Length:** {app_settings.content_config.target_length} words")
        st.write(f"**Primary Keyword:** {app_settings.seo_config.primary_keyword or 'Not set'}")
    
    with col2:
        st.subfield("SEO Settings:")
        st.write(f"**Keyword Density:** {app_settings.seo_config.keyword_density}%")
        st.write(f"**Secondary Keywords:** {len(app_settings.seo_config.secondary_keywords)} keywords")
        st.write(f"**Include Meta Tags:** {app_settings.seo_config.include_meta_description}")
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate SEO Content", type="primary", use_container_width=True):
            generate_seo_content()
    
    st.markdown('</div>', unsafe_allow_html=True)

def generate_seo_content():
    """Generate SEO-optimized content"""
    with st.spinner("Generating SEO-optimized content..."):
        try:
            # Placeholder for actual content generation
            st.session_state['generated_content'] = {
                'title': 'Generated SEO Title',
                'meta_description': 'Generated meta description...',
                'content': 'Generated SEO-optimized content...',
                'headers': ['H1: Main Title', 'H2: Section 1', 'H2: Section 2'],
                'seo_score': 85
            }
            st.session_state['content_generated'] = True
            st.success("✅ SEO content generated successfully!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error generating content: {str(e)}")

def render_output_section():
    """Render output and editing section"""
    st.markdown('<div class="output-section">', unsafe_allow_html=True)
    st.header("📝 Generated Content")
    
    if 'generated_content' in st.session_state:
        content = st.session_state['generated_content']
        
        # Content tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📄 Content", "🏷️ SEO Elements", "📊 Analysis", "⚙️ Actions"])
        
        with tab1:
            render_content_editor(content)
        
        with tab2:
            render_seo_elements(content)
        
        with tab3:
            render_content_analysis(content)
        
        with tab4:
            render_action_buttons(content)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_content_editor(content):
    """Render content editing interface"""
    st.subheader("Edit Content")
    
    # Title editor
    edited_title = st.text_input("Title:", value=content.get('title', ''))
    
    # Content editor
    edited_content = st.text_area(
        "Content:",
        value=content.get('content', ''),
        height=400
    )
    
    # Update buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Regenerate Title"):
            st.info("Regenerating title...")
    
    with col2:
        if st.button("🔄 Regenerate Section"):
            st.info("Select section to regenerate...")
    
    with col3:
        if st.button("💾 Save Changes"):
            # Update session state
            st.session_state['generated_content']['title'] = edited_title
            st.session_state['generated_content']['content'] = edited_content
            st.success("Changes saved!")

def render_seo_elements(content):
    """Render SEO elements"""
    st.subheader("SEO Elements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Meta Title:", value=content.get('title', ''))
        st.text_area("Meta Description:", value=content.get('meta_description', ''))
    
    with col2:
        st.write("**Header Structure:**")
        for header in content.get('headers', []):
            st.write(f"- {header}")
        
        st.metric("SEO Score", f"{content.get('seo_score', 0)}%")

def render_content_analysis(content):
    """Render content analysis"""
    st.subheader("Content Analysis")
    
    # Placeholder analysis
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Word Count", "1,250")
        st.metric("Reading Time", "5 min")
    
    with col2:
        st.metric("Keyword Density", "2.1%")
        st.metric("Readability Score", "72")
    
    with col3:
        st.metric("SEO Score", f"{content.get('seo_score', 0)}%")
        st.metric("Headers", len(content.get('headers', [])))

def render_action_buttons(content):
    """Render action buttons"""
    st.subheader("Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Download as Markdown", use_container_width=True):
            # Create markdown content
            markdown_content = f"# {content.get('title', '')}\n\n{content.get('content', '')}"
            st.download_button(
                "Download Markdown",
                markdown_content,
                file_name="generated_content.md",
                mime="text/markdown"
            )
    
    with col2:
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            st.info("Copy functionality will be implemented with JavaScript")
    
    with col3:
        if st.button("🔄 Start New Project", use_container_width=True):
            # Clear session state
            for key in list(st.session_state.keys()):
                if key.startswith(('content_', 'generated_', 'input_', 'processed_')):
                    del st.session_state[key]
            st.rerun()

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'content_processed' not in st.session_state:
        st.session_state['content_processed'] = False
    if 'content_generated' not in st.session_state:
        st.session_state['content_generated'] = False

if __name__ == "__main__":
    init_session_state()
    main()
