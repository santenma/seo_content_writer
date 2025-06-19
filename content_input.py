import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import re
from typing import Dict, Optional, Tuple, List
import time
from datetime import datetime

class ContentExtractor:
    """Enhanced content extraction from various sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def extract_from_url(self, url: str) -> Tuple[bool, Dict]:
        """Extract content from article URL"""
        try:
            # Validate URL
            if not self.is_valid_url(url):
                return False, {"error": "Invalid URL format"}
            
            # Add progress indicator
            progress_placeholder = st.empty()
            progress_placeholder.info("🔍 Extracting content from URL...")
            
            # Fetch content
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content
            extracted_data = self.parse_article_content(soup, url)
            
            progress_placeholder.success("✅ Content extracted successfully!")
            time.sleep(1)
            progress_placeholder.empty()
            
            return True, extracted_data
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error fetching URL: {str(e)}"
            return False, {"error": error_msg}
        except Exception as e:
            error_msg = f"Error parsing content: {str(e)}"
            return False, {"error": error_msg}
    
    def parse_article_content(self, soup: BeautifulSoup, url: str) -> Dict:
        """Parse and extract article content from HTML"""
        
        # Extract title
        title = self.extract_title(soup)
        
        # Extract main content
        content = self.extract_main_content(soup)
        
        # Extract metadata
        meta_description = self.extract_meta_description(soup)
        meta_keywords = self.extract_meta_keywords(soup)
        
        # Extract images
        images = self.extract_images(soup, url)
        
        # Calculate reading time
        reading_time = self.calculate_reading_time(content)
        
        # Extract headings structure
        headings = self.extract_headings(soup)
        
        return {
            "title": title,
            "content": content,
            "meta_description": meta_description,
            "meta_keywords": meta_keywords,
            "images": images,
            "reading_time": reading_time,
            "headings": headings,
            "url": url,
            "extracted_at": datetime.now().isoformat(),
            "word_count": len(content.split()) if content else 0
        }
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title"""
        # Try multiple selectors for title
        title_selectors = [
            'h1',
            'title',
            '[property="og:title"]',
            '[name="twitter:title"]',
            '.article-title',
            '.post-title',
            '.entry-title'
        ]
        
        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get('content') if element.get('content') else element.get_text()
                if title and len(title.strip()) > 0:
                    return title.strip()
        
        return "Untitled Article"
    
    def extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract main article content"""
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside", "ad"]):
            element.decompose()
        
        # Try multiple selectors for main content
        content_selectors = [
            'article',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.content',
            '.main-content',
            '#content',
            '.article-body',
            '.story-body'
        ]
        
        content_text = ""
        
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                for element in elements:
                    text = element.get_text(separator=' ', strip=True)
                    if len(text) > len(content_text):
                        content_text = text
        
        # If no specific content found, try paragraphs
        if not content_text:
            paragraphs = soup.find_all('p')
            content_text = ' '.join([p.get_text(strip=True) for p in paragraphs])
        
        # Clean up text
        content_text = re.sub(r'\s+', ' ', content_text).strip()
        
        return content_text
    
    def extract_meta_description(self, soup: BeautifulSoup) -> str:
        """Extract meta description"""
        meta_selectors = [
            '[name="description"]',
            '[property="og:description"]',
            '[name="twitter:description"]'
        ]
        
        for selector in meta_selectors:
            element = soup.select_one(selector)
            if element and element.get('content'):
                return element.get('content').strip()
        
        return ""
    
    def extract_meta_keywords(self, soup: BeautifulSoup) -> List[str]:
        """Extract meta keywords"""
        keywords_element = soup.select_one('[name="keywords"]')
        if keywords_element and keywords_element.get('content'):
            keywords = keywords_element.get('content').split(',')
            return [kw.strip() for kw in keywords if kw.strip()]
        return []
    
    def extract_images(self, soup: BeautifulSoup, base_url: str) -> List[Dict]:
        """Extract images from article"""
        images = []
        img_elements = soup.find_all('img')
        
        for img in img_elements[:5]:  # Limit to first 5 images
            src = img.get('src')
            if src:
                # Convert relative URLs to absolute
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = urljoin(base_url, src)
                
                images.append({
                    'src': src,
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                })
        
        return images
    
    def extract_headings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract heading structure"""
        headings = []
        heading_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        
        for heading in heading_tags:
            headings.append({
                'level': int(heading.name[1]),
                'text': heading.get_text(strip=True),
                'tag': heading.name
            })
        
        return headings
    
    def calculate_reading_time(self, content: str) -> int:
        """Calculate estimated reading time in minutes"""
        if not content:
            return 0
        
        words = len(content.split())
        # Average reading speed: 200-250 words per minute
        reading_time = max(1, round(words / 225))
        return reading_time
    
    def is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def extract_from_text(self, text: str) -> Dict:
        """Process manual text input"""
        if not text or not text.strip():
            return {"error": "No text provided"}
        
        # Clean text
        cleaned_text = re.sub(r'\s+', ' ', text.strip())
        
        # Extract potential title (first line if it looks like a title)
        lines = cleaned_text.split('\n')
        potential_title = lines[0].strip() if lines else ""
        
        # Check if first line is likely a title
        title = ""
        content = cleaned_text
        
        if potential_title and len(potential_title) < 100 and not potential_title.endswith('.'):
            title = potential_title
            content = '\n'.join(lines[1:]).strip() if len(lines) > 1 else cleaned_text
        
        return {
            "title": title or "Manual Text Input",
            "content": content,
            "meta_description": "",
            "meta_keywords": [],
            "images": [],
            "reading_time": self.calculate_reading_time(content),
            "headings": [],
            "url": "",
            "extracted_at": datetime.now().isoformat(),
            "word_count": len(content.split())
        }

