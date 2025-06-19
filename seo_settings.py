import streamlit as st
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re

class SEOSettingsManager:
    """Advanced SEO settings management system"""
    
    def __init__(self):
        self.default_settings = self.load_default_settings()
        self.presets = self.load_seo_presets()
        
    def load_default_settings(self) -> Dict:
        """Load default SEO settings"""
        return {
            "primary_keyword": "",
            "secondary_keywords": [],
            "content_length": 800,
            "tone": "professional",
            "content_type": "blog_post",
            "keyword_density": {
                "primary_min": 1.0,
                "primary_max": 2.5,
                "secondary_min": 0.5,
                "secondary_max": 1.5
            },
            "structure_settings": {
                "h1_count": 1,
                "h2_min": 3,
                "h2_max": 8,
                "h3_per_h2": 2,
                "intro_length": 150,
                "conclusion_length": 100
            },
            "meta_settings": {
                "title_length_max": 60,
                "description_length_max": 160,
                "include_brand": False,
                "brand_name": "",
                "title_pattern": "keyword_first"
            },
            "readability": {
                "target_grade_level": 8,
                "max_sentence_length": 20,
                "passive_voice_max": 10,
                "transition_words_min": 30
            },
            "advanced": {
                "include_faq": False,
                "include_schema": True,
                "include_social_meta": True,
                "internal_links_min": 2,
                "external_links_min": 1,
                "image_alt_optimization": True
            }
        }
    
    def load_seo_presets(self) -> Dict:
        """Load predefined SEO presets for different use cases"""
        return {
            "beginner_blog": {
                "name": "Beginner Blog",
                "description": "Simple SEO settings for new bloggers",
                "settings": {
                    "content_length": 600,
                    "tone": "conversational",
                    "keyword_density": {"primary_min": 1.0, "primary_max": 2.0},
                    "structure_settings": {"h2_min": 2, "h2_max": 5},
                    "readability": {"target_grade_level": 6, "max_sentence_length": 15}
                }
            },
            "professional_article": {
                "name": "Professional Article",
                "description": "High-quality content for business websites",
                "settings": {
                    "content_length": 1200,
                    "tone": "professional",
                    "keyword_density": {"primary_min": 1.2, "primary_max": 2.2},
                    "structure_settings": {"h2_min": 4, "h2_max": 7},
                    "readability": {"target_grade_level": 10, "max_sentence_length": 20}
                }
            },
            "seo_optimized": {
                "name": "SEO Optimized",
                "description": "Maximum SEO optimization for competitive keywords",
                "settings": {
                    "content_length": 1500,
                    "tone": "authoritative",
                    "keyword_density": {"primary_min": 1.5, "primary_max": 2.5},
                    "structure_settings": {"h2_min": 5, "h2_max": 8},
                    "advanced": {"include_faq": True, "include_schema": True}
                }
            },
            "landing_page": {
                "name": "Landing Page",
                "description": "Conversion-focused content for landing pages",
                "settings": {
                    "content_length": 800,
                    "tone": "persuasive",
                    "content_type": "landing_page",
                    "structure_settings": {"h2_min": 3, "h2_max": 5},
                    "advanced": {"include_social_meta": True}
                }
            },
            "technical_guide": {
                "name": "Technical Guide",
                "description": "In-depth technical content",
                "settings": {
                    "content_length": 2000,
                    "tone": "technical",
                    "content_type": "how_to_guide",
                    "structure_settings": {"h2_min": 6, "h2_max": 10},
                    "readability": {"target_grade_level": 12}
                }
            }
        }
    
    def apply_preset(self, preset_name: str, current_settings: Dict) -> Dict:
        """Apply a preset to current settings"""
        if preset_name not in self.presets:
            return current_settings
        
        preset = self.presets[preset_name]
        preset_settings = preset["settings"]
        
        # Deep merge preset settings with current settings
        updated_settings = current_settings.copy()
        
        for key, value in preset_settings.items():
            if isinstance(value, dict) and key in updated_settings:
                updated_settings[key].update(value)
            else:
                updated_settings[key] = value
        
        return updated_settings
    
    def validate_settings(self, settings: Dict) -> Tuple[bool, List[str]]:
        """Validate SEO settings and return errors if any"""
        errors = []
        
        # Primary keyword validation
        if not settings.get("primary_keyword", "").strip():
            errors.append("Primary keyword is required")
        
        # Keyword density validation
        density = settings.get("keyword_density", {})
        if density.get("primary_min", 0) >= density.get("primary_max", 0):
            errors.append("Primary keyword minimum density must be less than maximum")
        
        # Content length validation
        if settings.get("content_length", 0) < 200:
            errors.append("Content length must be at least 200 words")
        
        # Structure validation
        structure = settings.get("structure_settings", {})
        if structure.get("h2_min", 0) > structure.get("h2_max", 0):
            errors.append("Minimum H2 headings must be less than or equal to maximum")
        
        # Meta settings validation
        meta = settings.get("meta_settings", {})
        if meta.get("include_brand", False) and not meta.get("brand_name", "").strip():
            errors.append("Brand name is required when brand inclusion is enabled")
        
        return len(errors) == 0, errors

