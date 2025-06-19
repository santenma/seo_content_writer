import streamlit as st
import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import difflib

class ContentEditor:
    """Advanced content editing and refinement system"""
    
    def __init__(self):
        self.editing_history = []
        self.suggestions_cache = {}
        self.auto_save_enabled = True
        
    def initialize_editor_session(self, content_data: Dict):
        """Initialize editing session with content data"""
        if 'editor_session' not in st.session_state:
            st.session_state.editor_session = {
                'original_content': content_data.copy(),
                'current_content': content_data.copy(),
                'editing_history': [],
                'undo_stack': [],
                'redo_stack': [],
                'auto_save_timer': None,
                'has_unsaved_changes': False,
                'active_section': None,
                'suggestions': {},
                'real_time_feedback': True
            }
        
        return st.session_state.editor_session
    
    def save_content_state(self, session: Dict, description: str = "Manual save"):
        """Save current content state to history"""
        timestamp = datetime.now().isoformat()
        state_snapshot = {
            'content': session['current_content'].copy(),
            'timestamp': timestamp,
            'description': description,
            'user': st.session_state.get('username', 'anonymous')
        }
        
        # Add to undo stack
        session['undo_stack'].append(state_snapshot)
        
        # Clear redo stack when new action is performed
        session['redo_stack'] = []
        
        # Limit undo stack size
        if len(session['undo_stack']) > 50:
            session['undo_stack'] = session['undo_stack'][-50:]
        
        session['has_unsaved_changes'] = True
    
    def undo_last_change(self, session: Dict) -> bool:
        """Undo the last change"""
        if session['undo_stack']:
            # Save current state to redo stack
            current_state = {
                'content': session['current_content'].copy(),
                'timestamp': datetime.now().isoformat(),
                'description': "Before undo",
                'user': st.session_state.get('username', 'anonymous')
            }
            session['redo_stack'].append(current_state)
            
            # Restore previous state
            previous_state = session['undo_stack'].pop()
            session['current_content'] = previous_state['content'].copy()
            
            return True
        return False
    
    def redo_last_change(self, session: Dict) -> bool:
        """Redo the last undone change"""
        if session['redo_stack']:
            # Save current state to undo stack
            current_state = {
                'content': session['current_content'].copy(),
                'timestamp': datetime.now().isoformat(),
                'description': "Before redo",
                'user': st.session_state.get('username', 'anonymous')
            }
            session['undo_stack'].append(current_state)
            
            # Restore redo state
            redo_state = session['redo_stack'].pop()
            session['current_content'] = redo_state['content'].copy()
            
            return True
        return False
    
    def analyze_content_structure(self, content: str) -> Dict:
        """Analyze content structure and provide insights"""
        
        # Basic metrics
        words = content.split()
        sentences = re.split(r'[.!?]+', content)
        paragraphs = content.split('\n\n')
        
        # Heading analysis
        headings = {
            'h1': len(re.findall(r'^# ', content, re.MULTILINE)),
            'h2': len(re.findall(r'^## ', content, re.MULTILINE)),
            'h3': len(re.findall(r'^### ', content, re.MULTILINE)),
            'h4': len(re.findall(r'^#### ', content, re.MULTILINE))
        }
        
        # Readability metrics
        avg_sentence_length = len(words) / max(len([s for s in sentences if s.strip()]), 1)
        avg_paragraph_length = len(words) / max(len([p for p in paragraphs if p.strip()]), 1)
        
        # Content features
        has_bullet_points = '•' in content or '*' in content or '-' in content
        has_numbered_lists = bool(re.search(r'\d+\.', content))
        has_bold_text = '**' in content
        has_italic_text = '*' in content and not has_bold_text
        
        return {
            'word_count': len(words),
            'sentence_count': len([s for s in sentences if s.strip()]),
            'paragraph_count': len([p for p in paragraphs if p.strip()]),
            'avg_sentence_length': round(avg_sentence_length, 1),
            'avg_paragraph_length': round(avg_paragraph_length, 1),
            'headings': headings,
            'features': {
                'bullet_points': has_bullet_points,
                'numbered_lists': has_numbered_lists,
                'bold_text': has_bold_text,
                'italic_text': has_italic_text
            }
        }
    
    def generate_improvement_suggestions(self, content: str, seo_settings: Dict) -> List[Dict]:
        """Generate improvement suggestions based on content analysis"""
        suggestions = []
        
        analysis = self.analyze_content_structure(content)
        primary_keyword = seo_settings.get('primary_keyword', '')
        
        # Word count suggestions
        target_length = seo_settings.get('content_length', 800)
        current_length = analysis['word_count']
        
        if current_length < target_length * 0.8:
            suggestions.append({
                'type': 'length',
                'priority': 'high',
                'title': 'Content too short',
                'description': f'Current: {current_length} words, Target: {target_length} words',
                'suggestion': 'Consider adding more detailed explanations, examples, or additional sections.',
                'action': 'expand_content'
            })
        elif current_length > target_length * 1.3:
            suggestions.append({
                'type': 'length',
                'priority': 'medium',
                'title': 'Content might be too long',
                'description': f'Current: {current_length} words, Target: {target_length} words',
                'suggestion': 'Consider breaking into multiple articles or removing less relevant sections.',
                'action': 'trim_content'
            })
        
        # Heading structure suggestions
        if analysis['headings']['h2'] < 3:
            suggestions.append({
                'type': 'structure',
                'priority': 'high',
                'title': 'Add more H2 headings',
                'description': f'Current: {analysis["headings"]["h2"]} H2 headings',
                'suggestion': 'Break content into 3-5 main sections with H2 headings for better SEO.',
                'action': 'add_headings'
            })
        
        # Keyword density suggestions
        if primary_keyword:
            keyword_count = content.lower().count(primary_keyword.lower())
            keyword_density = (keyword_count / analysis['word_count']) * 100 if analysis['word_count'] > 0 else 0
            
            if keyword_density < 1.0:
                suggestions.append({
                    'type': 'seo',
                    'priority': 'high',
                    'title': 'Low keyword density',
                    'description': f'"{primary_keyword}" appears {keyword_count} times ({keyword_density:.1f}%)',
                    'suggestion': 'Include the primary keyword more naturally throughout the content.',
                    'action': 'increase_keyword_density'
                })
            elif keyword_density > 3.0:
                suggestions.append({
                    'type': 'seo',
                    'priority': 'medium',
                    'title': 'High keyword density',
                    'description': f'"{primary_keyword}" appears {keyword_count} times ({keyword_density:.1f}%)',
                    'suggestion': 'Reduce keyword usage to avoid over-optimization.',
                    'action': 'decrease_keyword_density'
                })
        
        # Readability suggestions
        if analysis['avg_sentence_length'] > 25:
            suggestions.append({
                'type': 'readability',
                'priority': 'medium',
                'title': 'Sentences too long',
                'description': f'Average: {analysis["avg_sentence_length"]} words per sentence',
                'suggestion': 'Break long sentences into shorter ones for better readability.',
                'action': 'shorten_sentences'
            })
        
        # Content features suggestions
        if not analysis['features']['bullet_points'] and analysis['word_count'] > 400:
            suggestions.append({
                'type': 'formatting',
                'priority': 'low',
                'title': 'Add bullet points',
                'description': 'No bullet points found',
                'suggestion': 'Use bullet points to break up text and improve scannability.',
                'action': 'add_bullet_points'
            })
        
        return suggestions
    
    def apply_quick_fix(self, content: str, action: str, **kwargs) -> str:
        """Apply quick fixes to content based on suggestion actions"""
        
        if action == 'add_headings':
            # Auto-suggest heading placements
            paragraphs = content.split('\n\n')
            if len(paragraphs) > 3:
                # Add H2 headings before major sections
                modified_content = paragraphs[0] + '\n\n'
                
                for i, paragraph in enumerate(paragraphs[1:], 1):
                    if i % 2 == 1 and len(paragraph.split()) > 30:
                        # Add a sample H2 heading
                        heading = f"## Key Point {(i//2)+1}\n\n"
                        modified_content += heading + paragraph + '\n\n'
                    else:
                        modified_content += paragraph + '\n\n'
                
                return modified_content.strip()
        
        elif action == 'add_bullet_points':
            # Convert some paragraphs to bullet points
            lines = content.split('\n')
            modified_lines = []
            
            for line in lines:
                # Look for sentences that could be bullet points
                if (len(line.split()) > 5 and len(line.split()) < 20 and 
                    not line.strip().startswith('#') and line.strip().endswith('.')):
                    modified_lines.append(f"• {line.strip()}")
                else:
                    modified_lines.append(line)
            
            return '\n'.join(modified_lines)
        
        elif action == 'shorten_sentences':
            # Break long sentences at conjunctions
            sentences = re.split(r'([.!?])', content)
            modified_sentences = []
            
            for i in range(0, len(sentences)-1, 2):
                sentence = sentences[i]
                punctuation = sentences[i+1] if i+1 < len(sentences) else ''
                
                if len(sentence.split()) > 25:
                    # Try to split at 'and', 'but', 'however', etc.
                    conjunctions = [' and ', ' but ', ' however ', ' moreover ', ' furthermore ']
                    for conj in conjunctions:
                        if conj in sentence:
                            parts = sentence.split(conj, 1)
                            if len(parts) == 2 and len(parts[0].split()) > 8:
                                sentence = parts[0].strip() + punctuation + ' ' + parts[1].strip()
                                break
                
                modified_sentences.append(sentence + punctuation)
            
            return ''.join(modified_sentences)
        
        return content  # Return original if no action matches

