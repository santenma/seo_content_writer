import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import random

class StyleCustomizationManager:
    """Advanced content style and voice customization system"""
    
    def __init__(self):
        self.style_profiles = self.load_style_profiles()
        self.tone_definitions = self.load_tone_definitions()
        self.voice_characteristics = self.load_voice_characteristics()
        self.writing_patterns = self.load_writing_patterns()
        
    def load_style_profiles(self) -> Dict:
        """Load predefined style profiles for different content types"""
        return {
            "professional_executive": {
                "name": "Professional Executive",
                "description": "Authoritative, data-driven content for C-suite audience",
                "tone": "authoritative",
                "voice": "expert",
                "formality": "formal",
                "vocabulary": "advanced",
                "sentence_structure": "complex",
                "perspective": "third_person",
                "characteristics": {
                    "uses_statistics": True,
                    "industry_jargon": True,
                    "call_to_action_style": "subtle",
                    "emotional_appeal": "logical",
                    "evidence_style": "data_heavy"
                }
            },
            "friendly_blogger": {
                "name": "Friendly Blogger",
                "description": "Casual, relatable content for general audience",
                "tone": "conversational",
                "voice": "friendly",
                "formality": "informal",
                "vocabulary": "simple",
                "sentence_structure": "simple",
                "perspective": "second_person",
                "characteristics": {
                    "uses_contractions": True,
                    "personal_anecdotes": True,
                    "call_to_action_style": "direct",
                    "emotional_appeal": "personal",
                    "evidence_style": "example_based"
                }
            },
            "technical_expert": {
                "name": "Technical Expert",
                "description": "Detailed, precise content for technical professionals",
                "tone": "technical",
                "voice": "expert",
                "formality": "formal",
                "vocabulary": "technical",
                "sentence_structure": "detailed",
                "perspective": "third_person",
                "characteristics": {
                    "step_by_step": True,
                    "technical_accuracy": True,
                    "call_to_action_style": "instructional",
                    "emotional_appeal": "practical",
                    "evidence_style": "method_based"
                }
            },
            "marketing_persuasive": {
                "name": "Marketing Persuasive",
                "description": "Compelling, action-oriented content for conversions",
                "tone": "persuasive",
                "voice": "confident",
                "formality": "semi_formal",
                "vocabulary": "powerful",
                "sentence_structure": "varied",
                "perspective": "second_person",
                "characteristics": {
                    "urgency_creation": True,
                    "benefit_focused": True,
                    "call_to_action_style": "strong",
                    "emotional_appeal": "aspirational",
                    "evidence_style": "benefit_proof"
                }
            },
            "educational_teacher": {
                "name": "Educational Teacher",
                "description": "Clear, instructive content for learning",
                "tone": "educational",
                "voice": "helpful",
                "formality": "semi_formal",
                "vocabulary": "clear",
                "sentence_structure": "structured",
                "perspective": "second_person",
                "characteristics": {
                    "learning_objectives": True,
                    "progressive_difficulty": True,
                    "call_to_action_style": "encouraging",
                    "emotional_appeal": "supportive",
                    "evidence_style": "example_rich"
                }
            },
            "creative_storyteller": {
                "name": "Creative Storyteller",
                "description": "Engaging, narrative-driven content",
                "tone": "creative",
                "voice": "engaging",
                "formality": "informal",
                "vocabulary": "descriptive",
                "sentence_structure": "varied",
                "perspective": "mixed",
                "characteristics": {
                    "storytelling": True,
                    "vivid_imagery": True,
                    "call_to_action_style": "inspiring",
                    "emotional_appeal": "emotional",
                    "evidence_style": "story_based"
                }
            }
        }
    
    def load_tone_definitions(self) -> Dict:
        """Load detailed tone definitions and characteristics"""
        return {
            "professional": {
                "description": "Formal, business-appropriate language",
                "characteristics": ["Clear", "Objective", "Respectful", "Structured"],
                "avoid": ["Slang", "Overly casual phrases", "Personal opinions"],
                "sentence_starters": [
                    "According to research,", "Industry analysis shows,", "Best practices indicate,"
                ],
                "vocabulary_level": "intermediate_to_advanced",
                "emotional_tone": "neutral_positive"
            },
            "conversational": {
                "description": "Friendly, approachable, like talking to a friend",
                "characteristics": ["Warm", "Relatable", "Personal", "Easy-going"],
                "avoid": ["Overly formal language", "Jargon", "Distant tone"],
                "sentence_starters": [
                    "You know,", "Here's the thing,", "Let me tell you,", "Have you ever,"
                ],
                "vocabulary_level": "simple_to_intermediate",
                "emotional_tone": "warm_friendly"
            },
            "authoritative": {
                "description": "Expert, confident, commanding respect",
                "characteristics": ["Confident", "Knowledgeable", "Decisive", "Credible"],
                "avoid": ["Uncertain language", "Hedge words", "Apologetic tone"],
                "sentence_starters": [
                    "The evidence clearly shows,", "Research confirms,", "It is essential to,"
                ],
                "vocabulary_level": "advanced",
                "emotional_tone": "confident_assured"
            },
            "friendly": {
                "description": "Warm, supportive, encouraging",
                "characteristics": ["Supportive", "Encouraging", "Positive", "Helpful"],
                "avoid": ["Criticism without solutions", "Negative language", "Intimidating terms"],
                "sentence_starters": [
                    "Don't worry,", "You're not alone,", "Here to help,", "Let's figure this out,"
                ],
                "vocabulary_level": "simple",
                "emotional_tone": "supportive_positive"
            },
            "technical": {
                "description": "Precise, detailed, focused on accuracy",
                "characteristics": ["Precise", "Detailed", "Accurate", "Methodical"],
                "avoid": ["Ambiguous terms", "Emotional language", "Generalizations"],
                "sentence_starters": [
                    "The process involves,", "Step 1 requires,", "Technical specifications show,"
                ],
                "vocabulary_level": "technical_advanced",
                "emotional_tone": "neutral_factual"
            },
            "persuasive": {
                "description": "Compelling, action-oriented, motivating",
                "characteristics": ["Compelling", "Motivating", "Action-focused", "Benefit-driven"],
                "avoid": ["Weak language", "Passive voice", "Uncertain claims"],
                "sentence_starters": [
                    "Imagine if,", "What if you could,", "Don't miss out on,", "Transform your,"
                ],
                "vocabulary_level": "powerful_engaging",
                "emotional_tone": "motivational_exciting"
            },
            "creative": {
                "description": "Imaginative, engaging, expressive",
                "characteristics": ["Imaginative", "Expressive", "Engaging", "Original"],
                "avoid": ["Clichés", "Boring descriptions", "Predictable patterns"],
                "sentence_starters": [
                    "Picture this:", "Once upon a time,", "In a world where,", "Imagine a place,"
                ],
                "vocabulary_level": "descriptive_varied",
                "emotional_tone": "engaging_inspiring"
            },
            "educational": {
                "description": "Clear, instructive, focused on learning",
                "characteristics": ["Clear", "Instructive", "Patient", "Progressive"],
                "avoid": ["Overwhelming complexity", "Assumptions about knowledge", "Rushed explanations"],
                "sentence_starters": [
                    "Let's start with,", "First, you need to understand,", "The key concept is,"
                ],
                "vocabulary_level": "clear_educational",
                "emotional_tone": "patient_helpful"
            }
        }
    
    def load_voice_characteristics(self) -> Dict:
        """Load voice characteristics and personality traits"""
        return {
            "expert": {
                "description": "Knowledgeable authority in the field",
                "traits": ["Credible", "Experienced", "Authoritative", "Insightful"],
                "language_patterns": {
                    "certainty_level": "high",
                    "uses_data": True,
                    "references_experience": True,
                    "provides_deep_insights": True
                }
            },
            "friendly": {
                "description": "Approachable and supportive companion",
                "traits": ["Warm", "Supportive", "Approachable", "Understanding"],
                "language_patterns": {
                    "certainty_level": "medium",
                    "uses_encouragement": True,
                    "personal_touch": True,
                    "empathetic_language": True
                }
            },
            "confident": {
                "description": "Self-assured and decisive leader",
                "traits": ["Decisive", "Bold", "Assertive", "Results-oriented"],
                "language_patterns": {
                    "certainty_level": "very_high",
                    "action_oriented": True,
                    "minimizes_hedging": True,
                    "strong_statements": True
                }
            },
            "helpful": {
                "description": "Supportive guide focused on assistance",
                "traits": ["Patient", "Thorough", "Caring", "Solution-focused"],
                "language_patterns": {
                    "certainty_level": "medium",
                    "step_by_step": True,
                    "anticipates_problems": True,
                    "offers_alternatives": True
                }
            },
            "engaging": {
                "description": "Captivating storyteller and entertainer",
                "traits": ["Charismatic", "Creative", "Dynamic", "Memorable"],
                "language_patterns": {
                    "certainty_level": "medium_high",
                    "uses_storytelling": True,
                    "vivid_descriptions": True,
                    "emotional_connection": True
                }
            }
        }
    
    def load_writing_patterns(self) -> Dict:
        """Load writing patterns and structural elements"""
        return {
            "sentence_structures": {
                "simple": {
                    "description": "Short, clear sentences (8-15 words)",
                    "patterns": ["Subject + Verb + Object", "Simple statements"],
                    "average_length": 12,
                    "complexity": "low"
                },
                "complex": {
                    "description": "Longer, detailed sentences (15-25 words)",
                    "patterns": ["Multiple clauses", "Detailed explanations"],
                    "average_length": 20,
                    "complexity": "high"
                },
                "varied": {
                    "description": "Mix of short and long sentences",
                    "patterns": ["Alternating lengths", "Rhythm creation"],
                    "average_length": 16,
                    "complexity": "medium"
                },
                "structured": {
                    "description": "Organized, logical flow",
                    "patterns": ["Clear progression", "Logical connections"],
                    "average_length": 18,
                    "complexity": "medium_high"
                }
            },
            "vocabulary_levels": {
                "simple": {
                    "description": "Common, everyday words",
                    "grade_level": 6,
                    "characteristics": ["Easy to understand", "Accessible to all"]
                },
                "intermediate": {
                    "description": "Standard business vocabulary",
                    "grade_level": 8,
                    "characteristics": ["Professional but accessible", "Industry-appropriate"]
                },
                "advanced": {
                    "description": "Sophisticated, nuanced language",
                    "grade_level": 12,
                    "characteristics": ["Precise terminology", "Expert-level"]
                },
                "technical": {
                    "description": "Specialized, field-specific terms",
                    "grade_level": 14,
                    "characteristics": ["Domain expertise", "Precise technical language"]
                }
            },
            "perspectives": {
                "first_person": {
                    "description": "I, we, our perspective",
                    "pronouns": ["I", "we", "our", "my"],
                    "effect": "Personal, authoritative"
                },
                "second_person": {
                    "description": "You, your perspective",
                    "pronouns": ["you", "your", "yourself"],
                    "effect": "Direct, engaging"
                },
                "third_person": {
                    "description": "They, it, objective perspective",
                    "pronouns": ["they", "it", "one", "people"],
                    "effect": "Objective, professional"
                },
                "mixed": {
                    "description": "Combination of perspectives",
                    "pronouns": ["varied"],
                    "effect": "Dynamic, storytelling"
                }
            }
        }
    
    def apply_style_profile(self, profile_name: str, current_settings: Dict) -> Dict:
        """Apply a complete style profile to current settings"""
        if profile_name not in self.style_profiles:
            return current_settings
        
        profile = self.style_profiles[profile_name]
        
        # Update style-related settings
        updated_settings = current_settings.copy()
        
        # Ensure style_settings exists
        if "style_settings" not in updated_settings:
            updated_settings["style_settings"] = {}
        
        # Apply profile settings
        style_settings = updated_settings["style_settings"]
        style_settings.update({
            "tone": profile["tone"],
            "voice": profile["voice"],
            "formality": profile["formality"],
            "vocabulary": profile["vocabulary"],
            "sentence_structure": profile["sentence_structure"],
            "perspective": profile["perspective"],
            "characteristics": profile["characteristics"].copy()
        })
        
        # Update related settings
        updated_settings["tone"] = profile["tone"]
        
        return updated_settings
    
    def get_style_recommendations(self, content_type: str, target_audience: str) -> List[str]:
        """Get style recommendations based on content type and audience"""
        recommendations = []
        
        # Content type recommendations
        if content_type == "blog_post":
            recommendations.extend([
                "Consider conversational or friendly tone for better engagement",
                "Use second person perspective to connect with readers",
                "Mix sentence structures to maintain interest"
            ])
        elif content_type == "how_to_guide":
            recommendations.extend([
                "Educational or helpful voice works best for tutorials",
                "Use clear, structured language with step-by-step approach",
                "Second person perspective for direct instruction"
            ])
        elif content_type == "review":
            recommendations.extend([
                "Authoritative or expert voice builds trust",
                "Balance objective analysis with personal insights",
                "Use specific examples and evidence"
            ])
        elif content_type == "landing_page":
            recommendations.extend([
                "Persuasive tone drives action",
                "Confident voice builds trust",
                "Benefit-focused language resonates with visitors"
            ])
        
        # Audience recommendations
        if "beginner" in target_audience.lower():
            recommendations.extend([
                "Use simple vocabulary and clear explanations",
                "Friendly or helpful voice reduces intimidation",
                "Avoid technical jargon"
            ])
        elif "professional" in target_audience.lower():
            recommendations.extend([
                "Professional or authoritative tone expected",
                "Industry-appropriate vocabulary level",
                "Data-driven content builds credibility"
            ])
        elif "technical" in target_audience.lower():
            recommendations.extend([
                "Technical tone with expert voice",
                "Precise, detailed language",
                "Method-based evidence and examples"
            ])
        
        return recommendations