def render_seo_settings_interface():
    """Render the advanced SEO settings interface"""
    st.markdown("## ⚙️ Advanced SEO Configuration")
    st.markdown("Fine-tune your SEO settings for optimal content generation.")
    
    # Initialize settings manager
    if 'seo_manager' not in st.session_state:
        st.session_state.seo_manager = SEOSettingsManager()
    
    # Ensure seo_settings exists
    if 'seo_settings' not in st.session_state:
        st.session_state.seo_settings = st.session_state.seo_manager.default_settings.copy()
    
    # Settings tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Keywords", "📏 Structure", "📝 Meta Tags", "📖 Readability", "🔧 Advanced"
    ])
    
    with tab1:
        render_keyword_settings()
    
    with tab2:
        render_structure_settings()
    
    with tab3:
        render_meta_settings()
    
    with tab4:
        render_readability_settings()
    
    with tab5:
        render_advanced_settings()
    
    # Presets and actions
    render_presets_section()
    render_settings_actions()

def render_keyword_settings():
    """Render keyword configuration settings"""
    st.markdown("### 🎯 Keyword Configuration")
    
    settings = st.session_state.seo_settings
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Primary keyword
        primary_keyword = st.text_input(
            "🎯 Primary Keyword *",
            value=settings.get("primary_keyword", ""),
            placeholder="Enter your main target keyword",
            help="The main keyword you want to rank for"
        )
        
        # Content type
        content_type = st.selectbox(
            "📄 Content Type",
            ["blog_post", "how_to_guide", "review", "landing_page"],
            format_func=lambda x: {
                "blog_post": "📝 Blog Post",
                "how_to_guide": "📋 How-To Guide",
                "review": "⭐ Review Article", 
                "landing_page": "🎯 Landing Page"
            }[x],
            index=["blog_post", "how_to_guide", "review", "landing_page"].index(
                settings.get("content_type", "blog_post")
            )
        )
        
        # Writing tone
        tone = st.selectbox(
            "🎭 Writing Tone",
            ["professional", "conversational", "authoritative", "friendly", "technical", "persuasive"],
            index=["professional", "conversational", "authoritative", "friendly", "technical", "persuasive"].index(
                settings.get("tone", "professional")
            )
        )
    
    with col2:
        # Secondary keywords
        secondary_keywords_text = st.text_area(
            "🔍 Secondary Keywords",
            value='\n'.join(settings.get("secondary_keywords", [])),
            placeholder="Enter one keyword per line\nrelated keyword 1\nrelated keyword 2\nlong tail keyword",
            height=120,
            help="Related keywords to include naturally in content"
        )
        
        # Keyword analysis
        if primary_keyword:
            st.markdown("#### 📊 Keyword Analysis")
            keyword_length = len(primary_keyword.split())
            
            if keyword_length == 1:
                st.info("💡 Single word keyword - highly competitive")
            elif keyword_length <= 3:
                st.success("✅ Good keyword length")
            else:
                st.warning("⚠️ Long keyword - consider shorter alternatives")
            
            # Keyword suggestions
            if st.button("🔍 Get Keyword Suggestions"):
                st.info("🚧 Keyword suggestion feature will be implemented in future updates")
    
    # Keyword density settings
    st.markdown("#### 🎯 Keyword Density Settings")
    
    density_col1, density_col2 = st.columns(2)
    
    with density_col1:
        st.markdown("**Primary Keyword Density**")
        primary_min = st.slider(
            "Minimum %",
            min_value=0.5,
            max_value=3.0,
            value=settings.get("keyword_density", {}).get("primary_min", 1.0),
            step=0.1,
            key="primary_density_min"
        )
        
        primary_max = st.slider(
            "Maximum %",
            min_value=primary_min + 0.1,
            max_value=5.0,
            value=max(settings.get("keyword_density", {}).get("primary_max", 2.5), primary_min + 0.1),
            step=0.1,
            key="primary_density_max"
        )
    
    with density_col2:
        st.markdown("**Secondary Keyword Density**")
        secondary_min = st.slider(
            "Minimum %",
            min_value=0.1,
            max_value=2.0,
            value=settings.get("keyword_density", {}).get("secondary_min", 0.5),
            step=0.1,
            key="secondary_density_min"
        )
        
        secondary_max = st.slider(
            "Maximum %",
            min_value=secondary_min + 0.1,
            max_value=3.0,
            value=max(settings.get("keyword_density", {}).get("secondary_max", 1.5), secondary_min + 0.1),
            step=0.1,
            key="secondary_density_max"
        )
    
    # Update settings
    secondary_keywords_list = [kw.strip() for kw in secondary_keywords_text.split('\n') if kw.strip()]
    
    settings.update({
        "primary_keyword": primary_keyword,
        "secondary_keywords": secondary_keywords_list,
        "content_type": content_type,
        "tone": tone,
        "keyword_density": {
            "primary_min": primary_min,
            "primary_max": primary_max,
            "secondary_min": secondary_min,
            "secondary_max": secondary_max
        }
    })