def render_content_input_interface():
    """Render enhanced content input interface"""
    st.markdown("## 📥 Content Input")
    st.markdown("Choose your content source and let's create SEO-optimized articles!")
    
    # Initialize content extractor
    if 'content_extractor' not in st.session_state:
        st.session_state.content_extractor = ContentExtractor()
    
    # Input source selection with improved UI
    col1, col2 = st.columns([2, 1])
    
    with col1:
        input_type = st.selectbox(
            "📋 Select Content Source:",
            [
                "🖊️ Manual Text Input",
                "🔗 Article URL",
                "🎥 YouTube Video",
                "🎧 Audio File",
                "📄 Document Upload"
            ],
            key="input_type_selector",
            help="Choose how you want to provide content for optimization"
        )
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        if 'current_content' in st.session_state and st.session_state.current_content:
            content_data = st.session_state.current_content
            st.metric("Word Count", content_data.get('word_count', 0))
            st.metric("Reading Time", f"{content_data.get('reading_time', 0)} min")
    
    # Render input interface based on selection
    if input_type == "🖊️ Manual Text Input":
        render_text_input()
    elif input_type == "🔗 Article URL":
        render_url_input()
    elif input_type == "🎥 YouTube Video":
        render_youtube_input()
    elif input_type == "🎧 Audio File":
        render_audio_input()
    elif input_type == "📄 Document Upload":
        render_document_input()
    
    # Display extracted content if available
    if 'current_content' in st.session_state and st.session_state.current_content:
        display_extracted_content()

def render_text_input():
    """Render manual text input interface"""
    st.markdown("### ✍️ Enter Your Content")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text_content = st.text_area(
            "Content Text:",
            height=300,
            placeholder="Paste your article, notes, or any text content here...\n\nTip: Put your title on the first line for better recognition.",
            key="manual_text_input",
            help="Enter the content you want to optimize for SEO"
        )
    
    with col2:
        st.markdown("#### 💡 Tips")
        st.markdown("""
        - **First line** as title works best
        - **Longer content** = better optimization
        - **Include key concepts** you want to rank for
        - **Natural language** preferred
        """)
        
        if text_content:
            word_count = len(text_content.split())
            st.metric("Current Words", word_count)
            
            if word_count < 100:
                st.warning("⚠️ Consider adding more content for better SEO")
            elif word_count > 500:
                st.success("✅ Good content length!")
    
    if st.button("🚀 Process Text Content", type="primary", disabled=not text_content):
        if text_content:
            extractor = st.session_state.content_extractor
            extracted_data = extractor.extract_from_text(text_content)
            st.session_state.current_content = extracted_data
            st.success("✅ Text content processed successfully!")
            st.rerun()

def render_url_input():
    """Render URL input interface"""
    st.markdown("### 🔗 Extract from Article URL")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url_input = st.text_input(
            "Article URL:",
            placeholder="https://example.com/article",
            key="url_input_field",
            help="Enter the URL of the article you want to extract content from"
        )
        
        # URL validation feedback
        if url_input:
            extractor = st.session_state.content_extractor
            if extractor.is_valid_url(url_input):
                st.success("✅ Valid URL format")
            else:
                st.error("❌ Invalid URL format")
    
    with col2:
        st.markdown("#### 🎯 Supported Sites")
        st.markdown("""
        - **News sites**
        - **Blog articles**
        - **Medium posts**
        - **Most websites**
        """)
        
        st.markdown("#### ⚠️ Note")
        st.caption("Some sites may block automated access")
    
    if st.button("📖 Extract Content", type="primary", disabled=not url_input):
        if url_input:
            extractor = st.session_state.content_extractor
            success, result = extractor.extract_from_url(url_input)
            
            if success:
                st.session_state.current_content = result
                st.success(f"✅ Content extracted successfully! Found {result.get('word_count', 0)} words.")
                st.rerun()
            else:
                st.error(f"❌ {result.get('error', 'Failed to extract content')}")