def render_style_customization_interface():
    """Render the advanced style customization interface"""
    st.markdown("## 🎨 Content Style Customization")
    st.markdown("Customize the tone, voice, and writing style to match your brand and audience.")
    
    # Initialize style manager
    if 'style_manager' not in st.session_state:
        st.session_state.style_manager = StyleCustomizationManager()
    
    # Ensure style settings exist
    if 'style_settings' not in st.session_state.seo_settings:
        st.session_state.seo_settings['style_settings'] = {
            "tone": "professional",
            "voice": "expert",
            "formality": "semi_formal",
            "vocabulary": "intermediate",
            "sentence_structure": "varied",
            "perspective": "second_person",
            "characteristics": {}
        }
    
    # Style customization tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎭 Quick Profiles", "🗣️ Tone & Voice", "✍️ Writing Style", "👥 Audience", "🔧 Advanced"
    ])
    
    with tab1:
        render_style_profiles()
    
    with tab2:
        render_tone_voice_settings()
    
    with tab3:
        render_writing_style_settings()
    
    with tab4:
        render_audience_targeting()
    
    with tab5:
        render_advanced_style_settings()
    
    # Style preview and recommendations
    render_style_preview()

def render_style_profiles():
    """Render quick style profiles selection"""
    st.markdown("### 🎭 Quick Style Profiles")
    st.markdown("Choose a predefined style profile that matches your content goals.")
    
    manager = st.session_state.style_manager
    profiles = manager.style_profiles
    
    # Profile selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_profile = st.selectbox(
            "Choose a Style Profile:",
            [""] + list(profiles.keys()),
            format_func=lambda x: "Select a profile..." if x == "" else profiles[x]["name"],
            key="style_profile_selector"
        )
    
    with col2:
        if selected_profile and st.button("🚀 Apply Profile", type="primary"):
            current_settings = st.session_state.seo_settings
            updated_settings = manager.apply_style_profile(selected_profile, current_settings)
            st.session_state.seo_settings = updated_settings
            st.success(f"✅ Applied '{profiles[selected_profile]['name']}' style profile!")
            st.rerun()
    
    # Profile cards display
    if selected_profile and selected_profile in profiles:
        profile_data = profiles[selected_profile]
        
        st.markdown(f"#### 📋 {profile_data['name']}")
        st.info(profile_data['description'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Style Elements:**")
            st.markdown(f"• **Tone:** {profile_data['tone'].title()}")
            st.markdown(f"• **Voice:** {profile_data['voice'].title()}")
            st.markdown(f"• **Formality:** {profile_data['formality'].replace('_', ' ').title()}")
        
        with col2:
            st.markdown("**Language:**")
            st.markdown(f"• **Vocabulary:** {profile_data['vocabulary'].title()}")
            st.markdown(f"• **Structure:** {profile_data['sentence_structure'].replace('_', ' ').title()}")
            st.markdown(f"• **Perspective:** {profile_data['perspective'].replace('_', ' ').title()}")
        
        with col3:
            st.markdown("**Characteristics:**")
            characteristics = profile_data['characteristics']
            for key, value in list(characteristics.items())[:3]:
                if value:
                    st.markdown(f"• {key.replace('_', ' ').title()}")
    
    else:
        # Show all profiles in cards
        st.markdown("### 📋 Available Style Profiles")
        
        profile_cols = st.columns(2)
        
        for i, (profile_key, profile_data) in enumerate(profiles.items()):
            with profile_cols[i % 2]:
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0;">
                        <h4>{profile_data['name']}</h4>
                        <p style="color: #666; font-size: 14px;">{profile_data['description']}</p>
                        <p style="font-size: 12px;"><strong>Tone:</strong> {profile_data['tone'].title()} | <strong>Voice:</strong> {profile_data['voice'].title()}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Apply {profile_data['name']}", key=f"apply_style_{profile_key}"):
                        current_settings = st.session_state.seo_settings
                        updated_settings = manager.apply_style_profile(profile_key, current_settings)
                        st.session_state.seo_settings = updated_settings
                        st.success(f"✅ Applied '{profile_data['name']}' style!")
                        st.rerun()

def render_tone_voice_settings():
    """Render detailed tone and voice settings"""
    st.markdown("### 🗣️ Tone & Voice Configuration")
    
    manager = st.session_state.style_manager
    style_settings = st.session_state.seo_settings['style_settings']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎭 Tone Selection")
        
        tone_options = list(manager.tone_definitions.keys())
        current_tone = style_settings.get("tone", "professional")
        
        selected_tone = st.selectbox(
            "Writing Tone:",
            tone_options,
            index=tone_options.index(current_tone) if current_tone in tone_options else 0,
            key="tone_selector"
        )
        
        # Tone description
        if selected_tone in manager.tone_definitions:
            tone_def = manager.tone_definitions[selected_tone]
            st.info(f"📝 {tone_def['description']}")
            
            # Tone characteristics
            st.markdown("**Characteristics:**")
            for char in tone_def['characteristics']:
                st.markdown(f"• {char}")
            
            # What to avoid
            if tone_def.get('avoid'):
                with st.expander("⚠️ What to Avoid"):
                    for avoid_item in tone_def['avoid']:
                        st.markdown(f"• {avoid_item}")
    
    with col2:
        st.markdown("#### 🎤 Voice Selection")
        
        voice_options = list(manager.voice_characteristics.keys())
        current_voice = style_settings.get("voice", "expert")
        
        selected_voice = st.selectbox(
            "Writing Voice:",
            voice_options,
            index=voice_options.index(current_voice) if current_voice in voice_options else 0,
            key="voice_selector"
        )
        
        # Voice description
        if selected_voice in manager.voice_characteristics:
            voice_def = manager.voice_characteristics[selected_voice]
            st.info(f"👤 {voice_def['description']}")
            
            # Voice traits
            st.markdown("**Personality Traits:**")
            for trait in voice_def['traits']:
                st.markdown(f"• {trait}")
            
            # Language patterns
            patterns = voice_def.get('language_patterns', {})
            if patterns:
                with st.expander("🔧 Language Patterns"):
                    for pattern, value in patterns.items():
                        if isinstance(value, bool):
                            status = "✅" if value else "❌"
                            st.markdown(f"{status} {pattern.replace('_', ' ').title()}")
                        else:
                            st.markdown(f"• **{pattern.replace('_', ' ').title()}:** {value}")
    
    # Tone and voice combination analysis
    st.markdown("#### 🎯 Tone + Voice Analysis")
    
    combination_col1, combination_col2 = st.columns(2)
    
    with combination_col1:
        st.markdown("**Combination Effect:**")
        
        # Analyze combination
        if selected_tone == "professional" and selected_voice == "expert":
            st.success("✅ Excellent for business and technical content")
        elif selected_tone == "conversational" and selected_voice == "friendly":
            st.success("✅ Perfect for blog posts and casual content")
        elif selected_tone == "persuasive" and selected_voice == "confident":
            st.success("✅ Ideal for marketing and sales content")
        elif selected_tone == "educational" and selected_voice == "helpful":
            st.success("✅ Great for tutorials and guides")
        else:
            st.info("ℹ️ Custom combination - ensure consistency")
    
    with combination_col2:
        # Sample sentence starters
        tone_def = manager.tone_definitions.get(selected_tone, {})
        sample_starters = tone_def.get('sentence_starters', [])
        
        if sample_starters:
            st.markdown("**Sample Openings:**")
            for starter in sample_starters[:3]:
                st.markdown(f"• \"{starter}\"")
    
    # Update settings
    style_settings["tone"] = selected_tone
    style_settings["voice"] = selected_voice
    
    # Update main seo_settings for backward compatibility
    st.session_state.seo_settings["tone"] = selected_tone

def render_writing_style_settings():
    """Render writing style and structure settings"""
    st.markdown("### ✍️ Writing Style & Structure")
    
    manager = st.session_state.style_manager
    style_settings = st.session_state.seo_settings['style_settings']
    patterns = manager.writing_patterns
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Language Complexity")
        
        # Vocabulary level
        vocab_options = list(patterns['vocabulary_levels'].keys())
        current_vocab = style_settings.get("vocabulary", "intermediate")
        
        selected_vocabulary = st.selectbox(
            "Vocabulary Level:",
            vocab_options,
            index=vocab_options.index(current_vocab) if current_vocab in vocab_options else 0,
            key="vocabulary_selector"
        )
        
        # Vocabulary description
        if selected_vocabulary in patterns['vocabulary_levels']:
            vocab_def = patterns['vocabulary_levels'][selected_vocabulary]
            st.info(f"📚 {vocab_def['description']}")
            st.markdown(f"**Grade Level:** {vocab_def['grade_level']}")
            
            for char in vocab_def['characteristics']:
                st.markdown(f"• {char}")
        
        # Formality level
        formality_options = ["informal", "semi_formal", "formal"]
        current_formality = style_settings.get("formality", "semi_formal")
        
        selected_formality = st.selectbox(
            "Formality Level:",
            formality_options,
            format_func=lambda x: x.replace("_", " ").title(),
            index=formality_options.index(current_formality) if current_formality in formality_options else 1,
            key="formality_selector"
        )
        
        # Formality explanation
        formality_explanations = {
            "informal": "Casual, relaxed language with contractions and colloquialisms",
            "semi_formal": "Professional but approachable, business-appropriate",
            "formal": "Strictly professional, academic or corporate language"
        }
        
        st.info(f"📋 {formality_explanations[selected_formality]}")
    
    with col2:
        st.markdown("#### 🏗️ Sentence Structure")
        
        # Sentence structure
        structure_options = list(patterns['sentence_structures'].keys())
        current_structure = style_settings.get("sentence_structure", "varied")
        
        selected_structure = st.selectbox(
            "Sentence Structure:",
            structure_options,
            index=structure_options.index(current_structure) if current_structure in structure_options else 0,
            key="structure_selector"
        )
        
        # Structure description
        if selected_structure in patterns['sentence_structures']:
            struct_def = patterns['sentence_structures'][selected_structure]
            st.info(f"📐 {struct_def['description']}")
            st.markdown(f"**Average Length:** {struct_def['average_length']} words")
            st.markdown(f"**Complexity:** {struct_def['complexity'].title()}")
            
            for pattern in struct_def['patterns']:
                st.markdown(f"• {pattern}")
        
        # Perspective
        perspective_options = list(patterns['perspectives'].keys())
        current_perspective = style_settings.get("perspective", "second_person")
        
        selected_perspective = st.selectbox(
            "Writing Perspective:",
            perspective_options,
            format_func=lambda x: x.replace("_", " ").title(),
            index=perspective_options.index(current_perspective) if current_perspective in perspective_options else 1,
            key="perspective_selector"
        )
        
        # Perspective description
        if selected_perspective in patterns['perspectives']:
            persp_def = patterns['perspectives'][selected_perspective]
            st.info(f"👁️ {persp_def['description']}")
            st.markdown(f"**Effect:** {persp_def['effect']}")
            
            if persp_def['pronouns'] != ['varied']:
                pronouns_text = ", ".join(persp_def['pronouns'])
                st.markdown(f"**Key Words:** {pronouns_text}")
    
    # Writing characteristics
    st.markdown("#### 🎯 Writing Characteristics")
    
    char_col1, char_col2, char_col3 = st.columns(3)
    
    current_characteristics = style_settings.get("characteristics", {})
    
    with char_col1:
        st.markdown("**Content Elements:**")
        
        uses_statistics = st.checkbox(
            "Include Statistics & Data",
            value=current_characteristics.get("uses_statistics", False),
            key="char_statistics"
        )
        
        personal_anecdotes = st.checkbox(
            "Use Personal Examples",
            value=current_characteristics.get("personal_anecdotes", False),
            key="char_anecdotes"
        )
        
        storytelling = st.checkbox(
            "Include Storytelling",
            value=current_characteristics.get("storytelling", False),
            key="char_storytelling"
        )
        
        step_by_step = st.checkbox(
            "Step-by-Step Approach",
            value=current_characteristics.get("step_by_step", False),
            key="char_step_by_step"
        )
    
    with char_col2:
        st.markdown("**Language Style:**")
        
        uses_contractions = st.checkbox(
            "Use Contractions (don't, won't)",
            value=current_characteristics.get("uses_contractions", False),
            key="char_contractions"
        )
        
        industry_jargon = st.checkbox(
            "Include Industry Jargon",
            value=current_characteristics.get("industry_jargon", False),
            key="char_jargon"
        )
        
        vivid_imagery = st.checkbox(
            "Use Vivid Descriptions",
            value=current_characteristics.get("vivid_imagery", False),
            key="char_imagery"
        )
        
        technical_accuracy = st.checkbox(
            "Emphasize Technical Accuracy",
            value=current_characteristics.get("technical_accuracy", False),
            key="char_technical"
        )
    
    with char_col3:
        st.markdown("**Engagement Style:**")
        
        call_to_action_style = st.selectbox(
            "Call-to-Action Style:",
            ["subtle", "direct", "strong", "encouraging", "instructional", "inspiring"],
            index=["subtle", "direct", "strong", "encouraging", "instructional", "inspiring"].index(
                current_characteristics.get("call_to_action_style", "direct")
            ),
            key="char_cta_style"
        )
        
        emotional_appeal = st.selectbox(
            "Emotional Appeal:",
            ["logical", "personal", "practical", "aspirational", "supportive", "emotional"],
            index=["logical", "personal", "practical", "aspirational", "supportive", "emotional"].index(
                current_characteristics.get("emotional_appeal", "logical")
            ),
            key="char_emotional"
        )
        
        evidence_style = st.selectbox(
            "Evidence Style:",
            ["data_heavy", "example_based", "method_based", "benefit_proof", "example_rich", "story_based"],
            format_func=lambda x: x.replace("_", " ").title(),
            index=["data_heavy", "example_based", "method_based", "benefit_proof", "example_rich", "story_based"].index(
                current_characteristics.get("evidence_style", "example_based")
            ),
            key="char_evidence"
        )
    
    # Update style settings
    style_settings.update({
        "vocabulary": selected_vocabulary,
        "formality": selected_formality,
        "sentence_structure": selected_structure,
        "perspective": selected_perspective,
        "characteristics": {
            "uses_statistics": uses_statistics,
            "personal_anecdotes": personal_anecdotes,
            "storytelling": storytelling,
            "step_by_step": step_by_step,
            "uses_contractions": uses_contractions,
            "industry_jargon": industry_jargon,
            "vivid_imagery": vivid_imagery,
            "technical_accuracy": technical_accuracy,
            "call_to_action_style": call_to_action_style,
            "emotional_appeal": emotional_appeal,
            "evidence_style": evidence_style
        }
    })

def render_audience_targeting():
    """Render audience targeting and personalization settings"""
    st.markdown("### 👥 Audience Targeting & Personalization")
    
    manager = st.session_state.style_manager
    style_settings = st.session_state.seo_settings['style_settings']
    
    # Ensure audience_settings exists
    if "audience_settings" not in style_settings:
        style_settings["audience_settings"] = {}
    
    audience_settings = style_settings["audience_settings"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Target Audience")
        
        # Primary audience
        audience_type = st.selectbox(
            "Primary Audience:",
            [
                "general_public", "business_professionals", "technical_experts", 
                "beginners", "intermediate_users", "advanced_users",
                "decision_makers", "students", "researchers"
            ],
            format_func=lambda x: x.replace("_", " ").title(),
            index=0,
            key="audience_type"
        )
        
        # Experience level
        experience_level = st.selectbox(
            "Experience Level:",
            ["beginner", "intermediate", "advanced", "expert", "mixed"],
            index=audience_settings.get("experience_level_index", 1),
            key="experience_level"
        )
        
        # Industry focus
        industry_focus = st.text_input(
            "Industry/Field (optional):",
            value=audience_settings.get("industry_focus", ""),
            placeholder="e.g., healthcare, technology, finance",
            key="industry_focus"
        )
        
        # Reading context
        reading_context = st.selectbox(
            "Reading Context:",
            ["work_research", "casual_browsing", "problem_solving", "learning", "decision_making"],
            format_func=lambda x: x.replace("_", " ").title(),
            index=audience_settings.get("reading_context_index", 0),
            key="reading_context"
        )
    
    with col2:
        st.markdown("#### 📱 Content Consumption")
        
        # Device preference
        device_preference = st.selectbox(
            "Primary Device:",
            ["desktop", "mobile", "tablet", "mixed"],
            index=audience_settings.get("device_preference_index", 3),
            key="device_preference"
        )
        
        # Reading time availability
        reading_time = st.selectbox(
            "Available Reading Time:",
            ["quick_scan", "moderate_read", "deep_dive", "varies"],
            format_func=lambda x: {
                "quick_scan": "Quick Scan (1-2 min)",
                "moderate_read": "Moderate Read (3-5 min)",
                "deep_dive": "Deep Dive (10+ min)",
                "varies": "Varies by Section"
            }[x],
            index=audience_settings.get("reading_time_index", 1),
            key="reading_time"
        )
        
        # Content goals
        content_goals = st.multiselect(
            "Reader Goals:",
            [
                "learn_something_new", "solve_a_problem", "make_a_decision",
                "stay_informed", "find_inspiration", "compare_options",
                "get_started", "improve_skills"
            ],
            default=audience_settings.get("content_goals", ["learn_something_new"]),
            format_func=lambda x: x.replace("_", " ").title(),
            key="content_goals"
        )
        
        # Pain points
        pain_points = st.text_area(
            "Common Pain Points:",
            value=audience_settings.get("pain_points", ""),
            placeholder="What challenges does your audience face?",
            height=80,
            key="pain_points"
        )
    
    # Audience insights and recommendations
    st.markdown("#### 💡 Audience-Based Recommendations")
    
    content_type = st.session_state.seo_settings.get("content_type", "blog_post")
    recommendations = manager.get_style_recommendations(content_type, f"{audience_type} {experience_level}")
    
    if recommendations:
        rec_col1, rec_col2 = st.columns(2)
        
        with rec_col1:
            st.markdown("**Style Recommendations:**")
            for rec in recommendations[:3]:
                st.info(f"💡 {rec}")
        
        with rec_col2:
            st.markdown("**Audience-Specific Tips:**")
            
            if experience_level == "beginner":
                st.success("✅ Use simple language and explain concepts clearly")
                st.success("✅ Include step-by-step instructions")
                st.success("✅ Define technical terms")
            elif experience_level == "advanced":
                st.success("✅ Use industry terminology confidently")
                st.success("✅ Focus on advanced insights and nuances")
                st.success("✅ Reference latest developments")
            else:
                st.success("✅ Balance accessibility with depth")
                st.success("✅ Provide both basic and advanced information")
                st.success("✅ Use progressive disclosure")
    
    # Update audience settings
    audience_settings.update({
        "audience_type": audience_type,
        "experience_level": experience_level,
        "experience_level_index": ["beginner", "intermediate", "advanced", "expert", "mixed"].index(experience_level),
        "industry_focus": industry_focus,
        "reading_context": reading_context,
        "reading_context_index": ["work_research", "casual_browsing", "problem_solving", "learning", "decision_making"].index(reading_context),
        "device_preference": device_preference,
        "device_preference_index": ["desktop", "mobile", "tablet", "mixed"].index(device_preference),
        "reading_time": reading_time,
        "reading_time_index": ["quick_scan", "moderate_read", "deep_dive", "varies"].index(reading_time),
        "content_goals": content_goals,
        "pain_points": pain_points
    })

def render_advanced_style_settings():
    """Render advanced style and customization settings"""
    st.markdown("### 🔧 Advanced Style Configuration")
    
    style_settings = st.session_state.seo_settings['style_settings']
    
    # Ensure advanced_style exists
    if "advanced_style" not in style_settings:
        style_settings["advanced_style"] = {}
    
    advanced_style = style_settings["advanced_style"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎨 Content Formatting")
        
        # Formatting preferences
        use_bullet_points = st.checkbox(
            "Emphasize Bullet Points",
            value=advanced_style.get("use_bullet_points", True),
            help="Use bullet points for better readability",
            key="formatting_bullets"
        )
        
        use_numbered_lists = st.checkbox(
            "Include Numbered Lists",
            value=advanced_style.get("use_numbered_lists", True),
            help="Use numbered lists for step-by-step content",
            key="formatting_numbers"
        )
        
        use_subheadings = st.checkbox(
            "Rich Subheading Structure",
            value=advanced_style.get("use_subheadings", True),
            help="Create detailed subheading hierarchy",
            key="formatting_subheadings"
        )
        
        bold_emphasis = st.selectbox(
            "Bold Text Usage:",
            ["minimal", "moderate", "frequent"],
            index=["minimal", "moderate", "frequent"].index(advanced_style.get("bold_emphasis", "moderate")),
            help="How often to use bold text for emphasis",
            key="formatting_bold"
        )
        
        # Content flow
        st.markdown("#### 🌊 Content Flow")
        
        transition_style = st.selectbox(
            "Transition Style:",
            ["minimal", "natural", "explicit", "creative"],
            index=["minimal", "natural", "explicit", "creative"].index(advanced_style.get("transition_style", "natural")),
            help="How to connect paragraphs and sections",
            key="flow_transitions"
        )
        
        paragraph_rhythm = st.selectbox(
            "Paragraph Rhythm:",
            ["consistent", "varied", "short_punchy", "detailed"],
            index=["consistent", "varied", "short_punchy", "detailed"].index(advanced_style.get("paragraph_rhythm", "varied")),
            help="Pattern of paragraph lengths",
            key="flow_rhythm"
        )
    
    with col2:
        st.markdown("#### 🗣️ Voice Consistency")
        
        # Voice consistency settings
        maintain_voice = st.checkbox(
            "Strict Voice Consistency",
            value=advanced_style.get("maintain_voice", True),
            help="Maintain consistent voice throughout content",
            key="voice_consistency"
        )
        
        allow_personality = st.checkbox(
            "Allow Personality Touches",
            value=advanced_style.get("allow_personality", False),
            help="Include subtle personality elements",
            key="voice_personality"
        )
        
        brand_voice_alignment = st.slider(
            "Brand Voice Alignment:",
            min_value=1,
            max_value=10,
            value=advanced_style.get("brand_voice_alignment", 7),
            help="How closely to match established brand voice (1=flexible, 10=strict)",
            key="voice_brand"
        )
        
        # Content depth
        st.markdown("#### 📊 Content Depth")
        
        detail_level = st.selectbox(
            "Detail Level:",
            ["overview", "balanced", "comprehensive", "exhaustive"],
            index=["overview", "balanced", "comprehensive", "exhaustive"].index(advanced_style.get("detail_level", "balanced")),
            help="How much detail to include",
            key="depth_detail"
        )
        
        example_frequency = st.selectbox(
            "Example Usage:",
            ["rare", "occasional", "frequent", "abundant"],
            index=["rare", "occasional", "frequent", "abundant"].index(advanced_style.get("example_frequency", "frequent")),
            help="How often to include examples",
            key="depth_examples"
        )
        
        supporting_evidence = st.selectbox(
            "Supporting Evidence:",
            ["minimal", "standard", "research_heavy", "citation_rich"],
            index=["minimal", "standard", "research_heavy", "citation_rich"].index(advanced_style.get("supporting_evidence", "standard")),
            help="Level of evidence and citations to include",
            key="depth_evidence"
        )
    
    # Custom style rules
    with st.expander("📝 Custom Style Rules"):
        st.markdown("#### ✏️ Custom Writing Rules")
        
        custom_rules = st.text_area(
            "Custom Style Guidelines:",
            value=advanced_style.get("custom_rules", ""),
            placeholder="Enter specific style rules, phrases to avoid, or unique requirements...",
            height=100,
            help="Add any specific style requirements for your content",
            key="custom_style_rules"
        )
        
        banned_phrases = st.text_area(
            "Phrases to Avoid:",
            value=advanced_style.get("banned_phrases", ""),
            placeholder="Enter phrases to avoid, one per line...",
            height=80,
            help="List specific phrases or words to avoid in the content",
            key="banned_phrases"
        )
        
        preferred_phrases = st.text_area(
            "Preferred Expressions:",
            value=advanced_style.get("preferred_phrases", ""),
            placeholder="Enter preferred phrases or expressions, one per line...",
            height=80,
            help="List preferred phrases or expressions to use when possible",
            key="preferred_phrases"
        )
    
    # Update advanced style settings
    advanced_style.update({
        "use_bullet_points": use_bullet_points,
        "use_numbered_lists": use_numbered_lists,
        "use_subheadings": use_subheadings,
        "bold_emphasis": bold_emphasis,
        "transition_style": transition_style,
        "paragraph_rhythm": paragraph_rhythm,
        "maintain_voice": maintain_voice,
        "allow_personality": allow_personality,
        "brand_voice_alignment": brand_voice_alignment,
        "detail_level": detail_level,
        "example_frequency": example_frequency,
        "supporting_evidence": supporting_evidence,
        "custom_rules": custom_rules,
        "banned_phrases": banned_phrases,
        "preferred_phrases": preferred_phrases
    })

def render_style_preview():
    """Render style preview and analysis"""
    st.markdown("---")
    st.markdown("## 👁️ Style Preview & Analysis")
    
    style_settings = st.session_state.seo_settings.get('style_settings', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Current Style Profile")
        
        # Style summary
        tone = style_settings.get('tone', 'professional').title()
        voice = style_settings.get('voice', 'expert').title()
        formality = style_settings.get('formality', 'semi_formal').replace('_', ' ').title()
        vocabulary = style_settings.get('vocabulary', 'intermediate').title()
        
        st.info(f"""
        **Style Summary:**
        • **Tone:** {tone}
        • **Voice:** {voice}  
        • **Formality:** {formality}
        • **Vocabulary:** {vocabulary}
        """)
        
        # Characteristics summary
        characteristics = style_settings.get('characteristics', {})
        active_chars = [k.replace('_', ' ').title() for k, v in characteristics.items() if v and isinstance(v, bool)]
        
        if active_chars:
            st.markdown("**Active Characteristics:**")
            for char in active_chars[:5]:
                st.markdown(f"✅ {char}")
            
            if len(active_chars) > 5:
                st.markdown(f"... and {len(active_chars) - 5} more")
    
    with col2:
        st.markdown("### 🎯 Style Recommendations")
        
        # Generate recommendations based on current settings
        content_type = st.session_state.seo_settings.get('content_type', 'blog_post')
        audience_settings = style_settings.get('audience_settings', {})
        audience_type = audience_settings.get('audience_type', 'general_public')
        
        manager = st.session_state.style_manager
        recommendations = manager.get_style_recommendations(content_type, audience_type)
        
        if recommendations:
            for rec in recommendations[:4]:
                st.success(f"💡 {rec}")
        
        # Style consistency check
        consistency_score = calculate_style_consistency(style_settings)
        
        if consistency_score >= 8:
            st.success(f"✅ Style Consistency: {consistency_score}/10 (Excellent)")
        elif consistency_score >= 6:
            st.warning(f"⚠️ Style Consistency: {consistency_score}/10 (Good)")
        else:
            st.error(f"❌ Style Consistency: {consistency_score}/10 (Needs Improvement)")
    
    # Sample content preview
    if st.button("📖 Generate Style Preview", type="secondary"):
        generate_style_preview_content()

def calculate_style_consistency(style_settings: Dict) -> int:
    """Calculate style consistency score based on settings"""
    score = 10
    
    tone = style_settings.get('tone', '')
    voice = style_settings.get('voice', '')
    formality = style_settings.get('formality', '')
    
    # Check for conflicting combinations
    if tone == 'conversational' and formality == 'formal':
        score -= 2
    
    if tone == 'technical' and voice == 'friendly':
        score -= 1
    
    if tone == 'persuasive' and voice == 'expert' and formality == 'informal':
        score -= 1
    
    # Check completeness
    required_fields = ['tone', 'voice', 'formality', 'vocabulary']
    missing_fields = sum(1 for field in required_fields if not style_settings.get(field))
    score -= missing_fields
    
    return max(0, score)

def generate_style_preview_content():
    """Generate a preview of content in the selected style"""
    style_settings = st.session_state.seo_settings.get('style_settings', {})
    primary_keyword = st.session_state.seo_settings.get('primary_keyword', 'your topic')
    
    tone = style_settings.get('tone', 'professional')
    voice = style_settings.get('voice', 'expert')
    perspective = style_settings.get('perspective', 'second_person')
    
    # Generate sample content based on style
    sample_content = generate_sample_paragraph(tone, voice, perspective, primary_keyword)
    
    st.markdown("### 📝 Style Preview")
    st.markdown("Here's how your content might look with the current style settings:")
    
    st.markdown(f"""
    <div style="border: 1px solid #ddd; padding: 20px; border-radius: 10px; background: #f9f9f9; font-family: Georgia, serif; line-height: 1.6;">
        {sample_content}
    </div>
    """, unsafe_allow_html=True)
    
    # Style analysis
    st.markdown("#### 📊 Style Analysis")
    
    analysis_col1, analysis_col2 = st.columns(2)
    
    with analysis_col1:
        # Count characteristics
        word_count = len(sample_content.split())
        sentence_count = sample_content.count('.') + sample_content.count('!') + sample_content.count('?')
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        st.metric("Word Count", word_count)
        st.metric("Sentences", sentence_count)
        st.metric("Avg Sentence Length", f"{avg_sentence_length:.1f}")
    
    with analysis_col2:
        # Style characteristics
        has_contractions = "'" in sample_content
        has_questions = "?" in sample_content
        has_exclamations = "!" in sample_content
        
        st.markdown("**Style Elements:**")
        st.markdown(f"{'✅' if has_contractions else '❌'} Contractions")
        st.markdown(f"{'✅' if has_questions else '❌'} Questions")
        st.markdown(f"{'✅' if has_exclamations else '❌'} Exclamations")

def generate_sample_paragraph(tone: str, voice: str, perspective: str, keyword: str) -> str:
    """Generate a sample paragraph based on style settings"""
    
    # Sample content templates based on tone and voice combinations
    templates = {
        ("professional", "expert"): f"Understanding {keyword} requires a systematic approach backed by industry best practices. Research demonstrates that organizations implementing effective {keyword} strategies achieve measurable improvements in performance metrics. The key lies in developing a comprehensive framework that addresses both immediate needs and long-term objectives.",
        
        ("conversational", "friendly"): f"Let's talk about {keyword} for a moment. You've probably heard the term thrown around, but what does it really mean for you? Don't worry - we're going to break this down in a way that actually makes sense. Think of {keyword} as your secret weapon for getting better results.",
        
        ("technical", "expert"): f"The implementation of {keyword} methodologies involves several critical components that must be precisely configured. Each parameter affects system performance according to established algorithms. Documentation indicates that optimal {keyword} requires adherence to specific protocols and continuous monitoring of key metrics.",
        
        ("persuasive", "confident"): f"Here's what most people don't realize about {keyword}: it's not just another buzzword - it's the game-changer that separates successful organizations from those still struggling with outdated approaches. When you master {keyword}, you're not just improving one area - you're transforming your entire operation.",
        
        ("educational", "helpful"): f"Learning about {keyword} doesn't have to be overwhelming. We'll start with the basics and build your understanding step by step. First, let's define what {keyword} means in simple terms. Then, we'll explore why it matters and how you can apply these concepts in real-world situations.",
        
        ("creative", "engaging"): f"Picture this: a world where {keyword} isn't just a concept, but a living, breathing part of your daily routine. Imagine the possibilities that unfold when you truly understand and harness the power of {keyword}. This isn't just theory - this is your roadmap to transformation."
    }
    
    # Get template or create default
    template = templates.get((tone, voice), f"When it comes to {keyword}, understanding the fundamental principles is essential for success. This comprehensive approach ensures optimal results while maintaining focus on key objectives.")
    
    # Adjust for perspective
    if perspective == "first_person":
        template = template.replace("you", "we").replace("You", "We").replace("your", "our").replace("Your", "Our")
    elif perspective == "third_person":
        template = template.replace("you", "they").replace("You", "They").replace("your", "their").replace("Your", "Their")
    
    return template

# Main interface function
def render_complete_style_customization():
    """Render complete style customization interface"""
    render_style_customization_interface()