def render_output_editor_interface():
    """Render the comprehensive output editing interface"""
    st.markdown("## ✏️ Content Editor")
    st.markdown("Edit, refine, and perfect your generated content with advanced editing tools.")
    
    # Check if we have content to edit
    if 'generated_article' not in st.session_state or not st.session_state.generated_article:
        st.warning("⚠️ No generated content found. Please generate an article first.")
        
        if st.button("🚀 Go to Content Generation", type="primary"):
            st.session_state.current_page = "generate"
            st.rerun()
        return
    
    # Initialize editor
    editor = ContentEditor()
    session = editor.initialize_editor_session(st.session_state.generated_article)
    
    # Editor toolbar
    render_editor_toolbar(editor, session)
    
    # Main editing interface
    tab1, tab2, tab3, tab4 = st.tabs([
        "✏️ Visual Editor", "📝 Raw Editor", "💡 Suggestions", "📊 Analytics"
    ])
    
    with tab1:
        render_visual_editor(editor, session)
    
    with tab2:
        render_raw_editor(editor, session)
    
    with tab3:
        render_suggestions_panel(editor, session)
    
    with tab4:
        render_content_analytics(editor, session)
    
    # Save changes back to generated_article
    st.session_state.generated_article = session['current_content'].copy()

def render_editor_toolbar(editor: ContentEditor, session: Dict):
    """Render the editor toolbar with actions"""
    st.markdown("### 🛠️ Editor Toolbar")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("↶ Undo", disabled=not session['undo_stack']):
            if editor.undo_last_change(session):
                st.success("✅ Change undone")
                st.rerun()
    
    with col2:
        if st.button("↷ Redo", disabled=not session['redo_stack']):
            if editor.redo_last_change(session):
                st.success("✅ Change restored")
                st.rerun()
    
    with col3:
        if st.button("💾 Save"):
            editor.save_content_state(session, "Manual save")
            session['has_unsaved_changes'] = False
            st.success("✅ Content saved")
    
    with col4:
        if st.button("🔄 Reset"):
            if st.button("⚠️ Confirm Reset", key="confirm_reset_editor"):
                session['current_content'] = session['original_content'].copy()
                session['has_unsaved_changes'] = True
                st.success("✅ Content reset to original")
                st.rerun()
    
    with col5:
        if st.button("📤 Export"):
            st.session_state.show_export_modal = True
    
    with col6:
        real_time_feedback = st.checkbox(
            "Real-time feedback",
            value=session.get('real_time_feedback', True),
            key="real_time_feedback_toggle"
        )
        session['real_time_feedback'] = real_time_feedback
    
    # Status indicators
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        if session['has_unsaved_changes']:
            st.warning("⚠️ Unsaved changes")
        else:
            st.success("✅ All changes saved")
    
    with status_col2:
        undo_count = len(session['undo_stack'])
        st.info(f"📚 {undo_count} actions in history")
    
    with status_col3:
        word_count = len(session['current_content'].get('content', '').split())
        st.info(f"📝 {word_count} words")