def render_youtube_input():
    """Render YouTube input interface with enhanced functionality"""
    st.markdown("### 🎥 YouTube Video Content")
    
    # Import YouTube extractor functionality
    from youtube_extractor import render_complete_youtube_extractor
    
    # Render the complete YouTube extraction interface
    render_complete_youtube_extractor()
    
    # Integration note
    st.info("💡 YouTube content will be automatically processed and ready for article generation once extracted.")

def render_audio_input():
    """Render audio input interface (placeholder for future implementation)"""
    st.markdown("### 🎧 Audio File Processing")
    
    audio_file = st.file_uploader(
        "Upload Audio File:",
        type=['mp3', 'wav', 'ogg', 'm4a', 'flac'],
        help="Upload audio file for transcription"
    )
    
    if audio_file:
        col1, col2 = st.columns(2)
        
        with col1:
            st.audio(audio_file, format='audio/mp3')
        
        with col2:
            st.markdown("#### ⚙️ Transcription Options")
            language = st.selectbox("Language:", ["English", "Spanish", "French", "German"])
            quality = st.select_slider("Quality:", ["Fast", "Balanced", "High"])
    
    if st.button("🎧 Transcribe Audio", type="primary", disabled=not audio_file):
        st.info("🚧 Audio transcription will be implemented in Phase 3")

def render_document_input():
    """Render document upload interface"""
    st.markdown("### 📄 Document Upload")
    
    uploaded_file = st.file_uploader(
        "Upload Document:",
        type=['txt', 'docx', 'pdf'],
        help="Upload text document to extract content"
    )
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        
        if st.button("📄 Extract Document Content", type="primary"):
            st.info("🚧 Document processing will be implemented in Phase 3")

def display_extracted_content():
    """Display extracted content with preview and editing options"""
    st.markdown("---")
    st.markdown("## 📋 Extracted Content Preview")
    
    content_data = st.session_state.current_content
    
    # Content overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Words", content_data.get('word_count', 0))
    with col2:
        st.metric("⏱️ Read Time", f"{content_data.get('reading_time', 0)} min")
    with col3:
        st.metric("🖼️ Images", len(content_data.get('images', [])))
    with col4:
        st.metric("📑 Headings", len(content_data.get('headings', [])))
    
    # Tabbed content display
    tab1, tab2, tab3 = st.tabs(["📄 Content", "🔧 Edit", "📊 Analysis"])
    
    with tab1:
        # Title
        if content_data.get('title'):
            st.markdown(f"### 📰 {content_data['title']}")
        
        # Content preview
        content_text = content_data.get('content', '')
        if content_text:
            # Show first 500 characters
            preview_text = content_text[:500] + "..." if len(content_text) > 500 else content_text
            st.markdown("#### Content Preview:")
            st.text_area("", value=preview_text, height=200, disabled=True)
            
            if len(content_text) > 500:
                if st.button("📖 Show Full Content"):
                    st.markdown("#### Full Content:")
                    st.text_area("", value=content_text, height=400, disabled=True)
    
    with tab2:
        st.markdown("#### ✏️ Edit Content")
        
        # Editable title
        edited_title = st.text_input(
            "Title:",
            value=content_data.get('title', ''),
            key="edit_title"
        )
        
        # Editable content
        edited_content = st.text_area(
            "Content:",
            value=content_data.get('content', ''),
            height=300,
            key="edit_content"
        )
        
        if st.button("💾 Save Changes"):
            st.session_state.current_content['title'] = edited_title
            st.session_state.current_content['content'] = edited_content
            st.session_state.current_content['word_count'] = len(edited_content.split())
            st.session_state.current_content['reading_time'] = st.session_state.content_extractor.calculate_reading_time(edited_content)
            st.success("✅ Changes saved!")
            st.rerun()
    
    with tab3:
        st.markdown("#### 📊 Content Analysis")
        
        if content_data.get('headings'):
            st.markdown("**Heading Structure:**")
            for heading in content_data['headings']:
                level_indicator = "  " * (heading['level'] - 1) + "•"
                st.markdown(f"{level_indicator} **{heading['tag'].upper()}:** {heading['text']}")
        
        if content_data.get('meta_keywords'):
            st.markdown("**Detected Keywords:**")
            st.write(", ".join(content_data['meta_keywords']))
        
        if content_data.get('images'):
            st.markdown("**Images Found:**")
            for img in content_data['images'][:3]:
                st.markdown(f"• {img.get('alt', 'No alt text')} - [View]({img['src']})")
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Clear Content", type="secondary"):
            if 'current_content' in st.session_state:
                del st.session_state.current_content
            st.rerun()
    
    with col2:
        if st.button("⚙️ Configure SEO", type="secondary"):
            st.session_state.current_page = "seo_settings"
            st.rerun()
    
    with col3:
        if st.button("🚀 Generate Article", type="primary"):
            st.session_state.current_page = "generator"
            st.info("🚧 Content generation will be implemented in the next phase")
