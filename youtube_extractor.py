import streamlit as st
import re
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import json

class YouTubeExtractor:
    """Advanced YouTube content extraction system"""
    
    def __init__(self):
        self.api_key = None  # Will be set from environment or user input
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese'
        }
    
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)',
            r'youtu\.be\/([^&\n?#]+)',
            r'youtube\.com\/v\/([^&\n?#]+)',
            r'youtube\.com\/embed\/([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def validate_youtube_url(self, url: str) -> Tuple[bool, str]:
        """Validate YouTube URL and provide feedback"""
        if not url:
            return False, "Please enter a YouTube URL"
        
        video_id = self.extract_video_id(url)
        if not video_id:
            return False, "Invalid YouTube URL format"
        
        # Basic format validation
        if len(video_id) != 11:
            return False, "Invalid video ID length"
        
        return True, f"Valid YouTube video ID: {video_id}"
    
    def get_video_info(self, video_id: str, api_key: str = None) -> Dict:
        """Get video metadata using YouTube Data API"""
        if not api_key:
            # Return mock data for demo purposes
            return self.get_mock_video_info(video_id)
        
        try:
            url = f"{self.base_url}/videos"
            params = {
                'part': 'snippet,statistics,contentDetails',
                'id': video_id,
                'key': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get('items'):
                return {"error": "Video not found or is private"}
            
            video_data = data['items'][0]
            
            return self.parse_video_data(video_data)
            
        except requests.exceptions.RequestException as e:
            return {"error": f"API request failed: {str(e)}"}
        except Exception as e:
            return {"error": f"Error processing video data: {str(e)}"}
    
    def parse_video_data(self, video_data: Dict) -> Dict:
        """Parse video data from YouTube API response"""
        snippet = video_data.get('snippet', {})
        statistics = video_data.get('statistics', {})
        content_details = video_data.get('content_details', {})
        
        # Parse duration
        duration_str = content_details.get('duration', 'PT0S')
        duration_seconds = self.parse_duration(duration_str)
        
        # Parse published date
        published_at = snippet.get('publishedAt', '')
        published_date = None
        if published_at:
            try:
                published_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            except:
                pass
        
        return {
            'title': snippet.get('title', ''),
            'description': snippet.get('description', ''),
            'channel_title': snippet.get('channelTitle', ''),
            'published_at': published_date.isoformat() if published_date else '',
            'duration_seconds': duration_seconds,
            'duration_formatted': self.format_duration(duration_seconds),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
            'tags': snippet.get('tags', []),
            'category_id': snippet.get('categoryId', ''),
            'language': snippet.get('defaultLanguage', 'en'),
            'thumbnail_url': self.get_best_thumbnail(snippet.get('thumbnails', {}))
        }
    
    def get_mock_video_info(self, video_id: str) -> Dict:
        """Return mock video info for demo purposes"""
        return {
            'title': 'Sample YouTube Video Title',
            'description': 'This is a sample video description that would normally be extracted from YouTube. In a production environment, this would contain the actual video description.',
            'channel_title': 'Sample Channel',
            'published_at': (datetime.now() - timedelta(days=30)).isoformat(),
            'duration_seconds': 600,
            'duration_formatted': '10:00',
            'view_count': 15000,
            'like_count': 500,
            'comment_count': 50,
            'tags': ['tutorial', 'education', 'technology'],
            'category_id': '27',
            'language': 'en',
            'thumbnail_url': 'https://via.placeholder.com/480x360?text=Video+Thumbnail'
        }
    
    def get_transcript_methods(self) -> List[Dict]:
        """Get available transcript extraction methods"""
        return [
            {
                'id': 'youtube_transcript_api',
                'name': 'YouTube Transcript API',
                'description': 'Extract official captions using youtube-transcript-api library',
                'pros': ['Most accurate', 'Preserves timing', 'Multiple languages'],
                'cons': ['Requires captions to exist', 'May not work for all videos'],
                'available': True
            },
            {
                'id': 'manual_upload',
                'name': 'Manual Transcript Upload',
                'description': 'Upload your own transcript file',
                'pros': ['100% accurate', 'Custom formatting', 'Works for any video'],
                'cons': ['Manual work required', 'Time consuming'],
                'available': True
            },
            {
                'id': 'audio_extraction',
                'name': 'Audio Extraction + Whisper',
                'description': 'Extract audio and use AI transcription',
                'pros': ['Works for videos without captions', 'High accuracy'],
                'cons': ['Requires additional processing', 'May violate terms of service'],
                'available': False  # Would require additional setup
            }
        ]
    
    def extract_transcript_api(self, video_id: str, language: str = 'en') -> Dict:
        """Extract transcript using youtube-transcript-api (mock implementation)"""
        # In production, this would use: from youtube_transcript_api import YouTubeTranscriptApi
        
        try:
            # Mock transcript data for demo
            mock_transcript = [
                {'text': 'Welcome to this comprehensive tutorial', 'start': 0.0, 'duration': 3.5},
                {'text': 'Today we will be covering advanced techniques', 'start': 3.5, 'duration': 4.2},
                {'text': 'that will help you improve your skills', 'start': 7.7, 'duration': 3.8},
                {'text': 'First, let\'s start with the basics', 'start': 11.5, 'duration': 3.2},
                {'text': 'Understanding the fundamental concepts is crucial', 'start': 14.7, 'duration': 4.5},
                {'text': 'for building a strong foundation', 'start': 19.2, 'duration': 3.1},
                {'text': 'Now let\'s move on to more advanced topics', 'start': 22.3, 'duration': 4.0},
                {'text': 'These techniques will take your work to the next level', 'start': 26.3, 'duration': 4.8},
                {'text': 'Remember to practice what you learn', 'start': 31.1, 'duration': 3.5},
                {'text': 'Thank you for watching and see you next time', 'start': 34.6, 'duration': 4.2}
            ]
            
            # Convert to full text
            full_text = ' '.join([entry['text'] for entry in mock_transcript])
            
            return {
                'success': True,
                'transcript': mock_transcript,
                'full_text': full_text,
                'language': language,
                'word_count': len(full_text.split()),
                'duration_seconds': mock_transcript[-1]['start'] + mock_transcript[-1]['duration']
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f"Failed to extract transcript: {str(e)}",
                'suggestion': 'Try manual transcript upload or check if video has captions'
            }
    
    def process_manual_transcript(self, transcript_text: str, video_info: Dict) -> Dict:
        """Process manually uploaded transcript"""
        if not transcript_text.strip():
            return {'success': False, 'error': 'Empty transcript provided'}
        
        # Clean up the transcript
        cleaned_text = self.clean_transcript_text(transcript_text)
        
        # Create mock timing data
        words = cleaned_text.split()
        estimated_duration = video_info.get('duration_seconds', len(words) * 0.5)
        
        # Create timed segments (simplified)
        segments = self.create_timed_segments(cleaned_text, estimated_duration)
        
        return {
            'success': True,
            'transcript': segments,
            'full_text': cleaned_text,
            'language': 'manual',
            'word_count': len(words),
            'duration_seconds': estimated_duration,
            'source': 'manual_upload'
        }
    
    def clean_transcript_text(self, text: str) -> str:
        """Clean and format transcript text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove speaker labels if present
        text = re.sub(r'^[A-Z][a-z]*:\s*', '', text, flags=re.MULTILINE)
        
        # Remove time stamps if present
        text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
        text = re.sub(r'\d{2}:\d{2}:\d{2}', '', text)
        
        # Fix punctuation
        text = re.sub(r'\s+([,.!?])', r'\1', text)
        
        # Ensure sentences end with punctuation
        sentences = text.split('.')
        formatted_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and not sentence[-1] in '!?':
                sentence += '.'
            if sentence:
                formatted_sentences.append(sentence)
        
        return ' '.join(formatted_sentences)
    
    def create_timed_segments(self, text: str, total_duration: float) -> List[Dict]:
        """Create timed segments from text"""
        sentences = [s.strip() + '.' for s in text.split('.') if s.strip()]
        
        segments = []
        current_time = 0.0
        avg_duration = total_duration / max(len(sentences), 1)
        
        for sentence in sentences:
            word_count = len(sentence.split())
            duration = max(2.0, word_count * 0.5)  # Estimate speaking time
            
            segments.append({
                'text': sentence,
                'start': current_time,
                'duration': duration
            })
            
            current_time += duration
        
        return segments
    
    def create_content_structure(self, transcript_data: Dict, video_info: Dict) -> Dict:
        """Create structured content from transcript and video info"""
        full_text = transcript_data.get('full_text', '')
        video_title = video_info.get('title', 'YouTube Video')
        video_description = video_info.get('description', '')
        
        # Extract key topics from transcript
        topics = self.extract_key_topics(full_text)
        
        # Create structured content
        structured_content = {
            'title': video_title,
            'description': video_description,
            'transcript': full_text,
            'key_topics': topics,
            'video_metadata': video_info,
            'transcript_metadata': transcript_data,
            'content_analysis': self.analyze_content(full_text),
            'suggested_headings': self.suggest_headings(full_text, topics),
            'estimated_reading_time': max(1, round(transcript_data.get('word_count', 0) / 225))
        }
        
        return structured_content
    
    def extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from transcript text"""
        # Simple keyword extraction (in production, use more advanced NLP)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Count word frequency
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get most frequent meaningful words
        common_words = {'this', 'that', 'with', 'have', 'will', 'from', 'they', 'been', 'have', 'their', 'said', 'each', 'which', 'them', 'been', 'like', 'into', 'time', 'very', 'when', 'much', 'more', 'some', 'what', 'know', 'just', 'first', 'also', 'after', 'back', 'other', 'many', 'than', 'then', 'them', 'well', 'were'}
        
        filtered_words = {word: freq for word, freq in word_freq.items() 
                         if freq > 2 and word not in common_words and len(word) > 4}
        
        # Sort by frequency and return top topics
        topics = sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)
        return [topic[0].title() for topic in topics[:10]]
    
    def analyze_content(self, text: str) -> Dict:
        """Analyze transcript content for insights"""
        words = text.split()
        sentences = [s for s in text.split('.') if s.strip()]
        
        return {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_sentence_length': len(words) / max(len(sentences), 1),
            'estimated_speech_rate': len(words) / 10,  # Assume 10 minutes for demo
            'complexity_indicators': {
                'long_sentences': len([s for s in sentences if len(s.split()) > 20]),
                'technical_terms': len([w for w in words if len(w) > 8]),
                'questions': text.count('?'),
                'emphasis': text.count('!')
            }
        }
    
    def suggest_headings(self, text: str, topics: List[str]) -> List[str]:
        """Suggest section headings based on content"""
        headings = []
        
        # Add introduction
        headings.append("Introduction")
        
        # Add topic-based headings
        for topic in topics[:5]:
            if topic.lower() in text.lower():
                headings.append(f"Understanding {topic}")
        
        # Add common conclusion patterns
        if any(word in text.lower() for word in ['conclusion', 'summary', 'finally', 'thank you']):
            headings.append("Key Takeaways")
        
        return headings
    
    def parse_duration(self, duration_str: str) -> int:
        """Parse ISO 8601 duration string to seconds"""
        # Parse PT1H2M10S format
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0) 
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    def format_duration(self, seconds: int) -> str:
        """Format duration in seconds to readable format"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
    
    def get_best_thumbnail(self, thumbnails: Dict) -> str:
        """Get the best quality thumbnail URL"""
        quality_order = ['maxres', 'high', 'medium', 'default']
        
        for quality in quality_order:
            if quality in thumbnails:
                return thumbnails[quality]['url']
        
        return 'https://via.placeholder.com/480x360?text=No+Thumbnail'

def render_youtube_extraction_interface():
    """Render YouTube content extraction interface"""
    st.markdown("### 🎥 YouTube Content Extraction")
    st.markdown("Extract transcripts and metadata from YouTube videos for content generation.")
    
    # Initialize YouTube extractor
    if 'youtube_extractor' not in st.session_state:
        st.session_state.youtube_extractor = YouTubeExtractor()
    
    extractor = st.session_state.youtube_extractor
    
    # YouTube URL input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        youtube_url = st.text_input(
            "🔗 YouTube Video URL:",
            placeholder="https://youtube.com/watch?v=...",
            key="youtube_url_input",
            help="Enter the URL of the YouTube video you want to extract content from"
        )
    
    with col2:
        st.markdown("#### 🔍 URL Validation")
        if youtube_url:
            is_valid, message = extractor.validate_youtube_url(youtube_url)
            if is_valid:
                st.success("✅ Valid URL")
            else:
                st.error(f"❌ {message}")
        else:
            st.info("ℹ️ Enter URL above")
    
    if youtube_url and extractor.validate_youtube_url(youtube_url)[0]:
        video_id = extractor.extract_video_id(youtube_url)
        
        # Video information section
        render_video_info_section(extractor, video_id)
        
        # Transcript extraction section
        render_transcript_extraction_section(extractor, video_id)

def render_video_info_section(extractor: YouTubeExtractor, video_id: str):
    """Render video information section"""
    st.markdown("#### 📺 Video Information")
    
    # API key configuration
    with st.expander("⚙️ API Configuration (Optional)"):
        st.markdown("**YouTube Data API Key (for enhanced features):**")
        api_key = st.text_input(
            "API Key:",
            type="password",
            key="youtube_api_key",
            help="Get your API key from Google Cloud Console. Leave empty to use demo mode."
        )
        
        if api_key:
            st.success("✅ API key configured")
        else:
            st.info("ℹ️ Running in demo mode with mock data")
    
    # Get video information
    if st.button("📋 Get Video Info", type="secondary"):
        with st.spinner("Fetching video information..."):
            video_info = extractor.get_video_info(video_id, api_key)
        
        if 'error' in video_info:
            st.error(f"❌ {video_info['error']}")
        else:
            st.session_state.current_video_info = video_info
            st.success("✅ Video information retrieved successfully!")
    
    # Display video information if available
    if 'current_video_info' in st.session_state:
        display_video_info(st.session_state.current_video_info)

def display_video_info(video_info: Dict):
    """Display extracted video information"""
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📋 Video Details")
        
        # Title and basic info
        st.markdown(f"**Title:** {video_info.get('title', 'N/A')}")
        st.markdown(f"**Channel:** {video_info.get('channel_title', 'N/A')}")
        st.markdown(f"**Duration:** {video_info.get('duration_formatted', 'N/A')}")
        st.markdown(f"**Published:** {video_info.get('published_at', 'N/A')[:10]}")
        
        # Statistics
        if video_info.get('view_count'):
            st.markdown("**Statistics:**")
            st.markdown(f"• Views: {video_info['view_count']:,}")
            st.markdown(f"• Likes: {video_info['like_count']:,}")
            st.markdown(f"• Comments: {video_info['comment_count']:,}")
        
        # Description
        description = video_info.get('description', '')
        if description:
            st.markdown("**Description:**")
            with st.expander("📄 Full Description"):
                st.text_area("", value=description, height=200, disabled=True)
        
        # Tags
        tags = video_info.get('tags', [])
        if tags:
            st.markdown(f"**Tags:** {', '.join(tags[:10])}")
    
    with col2:
        # Thumbnail
        thumbnail_url = video_info.get('thumbnail_url')
        if thumbnail_url:
            st.markdown("#### 🖼️ Thumbnail")
            st.image(thumbnail_url, width=250)
        
        # Quick stats
        st.markdown("#### 📊 Quick Stats")
        st.metric("Duration", video_info.get('duration_formatted', 'N/A'))
        st.metric("Views", f"{video_info.get('view_count', 0):,}")
        st.metric("Language", video_info.get('language', 'Unknown'))

def render_transcript_extraction_section(extractor: YouTubeExtractor, video_id: str):
    """Render transcript extraction section"""
    st.markdown("---")
    st.markdown("#### 📝 Transcript Extraction")
    
    # Method selection
    methods = extractor.get_transcript_methods()
    
    method_col1, method_col2 = st.columns(2)
    
    with method_col1:
        st.markdown("**Available Methods:**")
        
        selected_method = st.radio(
            "Choose extraction method:",
            options=[method['id'] for method in methods if method['available']],
            format_func=lambda x: next(m['name'] for m in methods if m['id'] == x),
            key="transcript_method"
        )
    
    with method_col2:
        # Show method details
        method_info = next(m for m in methods if m['id'] == selected_method)
        
        st.markdown(f"**{method_info['name']}**")
        st.markdown(method_info['description'])
        
        st.markdown("**Pros:**")
        for pro in method_info['pros']:
            st.markdown(f"✅ {pro}")
        
        st.markdown("**Cons:**")
        for con in method_info['cons']:
            st.markdown(f"⚠️ {con}")
    
    # Method-specific interfaces
    if selected_method == 'youtube_transcript_api':
        render_api_transcript_interface(extractor, video_id)
    elif selected_method == 'manual_upload':
        render_manual_transcript_interface(extractor, video_id)

def render_api_transcript_interface(extractor: YouTubeExtractor, video_id: str):
    """Render API-based transcript extraction interface"""
    st.markdown("##### 🤖 Automatic Transcript Extraction")
    
    # Language selection
    col1, col2 = st.columns(2)
    
    with col1:
        selected_language = st.selectbox(
            "Preferred Language:",
            options=list(extractor.supported_languages.keys()),
            format_func=lambda x: f"{extractor.supported_languages[x]} ({x})",
            key="transcript_language"
        )
    
    with col2:
        st.markdown("#### ⚙️ Options")
        auto_detect = st.checkbox("Auto-detect language", value=True, key="auto_detect_lang")
        include_timing = st.checkbox("Include timing information", value=True, key="include_timing")
    
    # Extract transcript
    if st.button("🎯 Extract Transcript", type="primary"):
        with st.spinner("Extracting transcript from YouTube..."):
            transcript_result = extractor.extract_transcript_api(video_id, selected_language)
        
        if transcript_result.get('success'):
            st.session_state.current_transcript = transcript_result
            st.success("✅ Transcript extracted successfully!")
            
            # Display transcript preview
            display_transcript_preview(transcript_result)
            
            # Process content button
            if st.button("🚀 Process for Content Generation", type="primary"):
                process_youtube_content(extractor)
                
        else:
            st.error(f"❌ {transcript_result.get('error', 'Unknown error')}")
            st.info(f"💡 Suggestion: {transcript_result.get('suggestion', 'Try a different method')}")

def render_manual_transcript_interface(extractor: YouTubeExtractor, video_id: str):
    """Render manual transcript upload interface"""
    st.markdown("##### 📤 Manual Transcript Upload")
    
    # File upload option
    transcript_file = st.file_uploader(
        "Upload transcript file:",
        type=['txt', 'srt', 'vtt', 'sbv'],
        key="manual_transcript_file",
        help="Upload a transcript file in TXT, SRT, VTT, or SBV format"
    )
    
    if transcript_file:
        transcript_content = transcript_file.read().decode('utf-8')
        st.success(f"✅ File uploaded: {transcript_file.name}")
        
        # Preview uploaded content
        with st.expander("📄 Preview Uploaded Content"):
            st.text_area("", value=transcript_content[:1000] + "..." if len(transcript_content) > 1000 else transcript_content, height=200, disabled=True)
    else:
        # Text area for manual input
        st.markdown("**Or paste transcript directly:**")
        transcript_content = st.text_area(
            "Transcript text:",
            height=300,
            placeholder="Paste the video transcript here...",
            key="manual_transcript_text"
        )
    
    # Processing options
    if transcript_content:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ⚙️ Processing Options")
            clean_text = st.checkbox("Clean and format text", value=True, key="clean_manual_text")
            remove_timestamps = st.checkbox("Remove timestamps", value=True, key="remove_timestamps")
            add_punctuation = st.checkbox("Fix punctuation", value=True, key="fix_punctuation")
        
        with col2:
            st.markdown("#### 📊 Content Analysis")
            word_count = len(transcript_content.split())
            st.metric("Word Count", word_count)
            st.metric("Estimated Reading Time", f"{max(1, round(word_count / 225))} min")
        
        # Process manual transcript
        if st.button("🎯 Process Transcript", type="primary"):
            video_info = st.session_state.get('current_video_info', {})
            
            with st.spinner("Processing manual transcript..."):
                transcript_result = extractor.process_manual_transcript(transcript_content, video_info)
            
            if transcript_result.get('success'):
                st.session_state.current_transcript = transcript_result
                st.success("✅ Transcript processed successfully!")
                
                display_transcript_preview(transcript_result)
                
                # Process content button
                if st.button("🚀 Process for Content Generation", type="primary"):
                    process_youtube_content(extractor)
            else:
                st.error(f"❌ {transcript_result.get('error', 'Processing failed')}")

def display_transcript_preview(transcript_result: Dict):
    """Display transcript preview and analysis"""
    st.markdown("#### 📋 Transcript Preview")
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Word Count", transcript_result.get('word_count', 0))
    with col2:
        st.metric("Duration", f"{transcript_result.get('duration_seconds', 0):.0f}s")
    with col3:
        st.metric("Language", transcript_result.get('language', 'Unknown'))
    with col4:
        st.metric("Source", transcript_result.get('source', 'API'))
    
    # Preview text
    full_text = transcript_result.get('full_text', '')
    
    if full_text:
        with st.expander("📖 Full Transcript"):
            st.text_area("", value=full_text, height=300, disabled=True)
        
        # Show first few segments with timing if available
        transcript_segments = transcript_result.get('transcript', [])
        if transcript_segments and isinstance(transcript_segments[0], dict):
            st.markdown("**Timed Segments (first 5):**")
            
            for i, segment in enumerate(transcript_segments[:5]):
                start_time = segment.get('start', 0)
                duration = segment.get('duration', 0)
                text = segment.get('text', '')
                
                st.markdown(f"**{start_time:.1f}s** - {text}")

def process_youtube_content(extractor: YouTubeExtractor):
    """Process YouTube content for article generation"""
    video_info = st.session_state.get('current_video_info', {})
    transcript_result = st.session_state.get('current_transcript', {})
    
    if not video_info or not transcript_result:
        st.error("❌ Missing video information or transcript data")
        return
    
    with st.spinner("Processing YouTube content for article generation..."):
        # Create structured content
        structured_content = extractor.create_content_structure(transcript_result, video_info)
        
        # Store as current content for the application
        content_data = {
            'title': structured_content['title'],
            'content': structured_content['transcript'],
            'meta_description': structured_content['description'][:160] if structured_content['description'] else '',
            'meta_keywords': structured_content['key_topics'][:5],
            'images': [],
            'reading_time': structured_content['estimated_reading_time'],
            'headings': [{'level': 2, 'text': heading, 'tag': 'h2'} for heading in structured_content['suggested_headings']],
            'url': f"https://youtube.com/watch?v={extractor.extract_video_id(st.session_state.get('youtube_url_input', ''))}",
            'extracted_at': datetime.now().isoformat(),
            'word_count': transcript_result.get('word_count', 0),
            'source_type': 'youtube_video',
            'video_metadata': video_info,
            'transcript_metadata': transcript_result,
            'content_analysis': structured_content['content_analysis']
        }
        
        # Store in session state
        st.session_state.current_content = content_data
        
        st.success("✅ YouTube content processed and ready for article generation!")
        
        # Display processing results
        display_processing_results(structured_content)
        
        # Navigation options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🚀 Generate Article", type="primary"):
                st.session_state.current_page = "generate"
                st.rerun()
        
        with col2:
            if st.button("⚙️ Configure SEO", type="secondary"):
                st.session_state.current_page = "seo_settings"
                st.rerun()
        
        with col3:
            if st.button("🎨 Customize Style", type="secondary"):
                st.session_state.current_page = "style_settings"
                st.rerun()

def display_processing_results(structured_content: Dict):
    """Display the results of content processing"""
    st.markdown("#### 🎯 Processing Results")
    
    result_col1, result_col2 = st.columns(2)
    
    with result_col1:
        st.markdown("**📊 Content Analysis:**")
        analysis = structured_content['content_analysis']
        
        st.markdown(f"• **Words:** {analysis['word_count']:,}")
        st.markdown(f"• **Sentences:** {analysis['sentence_count']}")
        st.markdown(f"• **Avg Sentence Length:** {analysis['avg_sentence_length']:.1f} words")
        st.markdown(f"• **Estimated Speech Rate:** {analysis['estimated_speech_rate']:.1f} words/min")
        
        complexity = analysis['complexity_indicators']
        st.markdown("**Complexity Indicators:**")
        st.markdown(f"• Long sentences: {complexity['long_sentences']}")
        st.markdown(f"• Technical terms: {complexity['technical_terms']}")
        st.markdown(f"• Questions: {complexity['questions']}")
        st.markdown(f"• Emphasis marks: {complexity['emphasis']}")
    
    with result_col2:
        st.markdown("**🏷️ Extracted Topics:**")
        topics = structured_content['key_topics']
        
        if topics:
            for i, topic in enumerate(topics[:8], 1):
                st.markdown(f"{i}. {topic}")
        else:
            st.info("No specific topics identified")
        
        st.markdown("**📑 Suggested Headings:**")
        headings = structured_content['suggested_headings']
        
        if headings:
            for heading in headings[:6]:
                st.markdown(f"• {heading}")
        else:
            st.info("No headings suggested")
    
    # Content preview
    st.markdown("#### 📖 Content Preview")
    
    preview_text = structured_content['transcript'][:500] + "..." if len(structured_content['transcript']) > 500 else structured_content['transcript']
    
    with st.expander("📄 Transcript Content (First 500 characters)"):
        st.text_area("", value=preview_text, height=150, disabled=True)
    
    # Video metadata summary
    with st.expander("📹 Video Metadata Summary"):
        video_meta = structured_content['video_metadata']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Basic Info:**")
            st.markdown(f"• Title: {video_meta.get('title', 'N/A')}")
            st.markdown(f"• Channel: {video_meta.get('channel_title', 'N/A')}")
            st.markdown(f"• Duration: {video_meta.get('duration_formatted', 'N/A')}")
        
        with col2:
            st.markdown("**Engagement:**")
            st.markdown(f"• Views: {video_meta.get('view_count', 0):,}")
            st.markdown(f"• Likes: {video_meta.get('like_count', 0):,}")
            st.markdown(f"• Comments: {video_meta.get('comment_count', 0):,}")
        
        with col3:
            st.markdown("**Technical:**")
            st.markdown(f"• Language: {video_meta.get('language', 'Unknown')}")
            st.markdown(f"• Category: {video_meta.get('category_id', 'Unknown')}")
            st.markdown(f"• Published: {video_meta.get('published_at', 'Unknown')[:10]}")

def render_youtube_tips_and_help():
    """Render tips and help section for YouTube extraction"""
    st.markdown("#### 💡 Tips & Best Practices")
    
    tip_col1, tip_col2 = st.columns(2)
    
    with tip_col1:
        st.markdown("**📋 For Best Results:**")
        st.info("""
        • Use videos with official captions when possible
        • Educational and tutorial videos work best
        • Longer videos (5+ minutes) provide more content
        • Check video language matches your target
        • Ensure video is publicly accessible
        """)
        
        st.markdown("**🔧 Troubleshooting:**")
        st.warning("""
        • If API extraction fails, try manual upload
        • Some videos may not have captions available
        • Private/restricted videos cannot be processed
        • Very short videos may not have enough content
        """)
    
    with tip_col2:
        st.markdown("**⚖️ Legal Considerations:**")
        st.error("""
        • Respect copyright and fair use guidelines
        • Only extract content you have rights to use
        • Consider reaching out to creators for permission
        • Use extracted content as reference, not direct copy
        • Attribute original creators when appropriate
        """)
        
        st.markdown("**🎯 Content Generation Tips:**")
        st.success("""
        • Combine multiple video transcripts for comprehensive articles
        • Use video content as foundation, add your insights
        • Structure content with clear headings and sections
        • Include references to original video sources
        • Add your own analysis and commentary
        """)

def render_youtube_examples():
    """Render examples of good YouTube videos for content extraction"""
    st.markdown("#### 📝 Example Use Cases")
    
    example_col1, example_col2 = st.columns(2)
    
    with example_col1:
        st.markdown("**✅ Great Video Types for Extraction:**")
        
        examples = [
            {
                'type': '🎓 Educational Tutorials',
                'description': 'Step-by-step guides, how-to videos',
                'why': 'Clear structure, actionable content'
            },
            {
                'type': '💼 Business Presentations',
                'description': 'Conference talks, webinars',
                'why': 'Professional insights, expert knowledge'
            },
            {
                'type': '🔬 Technical Explanations',
                'description': 'Software tutorials, scientific content',
                'why': 'Detailed information, specific processes'
            },
            {
                'type': '📊 Industry Analysis',
                'description': 'Market reports, trend discussions',
                'why': 'Data-driven content, expert opinions'
            }
        ]
        
        for example in examples:
            st.markdown(f"**{example['type']}**")
            st.markdown(f"• {example['description']}")
            st.markdown(f"• Why: {example['why']}")
            st.markdown("")
    
    with example_col2:
        st.markdown("**❌ Videos to Avoid:**")
        
        avoid_examples = [
            '🎵 Music videos (lyrics only)',
            '🎮 Gaming streams (casual commentary)',
            '📺 Entertainment/comedy (not informational)',
            '🔒 Private or restricted videos',
            '⚡ Very short videos (<2 minutes)',
            '🗣️ Poor audio quality videos'
        ]
        
        for avoid in avoid_examples:
            st.markdown(f"• {avoid}")
        
        st.markdown("**💡 Pro Tips:**")
        st.markdown("""
        • Look for videos with good structure
        • Choose content that teaches or explains
        • Prefer videos with clear speech
        • Educational channels often work best
        • Check if captions are available
        • Consider video length vs content density
        """)

def render_batch_youtube_processing():
    """Render interface for processing multiple YouTube videos"""
    st.markdown("#### 🔄 Batch Processing")
    st.markdown("Process multiple YouTube videos for comprehensive content generation.")
    
    with st.expander("📋 Batch YouTube Processing"):
        st.markdown("**Enter multiple YouTube URLs (one per line):**")
        
        batch_urls = st.text_area(
            "YouTube URLs:",
            height=150,
            placeholder="https://youtube.com/watch?v=video1\nhttps://youtube.com/watch?v=video2\nhttps://youtube.com/watch?v=video3",
            key="batch_youtube_urls"
        )
        
        if batch_urls:
            urls = [url.strip() for url in batch_urls.split('\n') if url.strip()]
            st.info(f"📊 Found {len(urls)} URLs to process")
            
            col1, col2 = st.columns(2)
            
            with col1:
                batch_language = st.selectbox(
                    "Default Language:",
                    options=list(st.session_state.youtube_extractor.supported_languages.keys()),
                    format_func=lambda x: f"{st.session_state.youtube_extractor.supported_languages[x]} ({x})",
                    key="batch_language"
                )
            
            with col2:
                combine_content = st.checkbox(
                    "Combine into single article",
                    value=True,
                    key="combine_batch_content",
                    help="Merge all transcripts into one comprehensive article"
                )
            
            if st.button("🚀 Process Batch", type="primary"):
                st.info("🚧 Batch processing feature will be implemented with full API integration")
                
                # This would process all URLs and combine/separate content
                # For now, show what would happen
                st.markdown("**Would process:**")
                for i, url in enumerate(urls[:5], 1):  # Show first 5
                    st.markdown(f"{i}. {url}")
                
                if len(urls) > 5:
                    st.markdown(f"... and {len(urls) - 5} more videos")

# Main YouTube extraction interface
def render_complete_youtube_extractor():
    """Render complete YouTube extraction interface"""
    st.markdown("## 🎥 YouTube Content Extraction")
    st.markdown("Transform YouTube videos into structured content for article generation.")
    
    # Main extraction interface
    render_youtube_extraction_interface()
    
    # Additional sections
    col1, col2 = st.columns(2)
    
    with col1:
        render_youtube_tips_and_help()
    
    with col2:
        render_youtube_examples()
    
    # Batch processing
    render_batch_youtube_processing()
    
    # API setup help
    with st.expander("🔧 API Setup Instructions"):
        st.markdown("""
        ### Setting up YouTube Data API
        
        1. **Go to Google Cloud Console**
           - Visit: https://console.cloud.google.com/
        
        2. **Create or Select Project**
           - Create a new project or select existing one
        
        3. **Enable YouTube Data API v3**
           - Go to APIs & Services > Library
           - Search for "YouTube Data API v3"
           - Click Enable
        
        4. **Create API Key**
           - Go to APIs & Services > Credentials
           - Click "Create Credentials" > "API Key"
           - Copy your API key
        
        5. **Configure Restrictions (Recommended)**
           - Restrict API key to YouTube Data API v3
           - Add application restrictions if needed
        
        **Note:** The API has daily quotas. For production use, monitor your usage in the Google Cloud Console.
        """)