def render_visual_editor(editor: ContentEditor, session: Dict):
    """Render visual WYSIWYG-style editor"""
    st.markdown("### ✏️ Visual Content Editor")
    st.markdown("Edit your content with rich formatting and real-time preview.")
    
    current_content = session['current_content']
    
    # Section-based editing
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📝 Content Sections")
        
        # Title editing
        st.markdown("**Article Title:**")
        new_title = st.text_input(
            "Title",
            value=current_content.get('title', ''),
            key="visual_title_edit",
            label_visibility="collapsed"
        )
        
        if new_title != current_content.get('title', ''):
            editor.save_content_state(session, "Title change")
            current_content['title'] = new_title
            session['has_unsaved_changes'] = True
        
        # Meta description editing
        st.markdown("**Meta Description:**")
        new_meta = st.text_area(
            "Meta Description",
            value=current_content.get('meta_description', ''),
            height=80,
            key="visual_meta_edit",
            label_visibility="collapsed",
            help="Keep under 160 characters for optimal SEO"
        )
        
        if new_meta != current_content.get('meta_description', ''):
            current_content['meta_description'] = new_meta
            session['has_unsaved_changes'] = True
        
        # Content editing with sections
        st.markdown("**Article Content:**")
        
        # Split content into sections for easier editing
        content_text = current_content.get('content', '')
        sections = split_content_into_sections(content_text)
        
        edited_sections = []
        
        for i, section in enumerate(sections):
            with st.expander(f"Section {i+1}: {section['title'][:50]}..." if section['title'] else f"Section {i+1}"):
                
                if section['title']:
                    new_section_title = st.text_input(
                        "Section Title:",
                        value=section['title'],
                        key=f"section_title_{i}"
                    )
                    section['title'] = new_section_title
                
                new_section_content = st.text_area(
                    "Section Content:",
                    value=section['content'],
                    height=200,
                    key=f"section_content_{i}"
                )
                section['content'] = new_section_content
                
                # Quick formatting buttons
                format_col1, format_col2, format_col3 = st.columns(3)
                
                with format_col1:
                    if st.button(f"🔸 Add Bullet Points", key=f"bullets_{i}"):
                        section['content'] = add_bullet_points_to_text(section['content'])
                
                with format_col2:
                    if st.button(f"🔢 Add Numbers", key=f"numbers_{i}"):
                        section['content'] = add_numbered_list_to_text(section['content'])
                
                with format_col3:
                    if st.button(f"**B** Bold Key Terms", key=f"bold_{i}"):
                        primary_keyword = st.session_state.seo_settings.get('primary_keyword', '')
                        if primary_keyword:
                            section['content'] = section['content'].replace(
                                primary_keyword, f"**{primary_keyword}**"
                            )
            
            edited_sections.append(section)
        
        # Reconstruct content from sections
        new_content = reconstruct_content_from_sections(edited_sections)
        
        if new_content != content_text:
            editor.save_content_state(session, "Content section edit")
            current_content['content'] = new_content
            session['has_unsaved_changes'] = True
    
    with col2:
        st.markdown("#### 👁️ Live Preview")
        
        # Live preview of the content
        preview_container = st.container()
        
        with preview_container:
            st.markdown("---")
            
            # Preview title
            if current_content.get('title'):
                st.markdown(f"# {current_content['title']}")
            
            # Preview meta description
            if current_content.get('meta_description'):
                st.info(f"📝 {current_content['meta_description']}")
            
            # Preview content (first 500 characters)
            preview_content = current_content.get('content', '')
            if len(preview_content) > 500:
                preview_content = preview_content[:500] + "..."
            
            st.markdown(preview_content)
            
            st.markdown("---")
        
        # Quick stats
        st.markdown("#### 📊 Quick Stats")
        
        content_stats = editor.analyze_content_structure(current_content.get('content', ''))
        
        st.metric("Words", content_stats['word_count'])
        st.metric("Sentences", content_stats['sentence_count'])
        st.metric("Paragraphs", content_stats['paragraph_count'])
        st.metric("H2 Headings", content_stats['headings']['h2'])
        
        # Real-time suggestions
        if session.get('real_time_feedback', True):
            st.markdown("#### 💡 Quick Suggestions")
            
            suggestions = editor.generate_improvement_suggestions(
                current_content.get('content', ''), 
                st.session_state.seo_settings
            )
            
            for suggestion in suggestions[:3]:
                priority_color = {
                    'high': '🔴',
                    'medium': '🟡', 
                    'low': '🟢'
                }.get(suggestion['priority'], '⚪')
                
                st.warning(f"{priority_color} {suggestion['title']}")
                
                if st.button(f"Fix: {suggestion['action']}", key=f"quick_fix_{suggestion['action']}"):
                    fixed_content = editor.apply_quick_fix(
                        current_content.get('content', ''),
                        suggestion['action']
                    )
                    editor.save_content_state(session, f"Quick fix: {suggestion['action']}")
                    current_content['content'] = fixed_content
                    session['has_unsaved_changes'] = True
                    st.rerun()