def render_structure_settings():
    """Render content structure settings"""
    st.markdown("### 📏 Content Structure")
    
    settings = st.session_state.seo_settings
    structure = settings.get("structure_settings", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Content Length")
        
        content_length = st.slider(
            "Target Word Count",
            min_value=300,
            max_value=5000,
            value=settings.get("content_length", 800),
            step=100,
            help="Optimal length: 800-2000 words for most content"
        )
        
        # Length recommendations
        if content_length < 600:
            st.warning("⚠️ Short content may not rank well")
        elif content_length <= 1500:
            st.success("✅ Good content length")
        else:
            st.info("ℹ️ Long-form content - ensure high quality")
        
        st.markdown("#### 📐 Section Lengths")
        
        intro_length = st.slider(
            "Introduction Length (words)",
            min_value=50,
            max_value=300,
            value=structure.get("intro_length", 150),
            step=25
        )
        
        conclusion_length = st.slider(
            "Conclusion Length (words)",
            min_value=50,
            max_value=200,
            value=structure.get("conclusion_length", 100),
            step=25
        )
    
    with col2:
        st.markdown("#### 🏗️ Heading Structure")
        
        h1_count = st.selectbox(
            "H1 Headings",
            [1],
            index=0,
            help="Always use exactly one H1 per page"
        )
        
        h2_min = st.slider(
            "Minimum H2 Headings",
            min_value=2,
            max_value=15,
            value=structure.get("h2_min", 3),
            step=1
        )
        
        h2_max = st.slider(
            "Maximum H2 Headings",
            min_value=h2_min,
            max_value=20,
            value=max(structure.get("h2_max", 8), h2_min),
            step=1
        )
        
        h3_per_h2 = st.slider(
            "H3 Headings per H2 Section",
            min_value=0,
            max_value=5,
            value=structure.get("h3_per_h2", 2),
            step=1,
            help="Average number of H3 subheadings per H2 section"
        )
        
        # Structure preview
        st.markdown("#### 📋 Structure Preview")
        total_h2 = (h2_min + h2_max) // 2
        total_h3 = total_h2 * h3_per_h2
        
        st.info(f"""
        **Estimated Structure:**
        • 1 H1 (Title)
        • ~{total_h2} H2 sections
        • ~{total_h3} H3 subsections
        • {intro_length} word intro
        • {conclusion_length} word conclusion
        """)
    
    # Update structure settings
    settings["content_length"] = content_length
    settings["structure_settings"] = {
        "h1_count": h1_count,
        "h2_min": h2_min,
        "h2_max": h2_max,
        "h3_per_h2": h3_per_h2,
        "intro_length": intro_length,
        "conclusion_length": conclusion_length
    }

def render_meta_settings():
    """Render meta tag settings"""
    st.markdown("### 📝 Meta Tags & SEO Elements")
    
    settings = st.session_state.seo_settings
    meta = settings.get("meta_settings", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏷️ Title Tag Settings")
        
        title_length_max = st.slider(
            "Maximum Title Length",
            min_value=50,
            max_value=80,
            value=meta.get("title_length_max", 60),
            step=5,
            help="Google typically displays 50-60 characters"
        )
        
        title_pattern = st.selectbox(
            "Title Pattern",
            ["keyword_first", "brand_first", "benefit_first", "question_format"],
            format_func=lambda x: {
                "keyword_first": "🎯 Keyword First",
                "brand_first": "🏢 Brand First",
                "benefit_first": "✨ Benefit First",
                "question_format": "❓ Question Format"
            }[x],
            index=["keyword_first", "brand_first", "benefit_first", "question_format"].index(
                meta.get("title_pattern", "keyword_first")
            )
        )
        
        include_brand = st.checkbox(
            "Include Brand in Title",
            value=meta.get("include_brand", False),
            help="Add your brand name to title tags"
        )
        
        if include_brand:
            brand_name = st.text_input(
                "Brand Name",
                value=meta.get("brand_name", ""),
                placeholder="Your Brand Name"
            )
        else:
            brand_name = ""
    
    with col2:
        st.markdown("#### 📄 Meta Description")
        
        description_length_max = st.slider(
            "Maximum Description Length",
            min_value=140,
            max_value=180,
            value=meta.get("description_length_max", 160),
            step=5,
            help="Google typically displays up to 160 characters"
        )
        
        # Meta description preview
        st.markdown("#### 🔍 SERP Preview")
        primary_keyword = settings.get("primary_keyword", "Your Keyword")
        
        # Generate sample title
        if title_pattern == "keyword_first":
            sample_title = f"{primary_keyword.title()} - Complete Guide"
        elif title_pattern == "brand_first":
            sample_title = f"{brand_name or 'Brand'} | {primary_keyword.title()}"
        elif title_pattern == "benefit_first":
            sample_title = f"Master {primary_keyword.title()} in 2024"
        else:
            sample_title = f"How to {primary_keyword.title()}?"
        
        if include_brand and brand_name:
            sample_title += f" | {brand_name}"
        
        # Truncate if too long
        if len(sample_title) > title_length_max:
            sample_title = sample_title[:title_length_max-3] + "..."
        
        sample_description = f"Learn {primary_keyword} with our comprehensive guide. Expert tips and proven strategies to improve your results. Get started today."
        if len(sample_description) > description_length_max:
            sample_description = sample_description[:description_length_max-3] + "..."
        
        st.markdown(f"""
        <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; background: white;">
        <div style="color: #1a0dab; font-size: 18px; font-weight: normal;">{sample_title}</div>
        <div style="color: #006621; font-size: 14px;">https://example.com/article</div>
        <div style="color: #545454; font-size: 14px;">{sample_description}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Social media meta tags
    st.markdown("#### 📱 Social Media Meta Tags")
    
    social_col1, social_col2 = st.columns(2)
    
    with social_col1:
        include_social_meta = st.checkbox(
            "Include Open Graph Tags",
            value=settings.get("advanced", {}).get("include_social_meta", True),
            help="Optimize how content appears when shared on social media"
        )
    
    with social_col2:
        include_twitter_cards = st.checkbox(
            "Include Twitter Card Meta",
            value=meta.get("include_twitter_cards", True),
            help="Optimize for Twitter sharing"
        )
    
    # Update meta settings
    settings["meta_settings"] = {
        "title_length_max": title_length_max,
        "description_length_max": description_length_max,
        "title_pattern": title_pattern,
        "include_brand": include_brand,
        "brand_name": brand_name,
        "include_twitter_cards": include_twitter_cards
    }
    
    if "advanced" not in settings:
        settings["advanced"] = {}
    settings["advanced"]["include_social_meta"] = include_social_meta

def render_readability_settings():
    """Render readability and content quality settings"""
    st.markdown("### 📖 Readability & Content Quality")
    
    settings = st.session_state.seo_settings
    readability = settings.get("readability", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎓 Reading Level")
        
        target_grade_level = st.slider(
            "Target Grade Level",
            min_value=6,
            max_value=16,
            value=readability.get("target_grade_level", 8),
            step=1,
            help="Grade 8 = general audience, Grade 12 = educated audience"
        )
        
        # Grade level explanation
        grade_explanations = {
            6: "Elementary level - very simple language",
            8: "Middle school - general audience (recommended)",
            10: "High school - educated general audience",
            12: "College level - professional audience",
            14: "Graduate level - academic/technical",
            16: "Post-graduate - highly technical"
        }
        
        if target_grade_level in grade_explanations:
            st.info(f"📚 {grade_explanations[target_grade_level]}")
        
        max_sentence_length = st.slider(
            "Maximum Sentence Length (words)",
            min_value=10,
            max_value=30,
            value=readability.get("max_sentence_length", 20),
            step=1,
            help="Shorter sentences improve readability"
        )
    
    with col2:
        st.markdown("#### ✍️ Writing Quality")
        
        passive_voice_max = st.slider(
            "Maximum Passive Voice (%)",
            min_value=5,
            max_value=25,
            value=readability.get("passive_voice_max", 10),
            step=1,
            help="Lower percentages = more engaging content"
        )
        
        transition_words_min = st.slider(
            "Minimum Transition Words (%)",
            min_value=20,
            max_value=50,
            value=readability.get("transition_words_min", 30),
            step=5,
            help="Transition words improve flow and readability"
        )
        
        # Quality indicators
        st.markdown("#### 📊 Quality Targets")
        
        quality_metrics = [
            ("Sentence Length", "✅ Good" if max_sentence_length <= 20 else "⚠️ Consider shorter"),
            ("Passive Voice", "✅ Good" if passive_voice_max <= 10 else "⚠️ Reduce passive voice"),
            ("Reading Level", "✅ Good" if target_grade_level <= 10 else "⚠️ Consider simpler language"),
            ("Transitions", "✅ Good" if transition_words_min >= 25 else "⚠️ Add more transitions")
        ]
        
        for metric, status in quality_metrics:
            st.markdown(f"**{metric}:** {status}")
    
    # Advanced readability settings
    with st.expander("🔧 Advanced Readability Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            paragraph_length_max = st.slider(
                "Maximum Paragraph Length (sentences)",
                min_value=2,
                max_value=8,
                value=readability.get("paragraph_length_max", 4),
                step=1
            )
            
            subheading_frequency = st.slider(
                "Subheading Every N Paragraphs",
                min_value=2,
                max_value=6,
                value=readability.get("subheading_frequency", 3),
                step=1
            )
        
        with col2:
            bullet_points_min = st.slider(
                "Minimum Bullet Point Lists",
                min_value=0,
                max_value=5,
                value=readability.get("bullet_points_min", 2),
                step=1
            )
            
            numbered_lists_min = st.slider(
                "Minimum Numbered Lists",
                min_value=0,
                max_value=3,
                value=readability.get("numbered_lists_min", 1),
                step=1
            )
    
    # Update readability settings
    settings["readability"] = {
        "target_grade_level": target_grade_level,
        "max_sentence_length": max_sentence_length,
        "passive_voice_max": passive_voice_max,
        "transition_words_min": transition_words_min,
        "paragraph_length_max": paragraph_length_max,
        "subheading_frequency": subheading_frequency,
        "bullet_points_min": bullet_points_min,
        "numbered_lists_min": numbered_lists_min
    }

def render_advanced_settings():
    """Render advanced SEO settings"""
    st.markdown("### 🔧 Advanced SEO Features")
    
    settings = st.session_state.seo_settings
    advanced = settings.get("advanced", {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏗️ Schema & Structured Data")
        
        include_schema = st.checkbox(
            "Include Schema Markup",
            value=advanced.get("include_schema", True),
            help="Add JSON-LD structured data for rich snippets"
        )
        
        schema_types = st.multiselect(
            "Schema Types",
            ["Article", "HowTo", "FAQ", "Review", "Product"],
            default=["Article"],
            help="Types of schema markup to include"
        )
        
        include_faq = st.checkbox(
            "Generate FAQ Section",
            value=advanced.get("include_faq", False),
            help="Add FAQ section with common questions"
        )
        
        faq_questions_count = st.slider(
            "Number of FAQ Questions",
            min_value=3,
            max_value=10,
            value=advanced.get("faq_questions_count", 5),
            step=1,
            disabled=not include_faq
        )
    
    with col2:
        st.markdown("#### 🔗 Link Optimization")
        
        internal_links_min = st.slider(
            "Minimum Internal Links",
            min_value=0,
            max_value=10,
            value=advanced.get("internal_links_min", 2),
            step=1,
            help="Links to other pages on your site"
        )
        
        external_links_min = st.slider(
            "Minimum External Links",
            min_value=0,
            max_value=5,
            value=advanced.get("external_links_min", 1),
            step=1,
            help="Links to authoritative external sources"
        )
        
        link_anchor_optimization = st.checkbox(
            "Optimize Anchor Text",
            value=advanced.get("link_anchor_optimization", True),
            help="Use descriptive, keyword-rich anchor text"
        )
        
        nofollow_external = st.checkbox(
            "Add nofollow to External Links",
            value=advanced.get("nofollow_external", False),
            help="Add rel='nofollow' to external links"
        )
    
    # Image optimization
    st.markdown("#### 🖼️ Image Optimization")
    
    img_col1, img_col2 = st.columns(2)
    
    with img_col1:
        image_alt_optimization = st.checkbox(
            "Optimize Image Alt Text",
            value=advanced.get("image_alt_optimization", True),
            help="Generate SEO-friendly alt text for images"
        )
        
        images_min = st.slider(
            "Minimum Images",
            min_value=0,
            max_value=10,
            value=advanced.get("images_min", 1),
            step=1,
            help="Recommended number of images to include"
        )
    
    with img_col2:
        image_captions = st.checkbox(
            "Include Image Captions",
            value=advanced.get("image_captions", False),
            help="Add descriptive captions to images"
        )
        
        lazy_loading = st.checkbox(
            "Enable Lazy Loading",
            value=advanced.get("lazy_loading", True),
            help="Add loading='lazy' attribute to images"
        )
    
    # Performance optimization
    with st.expander("⚡ Performance & Technical SEO"):
        perf_col1, perf_col2 = st.columns(2)
        
        with perf_col1:
            minify_html = st.checkbox(
                "Minify HTML Output",
                value=advanced.get("minify_html", False),
                help="Remove unnecessary whitespace from HTML"
            )
            
            compress_images = st.checkbox(
                "Compress Images",
                value=advanced.get("compress_images", True),
                help="Optimize image file sizes"
            )
        
        with perf_col2:
            canonical_url = st.text_input(
                "Canonical URL (optional)",
                value=advanced.get("canonical_url", ""),
                placeholder="https://example.com/canonical-page",
                help="Specify the canonical version of this page"
            )
            
            robots_meta = st.selectbox(
                "Robots Meta Tag",
                ["index,follow", "index,nofollow", "noindex,follow", "noindex,nofollow"],
                index=0,
                help="Control how search engines crawl and index this page"
            )
    
    # Update advanced settings
    settings["advanced"] = {
        "include_schema": include_schema,
        "schema_types": schema_types,
        "include_faq": include_faq,
        "faq_questions_count": faq_questions_count,
        "internal_links_min": internal_links_min,
        "external_links_min": external_links_min,
        "link_anchor_optimization": link_anchor_optimization,
        "nofollow_external": nofollow_external,
        "image_alt_optimization": image_alt_optimization,
        "images_min": images_min,
        "image_captions": image_captions,
        "lazy_loading": lazy_loading,
        "minify_html": minify_html,
        "compress_images": compress_images,
        "canonical_url": canonical_url,
        "robots_meta": robots_meta
    }

def render_presets_section():
    """Render SEO presets section"""
    st.markdown("---")
    st.markdown("## 🎨 SEO Presets")
    st.markdown("Quick setup with predefined configurations for common use cases.")
    
    manager = st.session_state.seo_manager
    presets = manager.presets
    
    # Preset selection
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        selected_preset = st.selectbox(
            "Choose a Preset:",
            [""] + list(presets.keys()),
            format_func=lambda x: "Select a preset..." if x == "" else presets[x]["name"],
            key="preset_selector"
        )
    
    with col2:
        if selected_preset:
            st.info(f"📝 {presets[selected_preset]['description']}")
    
    with col3:
        if selected_preset and st.button("🚀 Apply Preset", type="primary"):
            # Apply selected preset
            current_settings = st.session_state.seo_settings
            updated_settings = manager.apply_preset(selected_preset, current_settings)
            st.session_state.seo_settings = updated_settings
            st.success(f"✅ Applied '{presets[selected_preset]['name']}' preset!")
            st.rerun()
    
    # Preset cards display
    if not selected_preset:
        st.markdown("### 📋 Available Presets")
        
        preset_cols = st.columns(3)
        
        for i, (preset_key, preset_data) in enumerate(presets.items()):
            with preset_cols[i % 3]:
                with st.container():
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; padding: 15px; border-radius: 10px; margin: 10px 0;">
                        <h4>{preset_data['name']}</h4>
                        <p style="color: #666; font-size: 14px;">{preset_data['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Apply {preset_data['name']}", key=f"apply_{preset_key}"):
                        current_settings = st.session_state.seo_settings
                        updated_settings = manager.apply_preset(preset_key, current_settings)
                        st.session_state.seo_settings = updated_settings
                        st.success(f"✅ Applied '{preset_data['name']}' preset!")
                        st.rerun()

def render_settings_actions():
    """Render settings actions (save, load, export, etc.)"""
    st.markdown("---")
    st.markdown("## 💾 Settings Management")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💾 Save Settings", type="primary"):
            save_settings_to_profile()
    
    with col2:
        if st.button("📁 Load Settings"):
            load_settings_from_profile()
    
    with col3:
        if st.button("📤 Export Settings"):
            export_settings()
    
    with col4:
        if st.button("🔄 Reset to Default"):
            reset_to_default_settings()
    
    # Settings validation
    st.markdown("### ✅ Settings Validation")
    
    manager = st.session_state.seo_manager
    is_valid, errors = manager.validate_settings(st.session_state.seo_settings)
    
    if is_valid:
        st.success("✅ All settings are valid and ready to use!")
    else:
        st.error("❌ Please fix the following issues:")
        for error in errors:
            st.error(f"• {error}")
    
    # Settings summary
    with st.expander("📊 Current Settings Summary"):
        settings = st.session_state.seo_settings
        
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown("**Keywords:**")
            st.markdown(f"• Primary: {settings.get('primary_keyword', 'Not set')}")
            st.markdown(f"• Secondary: {len(settings.get('secondary_keywords', []))} keywords")
            
            st.markdown("**Content:**")
            st.markdown(f"• Length: {settings.get('content_length', 0)} words")
            st.markdown(f"• Type: {settings.get('content_type', 'blog_post').replace('_', ' ').title()}")
            st.markdown(f"• Tone: {settings.get('tone', 'professional').title()}")
        
        with summary_col2:
            structure = settings.get('structure_settings', {})
            st.markdown("**Structure:**")
            st.markdown(f"• H2 Headings: {structure.get('h2_min', 0)}-{structure.get('h2_max', 0)}")
            st.markdown(f"• Introduction: {structure.get('intro_length', 0)} words")
            
            density = settings.get('keyword_density', {})
            st.markdown("**Density:**")
            st.markdown(f"• Primary: {density.get('primary_min', 0)}-{density.get('primary_max', 0)}%")
            st.markdown(f"• Secondary: {density.get('secondary_min', 0)}-{density.get('secondary_max', 0)}%")

def save_settings_to_profile():
    """Save current settings to user profile"""
    if not st.session_state.get('authenticated', False):
        st.warning("⚠️ Please login to save settings to your profile.")
        return
    
    try:
        # In a real implementation, this would save to a database
        # For now, we'll use session state
        if 'saved_seo_settings' not in st.session_state:
            st.session_state.saved_seo_settings = {}
        
        username = st.session_state.get('username', 'default')
        st.session_state.saved_seo_settings[username] = st.session_state.seo_settings.copy()
        
        st.success("✅ Settings saved to your profile!")
        
    except Exception as e:
        st.error(f"❌ Error saving settings: {str(e)}")

def load_settings_from_profile():
    """Load settings from user profile"""
    if not st.session_state.get('authenticated', False):
        st.warning("⚠️ Please login to load settings from your profile.")
        return
    
    try:
        username = st.session_state.get('username', 'default')
        saved_settings = st.session_state.get('saved_seo_settings', {})
        
        if username in saved_settings:
            st.session_state.seo_settings = saved_settings[username].copy()
            st.success("✅ Settings loaded from your profile!")
            st.rerun()
        else:
            st.info("ℹ️ No saved settings found in your profile.")
            
    except Exception as e:
        st.error(f"❌ Error loading settings: {str(e)}")

def export_settings():
    """Export settings as JSON file"""
    try:
        settings_data = {
            "seo_settings": st.session_state.seo_settings,
            "exported_at": datetime.now().isoformat(),
            "exported_by": st.session_state.get('username', 'anonymous'),
            "version": "1.0"
        }
        
        json_data = json.dumps(settings_data, indent=2)
        
        st.download_button(
            label="📥 Download Settings JSON",
            data=json_data,
            file_name=f"seo_settings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        st.success("✅ Settings ready for download!")
        
    except Exception as e:
        st.error(f"❌ Error exporting settings: {str(e)}")

def reset_to_default_settings():
    """Reset all settings to default values"""
    if st.button("⚠️ Confirm Reset", type="secondary", key="confirm_reset"):
        manager = st.session_state.seo_manager
        st.session_state.seo_settings = manager.default_settings.copy()
        st.success("✅ Settings reset to default values!")
        st.rerun()
    else:
        st.warning("⚠️ Click 'Confirm Reset' to reset all settings to default values.")

def render_settings_import():
    """Render settings import functionality"""
    st.markdown("### 📥 Import Settings")
    
    uploaded_file = st.file_uploader(
        "Upload Settings JSON File",
        type=['json'],
        help="Upload a previously exported settings file"
    )
    
    if uploaded_file is not None:
        try:
            settings_data = json.load(uploaded_file)
            
            if "seo_settings" in settings_data:
                # Validate imported settings
                manager = st.session_state.seo_manager
                imported_settings = settings_data["seo_settings"]
                is_valid, errors = manager.validate_settings(imported_settings)
                
                if is_valid:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.success("✅ Valid settings file detected!")
                        st.info(f"Exported: {settings_data.get('exported_at', 'Unknown')}")
                        st.info(f"By: {settings_data.get('exported_by', 'Unknown')}")
                    
                    with col2:
                        if st.button("🚀 Import Settings", type="primary"):
                            st.session_state.seo_settings = imported_settings
                            st.success("✅ Settings imported successfully!")
                            st.rerun()
                else:
                    st.error("❌ Invalid settings file:")
                    for error in errors:
                        st.error(f"• {error}")
            else:
                st.error("❌ Invalid file format. Please upload a valid settings JSON file.")
                
        except json.JSONDecodeError:
            st.error("❌ Invalid JSON file. Please check the file format.")
        except Exception as e:
            st.error(f"❌ Error importing settings: {str(e)}")

# Main interface function that includes import functionality
def render_complete_seo_settings():
    """Render complete SEO settings interface with all features"""
    render_seo_settings_interface()
    
    # Add import functionality
    with st.expander("📥 Import/Export Settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📥 Import Settings")
            render_settings_import()
        
        with col2:
            st.markdown("#### 📤 Quick Export")
            if st.button("📤 Export Current Settings"):
                export_settings()
