import streamlit as st
import os
import tempfile
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import base64

class AudioProcessor:
    """Advanced audio processing and transcription system"""
    
    def __init__(self):
        self.supported_formats = {
            'mp3': {'name': 'MP3', 'description': 'Most common audio format', 'max_size': 25},
            'wav': {'name': 'WAV', 'description': 'Uncompressed, high quality', 'max_size': 25},
            'ogg': {'name': 'OGG', 'description': 'Open source format', 'max_size': 25},
            'm4a': {'name': 'M4A', 'description': 'Apple audio format', 'max_size': 25},
            'flac': {'name': 'FLAC', 'description': 'Lossless compression', 'max_size': 25},
            'aac': {'name': 'AAC', 'description': 'Advanced Audio Coding', 'max_size': 25},
            'wma': {'name': 'WMA', 'description': 'Windows Media Audio', 'max_size': 25}
        }
        
        self.transcription_services = {
            'whisper_local': {
                'name': 'OpenAI Whisper (Local)',
                'description': 'Run Whisper locally for privacy',
                'pros': ['High accuracy', 'Privacy-focused', 'No API costs'],
                'cons': ['Requires local setup', 'Slower processing'],
                'languages': 99,
                'available': False  # Requires whisper installation
            },
            'whisper_api': {
                'name': 'OpenAI Whisper (API)',
                'description': 'Cloud-based Whisper transcription',
                'pros': ['Fastest processing', 'No setup required', 'Latest models'],
                'cons': ['API costs', 'File upload required'],
                'languages': 99,
                'available': True
            },
            'mock_transcription': {
                'name': 'Demo Transcription',
                'description': 'Mock transcription for testing',
                'pros': ['Instant results', 'No setup required'],
                'cons': ['Not real transcription', 'Demo purposes only'],
                'languages': 1,
                'available': True
            }
        }
        
        self.quality_settings = {
            'draft': {
                'name': 'Draft Quality',
                'description': 'Quick transcription for initial review',
                'processing_time': 'Fast',
                'accuracy': 'Good'
            },
            'standard': {
                'name': 'Standard Quality',
                'description': 'Balanced speed and accuracy',
                'processing_time': 'Medium',
                'accuracy': 'Very Good'
            },
            'premium': {
                'name': 'Premium Quality',
                'description': 'Best accuracy with advanced processing',
                'processing_time': 'Slow',
                'accuracy': 'Excellent'
            }
        }
    
    def validate_audio_file(self, uploaded_file) -> Tuple[bool, str, Dict]:
        """Validate uploaded audio file"""
        if not uploaded_file:
            return False, "No file uploaded", {}
        
        # Check file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension not in self.supported_formats:
            supported_list = ', '.join(self.supported_formats.keys())
            return False, f"Unsupported format. Supported: {supported_list}", {}
        
        # Check file size (in MB)
        file_size_mb = uploaded_file.size / (1024 * 1024)
        max_size = self.supported_formats[file_extension]['max_size']
        
        if file_size_mb > max_size:
            return False, f"File too large. Maximum size: {max_size}MB", {}
        
        # File info
        file_info = {
            'name': uploaded_file.name,
            'size_mb': round(file_size_mb, 2),
            'format': self.supported_formats[file_extension]['name'],
            'extension': file_extension,
            'estimated_duration': self.estimate_duration_from_size(file_size_mb, file_extension)
        }
        
        return True, "File validated successfully", file_info
    
    def estimate_duration_from_size(self, size_mb: float, format_type: str) -> str:
        """Estimate audio duration from file size"""
        # Rough estimates based on common bitrates
        bitrate_estimates = {
            'mp3': 128,  # kbps
            'wav': 1411,  # kbps (CD quality)
            'ogg': 112,
            'm4a': 128,
            'flac': 800,
            'aac': 128,
            'wma': 128
        }
        
        bitrate = bitrate_estimates.get(format_type, 128)
        duration_seconds = (size_mb * 8 * 1024) / bitrate
        
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        
        return f"~{minutes}:{seconds:02d}"
    
    def analyze_audio_metadata(self, uploaded_file) -> Dict:
        """Analyze audio file metadata (mock implementation)"""
        # In production, this would use libraries like mutagen or librosa
        return {
            'duration': '5:23',
            'sample_rate': '44.1 kHz',
            'bit_depth': '16-bit',
            'channels': 'Stereo',
            'bitrate': '128 kbps',
            'encoding': 'MP3',
            'estimated_words': 800,
            'audio_quality': 'Good',
            'noise_level': 'Low',
            'speaker_count': 'Single speaker detected'
        }
    
    def transcribe_audio_mock(self, file_info: Dict, options: Dict) -> Dict:
        """Mock transcription for demo purposes"""
        # Simulate processing time
        import time
        
        # Generate mock transcript based on options
        language = options.get('language', 'en')
        quality = options.get('quality', 'standard')
        
        mock_segments = [
            {
                'start': 0.0,
                'end': 4.2,
                'text': 'Welcome to this audio recording. Today we will be discussing important topics that can help improve your understanding.',
                'confidence': 0.95
            },
            {
                'start': 4.2,
                'end': 8.8,
                'text': 'First, let me introduce the key concepts that we will be covering in this session.',
                'confidence': 0.92
            },
            {
                'start': 8.8,
                'end': 13.5,
                'text': 'The main objective is to provide you with practical knowledge that you can apply immediately.',
                'confidence': 0.94
            },
            {
                'start': 13.5,
                'end': 18.1,
                'text': 'We will start with the fundamentals and gradually move to more advanced techniques.',
                'confidence': 0.91
            },
            {
                'start': 18.1,
                'end': 22.7,
                'text': 'Understanding these principles is crucial for achieving the best results in your work.',
                'confidence': 0.93
            },
            {
                'start': 22.7,
                'end': 27.3,
                'text': 'Let me show you some practical examples that demonstrate these concepts in action.',
                'confidence': 0.89
            },
            {
                'start': 27.3,
                'end': 31.9,
                'text': 'Pay attention to the details as they will be important for your implementation.',
                'confidence': 0.92
            },
            {
                'start': 31.9,
                'end': 36.5,
                'text': 'Remember that practice is essential for mastering these skills and techniques.',
                'confidence': 0.94
            },
            {
                'start': 36.5,
                'end': 41.1,
                'text': 'In the next section, we will explore advanced strategies and best practices.',
                'confidence': 0.90
            },
            {
                'start': 41.1,
                'end': 45.0,
                'text': 'Thank you for your attention, and I hope you find this information valuable.',
                'confidence': 0.93
            }
        ]
        
        # Combine segments into full text
        full_text = ' '.join([segment['text'] for segment in mock_segments])
        
        # Calculate average confidence
        avg_confidence = sum([segment['confidence'] for segment in mock_segments]) / len(mock_segments)
        
        return {
            'success': True,
            'transcript': {
                'segments': mock_segments,
                'full_text': full_text,
                'language': language,
                'duration': 45.0,
                'word_count': len(full_text.split()),
                'average_confidence': avg_confidence,
                'processing_time': 2.5,
                'quality_score': 0.92
            },
            'metadata': {
                'service_used': 'mock_transcription',
                'model_version': 'demo-v1',
                'processing_date': datetime.now().isoformat(),
                'settings_used': options
            }
        }
    
    def transcribe_with_whisper_api(self, uploaded_file, options: Dict) -> Dict:
        """Transcribe using OpenAI Whisper API (placeholder)"""
        # This would implement actual Whisper API integration
        return {
            'success': False,
            'error': 'Whisper API integration requires OpenAI API key configuration',
            'suggestion': 'Use demo transcription or configure API key in settings'
        }
    
    def enhance_transcript_quality(self, transcript: Dict, options: Dict) -> Dict:
        """Enhance transcript quality with post-processing"""
        if not transcript.get('success'):
            return transcript
        
        segments = transcript['transcript']['segments']
        enhanced_segments = []
        
        for segment in segments:
            enhanced_segment = segment.copy()
            
            # Clean up text
            text = segment['text']
            
            # Fix common transcription issues
            if options.get('fix_punctuation', True):
                text = self.fix_punctuation(text)
            
            if options.get('fix_capitalization', True):
                text = self.fix_capitalization(text)
            
            if options.get('remove_filler_words', False):
                text = self.remove_filler_words(text)
            
            enhanced_segment['text'] = text
            enhanced_segment['enhanced'] = True
            enhanced_segments.append(enhanced_segment)
        
        # Update transcript
        enhanced_transcript = transcript.copy()
        enhanced_transcript['transcript']['segments'] = enhanced_segments
        enhanced_transcript['transcript']['full_text'] = ' '.join([seg['text'] for seg in enhanced_segments])
        enhanced_transcript['transcript']['enhanced'] = True
        
        return enhanced_transcript
    
    def fix_punctuation(self, text: str) -> str:
        """Fix punctuation in transcribed text"""
        # Add periods at the end of sentences
        text = re.sub(r'([a-z])\s+([A-Z])', r'\1. \2', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([,.!?])', r'\1', text)
        text = re.sub(r'([,.!?])([A-Za-z])', r'\1 \2', text)
        
        # Ensure text ends with punctuation
        if text and not text[-1] in '.!?':
            text += '.'
        
        return text
    
    def fix_capitalization(self, text: str) -> str:
        """Fix capitalization in transcribed text"""
        # Capitalize first letter
        if text:
            text = text[0].upper() + text[1:]
        
        # Capitalize after periods
        text = re.sub(r'(\. )([a-z])', lambda m: m.group(1) + m.group(2).upper(), text)
        
        return text
    
    def remove_filler_words(self, text: str) -> str:
        """Remove filler words from transcript"""
        filler_words = ['um', 'uh', 'ah', 'like', 'you know', 'so', 'well']
        
        for filler in filler_words:
            # Remove filler words (case insensitive)
            pattern = r'\b' + re.escape(filler) + r'\b'
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def analyze_transcript_content(self, transcript: Dict) -> Dict:
        """Analyze transcript content for insights"""
        if not transcript.get('success'):
            return {}
        
        full_text = transcript['transcript']['full_text']
        segments = transcript['transcript']['segments']
        
        # Basic metrics
        word_count = len(full_text.split())
        sentence_count = full_text.count('.') + full_text.count('!') + full_text.count('?')
        
        # Speaking rate analysis
        duration = transcript['transcript']['duration']
        words_per_minute = (word_count / duration) * 60 if duration > 0 else 0
        
        # Confidence analysis
        confidences = [seg.get('confidence', 0) for seg in segments]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        low_confidence_segments = len([c for c in confidences if c < 0.8])
        
        # Content analysis
        questions = full_text.count('?')
        exclamations = full_text.count('!')
        
        # Identify potential topics (simple keyword extraction)
        words = re.findall(r'\b[a-zA-Z]{4,}\b', full_text.lower())
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top keywords
        common_words = {'this', 'that', 'with', 'will', 'have', 'they', 'been', 'from', 'would', 'could', 'should'}
        keywords = [(word, freq) for word, freq in word_freq.items() 
                   if freq > 2 and word not in common_words]
        keywords.sort(key=lambda x: x[1], reverse=True)
        
        return {
            'basic_metrics': {
                'word_count': word_count,
                'sentence_count': sentence_count,
                'average_sentence_length': word_count / max(sentence_count, 1),
                'speaking_rate_wpm': round(words_per_minute, 1),
                'duration_minutes': round(duration / 60, 1)
            },
            'quality_metrics': {
                'average_confidence': round(avg_confidence, 2),
                'low_confidence_segments': low_confidence_segments,
                'confidence_distribution': {
                    'high': len([c for c in confidences if c >= 0.9]),
                    'medium': len([c for c in confidences if 0.7 <= c < 0.9]),
                    'low': len([c for c in confidences if c < 0.7])
                }
            },
            'content_features': {
                'questions_count': questions,
                'exclamations_count': exclamations,
                'top_keywords': keywords[:10],
                'estimated_complexity': self.estimate_content_complexity(full_text)
            }
        }
    
    def estimate_content_complexity(self, text: str) -> str:
        """Estimate content complexity level"""
        words = text.split()
        long_words = len([w for w in words if len(w) > 6])
        long_word_ratio = long_words / len(words) if words else 0
        
        sentences = [s for s in text.split('.') if s.strip()]
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        if long_word_ratio > 0.2 or avg_sentence_length > 20:
            return 'High'
        elif long_word_ratio > 0.1 or avg_sentence_length > 15:
            return 'Medium'
        else:
            return 'Low'
    
    def create_structured_content(self, transcript: Dict, file_info: Dict, analysis: Dict) -> Dict:
        """Create structured content from transcript"""
        if not transcript.get('success'):
            return {}
        
        transcript_data = transcript['transcript']
        
        # Generate title from content
        title = self.generate_title_from_content(transcript_data['full_text'], file_info['name'])
        
        # Extract key topics for meta description
        keywords = analysis.get('content_features', {}).get('top_keywords', [])
        top_keywords = [kw[0] for kw in keywords[:5]]
        
        # Generate meta description
        meta_description = self.generate_meta_description(transcript_data['full_text'], top_keywords)
        
        # Suggest content structure
        suggested_headings = self.suggest_content_headings(transcript_data['full_text'], transcript_data['segments'])
        
        return {
            'title': title,
            'content': transcript_data['full_text'],
            'meta_description': meta_description,
            'meta_keywords': top_keywords,
            'word_count': transcript_data['word_count'],
            'reading_time': max(1, round(transcript_data['word_count'] / 225)),
            'audio_duration': transcript_data['duration'],
            'suggested_headings': suggested_headings,
            'transcript_segments': transcript_data['segments'],
            'quality_score': transcript_data.get('quality_score', 0),
            'confidence_score': transcript_data.get('average_confidence', 0),
            'source_type': 'audio_transcription',
            'file_info': file_info,
            'analysis': analysis,
            'extracted_at': datetime.now().isoformat()
        }
    
    def generate_title_from_content(self, content: str, filename: str) -> str:
        """Generate a title from content"""
        # Try to extract a meaningful title from the first sentence
        sentences = [s.strip() for s in content.split('.') if s.strip()]
        
        if sentences:
            first_sentence = sentences[0]
            # If first sentence is short and declarative, use it
            if len(first_sentence.split()) < 12 and not first_sentence.lower().startswith(('welcome', 'hello', 'hi')):
                return first_sentence
        
        # Generate title from filename
        base_name = os.path.splitext(filename)[0]
        # Clean filename and make it title-case
        title = re.sub(r'[_-]', ' ', base_name)
        title = ' '.join(word.capitalize() for word in title.split())
        
        return f"Audio Content: {title}"
    
    def generate_meta_description(self, content: str, keywords: List[str]) -> str:
        """Generate meta description from content"""
        # Use first 2-3 sentences, up to 160 characters
        sentences = [s.strip() + '.' for s in content.split('.') if s.strip()]
        
        description = ""
        for sentence in sentences[:3]:
            if len(description + sentence) <= 160:
                description += sentence + " "
            else:
                break
        
        if not description and keywords:
            description = f"Audio transcript covering {', '.join(keywords[:3])} and related topics."
        
        return description.strip()[:160]
    
    def suggest_content_headings(self, content: str, segments: List[Dict]) -> List[str]:
        """Suggest content headings based on transcript analysis"""
        headings = ["Introduction"]
        
        # Analyze segments for topic changes
        segment_texts = [seg['text'] for seg in segments]
        
        # Look for transition phrases that might indicate new sections
        transition_phrases = [
            'now let', 'next', 'moving on', 'another', 'also', 'furthermore',
            'in addition', 'let me', 'so now', 'the next', 'another important'
        ]
        
        section_count = 1
        for i, segment_text in enumerate(segment_texts):
            for phrase in transition_phrases:
                if phrase in segment_text.lower() and i > len(segment_texts) * 0.2:
                    section_count += 1
                    headings.append(f"Key Point {section_count}")
                    break
            
            if section_count >= 5:  # Limit number of sections
                break
        
        # Always add conclusion
        if len(headings) > 1:
            headings.append("Summary and Conclusion")
        
        return headings

def render_audio_processing_interface():
    """Render comprehensive audio processing interface"""
    st.markdown("### 🎧 Audio Processing & Transcription")
    st.markdown("Upload audio files and convert them to structured content for article generation.")
    
    # Initialize audio processor
    if 'audio_processor' not in st.session_state:
        st.session_state.audio_processor = AudioProcessor()
    
    processor = st.session_state.audio_processor
    
    # Audio upload section
    render_audio_upload_section(processor)

def render_audio_upload_section(processor: AudioProcessor):
    """Render audio file upload and validation section"""
    st.markdown("#### 📁 Upload Audio File")
    
    # File upload
    col1, col2 = st.columns([3, 1])
    
    with col1:
        supported_extensions = list(processor.supported_formats.keys())
        
        uploaded_file = st.file_uploader(
            "Choose audio file:",
            type=supported_extensions,
            help=f"Supported formats: {', '.join(supported_extensions)}. Max size: 25MB per file."
        )
    
    with col2:
        if uploaded_file:
            st.success("✅ File uploaded")
        else:
            st.info("ℹ️ No file selected")
    
    # Display supported formats
    with st.expander("📋 Supported Audio Formats"):
        format_col1, format_col2 = st.columns(2)
        
        formats_list = list(processor.supported_formats.items())
        mid_point = len(formats_list) // 2
        
        with format_col1:
            for fmt, info in formats_list[:mid_point]:
                st.markdown(f"**{info['name']} (.{fmt})**")
                st.markdown(f"• {info['description']}")
                st.markdown(f"• Max size: {info['max_size']}MB")
                st.markdown("")
        
        with format_col2:
            for fmt, info in formats_list[mid_point:]:
                st.markdown(f"**{info['name']} (.{fmt})**")
                st.markdown(f"• {info['description']}")
                st.markdown(f"• Max size: {info['max_size']}MB")
                st.markdown("")
    
    # Process uploaded file
    if uploaded_file:
        process_uploaded_audio_file(processor, uploaded_file)

def process_uploaded_audio_file(processor: AudioProcessor, uploaded_file):
    """Process the uploaded audio file"""
    # Validate file
    is_valid, message, file_info = processor.validate_audio_file(uploaded_file)
    
    if not is_valid:
        st.error(f"❌ {message}")
        return
    
    st.success(f"✅ {message}")
    
    # Display file information
    display_audio_file_info(file_info, processor, uploaded_file)
    
    # Transcription configuration
    render_transcription_configuration(processor, uploaded_file, file_info)

def display_audio_file_info(file_info: Dict, processor: AudioProcessor, uploaded_file):
    """Display audio file information"""
    st.markdown("#### 📊 File Information")
    
    info_col1, info_col2, info_col3 = st.columns(3)
    
    with info_col1:
        st.markdown("**Basic Info:**")
        st.markdown(f"• **Name:** {file_info['name']}")
        st.markdown(f"• **Format:** {file_info['format']}")
        st.markdown(f"• **Size:** {file_info['size_mb']} MB")
    
    with info_col2:
        st.markdown("**Estimated Properties:**")
        st.markdown(f"• **Duration:** {file_info['estimated_duration']}")
        
        # Get audio metadata (mock)
        metadata = processor.analyze_audio_metadata(uploaded_file)
        st.markdown(f"• **Quality:** {metadata.get('audio_quality', 'Unknown')}")
        st.markdown(f"• **Noise Level:** {metadata.get('noise_level', 'Unknown')}")
    
    with info_col3:
        st.markdown("**Transcription Estimates:**")
        metadata = processor.analyze_audio_metadata(uploaded_file)
        st.markdown(f"• **Est. Words:** {metadata.get('estimated_words', 'Unknown')}")
        st.markdown(f"• **Speakers:** {metadata.get('speaker_count', 'Unknown')}")
        st.markdown(f"• **Processing Time:** ~2-5 min")
    
    # Detailed metadata
    with st.expander("🔍 Detailed Audio Analysis"):
        metadata = processor.analyze_audio_metadata(uploaded_file)
        
        detail_col1, detail_col2 = st.columns(2)
        
        with detail_col1:
            st.markdown("**Technical Specifications:**")
            st.markdown(f"• Sample Rate: {metadata.get('sample_rate', 'Unknown')}")
            st.markdown(f"• Bit Depth: {metadata.get('bit_depth', 'Unknown')}")
            st.markdown(f"• Channels: {metadata.get('channels', 'Unknown')}")
            st.markdown(f"• Bitrate: {metadata.get('bitrate', 'Unknown')}")
        
        with detail_col2:
            st.markdown("**Content Analysis:**")
            st.markdown(f"• Encoding: {metadata.get('encoding', 'Unknown')}")
            st.markdown(f"• Audio Quality: {metadata.get('audio_quality', 'Unknown')}")
            st.markdown(f"• Background Noise: {metadata.get('noise_level', 'Unknown')}")
            st.markdown(f"• Speaker Detection: {metadata.get('speaker_count', 'Unknown')}")

def render_transcription_configuration(processor: AudioProcessor, uploaded_file, file_info: Dict):
    """Render transcription configuration options"""
    st.markdown("---")
    st.markdown("#### ⚙️ Transcription Configuration")
    
    # Service selection
    config_col1, config_col2 = st.columns(2)
    
    with config_col1:
        st.markdown("**Transcription Service:**")
        
        available_services = {k: v for k, v in processor.transcription_services.items() if v['available']}
        
        selected_service = st.radio(
            "Choose service:",
            options=list(available_services.keys()),
            format_func=lambda x: available_services[x]['name'],
            key="transcription_service"
        )
        
        # Show service details
        service_info = available_services[selected_service]
        st.markdown(f"**{service_info['name']}**")
        st.markdown(service_info['description'])
        
        st.markdown("**Pros:**")
        for pro in service_info['pros']:
            st.markdown(f"✅ {pro}")
        
        st.markdown("**Cons:**")
        for con in service_info['cons']:
            st.markdown(f"⚠️ {con}")
    
    with config_col2:
        st.markdown("**Quality & Options:**")
        
        # Quality selection
        quality_options = list(processor.quality_settings.keys())
        selected_quality = st.selectbox(
            "Processing Quality:",
            options=quality_options,
            format_func=lambda x: processor.quality_settings[x]['name'],
            index=1,  # Default to 'standard'
            key="transcription_quality"
        )
        
        quality_info = processor.quality_settings[selected_quality]
        st.info(f"📊 {quality_info['description']}")
        st.markdown(f"• **Speed:** {quality_info['processing_time']}")
        st.markdown(f"• **Accuracy:** {quality_info['accuracy']}")
        
        # Language selection
        if selected_service != 'mock_transcription':
            language = st.selectbox(
                "Audio Language:",
                options=['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh'],
                format_func=lambda x: {
                    'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
                    'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese',
                    'ko': 'Korean', 'zh': 'Chinese'
                }[x],
                key="audio_language"
            )
        else:
            language = 'en'
    
    # Advanced options
    render_advanced_transcription_options()
    
    # Start transcription
    transcription_options = {
        'service': selected_service,
        'quality': selected_quality,
        'language': language,
        'fix_punctuation': st.session_state.get('fix_punctuation', True),
        'fix_capitalization': st.session_state.get('fix_capitalization', True),
        'remove_filler_words': st.session_state.get('remove_filler_words', False),
        'include_timestamps': st.session_state.get('include_timestamps', True),
        'speaker_identification': st.session_state.get('speaker_identification', False)
    }
    
    if st.button("🎯 Start Transcription", type="primary"):
        start_transcription_process(processor, uploaded_file, file_info, transcription_options)

def render_advanced_transcription_options():
    """Render advanced transcription options"""
    with st.expander("🔧 Advanced Options"):
        adv_col1, adv_col2 = st.columns(2)
        
        with adv_col1:
            st.markdown("**Text Enhancement:**")
            
            st.checkbox(
                "Fix punctuation",
                value=True,
                key="fix_punctuation",
                help="Automatically add proper punctuation to transcript"
            )
            
            st.checkbox(
                "Fix capitalization",
                value=True,
                key="fix_capitalization",
                help="Automatically capitalize sentences and proper nouns"
            )
            
            st.checkbox(
                "Remove filler words",
                value=False,
                key="remove_filler_words",
                help="Remove 'um', 'uh', 'like' and other filler words"
            )
        
        with adv_col2:
            st.markdown("**Technical Options:**")
            
            st.checkbox(
                "Include timestamps",
                value=True,
                key="include_timestamps",
                help="Keep timing information for each segment"
            )
            
            st.checkbox(
                "Speaker identification",
                value=False,
                key="speaker_identification",
                help="Attempt to identify different speakers (experimental)"
            )
            
            st.checkbox(
                "Enhanced noise reduction",
                value=False,
                key="noise_reduction",
                help="Apply additional noise filtering (slower processing)"
            )

def start_transcription_process(processor: AudioProcessor, uploaded_file, file_info: Dict, options: Dict):
    """Start the transcription process"""
    
    # Create progress indicators
    progress_container = st.container()
    
    with progress_container:
        st.markdown("#### 🔄 Transcription in Progress")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: File preparation
        status_text.text("📁 Preparing audio file...")
        progress_bar.progress(20)
        
        # Step 2: Transcription
        status_text.text("🎯 Transcribing audio content...")
        progress_bar.progress(40)
        
        # Perform transcription based on selected service
        if options['service'] == 'mock_transcription':
            transcript_result = processor.transcribe_audio_mock(file_info, options)
        elif options['service'] == 'whisper_api':
            transcript_result = processor.transcribe_with_whisper_api(uploaded_file, options)
        else:
            transcript_result = {'success': False, 'error': 'Service not implemented'}
        
        progress_bar.progress(60)
        
        if not transcript_result.get('success'):
            status_text.text("❌ Transcription failed")
            st.error(f"Transcription failed: {transcript_result.get('error', 'Unknown error')}")
            
            if transcript_result.get('suggestion'):
                st.info(f"💡 Suggestion: {transcript_result['suggestion']}")
            
            progress_bar.empty()
            status_text.empty()
            return
        
        # Step 3: Enhancement
        status_text.text("✨ Enhancing transcript quality...")
        progress_bar.progress(80)
        
        enhanced_transcript = processor.enhance_transcript_quality(transcript_result, options)
        
        # Step 4: Analysis
        status_text.text("📊 Analyzing content...")
        progress_bar.progress(90)
        
        content_analysis = processor.analyze_transcript_content(enhanced_transcript)
        
        # Step 5: Finalization
        status_text.text("🎉 Finalizing results...")
        progress_bar.progress(100)
        
        # Store results
        st.session_state.current_transcript = enhanced_transcript
        st.session_state.current_audio_analysis = content_analysis
        st.session_state.current_audio_file_info = file_info
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
        
        st.success("✅ Audio transcription completed successfully!")
    
    # Display results
    display_transcription_results(processor, enhanced_transcript, content_analysis, file_info)

def display_transcription_results(processor: AudioProcessor, transcript: Dict, analysis: Dict, file_info: Dict):
    """Display transcription results and analysis"""
    st.markdown("#### 🎉 Transcription Results")
    
    transcript_data = transcript['transcript']
    
    # Results overview
    result_col1, result_col2, result_col3, result_col4 = st.columns(4)
    
    with result_col1:
        st.metric("Word Count", transcript_data['word_count'])
    
    with result_col2:
        st.metric("Duration", f"{transcript_data['duration']:.1f}s")
    
    with result_col3:
        confidence = transcript_data.get('average_confidence', 0)
        st.metric("Avg Confidence", f"{confidence:.1%}")
    
    with result_col4:
        quality = transcript_data.get('quality_score', 0)
        st.metric("Quality Score", f"{quality:.1%}")
    
    # Detailed results tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Transcript", "📊 Analysis", "⚙️ Settings", "🎯 Generate Content"])
    
    with tab1:
        render_transcript_display(transcript_data)
    
    with tab2:
        render_transcript_analysis(analysis)
    
    with tab3:
        render_processing_settings(transcript)
    
    with tab4:
        render_content_generation_options(processor, transcript, analysis, file_info)

def render_transcript_display(transcript_data: Dict):
    """Display the transcript content"""
    st.markdown("### 📄 Transcript Content")
    
    display_col1, display_col2 = st.columns([3, 1])
    
    with display_col1:
        # Full transcript
        st.markdown("#### 📖 Full Transcript")
        
        full_text = transcript_data['full_text']
        
        # Display options
        show_timestamps = st.checkbox("Show timestamps", value=False, key="show_timestamps_display")
        show_confidence = st.checkbox("Show confidence scores", value=False, key="show_confidence_display")
        
        if show_timestamps or show_confidence:
            st.markdown("**Segmented Transcript:**")
            
            segments = transcript_data.get('segments', [])
            
            for i, segment in enumerate(segments):
                segment_text = segment['text']
                
                # Add timestamp if requested
                if show_timestamps:
                    start_time = segment.get('start', 0)
                    end_time = segment.get('end', segment.get('start', 0) + segment.get('duration', 0))
                    timestamp = f"[{start_time:.1f}s - {end_time:.1f}s]"
                    segment_text = f"{timestamp} {segment_text}"
                
                # Add confidence if requested
                if show_confidence:
                    confidence = segment.get('confidence', 0)
                    conf_indicator = "🟢" if confidence > 0.9 else "🟡" if confidence > 0.7 else "🔴"
                    segment_text = f"{conf_indicator} {segment_text}"
                
                st.markdown(f"{i+1}. {segment_text}")
        else:
            # Simple full text display
            st.text_area(
                "Full transcript:",
                value=full_text,
                height=400,
                key="full_transcript_display"
            )
    
    with display_col2:
        st.markdown("#### 🎛️ Display Options")
        
        # Export options
        st.markdown("**Export Transcript:**")
        
        # Plain text export
        st.download_button(
            "📄 Download as Text",
            data=transcript_data['full_text'],
            file_name=f"transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
        # JSON export with timestamps
        transcript_json = json.dumps({
            'transcript': transcript_data,
            'exported_at': datetime.now().isoformat()
        }, indent=2)
        
        st.download_button(
            "📊 Download as JSON",
            data=transcript_json,
            file_name=f"transcript_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        # SRT subtitle format
        srt_content = generate_srt_format(transcript_data.get('segments', []))
        if srt_content:
            st.download_button(
                "🎬 Download as SRT",
                data=srt_content,
                file_name=f"subtitles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.srt",
                mime="text/plain"
            )
        
        # Quick stats
        st.markdown("#### 📊 Quick Stats")
        
        reading_time = max(1, round(transcript_data['word_count'] / 225))
        st.metric("Reading Time", f"{reading_time} min")
        
        speaking_rate = (transcript_data['word_count'] / transcript_data['duration']) * 60
        st.metric("Speaking Rate", f"{speaking_rate:.0f} WPM")

def render_transcript_analysis(analysis: Dict):
    """Display transcript analysis results"""
    st.markdown("### 📊 Content Analysis")
    
    if not analysis:
        st.info("No analysis data available")
        return
    
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        st.markdown("#### 📈 Basic Metrics")
        
        basic = analysis.get('basic_metrics', {})
        
        st.metric("Word Count", basic.get('word_count', 0))
        st.metric("Sentence Count", basic.get('sentence_count', 0))
        st.metric("Avg Sentence Length", f"{basic.get('average_sentence_length', 0):.1f} words")
        st.metric("Speaking Rate", f"{basic.get('speaking_rate_wpm', 0)} WPM")
        st.metric("Duration", f"{basic.get('duration_minutes', 0)} minutes")
        
        st.markdown("#### 🎯 Content Features")
        
        content_features = analysis.get('content_features', {})
        
        st.metric("Questions", content_features.get('questions_count', 0))
        st.metric("Exclamations", content_features.get('exclamations_count', 0))
        st.metric("Complexity", content_features.get('estimated_complexity', 'Unknown'))
    
    with analysis_col2:
        st.markdown("#### 🎤 Quality Metrics")
        
        quality = analysis.get('quality_metrics', {})
        
        avg_conf = quality.get('average_confidence', 0)
        st.metric("Average Confidence", f"{avg_conf:.1%}")
        
        low_conf = quality.get('low_confidence_segments', 0)
        st.metric("Low Confidence Segments", low_conf)
        
        # Confidence distribution
        conf_dist = quality.get('confidence_distribution', {})
        if conf_dist:
            st.markdown("**Confidence Distribution:**")
            st.markdown(f"• High (≥90%): {conf_dist.get('high', 0)} segments")
            st.markdown(f"• Medium (70-89%): {conf_dist.get('medium', 0)} segments")
            st.markdown(f"• Low (<70%): {conf_dist.get('low', 0)} segments")
        
        st.markdown("#### 🏷️ Top Keywords")
        
        keywords = content_features.get('top_keywords', [])
        if keywords:
            for i, (keyword, freq) in enumerate(keywords[:8], 1):
                st.markdown(f"{i}. **{keyword}** ({freq} times)")
        else:
            st.info("No significant keywords identified")

def render_processing_settings(transcript: Dict):
    """Display processing settings and metadata"""
    st.markdown("### ⚙️ Processing Information")
    
    metadata = transcript.get('metadata', {})
    transcript_data = transcript.get('transcript', {})
    
    settings_col1, settings_col2 = st.columns(2)
    
    with settings_col1:
        st.markdown("#### 🛠️ Processing Settings")
        
        settings_used = metadata.get('settings_used', {})
        
        st.markdown(f"**Service:** {settings_used.get('service', 'Unknown')}")
        st.markdown(f"**Quality:** {settings_used.get('quality', 'Unknown')}")
        st.markdown(f"**Language:** {settings_used.get('language', 'Unknown')}")
        st.markdown(f"**Model:** {metadata.get('model_version', 'Unknown')}")
        
        st.markdown("**Enhancements Applied:**")
        
        enhancements = [
            ('Fix punctuation', settings_used.get('fix_punctuation', False)),
            ('Fix capitalization', settings_used.get('fix_capitalization', False)),
            ('Remove filler words', settings_used.get('remove_filler_words', False)),
            ('Include timestamps', settings_used.get('include_timestamps', False))
        ]
        
        for enhancement, applied in enhancements:
            status = "✅" if applied else "❌"
            st.markdown(f"{status} {enhancement}")
    
    with settings_col2:
        st.markdown("#### 📊 Processing Results")
        
        processing_time = transcript_data.get('processing_time', 0)
        st.metric("Processing Time", f"{processing_time:.1f}s")
        
        quality_score = transcript_data.get('quality_score', 0)
        st.metric("Quality Score", f"{quality_score:.1%}")
        
        enhanced = transcript_data.get('enhanced', False)
        st.metric("Enhanced", "✅ Yes" if enhanced else "❌ No")
        
        st.markdown("#### 🕒 Timestamps")
        
        processing_date = metadata.get('processing_date', '')
        if processing_date:
            try:
                date_obj = datetime.fromisoformat(processing_date.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                st.markdown(f"**Processed:** {formatted_date}")
            except:
                st.markdown(f"**Processed:** {processing_date}")

def render_content_generation_options(processor: AudioProcessor, transcript: Dict, analysis: Dict, file_info: Dict):
    """Render content generation options"""
    st.markdown("### 🎯 Generate Article Content")
    st.markdown("Transform your audio transcript into a structured article.")
    
    # Content structure preview
    structured_content = processor.create_structured_content(transcript, file_info, analysis)
    
    if not structured_content:
        st.error("Unable to create structured content from transcript")
        return
    
    generation_col1, generation_col2 = st.columns(2)
    
    with generation_col1:
        st.markdown("#### 📋 Content Preview")
        
        st.markdown(f"**Generated Title:** {structured_content['title']}")
        st.markdown(f"**Meta Description:** {structured_content['meta_description']}")
        
        if structured_content.get('meta_keywords'):
            keywords_text = ', '.join(structured_content['meta_keywords'])
            st.markdown(f"**Keywords:** {keywords_text}")
        
        st.markdown("**Suggested Headings:**")
        for i, heading in enumerate(structured_content.get('suggested_headings', []), 1):
            st.markdown(f"{i}. {heading}")
        
        # Content preview
        content_preview = structured_content['content'][:300] + "..." if len(structured_content['content']) > 300 else structured_content['content']
        
        with st.expander("📖 Content Preview"):
            st.text_area("", value=content_preview, height=200, disabled=True)
    
    with generation_col2:
        st.markdown("#### 📊 Content Metrics")
        
        st.metric("Word Count", structured_content['word_count'])
        st.metric("Reading Time", f"{structured_content['reading_time']} min")
        st.metric("Audio Duration", f"{structured_content['audio_duration']:.1f}s")
        st.metric("Quality Score", f"{structured_content['quality_score']:.1%}")
        st.metric("Confidence", f"{structured_content['confidence_score']:.1%}")
        
        st.markdown("#### 🎯 Optimization Potential")
        
        # Assess content quality for article generation
        word_count = structured_content['word_count']
        confidence = structured_content['confidence_score']
        
        if word_count >= 500 and confidence >= 0.8:
            st.success("✅ Excellent for article generation")
        elif word_count >= 300 and confidence >= 0.7:
            st.info("ℹ️ Good for article generation")
        elif word_count >= 200:
            st.warning("⚠️ Consider additional content")
        else:
            st.error("❌ May need more content")
    
    # Generate content button
    st.markdown("---")
    
    if st.button("🚀 Process for Article Generation", type="primary"):
        # Store structured content for article generation
        st.session_state.current_content = structured_content
        
        st.success("✅ Audio content processed and ready for article generation!")
        
        # Navigation options
        nav_col1, nav_col2, nav_col3 = st.columns(3)
        
        with nav_col1:
            if st.button("📝 Generate Article", type="primary"):
                st.session_state.current_page = "generate"
                st.rerun()
        
        with nav_col2:
            if st.button("⚙️ Configure SEO", type="secondary"):
                st.session_state.current_page = "seo_settings"
                st.rerun()
        
        with nav_col3:
            if st.button("🎨 Customize Style", type="secondary"):
                st.session_state.current_page = "style_settings"
                st.rerun()

def generate_srt_format(segments: List[Dict]) -> str:
    """Generate SRT subtitle format from transcript segments"""
    if not segments:
        return ""
    
    srt_content = []
    
    for i, segment in enumerate(segments, 1):
        start_time = segment.get('start', 0)
        duration = segment.get('duration', 0)
        end_time = start_time + duration
        
        # Format time as SRT requires (HH:MM:SS,mmm)
        start_srt = format_srt_time(start_time)
        end_srt = format_srt_time(end_time)
        
        text = segment.get('text', '').strip()
        
        srt_content.append(f"{i}")
        srt_content.append(f"{start_srt} --> {end_srt}")
        srt_content.append(text)
        srt_content.append("")  # Empty line between entries
    
    return '\n'.join(srt_content)

def format_srt_time(seconds: float) -> str:
    """Format seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def render_audio_tips_and_best_practices():
    """Render tips and best practices for audio processing"""
    st.markdown("#### 💡 Audio Processing Tips")
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.markdown("**📱 Recording Quality Tips:**")
        st.info("""
        • Use a quiet environment
        • Speak clearly and at normal pace
        • Use a good quality microphone
        • Avoid background music
        • Keep consistent volume levels
        • Record in shorter segments for easier processing
        """)
        
        st.markdown("**🎯 Best Audio Types:**")
        st.success("""
        • Lectures and presentations
        • Interviews and podcasts
        • Training sessions
        • Webinars and meetings
        • Educational content
        • Clear, single-speaker recordings
        """)
    
    with tips_col2:
        st.markdown("**⚠️ Common Issues:**")
        st.warning("""
        • Background noise affects accuracy
        • Multiple speakers talking simultaneously
        • Poor audio quality reduces confidence
        • Very fast speech may be missed
        • Heavy accents may need manual review
        • Music or sound effects interfere
        """)
        
        st.markdown("**🔧 Troubleshooting:**")
        st.error("""
        • If accuracy is low, try manual review
        • Use noise reduction for noisy audio
        • Break long files into smaller segments
        • Consider re-recording if quality is poor
        • Use speaker identification for multi-speaker content
        """)

# Main audio processing interface
def render_complete_audio_processor():
    """Render complete audio processing interface"""
    st.markdown("## 🎧 Audio Processing & Transcription")
    st.markdown("Transform audio recordings into structured content for article generation.")
    
    # Main processing interface
    render_audio_processing_interface()
    
    # Tips and best practices
    st.markdown("---")
    render_audio_tips_and_best_practices()
    
    # Service setup information
    with st.expander("🔧 Service Setup & API Configuration"):
        st.markdown("""
        ### OpenAI Whisper API Setup
        
        To use the Whisper API for transcription:
        
        1. **Get OpenAI API Key**
           - Visit: https://platform.openai.com/api-keys
           - Create an account or log in
           - Generate a new API key
        
        2. **Configure API Key**
           - Add your API key to the application settings
           - Test the connection with a small audio file
        
        3. **Understanding Costs**
           - Whisper API charges per minute of audio
           - Current rate: $0.006 per minute
           - High accuracy with fast processing
        
        ### Local Whisper Setup
        
        For privacy and cost savings, install Whisper locally:
        
        ```bash
        pip install openai-whisper
        # For GPU acceleration (optional)
        pip install torch torchvision torchaudio
        ```
        
        **Note:** Local processing is slower but more private and cost-effective for large volumes.
        """)