def render_raw_editor(editor: ContentEditor, session: Dict):
    """Render raw text editor with markdown support"""
    st.markdown("### 📝 Raw Text Editor")
    st.markdown("Edit the content directly with markdown formatting support.")
    
    current_content = session['current_content']
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Raw content editing
        st.markdown("#### ✏️ Edit Content")
        
        # Title
        new_title = st.text_input(
            "Article Title:",
            value=current_content.get('title', ''),
            key="raw_title_edit"
        )
        
        # Meta description
        new_meta = st.text_area(
            "Meta Description:",
            value=current_content.get('meta_description', ''),
            height=80,
            key="raw_meta_edit"
        )
        
        # Main content with markdown support
        content_text = current_content.get('content', '')
        
        new_content = st.text_area(
            "Content (Markdown supported):",
            value=content_text,
            height=600,
            key="raw_content_edit",
            help="Use markdown formatting: ## for H2, ### for H3, **bold**, *italic*, • for bullets"
        )
        
        # Detect changes
        if (new_title != current_content.get('title', '') or 
            new_meta != current_content.get('meta_description', '') or 
            new_content != content_text):
            
            # Auto-save functionality
            if st.button("💾 Save Changes", type="primary"):
                editor.save_content_state(session, "Raw editor changes")
                current_content.update({
                    'title': new_title,
                    'meta_description': new_meta,
                    'content': new_content
                })
                session['has_unsaved_changes'] = False
                st.success("✅ Changes saved!")
                st.rerun()
            
            st.warning("⚠️ You have unsaved changes")
    
    with col2:
        st.markdown("#### 🛠️ Formatting Tools")
        
        # Markdown cheat sheet
        with st.expander("📋 Markdown Guide"):
            st.markdown("""
            **Headers:**
            - `## H2 Heading`
            - `### H3 Heading`
            
            **Text Formatting:**
            - `**bold text**`
            - `*italic text*`
            
            **Lists:**
            - `• Bullet point`
            - `1. Numbered item`
            
            **Links:**
            - `[link text](URL)`
            """)
        
        # Quick insert buttons
        st.markdown("#### ⚡ Quick Insert")
        
        if st.button("➕ Add H2 Section"):
            section_name = st.text_input("Section name:", key="h2_name")
            if section_name:
                insert_text = f"\n\n## {section_name}\n\n[Add your content here]\n\n"
                # This would need to be integrated with the text area
                st.info(f"Insert: `{insert_text.strip()}`")
        
        if st.button("🔸 Add Bullet List"):
            st.info("Insert: `• Point 1\\n• Point 2\\n• Point 3`")
        
        if st.button("🔢 Add Numbered List"):
            st.info("Insert: `1. First item\\n2. Second item\\n3. Third item`")
        
        # Content statistics
        st.markdown("#### 📊 Content Stats")
        
        stats = editor.analyze_content_structure(new_content)
        
        st.metric("Words", stats['word_count'])
        st.metric("Characters", len(new_content))
        st.metric("Lines", new_content.count('\n') + 1)
        st.metric("H2 Headings", stats['headings']['h2'])
        st.metric("H3 Headings", stats['headings']['h3'])

