import streamlit as st
import re
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import json

class SEOContentGenerator:
    """Advanced SEO content generation engine"""
    
    def __init__(self):
        self.content_templates = self.load_content_templates()
        self.seo_patterns = self.load_seo_patterns()
        
    def load_content_templates(self) -> Dict:
        """Load content templates for different article types"""
        return {
            "blog_post": {
                "structure": [
                    "introduction",
                    "main_content_sections",
                    "conclusion",
                    "call_to_action"
                ],
                "intro_hooks": [
                    "Did you know that {statistic}?",
                    "Have you ever wondered {question}?",
                    "In today's {context}, {main_topic} has become more important than ever.",
                    "{Primary_keyword} is transforming the way we {action}.",
                    "The ultimate guide to {main_topic} starts here."
                ]
            },
            "review": {
                "structure": [
                    "product_overview",
                    "key_features",
                    "pros_and_cons",
                    "comparison",
                    "final_verdict"
                ],
                "intro_hooks": [
                    "Looking for an honest {product_type} review?",
                    "After {time_period} of testing {product_name}, here's what we found.",
                    "Is {product_name} worth your money? Let's find out.",
                    "{Product_name} promises {benefit} - but does it deliver?"
                ]
            },
            "how_to_guide": {
                "structure": [
                    "overview",
                    "requirements",
                    "step_by_step",
                    "tips_and_tricks",
                    "conclusion"
                ],
                "intro_hooks": [
                    "Learning {skill} doesn't have to be complicated.",
                    "Master {topic} with this comprehensive guide.",
                    "Follow these {number} simple steps to {achieve_goal}.",
                    "Ready to {action}? Here's everything you need to know."
                ]
            },
            "landing_page": {
                "structure": [
                    "headline",
                    "problem_solution",
                    "benefits",
                    "social_proof",
                    "call_to_action"
                ],
                "intro_hooks": [
                    "Transform your {area} with {solution}.",
                    "Stop struggling with {problem} - there's a better way.",
                    "Join {number}+ people who have {achieved_result}.",
                    "The {adjective} solution to {problem} is finally here."
                ]
            }
        }
    
    def load_seo_patterns(self) -> Dict:
        """Load SEO optimization patterns"""
        return {
            "title_patterns": [
                "{number} {adjective} Ways to {action} {keyword}",
                "The Ultimate Guide to {keyword} in {year}",
                "How to {action} {keyword}: {benefit}",
                "{keyword}: Everything You Need to Know",
                "{adjective} {keyword} Tips for {target_audience}",
                "Why {keyword} is {adjective} for {context}",
                "{keyword} vs {alternative}: Which is Better?"
            ],
            "heading_patterns": {
                "h2": [
                    "What is {keyword}?",
                    "Benefits of {keyword}",
                    "How to {action} {keyword}",
                    "{keyword} Best Practices",
                    "Common {keyword} Mistakes to Avoid",
                    "{keyword} Tips and Tricks",
                    "The Future of {keyword}"
                ],
                "h3": [
                    "{specific_aspect} of {keyword}",
                    "Step {number}: {action}",
                    "{keyword} for {specific_use_case}",
                    "Advanced {keyword} Techniques"
                ]
            },
            "meta_patterns": [
                "Learn {keyword} with our comprehensive guide. {benefit} in {timeframe}. {call_to_action}.",
                "Discover {adjective} {keyword} strategies that {result}. Expert tips and {benefit}.",
                "{keyword} made simple. {benefit} with proven methods. {call_to_action}.",
                "Master {keyword} with this {adjective} guide. {benefit} and {additional_benefit}."
            ]
        }
    
    def generate_seo_article(self, source_content: Dict, seo_settings: Dict) -> Dict:
        """Generate complete SEO-optimized article"""
        try:
            # Extract settings
            primary_keyword = seo_settings.get('primary_keyword', '').strip()
            secondary_keywords = seo_settings.get('secondary_keywords', [])
            content_length = seo_settings.get('content_length', 800)
            tone = seo_settings.get('tone', 'professional')
            content_type = seo_settings.get('content_type', 'blog_post')
            
            if not primary_keyword:
                return {"error": "Primary keyword is required for SEO optimization"}
            
            # Generate article components
            article_title = self.generate_seo_title(primary_keyword, content_type, source_content)
            meta_description = self.generate_meta_description(primary_keyword, content_type)
            
            # Generate structured content
            article_sections = self.generate_article_sections(
                source_content, primary_keyword, secondary_keywords, 
                content_type, tone, content_length
            )
            
            # Optimize content for SEO
            optimized_content = self.optimize_content_for_seo(
                article_sections, primary_keyword, secondary_keywords
            )
            
            # Generate additional SEO elements
            schema_markup = self.generate_schema_markup(article_title, meta_description, primary_keyword)
            seo_analysis = self.analyze_seo_score(optimized_content, primary_keyword, secondary_keywords)
            
            return {
                "title": article_title,
                "meta_description": meta_description,
                "content": optimized_content,
                "schema_markup": schema_markup,
                "seo_analysis": seo_analysis,
                "word_count": len(optimized_content.split()),
                "generated_at": datetime.now().isoformat(),
                "settings_used": seo_settings,
                "primary_keyword": primary_keyword,
                "secondary_keywords": secondary_keywords
            }
            
        except Exception as e:
            return {"error": f"Error generating content: {str(e)}"}
    
    def generate_seo_title(self, primary_keyword: str, content_type: str, source_content: Dict) -> str:
        """Generate SEO-optimized title"""
        templates = self.seo_patterns["title_patterns"]
        template = random.choice(templates)
        
        # Replace placeholders
        title = template.replace("{keyword}", primary_keyword)
        title = title.replace("{year}", str(datetime.now().year))
        title = title.replace("{number}", str(random.randint(5, 15)))
        
        # Content type specific replacements
        adjectives = {
            "blog_post": ["Essential", "Proven", "Expert", "Complete", "Advanced"],
            "review": ["Honest", "Detailed", "Comprehensive", "In-Depth", "Unbiased"],
            "how_to_guide": ["Step-by-Step", "Complete", "Beginner's", "Ultimate", "Simple"],
            "landing_page": ["Revolutionary", "Game-Changing", "Powerful", "Innovative", "Premium"]
        }
        
        actions = {
            "blog_post": ["Master", "Improve", "Optimize", "Boost", "Transform"],
            "review": ["Choose", "Compare", "Evaluate", "Select", "Find"],
            "how_to_guide": ["Learn", "Master", "Create", "Build", "Achieve"],
            "landing_page": ["Transform", "Revolutionize", "Supercharge", "Optimize", "Enhance"]
        }
        
        title = title.replace("{adjective}", random.choice(adjectives.get(content_type, adjectives["blog_post"])))
        title = title.replace("{action}", random.choice(actions.get(content_type, actions["blog_post"])))
        
        # Ensure title length is SEO-friendly (under 60 characters)
        if len(title) > 60:
            title = f"{primary_keyword}: {random.choice(['Complete Guide', 'Expert Tips', 'Best Practices'])}"
        
        return title
    
    def generate_meta_description(self, primary_keyword: str, content_type: str) -> str:
        """Generate SEO-optimized meta description"""
        templates = self.seo_patterns["meta_patterns"]
        template = random.choice(templates)
        
        # Replace placeholders
        meta = template.replace("{keyword}", primary_keyword)
        
        benefits = {
            "blog_post": ["increase engagement", "boost performance", "improve results"],
            "review": ["make informed decisions", "save time and money", "choose the best option"],
            "how_to_guide": ["get started quickly", "avoid common mistakes", "achieve better results"],
            "landing_page": ["transform your business", "increase conversions", "boost ROI"]
        }
        
        timeframes = ["minutes", "today", "this week", "quickly"]
        ctas = ["Get started now", "Learn more", "Try it today", "Download free guide"]
        
        meta = meta.replace("{benefit}", random.choice(benefits.get(content_type, benefits["blog_post"])))
        meta = meta.replace("{timeframe}", random.choice(timeframes))
        meta = meta.replace("{call_to_action}", random.choice(ctas))
        meta = meta.replace("{adjective}", random.choice(["proven", "effective", "powerful", "simple"]))
        meta = meta.replace("{result}", "deliver real results")
        meta = meta.replace("{additional_benefit}", "save time")
        
        # Ensure meta description is under 160 characters
        if len(meta) > 160:
            meta = f"Learn {primary_keyword} with our comprehensive guide. Expert tips and proven strategies to improve your results. Get started today."
        
        return meta
    
    def generate_article_sections(self, source_content: Dict, primary_keyword: str, 
                                secondary_keywords: List[str], content_type: str, 
                                tone: str, target_length: int) -> Dict:
        """Generate structured article sections"""
        
        template = self.content_templates.get(content_type, self.content_templates["blog_post"])
        source_text = source_content.get('content', '')
        
        sections = {}
        
        # Introduction
        sections["introduction"] = self.generate_introduction(
            primary_keyword, source_text, content_type, tone
        )
        
        # Main content sections
        main_sections = self.generate_main_sections(
            source_text, primary_keyword, secondary_keywords, content_type, tone
        )
        sections.update(main_sections)
        
        # Conclusion
        sections["conclusion"] = self.generate_conclusion(
            primary_keyword, content_type, tone
        )
        
        return sections
    
    def generate_introduction(self, primary_keyword: str, source_text: str, 
                            content_type: str, tone: str) -> str:
        """Generate engaging introduction"""
        
        template = self.content_templates[content_type]
        hooks = template.get("intro_hooks", [])
        hook = random.choice(hooks)
        
        # Replace placeholders in hook
        hook = hook.replace("{Primary_keyword}", primary_keyword.title())
        hook = hook.replace("{main_topic}", primary_keyword)
        
        # Generate introduction paragraph
        intro_content = f"{hook}\n\n"
        
        if source_text:
            # Extract key points from source
            sentences = source_text.split('.')[:3]
            key_points = [s.strip() for s in sentences if len(s.strip()) > 20]
            
            if key_points:
                intro_content += f"In this comprehensive guide, we'll explore {primary_keyword} and discover how it can transform your approach. "
                intro_content += f"You'll learn practical strategies, expert tips, and actionable insights to master {primary_keyword}.\n\n"
        else:
            intro_content += f"Understanding {primary_keyword} is crucial in today's competitive landscape. "
            intro_content += f"This guide will provide you with everything you need to know about {primary_keyword}, "
            intro_content += f"from basic concepts to advanced strategies.\n\n"
        
        intro_content += f"Whether you're just getting started or looking to improve your existing {primary_keyword} approach, "
        intro_content += f"this article has something valuable for you. Let's dive in!"
        
        return intro_content
    
    def generate_main_sections(self, source_text: str, primary_keyword: str, 
                             secondary_keywords: List[str], content_type: str, tone: str) -> Dict:
        """Generate main content sections"""
        
        sections = {}
        
        # Generate H2 headings
        h2_patterns = self.seo_patterns["heading_patterns"]["h2"]
        
        # Section 1: What is [keyword]
        heading1 = h2_patterns[0].replace("{keyword}", primary_keyword.title())
        sections[f"section_1"] = {
            "heading": heading1,
            "content": self.generate_definition_section(primary_keyword, source_text, tone)
        }
        
        # Section 2: Benefits
        heading2 = h2_patterns[1].replace("{keyword}", primary_keyword.title())
        sections[f"section_2"] = {
            "heading": heading2,
            "content": self.generate_benefits_section(primary_keyword, secondary_keywords, tone)
        }
        
        # Section 3: How-to
        heading3 = h2_patterns[2].replace("{keyword}", primary_keyword)
        heading3 = heading3.replace("{action}", "implement")
        sections[f"section_3"] = {
            "heading": heading3,
            "content": self.generate_howto_section(primary_keyword, source_text, tone)
        }
        
        # Section 4: Best Practices
        heading4 = h2_patterns[3].replace("{keyword}", primary_keyword.title())
        sections[f"section_4"] = {
            "heading": heading4,
            "content": self.generate_best_practices_section(primary_keyword, secondary_keywords, tone)
        }
        
        return sections
    
    def generate_definition_section(self, primary_keyword: str, source_text: str, tone: str) -> str:
        """Generate definition/overview section"""
        content = f"{primary_keyword.title()} refers to the strategic approach of optimizing and implementing "
        content += f"{primary_keyword} to achieve better results and improved performance.\n\n"
        
        if source_text:
            # Extract relevant sentences from source
            sentences = source_text.split('.')
            relevant_sentences = [s.strip() for s in sentences if primary_keyword.lower() in s.lower()][:2]
            
            if relevant_sentences:
                content += "Key characteristics include:\n\n"
                for sentence in relevant_sentences:
                    if len(sentence.strip()) > 20:
                        content += f"• {sentence.strip()}.\n"
        else:
            content += f"The core principles of effective {primary_keyword} include strategic planning, "
            content += f"consistent implementation, and continuous optimization for best results.\n\n"
        
        content += f"\nUnderstanding these fundamentals is essential for anyone looking to leverage "
        content += f"{primary_keyword} effectively in their strategy."
        
        return content
    
    def generate_benefits_section(self, primary_keyword: str, secondary_keywords: List[str], tone: str) -> str:
        """Generate benefits section"""
        benefits = [
            f"Improved efficiency and performance in {primary_keyword} implementation",
            f"Better results through strategic {primary_keyword} optimization",
            f"Increased ROI and measurable outcomes",
            f"Enhanced competitive advantage in your market",
            f"Sustainable long-term growth and success"
        ]
        
        content = f"Implementing effective {primary_keyword} strategies offers numerous advantages:\n\n"
        
        for i, benefit in enumerate(benefits[:4], 1):
            content += f"**{i}. {benefit.split(primary_keyword)[0].strip().title()}{primary_keyword}{benefit.split(primary_keyword)[1] if primary_keyword in benefit else benefit}**\n"
            
            # Add explanation
            if i == 1:
                content += f"When you optimize your {primary_keyword} approach, you'll see immediate improvements in efficiency and effectiveness.\n\n"
            elif i == 2:
                content += f"Strategic {primary_keyword} implementation leads to measurable improvements in key performance indicators.\n\n"
            elif i == 3:
                content += f"Proper {primary_keyword} strategies provide clear return on investment through improved outcomes.\n\n"
            elif i == 4:
                content += f"Stay ahead of competitors by leveraging advanced {primary_keyword} techniques and best practices.\n\n"
        
        # Include secondary keywords if available
        if secondary_keywords:
            content += f"Additionally, integrating {', '.join(secondary_keywords[:2])} with your {primary_keyword} "
            content += f"strategy can amplify these benefits and create synergistic effects."
        
        return content
    
    def generate_howto_section(self, primary_keyword: str, source_text: str, tone: str) -> str:
        """Generate how-to section"""
        content = f"Here's a step-by-step approach to implementing {primary_keyword} effectively:\n\n"
        
        steps = [
            f"**Step 1: Plan Your {primary_keyword.title()} Strategy**\n"
            f"Begin by defining clear objectives and identifying key areas where {primary_keyword} can make the biggest impact.\n\n",
            
            f"**Step 2: Implement Best Practices**\n"
            f"Apply proven {primary_keyword} techniques and methodologies that align with your specific goals and requirements.\n\n",
            
            f"**Step 3: Monitor and Optimize**\n"
            f"Track performance metrics and continuously refine your {primary_keyword} approach based on data and results.\n\n",
            
            f"**Step 4: Scale and Expand**\n"
            f"Once you've achieved success with basic {primary_keyword} implementation, expand to more advanced strategies.\n\n"
        ]
        
        content += ''.join(steps)
        
        if source_text and len(source_text) > 200:
            content += f"\n**Pro Tip:** Based on industry insights, successful {primary_keyword} implementation "
            content += f"requires consistent effort and regular optimization to maintain peak performance."
        
        return content
    
    def generate_best_practices_section(self, primary_keyword: str, secondary_keywords: List[str], tone: str) -> str:
        """Generate best practices section"""
        practices = [
            f"Always start with a clear {primary_keyword} strategy and defined goals",
            f"Regularly monitor and analyze {primary_keyword} performance metrics",
            f"Stay updated with the latest {primary_keyword} trends and developments",
            f"Focus on quality over quantity in your {primary_keyword} approach",
            f"Test and iterate different {primary_keyword} methods to find what works best"
        ]
        
        content = f"Follow these essential {primary_keyword} best practices for optimal results:\n\n"
        
        for i, practice in enumerate(practices, 1):
            content += f"**{i}. {practice.title()}**\n"
            
            if i == 1:
                content += f"Clear objectives ensure your {primary_keyword} efforts are focused and measurable.\n\n"
            elif i == 2:
                content += f"Data-driven insights help you optimize your {primary_keyword} performance continuously.\n\n"
            elif i == 3:
                content += f"Staying current with {primary_keyword} innovations keeps you competitive.\n\n"
            elif i == 4:
                content += f"Quality {primary_keyword} implementation delivers better long-term results.\n\n"
            elif i == 5:
                content += f"Continuous testing helps you discover the most effective {primary_keyword} strategies.\n\n"
        
        if secondary_keywords:
            content += f"**Remember:** Integrating {', '.join(secondary_keywords[:2])} with your {primary_keyword} "
            content += f"strategy can significantly enhance overall effectiveness and results."
        
        return content
    
    def generate_conclusion(self, primary_keyword: str, content_type: str, tone: str) -> str:
        """Generate compelling conclusion"""
        content = f"Mastering {primary_keyword} is essential for achieving outstanding results in today's competitive environment. "
        content += f"By implementing the strategies and best practices outlined in this guide, you'll be well-equipped to "
        content += f"leverage {primary_keyword} effectively and achieve your goals.\n\n"
        
        content += f"Remember, successful {primary_keyword} implementation requires consistency, patience, and continuous learning. "
        content += f"Start with the fundamentals, track your progress, and gradually implement more advanced techniques "
        content += f"as you gain experience.\n\n"
        
        # Call to action based on content type
        if content_type == "blog_post":
            content += f"Ready to take your {primary_keyword} strategy to the next level? Start implementing these techniques today "
            content += f"and watch your results improve. Share your experience in the comments below!"
        elif content_type == "how_to_guide":
            content += f"Now you have all the tools needed to succeed with {primary_keyword}. Follow the steps outlined above, "
            content += f"stay consistent, and you'll see significant improvements in your results."
        elif content_type == "review":
            content += f"Based on our comprehensive analysis, {primary_keyword} offers significant value when implemented correctly. "
            content += f"Consider your specific needs and choose the approach that best aligns with your objectives."
        else:
            content += f"Take action today and transform your {primary_keyword} approach. The strategies in this guide "
            content += f"have helped countless others achieve success - now it's your turn."
        
        return content
    
    def optimize_content_for_seo(self, sections: Dict, primary_keyword: str, secondary_keywords: List[str]) -> str:
        """Combine and optimize all sections for SEO"""
        content = ""
        
        # Add introduction
        content += sections.get("introduction", "") + "\n\n"
        
        # Add main sections with headings
        section_keys = [key for key in sections.keys() if key.startswith("section_")]
        for key in sorted(section_keys):
            section = sections[key]
            if isinstance(section, dict):
                content += f"## {section.get('heading', '')}\n\n"
                content += section.get('content', '') + "\n\n"
            else:
                content += section + "\n\n"
        
        # Add conclusion
        content += "## Conclusion\n\n"
        content += sections.get("conclusion", "") + "\n\n"
        
        # Optimize keyword density
        content = self.optimize_keyword_density(content, primary_keyword, secondary_keywords)
        
        return content.strip()
    
    def optimize_keyword_density(self, content: str, primary_keyword: str, secondary_keywords: List[str]) -> str:
        """Optimize keyword density for SEO"""
        # Target keyword density: 1-2% for primary, 0.5-1% for secondary
        words = content.split()
        total_words = len(words)
        
        if total_words == 0:
            return content
        
        # Count current keyword occurrences
        primary_count = content.lower().count(primary_keyword.lower())
        primary_density = (primary_count / total_words) * 100
        
        # If density is too low, add keyword variations
        if primary_density < 1.0:
            # Add keyword variations naturally
            variations = [
                f"effective {primary_keyword}",
                f"{primary_keyword} strategies",
                f"successful {primary_keyword}",
                f"{primary_keyword} implementation"
            ]
            
            # Insert variations naturally (this is a simplified approach)
            for variation in variations[:2]:
                if variation.lower() not in content.lower():
                    # Find a good place to insert (after a paragraph)
                    paragraphs = content.split('\n\n')
                    if len(paragraphs) > 2:
                        insert_point = len(paragraphs) // 2
                        paragraphs[insert_point] += f" When it comes to {variation}, consistency is key."
                        content = '\n\n'.join(paragraphs)
        
        return content
    
    def generate_schema_markup(self, title: str, description: str, keyword: str) -> Dict:
        """Generate JSON-LD schema markup for SEO"""
        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": description,
            "keywords": keyword,
            "author": {
                "@type": "Organization",
                "name": "SEO Content Generator"
            },
            "publisher": {
                "@type": "Organization",
                "name": "SEO Content Generator"
            },
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat()
        }
        
        return schema
    
    def analyze_seo_score(self, content: str, primary_keyword: str, secondary_keywords: List[str]) -> Dict:
        """Analyze SEO score of generated content"""
        words = content.split()
        total_words = len(words)
        
        if total_words == 0:
            return {"score": 0, "issues": ["No content to analyze"]}
        
        score = 0
        max_score = 100
        issues = []
        recommendations = []
        
        # Keyword density check
        primary_count = content.lower().count(primary_keyword.lower())
        primary_density = (primary_count / total_words) * 100
        
        if 1.0 <= primary_density <= 2.0:
            score += 20
        elif primary_density < 1.0:
            score += 10
            issues.append(f"Primary keyword density is low ({primary_density:.1f}%)")
            recommendations.append("Increase primary keyword usage naturally")
        else:
            score += 5
            issues.append(f"Primary keyword density is high ({primary_density:.1f}%)")
            recommendations.append("Reduce keyword density to avoid over-optimization")
        
        # Content length check
        if 800 <= total_words <= 2000:
            score += 20
        elif total_words < 800:
            score += 10
            issues.append(f"Content is short ({total_words} words)")
            recommendations.append("Consider adding more comprehensive information")
        else:
            score += 15
        
        # Heading structure check
        h2_count = content.count('## ')
        if h2_count >= 3:
            score += 15
        elif h2_count >= 2:
            score += 10
        else:
            issues.append("Add more H2 headings for better structure")
            recommendations.append("Include 3-5 H2 headings for optimal structure")
        
        # Keyword in headings check
        headings = re.findall(r'## (.+)', content)
        keyword_in_headings = any(primary_keyword.lower() in heading.lower() for heading in headings)
        
        if keyword_in_headings:
            score += 15
        else:
            issues.append("Primary keyword not found in headings")
            recommendations.append("Include primary keyword in at least one heading")
        
        # Secondary keywords check
        if secondary_keywords:
            secondary_found = sum(1 for kw in secondary_keywords if kw.lower() in content.lower())
            if secondary_found > 0:
                score += 10
            else:
                issues.append("Secondary keywords not found in content")
                recommendations.append("Include secondary keywords naturally in content")
        
        # Readability check (simplified)
        avg_sentence_length = total_words / max(content.count('.'), 1)
        if avg_sentence_length <= 20:
            score += 10
        else:
            issues.append("Sentences are too long on average")
            recommendations.append("Use shorter sentences for better readability")
        
        # Final score calculation
        final_score = min(score, max_score)
        
        return {
            "score": final_score,
            "keyword_density": primary_density,
            "word_count": total_words,
            "h2_count": h2_count,
            "issues": issues,
            "recommendations": recommendations,
            "grade": self.get_seo_grade(final_score)
        }
    
    def get_seo_grade(self, score: int) -> str:
        """Convert SEO score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 80:
            return "A"
        elif score >= 70:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

def render_content_generation_interface():
    """Render the content generation interface"""
    st.markdown("## 🚀 Generate SEO Content")
    
    # Check if we have content to work with
    if 'current_content' not in st.session_state or not st.session_state.current_content:
        st.warning("⚠️ No content detected. Please extract content first using the Content Input section.")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Go to Content Input", type="primary"):
                st.session_state.current_page = "generator"
                st.rerun()
        
        with col2:
            if st.button("⚙️ Configure SEO Settings", type="secondary"):
                st.session_state.current_page = "seo_settings"
                st.rerun()
        
        return
    
    # Display source content summary
    content_data = st.session_state.current_content
    
    with st.expander("📋 Source Content Summary", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📝 Words", content_data.get('word_count', 0))
        with col2:
            st.metric("⏱️ Read Time", f"{content_data.get('reading_time', 0)} min")
        with col3:
            st.metric("📰 Title", "✅" if content_data.get('title') else "❌")
        
        if content_data.get('title'):
            st.markdown(f"**Title:** {content_data['title']}")
        
        preview = content_data.get('content', '')[:200] + "..." if len(content_data.get('content', '')) > 200 else content_data.get('content', '')
        st.markdown(f"**Preview:** {preview}")
    
    # SEO Settings Quick Config
    st.markdown("### ⚙️ SEO Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
                    primary_keyword = st.text_input(
            "🎯 Primary Keyword *",
            value=st.session_state.seo_settings.get('primary_keyword', ''),
            placeholder="Enter main keyword to optimize for",
            help="The main keyword you want to rank for"
        )
        
        content_length = st.slider(
            "📏 Target Word Count",
            min_value=300,
            max_value=3000,
            value=st.session_state.seo_settings.get('content_length', 800),
            step=100,
            help="Target length for the generated article"
        )
    
    with col2:
        secondary_keywords = st.text_area(
            "🔍 Secondary Keywords",
            value='\n'.join(st.session_state.seo_settings.get('secondary_keywords', [])),
            placeholder="Enter one keyword per line\nrelated keyword 1\nrelated keyword 2",
            height=80,
            help="Related keywords to include naturally"
        )
        
        tone = st.selectbox(
            "🎭 Content Tone",
            ["professional", "conversational", "authoritative", "friendly", "technical"],
            index=["professional", "conversational", "authoritative", "friendly", "technical"].index(
                st.session_state.seo_settings.get('tone', 'professional')
            ),
            help="Writing style for the generated content"
        )
    
    # Content type selection
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
            st.session_state.seo_settings.get('content_type', 'blog_post')
        ),
        help="Type of content to generate"
    )
    
    # Update session state
    secondary_keywords_list = [kw.strip() for kw in secondary_keywords.split('\n') if kw.strip()]
    
    st.session_state.seo_settings.update({
        'primary_keyword': primary_keyword,
        'secondary_keywords': secondary_keywords_list,
        'content_length': content_length,
        'tone': tone,
        'content_type': content_type
    })
    
    # Generation controls
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Generate Article", type="primary", disabled=not primary_keyword):
            generate_article_content()
    
    with col2:
        if st.button("⚙️ Advanced Settings"):
            st.session_state.current_page = "seo_settings" 
            st.rerun()
    
    with col3:
        if st.button("🔄 Reset Settings"):
            st.session_state.seo_settings = {
                'primary_keyword': '',
                'secondary_keywords': [],
                'content_length': 800,
                'tone': 'professional',
                'content_type': 'blog_post'
            }
            st.rerun()
    
    # Display generated content if available
    if 'generated_article' in st.session_state and st.session_state.generated_article:
        display_generated_article()

def generate_article_content():
    """Generate the SEO-optimized article"""
    try:
        # Initialize generator
        if 'seo_generator' not in st.session_state:
            st.session_state.seo_generator = SEOContentGenerator()
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🔄 Initializing content generation...")
        progress_bar.progress(20)
        
        status_text.text("📝 Generating article structure...")
        progress_bar.progress(40)
        
        # Generate content
        generator = st.session_state.seo_generator
        source_content = st.session_state.current_content
        seo_settings = st.session_state.seo_settings
        
        status_text.text("🎯 Optimizing for SEO...")
        progress_bar.progress(60)
        
        result = generator.generate_seo_article(source_content, seo_settings)
        
        status_text.text("📊 Analyzing SEO score...")
        progress_bar.progress(80)
        
        if "error" in result:
            st.error(f"❌ {result['error']}")
            progress_bar.empty()
            status_text.empty()
            return
        
        # Store generated content
        st.session_state.generated_article = result
        
        # Update user stats
        if st.session_state.authenticated and 'auth_manager' in st.session_state:
            st.session_state.auth_manager.update_user_stats(
                st.session_state.username, 
                content_generated=True
            )
        
        progress_bar.progress(100)
        status_text.text("✅ Article generated successfully!")
        
        # Clear progress indicators
        import time
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
        st.success("🎉 SEO-optimized article generated successfully!")
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Error generating content: {str(e)}")

def display_generated_article():
    """Display the generated article with options to edit and download"""
    st.markdown("---")
    st.markdown("## 📄 Generated Article")
    
    article_data = st.session_state.generated_article
    
    # SEO Score Display
    seo_analysis = article_data.get('seo_analysis', {})
    score = seo_analysis.get('score', 0)
    grade = seo_analysis.get('grade', 'F')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        score_color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
        st.metric("SEO Score", f"{score_color} {score}/100")
    
    with col2:
        st.metric("Grade", f"📊 {grade}")
    
    with col3:
        st.metric("Word Count", f"📝 {article_data.get('word_count', 0)}")
    
    with col4:
        keyword_density = seo_analysis.get('keyword_density', 0)
        st.metric("Keyword Density", f"🎯 {keyword_density:.1f}%")
    
    # Article content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Article", "✏️ Edit", "📊 SEO Analysis", "💾 Export"])
    
    with tab1:
        display_article_preview(article_data)
    
    with tab2:
        display_article_editor(article_data)
    
    with tab3:
        display_seo_analysis(seo_analysis)
    
    with tab4:
        display_export_options(article_data)

def display_article_preview(article_data):
    """Display article preview"""
    st.markdown("### 📰 Article Preview")
    
    # Title
    st.markdown(f"# {article_data.get('title', 'Untitled')}")
    
    # Meta description
    if article_data.get('meta_description'):
        with st.expander("📝 Meta Description"):
            st.write(article_data['meta_description'])
    
    # Article content
    content = article_data.get('content', '')
    st.markdown(content)
    
    # Schema markup preview
    if article_data.get('schema_markup'):
        with st.expander("🔧 Schema Markup (JSON-LD)"):
            st.json(article_data['schema_markup'])

def display_article_editor(article_data):
    """Display article editor"""
    st.markdown("### ✏️ Edit Your Article")
    
    # Editable title
    edited_title = st.text_input(
        "Article Title:",
        value=article_data.get('title', ''),
        key="edit_article_title"
    )
    
    # Editable meta description
    edited_meta = st.text_area(
        "Meta Description:",
        value=article_data.get('meta_description', ''),
        height=80,
        key="edit_meta_description",
        help="Keep under 160 characters for optimal SEO"
    )
    
    # Editable content
    edited_content = st.text_area(
        "Article Content:",
        value=article_data.get('content', ''),
        height=400,
        key="edit_article_content"
    )
    
    # Save changes
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Save Changes", type="primary"):
            # Update the generated article
            st.session_state.generated_article['title'] = edited_title
            st.session_state.generated_article['meta_description'] = edited_meta
            st.session_state.generated_article['content'] = edited_content
            st.session_state.generated_article['word_count'] = len(edited_content.split())
            
            # Recalculate SEO score
            generator = st.session_state.seo_generator
            primary_keyword = article_data.get('primary_keyword', '')
            secondary_keywords = article_data.get('secondary_keywords', [])
            
            new_analysis = generator.analyze_seo_score(edited_content, primary_keyword, secondary_keywords)
            st.session_state.generated_article['seo_analysis'] = new_analysis
            
            st.success("✅ Changes saved successfully!")
            st.rerun()
    
    with col2:
        if st.button("🔄 Reset to Original"):
            st.rerun()

def display_seo_analysis(seo_analysis):
    """Display detailed SEO analysis"""
    st.markdown("### 📊 Detailed SEO Analysis")
    
    # Overall metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Keyword Density", f"{seo_analysis.get('keyword_density', 0):.1f}%")
        density = seo_analysis.get('keyword_density', 0)
        if 1.0 <= density <= 2.0:
            st.success("✅ Optimal density")
        elif density < 1.0:
            st.warning("⚠️ Low density")
        else:
            st.error("❌ Too high")
    
    with col2:
        st.metric("Word Count", seo_analysis.get('word_count', 0))
        words = seo_analysis.get('word_count', 0)
        if 800 <= words <= 2000:
            st.success("✅ Good length")
        elif words < 800:
            st.warning("⚠️ Consider longer")
        else:
            st.info("ℹ️ Very comprehensive")
    
    with col3:
        st.metric("Headings (H2)", seo_analysis.get('h2_count', 0))
        h2s = seo_analysis.get('h2_count', 0)
        if h2s >= 3:
            st.success("✅ Well structured")
        else:
            st.warning("⚠️ Add more headings")
    
    # Issues and recommendations
    issues = seo_analysis.get('issues', [])
    recommendations = seo_analysis.get('recommendations', [])
    
    if issues:
        st.markdown("#### ⚠️ Issues Found")
        for issue in issues:
            st.warning(f"• {issue}")
    
    if recommendations:
        st.markdown("#### 💡 Recommendations")
        for rec in recommendations:
            st.info(f"• {rec}")
    
    if not issues and not recommendations:
        st.success("🎉 Excellent! No major SEO issues found.")

def display_export_options(article_data):
    """Display export options"""
    st.markdown("### 💾 Export Your Article")
    
    # Export formats
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Text Formats")
        
        # Markdown export
        markdown_content = f"# {article_data.get('title', '')}\n\n"
        markdown_content += f"**Meta Description:** {article_data.get('meta_description', '')}\n\n"
        markdown_content += article_data.get('content', '')
        
        st.download_button(
            label="📄 Download as Markdown",
            data=markdown_content,
            file_name=f"{article_data.get('title', 'article').replace(' ', '_').lower()}.md",
            mime="text/markdown"
        )
        
        # HTML export
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{article_data.get('title', '')}</title>
    <meta name="description" content="{article_data.get('meta_description', '')}">
    <meta name="keywords" content="{article_data.get('primary_keyword', '')}">
</head>
<body>
    <h1>{article_data.get('title', '')}</h1>
    {article_data.get('content', '').replace('## ', '<h2>').replace('\n\n', '</p><p>').replace('\n', '<br>')}
</body>
</html>"""
        
        st.download_button(
            label="🌐 Download as HTML",
            data=html_content,
            file_name=f"{article_data.get('title', 'article').replace(' ', '_').lower()}.html",
            mime="text/html"
        )
    
    with col2:
        st.markdown("#### 🔧 SEO Data")
        
        # JSON export with all data
        full_data = {
            "article": article_data,
            "exported_at": datetime.now().isoformat(),
            "seo_settings": st.session_state.seo_settings
        }
        
        st.download_button(
            label="📊 Download SEO Data (JSON)",
            data=json.dumps(full_data, indent=2),
            file_name=f"seo_data_{article_data.get('title', 'article').replace(' ', '_').lower()}.json",
            mime="application/json"
        )
        
        # Schema markup export
        if article_data.get('schema_markup'):
            st.download_button(
                label="🏷️ Download Schema Markup",
                data=json.dumps(article_data['schema_markup'], indent=2),
                file_name=f"schema_{article_data.get('title', 'article').replace(' ', '_').lower()}.json",
                mime="application/json"
            )
    
    # Copy to clipboard options
    st.markdown("#### 📋 Quick Copy")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 Copy Title"):
            st.code(article_data.get('title', ''), language=None)
    
    with col2:
        if st.button("📝 Copy Meta Description"):
            st.code(article_data.get('meta_description', ''), language=None)
    
    with col3:
        if st.button("🎯 Copy Primary Keyword"):
            st.code(article_data.get('primary_keyword', ''), language=None)
    
    # Bulk generation option
    st.markdown("---")
    st.markdown("#### 🚀 Generate More Content")
    
    if st.button("📊 Generate Bulk Articles", type="secondary"):
        st.session_state.current_page = "bulk"
        st.rerun()