def render_suggestions_panel(editor: ContentEditor, session: Dict):
    """Render AI-powered suggestions and improvements panel"""
    st.markdown("### 💡 Content Improvement Suggestions")
    st.markdown("Get AI-powered suggestions to enhance your content quality and SEO performance.")
    
    current_content = session['current_content']
    content_text = current_content.get('content', '')
    
    if not content_text:
        st.info("ℹ️ No content to analyze. Add some content first.")
        return
    
    # Generate suggestions
    suggestions = editor.generate_improvement_suggestions(
        content_text, 
        st.session_state.seo_settings
    )
    
    if not suggestions:
        st.success("🎉 Great job! No major improvements needed.")
        return
    
    # Group suggestions by type
    suggestion_groups = {}
    for suggestion in suggestions:
        group = suggestion['type']
        if group not in suggestion_groups:
            suggestion_groups[group] = []
        suggestion_groups[group].append(suggestion)
    
    # Display suggestions by category
    for group_name, group_suggestions in suggestion_groups.items():
        
        group_icons = {
            'seo': '🎯',
            'readability': '📖',
            'structure': '🏗️',
            'length': '📏',
            'formatting': '🎨'
        }
        
        icon = group_icons.get(group_name, '💡')
        
        with st.expander(f"{icon} {group_name.title()} Suggestions ({len(group_suggestions)})"):
            
            for i, suggestion in enumerate(group_suggestions):
                
                priority_colors = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }
                
                priority_icon = priority_colors.get(suggestion['priority'], '⚪')
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{priority_icon} {suggestion['title']}**")
                    st.markdown(suggestion['description'])
                    st.info(f"💡 {suggestion['suggestion']}")
                
                with col2:
                    if st.button(f"🔧 Apply Fix", key=f"apply_suggestion_{group_name}_{i}"):
                        
                        fixed_content = editor.apply_quick_fix(
                            content_text,
                            suggestion['action']
                        )
                        
                        if fixed_content != content_text:
                            editor.save_content_state(session, f"Applied suggestion: {suggestion['title']}")
                            current_content['content'] = fixed_content
                            session['has_unsaved_changes'] = True
                            st.success(f"✅ Applied: {suggestion['title']}")
                            st.rerun()
                        else:
                            st.warning("⚠️ No changes could be applied automatically")
                
                st.markdown("---")
    
    # Custom suggestion input
    st.markdown("#### 🗣️ Request Custom Improvement")
    
    custom_request = st.text_area(
        "Describe what you'd like to improve:",
        placeholder="e.g., 'Make the introduction more engaging' or 'Add more examples to section 2'",
        key="custom_suggestion_request"
    )
    
    if custom_request and st.button("🚀 Generate Custom Suggestion"):
        st.info("🚧 Custom AI suggestions will be implemented with AI model integration")

def render_content_analytics(editor: ContentEditor, session: Dict):
    """Render detailed content analytics and insights"""
    st.markdown("### 📊 Content Analytics & Insights")
    st.markdown("Detailed analysis of your content performance and optimization opportunities.")
    
    current_content = session['current_content']
    content_text = current_content.get('content', '')
    
    if not content_text:
        st.info("ℹ️ No content to analyze.")
        return
    
    # Perform comprehensive analysis
    analysis = editor.analyze_content_structure(content_text)
    seo_settings = st.session_state.seo_settings
    
    # Content Overview
    st.markdown("#### 📋 Content Overview")
    
    overview_col1, overview_col2, overview_col3, overview_col4 = st.columns(4)
    
    with overview_col1:
        st.metric(
            "Word Count",
            analysis['word_count'],
            delta=analysis['word_count'] - seo_settings.get('content_length', 800)
        )
    
    with overview_col2:
        reading_time = max(1, round(analysis['word_count'] / 225))
        st.metric(
            "Reading Time",
            f"{reading_time} min",
            delta=None
        )
    
    with overview_col3:
        st.metric(
            "Sentences",
            analysis['sentence_count'],
            delta=None
        )
    
    with overview_col4:
        st.metric(
            "Avg Sentence Length",
            f"{analysis['avg_sentence_length']} words",
            delta=None
        )
    
    # SEO Analysis
    st.markdown("#### 🎯 SEO Analysis")
    
    seo_col1, seo_col2 = st.columns(2)
    
    with seo_col1:
        # Keyword analysis
        primary_keyword = seo_settings.get('primary_keyword', '')
        
        if primary_keyword:
            keyword_count = content_text.lower().count(primary_keyword.lower())
            keyword_density = (keyword_count / analysis['word_count']) * 100 if analysis['word_count'] > 0 else 0
            
            st.markdown("**Primary Keyword Analysis:**")
            st.metric(f'"{primary_keyword}" Occurrences', keyword_count)
            st.metric("Keyword Density", f"{keyword_density:.1f}%")
            
            # Keyword density feedback
            if 1.0 <= keyword_density <= 2.5:
                st.success("✅ Optimal keyword density")
            elif keyword_density < 1.0:
                st.warning("⚠️ Keyword density too low")
            else:
                st.error("❌ Keyword density too high")
            
            # Keyword distribution
            st.markdown("**Keyword Distribution:**")
            
            # Check keyword in title
            title_has_keyword = primary_keyword.lower() in current_content.get('title', '').lower()
            st.markdown(f"{'✅' if title_has_keyword else '❌'} In title")
            
            # Check keyword in headings
            headings_text = ' '.join(re.findall(r'^#{1,6} (.+)', content_text, re.MULTILINE))
            headings_have_keyword = primary_keyword.lower() in headings_text.lower()
            st.markdown(f"{'✅' if headings_have_keyword else '❌'} In headings")
            
            # Check keyword in meta description
            meta_has_keyword = primary_keyword.lower() in current_content.get('meta_description', '').lower()
            st.markdown(f"{'✅' if meta_has_keyword else '❌'} In meta description")
        
        else:
            st.warning("⚠️ No primary keyword set for analysis")
    
    with seo_col2:
        # Content structure analysis
        st.markdown("**Content Structure:**")
        
        for heading_level, count in analysis['headings'].items():
            if count > 0:
                st.metric(f"{heading_level.upper()} Headings", count)
        
        # Structure recommendations
        st.markdown("**Structure Quality:**")
        
        h2_count = analysis['headings']['h2']
        if h2_count >= 3:
            st.success(f"✅ Good H2 structure ({h2_count} headings)")
        else:
            st.warning(f"⚠️ Add more H2 headings (current: {h2_count})")
        
        # Content features
        st.markdown("**Content Features:**")
        features = analysis['features']
        
        st.markdown(f"{'✅' if features['bullet_points'] else '❌'} Bullet points")
        st.markdown(f"{'✅' if features['numbered_lists'] else '❌'} Numbered lists")
        st.markdown(f"{'✅' if features['bold_text'] else '❌'} Bold text")
    
    # Readability Analysis
    st.markdown("#### 📖 Readability Analysis")
    
    readability_col1, readability_col2, readability_col3 = st.columns(3)
    
    with readability_col1:
        st.markdown("**Sentence Analysis:**")
        
        avg_length = analysis['avg_sentence_length']
        st.metric("Avg Sentence Length", f"{avg_length} words")
        
        if avg_length <= 15:
            st.success("✅ Easy to read")
        elif avg_length <= 20:
            st.info("ℹ️ Moderately easy")
        elif avg_length <= 25:
            st.warning("⚠️ Moderately difficult")
        else:
            st.error("❌ Difficult to read")
    
    with readability_col2:
        st.markdown("**Paragraph Analysis:**")
        
        avg_para_length = analysis['avg_paragraph_length']
        st.metric("Avg Paragraph Length", f"{avg_para_length} words")
        
        if avg_para_length <= 100:
            st.success("✅ Good paragraph length")
        elif avg_para_length <= 150:
            st.warning("⚠️ Consider shorter paragraphs")
        else:
            st.error("❌ Paragraphs too long")
    
    with readability_col3:
        st.markdown("**Complexity Score:**")
        
        # Simple complexity calculation
        complexity_score = calculate_content_complexity(content_text, analysis)
        st.metric("Complexity", f"{complexity_score}/10")
        
        if complexity_score <= 3:
            st.success("✅ Very easy to read")
        elif complexity_score <= 6:
            st.info("ℹ️ Moderately easy")
        elif complexity_score <= 8:
            st.warning("⚠️ Moderately difficult")
        else:
            st.error("❌ Very difficult")
    
    # Editing History
    st.markdown("#### 📚 Editing History")
    
    if session['undo_stack']:
        st.markdown("**Recent Changes:**")
        
        # Show last 5 changes
        recent_changes = session['undo_stack'][-5:]
        
        for i, change in enumerate(reversed(recent_changes)):
            timestamp = datetime.fromisoformat(change['timestamp'])
            time_str = timestamp.strftime("%H:%M:%S")
            
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"**{change['description']}**")
            
            with col2:
                st.markdown(f"🕐 {time_str}")
            
            with col3:
                if st.button(f"↶", key=f"revert_{i}", help="Revert to this state"):
                    # Revert to this specific state
                    session['current_content'] = change['content'].copy()
                    session['has_unsaved_changes'] = True
                    st.success("✅ Reverted to previous state")
                    st.rerun()
    else:
        st.info("ℹ️ No editing history available")
    
    # Content Comparison
    if session['original_content'] != session['current_content']:
        st.markdown("#### 🔄 Content Comparison")
        
        with st.expander("📊 Show Changes from Original"):
            original_text = session['original_content'].get('content', '')
            current_text = session['current_content'].get('content', '')
            
            # Show basic statistics comparison
            original_stats = editor.analyze_content_structure(original_text)
            current_stats = editor.analyze_content_structure(current_text)
            
            comp_col1, comp_col2, comp_col3 = st.columns(3)
            
            with comp_col1:
                st.markdown("**Original:**")
                st.markdown(f"Words: {original_stats['word_count']}")
                st.markdown(f"Sentences: {original_stats['sentence_count']}")
                st.markdown(f"H2 Headings: {original_stats['headings']['h2']}")
            
            with comp_col2:
                st.markdown("**Current:**")
                st.markdown(f"Words: {current_stats['word_count']}")
                st.markdown(f"Sentences: {current_stats['sentence_count']}")
                st.markdown(f"H2 Headings: {current_stats['headings']['h2']}")
            
            with comp_col3:
                st.markdown("**Changes:**")
                word_diff = current_stats['word_count'] - original_stats['word_count']
                sent_diff = current_stats['sentence_count'] - original_stats['sentence_count']
                h2_diff = current_stats['headings']['h2'] - original_stats['headings']['h2']
                
                st.markdown(f"Words: {word_diff:+d}")
                st.markdown(f"Sentences: {sent_diff:+d}")
                st.markdown(f"H2 Headings: {h2_diff:+d}")

def split_content_into_sections(content: str) -> List[Dict]:
    """Split content into editable sections based on headings"""
    sections = []
    
    # Split by H2 headings
    parts = re.split(r'\n## ', content)
    
    # First part (before first H2)
    if parts[0].strip():
        sections.append({
            'title': '',
            'content': parts[0].strip()
        })
    
    # Subsequent parts (each starts with H2)
    for part in parts[1:]:
        lines = part.split('\n', 1)
        title = lines[0] if lines else ''
        content_part = lines[1] if len(lines) > 1 else ''
        
        sections.append({
            'title': title,
            'content': content_part.strip()
        })
    
    return sections

def reconstruct_content_from_sections(sections: List[Dict]) -> str:
    """Reconstruct content from edited sections"""
    content_parts = []
    
    for section in sections:
        if section['title']:
            content_parts.append(f"## {section['title']}")
        
        if section['content']:
            content_parts.append(section['content'])
    
    return '\n\n'.join(content_parts)

def add_bullet_points_to_text(text: str) -> str:
    """Convert suitable sentences to bullet points"""
    lines = text.split('\n')
    converted_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        # Convert sentences that look like list items
        if (len(stripped.split()) > 3 and len(stripped.split()) < 20 and 
            stripped.endswith('.') and not stripped.startswith('•') and
            not stripped.startswith('#')):
            
            # Check if it starts with a number or action word
            first_words = ['first', 'second', 'third', 'next', 'then', 'also', 'additionally']
            if any(stripped.lower().startswith(word) for word in first_words):
                converted_lines.append(f"• {stripped}")
            else:
                converted_lines.append(line)
        else:
            converted_lines.append(line)
    
    return '\n'.join(converted_lines)

def add_numbered_list_to_text(text: str) -> str:
    """Convert suitable sentences to numbered list"""
    lines = text.split('\n')
    converted_lines = []
    list_counter = 1
    
    for line in lines:
        stripped = line.strip()
        
        # Convert sentences that look like sequential steps
        step_indicators = ['first', 'second', 'third', 'then', 'next', 'finally']
        if (len(stripped.split()) > 3 and 
            any(stripped.lower().startswith(indicator) for indicator in step_indicators) and
            not stripped.startswith(('1.', '2.', '3.'))):
            
            # Remove the step indicator and add number
            for indicator in step_indicators:
                if stripped.lower().startswith(indicator):
                    remaining_text = stripped[len(indicator):].lstrip(' ,')
                    converted_lines.append(f"{list_counter}. {remaining_text}")
                    list_counter += 1
                    break
        else:
            converted_lines.append(line)
    
    return '\n'.join(converted_lines)

def calculate_content_complexity(content: str, analysis: Dict) -> int:
    """Calculate content complexity score (1-10)"""
    score = 5  # Start with medium complexity
    
    # Adjust based on sentence length
    avg_sentence_length = analysis['avg_sentence_length']
    if avg_sentence_length > 25:
        score += 2
    elif avg_sentence_length > 20:
        score += 1
    elif avg_sentence_length < 12:
        score -= 1
    elif avg_sentence_length < 8:
        score -= 2
    
    # Adjust based on vocabulary complexity
    complex_words = count_complex_words(content)
    total_words = analysis['word_count']
    complex_ratio = complex_words / max(total_words, 1)
    
    if complex_ratio > 0.15:
        score += 2
    elif complex_ratio > 0.10:
        score += 1
    elif complex_ratio < 0.05:
        score -= 1
    
    # Adjust based on paragraph length
    avg_para_length = analysis['avg_paragraph_length']
    if avg_para_length > 150:
        score += 1
    elif avg_para_length < 75:
        score -= 1
    
    return max(1, min(10, score))

def count_complex_words(content: str) -> int:
    """Count words with 3+ syllables (simplified)"""
    words = re.findall(r'\b[a-zA-Z]+\b', content.lower())
    complex_count = 0
    
    for word in words:
        # Simple syllable count (vowel groups)
        syllables = len(re.findall(r'[aeiouy]+', word))
        if syllables >= 3:
            complex_count += 1
    
    return complex_count

# Export functionality
def render_export_modal():
    """Render export modal when triggered"""
    if st.session_state.get('show_export_modal', False):
        
        with st.container():
            st.markdown("### 📤 Export Content")
            
            current_content = st.session_state.editor_session['current_content']
            
            export_col1, export_col2 = st.columns(2)
            
            with export_col1:
                st.markdown("#### 📄 Document Formats")
                
                # Markdown export
                markdown_content = create_markdown_export(current_content)
                st.download_button(
                    "📝 Download as Markdown",
                    data=markdown_content,
                    file_name=f"{current_content.get('title', 'article').replace(' ', '_').lower()}.md",
                    mime="text/markdown"
                )
                
                # HTML export
                html_content = create_html_export(current_content)
                st.download_button(
                    "🌐 Download as HTML",
                    data=html_content,
                    file_name=f"{current_content.get('title', 'article').replace(' ', '_').lower()}.html",
                    mime="text/html"
                )
                
                # Word document (simulated)
                if st.button("📄 Prepare for Word"):
                    st.info("Copy the markdown content and paste into Word, then use 'Insert > Object > Text from File' for formatting")
            
            with export_col2:
                st.markdown("#### 🔧 Technical Formats")
                
                # JSON export
                json_content = json.dumps(current_content, indent=2)
                st.download_button(
                    "📊 Download as JSON",
                    data=json_content,
                    file_name=f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
                # CSV export (for analytics)
                if st.button("📈 Export Analytics CSV"):
                    st.info("Analytics export feature coming soon")
            
            if st.button("❌ Close Export"):
                st.session_state.show_export_modal = False
                st.rerun()

def create_markdown_export(content: Dict) -> str:
    """Create markdown export of content"""
    markdown = f"# {content.get('title', 'Untitled')}\n\n"
    
    if content.get('meta_description'):
        markdown += f"**Meta Description:** {content['meta_description']}\n\n"
    
    markdown += content.get('content', '')
    
    # Add export metadata
    markdown += f"\n\n---\n*Exported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
    
    return markdown

def create_html_export(content: Dict) -> str:
    """Create HTML export of content"""
    title = content.get('title', 'Untitled')
    meta_desc = content.get('meta_description', '')
    content_text = content.get('content', '')
    
    # Convert markdown-like content to HTML
    html_content = content_text.replace('\n\n', '</p><p>')
    html_content = html_content.replace('## ', '<h2>').replace('\n', '</h2>\n<p>', 1)
    html_content = html_content.replace('### ', '<h3>').replace('\n', '</h3>\n<p>', 1)
    html_content = html_content.replace('**', '<strong>').replace('**', '</strong>')
    html_content = html_content.replace('*', '<em>').replace('*', '</em>')
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
    <meta charset="UTF-8">
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #333; }}
        p {{ margin-bottom: 1em; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <p><em>{meta_desc}</em></p>
    <p>{html_content}</p>
    <hr>
    <p><small>Exported on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</small></p>
</body>
</html>"""
    
    return html

# Main interface function
def render_complete_output_editor():
    """Render complete output editor interface"""
    render_output_editor_interface()
    
    # Handle export modal
    if st.session_state.get('show_export_modal', False):
        render_export_modal()
