import streamlit as st
import json
import re
import base64
import zipfile
import io
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import xml.etree.ElementTree as ET

class DownloadManager:
    """Advanced download and export management system"""
    
    def __init__(self):
        self.export_formats = {
            'markdown': 'Markdown (.md)',
            'html': 'HTML (.html)',
            'json': 'JSON Data (.json)',
            'txt': 'Plain Text (.txt)',
            'csv': 'Analytics CSV (.csv)',
            'xml': 'XML (.xml)',
            'wordpress': 'WordPress XML (.xml)',
            'medium': 'Medium Import (.html)',
            'linkedin': 'LinkedIn Article (.txt)',
            'schema': 'Schema Markup (.json)',
            'pdf_ready': 'PDF-Ready HTML (.html)',
            'email': 'Email Template (.html)',
            'social_media': 'Social Media Package (.zip)'
        }
        
        self.publishing_platforms = {
            'wordpress': 'WordPress',
            'medium': 'Medium',
            'linkedin': 'LinkedIn',
            'ghost': 'Ghost',
            'jekyll': 'Jekyll',
            'hugo': 'Hugo',
            'notion': 'Notion',
            'confluence': 'Confluence'
        }
    
    def generate_filename(self, content: Dict, format_type: str, custom_name: str = None) -> str:
        """Generate appropriate filename for export"""
        if custom_name:
            base_name = re.sub(r'[^\w\-_\.]', '_', custom_name)
        else:
            title = content.get('title', 'article')
            base_name = re.sub(r'[^\w\-_\.]', '_', title.lower())
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        extensions = {
            'markdown': '.md',
            'html': '.html',
            'json': '.json',
            'txt': '.txt',
            'csv': '.csv',
            'xml': '.xml',
            'wordpress': '_wordpress.xml',
            'medium': '_medium.html',
            'linkedin': '_linkedin.txt',
            'schema': '_schema.json',
            'pdf_ready': '_pdf.html',
            'email': '_email.html',
            'social_media': '_social.zip'
        }
        
        extension = extensions.get(format_type, '.txt')
        return f"{base_name}_{timestamp}{extension}"
    
    def export_markdown(self, content: Dict, options: Dict = None) -> str:
        """Export content as Markdown with customizable options"""
        options = options or {}
        
        markdown_content = []
        
        # Title
        title = content.get('title', 'Untitled Article')
        if options.get('include_title', True):
            markdown_content.append(f"# {title}")
            markdown_content.append("")
        
        # Meta information
        if options.get('include_meta', True):
            meta_desc = content.get('meta_description', '')
            if meta_desc:
                markdown_content.append(f"**Meta Description:** {meta_desc}")
                markdown_content.append("")
            
            # Add keywords if available
            primary_keyword = content.get('primary_keyword', '')
            secondary_keywords = content.get('secondary_keywords', [])
            if primary_keyword or secondary_keywords:
                keywords = [primary_keyword] + secondary_keywords if primary_keyword else secondary_keywords
                markdown_content.append(f"**Keywords:** {', '.join(keywords)}")
                markdown_content.append("")
        
        # Main content
        article_content = content.get('content', '')
        if options.get('clean_markdown', True):
            # Clean up markdown formatting
            article_content = self.clean_markdown_content(article_content)
        
        markdown_content.append(article_content)
        
        # Footer information
        if options.get('include_footer', True):
            markdown_content.append("")
            markdown_content.append("---")
            markdown_content.append("")
            
            generation_date = content.get('generated_at', datetime.now().isoformat())
            if generation_date:
                try:
                    gen_date = datetime.fromisoformat(generation_date.replace('Z', '+00:00'))
                    formatted_date = gen_date.strftime('%B %d, %Y at %H:%M')
                    markdown_content.append(f"*Generated on {formatted_date}*")
                except:
                    markdown_content.append(f"*Generated on {generation_date}*")
            
            if options.get('include_seo_info', False):
                seo_analysis = content.get('seo_analysis', {})
                if seo_analysis:
                    score = seo_analysis.get('score', 0)
                    grade = seo_analysis.get('grade', 'N/A')
                    markdown_content.append(f"*SEO Score: {score}/100 (Grade: {grade})*")
        
        return '\n'.join(markdown_content)
    
    def export_html(self, content: Dict, options: Dict = None) -> str:
        """Export content as HTML with advanced formatting options"""
        options = options or {}
        
        title = content.get('title', 'Untitled Article')
        meta_desc = content.get('meta_description', '')
        article_content = content.get('content', '')
        
        # Convert markdown to HTML
        html_content = self.markdown_to_html(article_content)
        
        # CSS styling options
        css_style = self.get_html_css_style(options.get('style_theme', 'modern'))
        
        # Schema markup
        schema_markup = ""
        if options.get('include_schema', True):
            schema_data = content.get('schema_markup', {})
            if schema_data:
                schema_markup = f'<script type="application/ld+json">\n{json.dumps(schema_data, indent=2)}\n</script>'
        
        # Social media meta tags
        social_meta = ""
        if options.get('include_social_meta', True):
            social_meta = self.generate_social_meta_tags(content)
        
        # HTML template
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
    {social_meta}
    {schema_markup}
    <style>
        {css_style}
    </style>
</head>
<body>
    <article class="main-content">
        <header>
            <h1>{title}</h1>
            {f'<p class="meta-description">{meta_desc}</p>' if meta_desc and options.get('show_meta_in_content', False) else ''}
        </header>
        
        <main>
            {html_content}
        </main>
        
        {self.generate_html_footer(content, options) if options.get('include_footer', True) else ''}
    </article>
</body>
</html>"""
        
        return html_template
    
    def export_json(self, content: Dict, options: Dict = None) -> str:
        """Export content as structured JSON with metadata"""
        options = options or {}
        
        export_data = {
            "metadata": {
                "title": content.get('title', ''),
                "meta_description": content.get('meta_description', ''),
                "primary_keyword": content.get('primary_keyword', ''),
                "secondary_keywords": content.get('secondary_keywords', []),
                "word_count": content.get('word_count', 0),
                "generated_at": content.get('generated_at', ''),
                "exported_at": datetime.now().isoformat()
            },
            "content": {
                "raw_content": content.get('content', ''),
                "html_content": self.markdown_to_html(content.get('content', '')) if options.get('include_html', True) else None
            },
            "seo_data": content.get('seo_analysis', {}) if options.get('include_seo', True) else {},
            "settings_used": content.get('settings_used', {}) if options.get('include_settings', False) else {},
            "schema_markup": content.get('schema_markup', {}) if options.get('include_schema', True) else {}
        }
        
        # Remove None values if specified
        if options.get('clean_json', True):
            export_data = self.clean_json_data(export_data)
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)
    
    def export_wordpress(self, content: Dict, options: Dict = None) -> str:
        """Export content as WordPress WXR format"""
        options = options or {}
        
        title = content.get('title', 'Untitled Article')
        post_content = content.get('content', '')
        meta_desc = content.get('meta_description', '')
        
        # Convert markdown to HTML for WordPress
        wp_content = self.markdown_to_html(post_content)
        
        # Generate WordPress XML
        root = ET.Element("rss")
        root.set("version", "2.0")
        root.set("xmlns:excerpt", "http://wordpress.org/export/1.2/excerpt/")
        root.set("xmlns:content", "http://purl.org/rss/1.0/modules/content/")
        root.set("xmlns:wfw", "http://wellformedweb.org/CommentAPI/")
        root.set("xmlns:dc", "http://purl.org/dc/elements/1.1/")
        root.set("xmlns:wp", "http://wordpress.org/export/1.2/")
        
        channel = ET.SubElement(root, "channel")
        
        # Channel info
        ET.SubElement(channel, "title").text = "SEO Content Generator Export"
        ET.SubElement(channel, "description").text = "Generated content export"
        ET.SubElement(channel, "wp:wxr_version").text = "1.2"
        
        # Post item
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "dc:creator").text = options.get('author', 'SEO Content Generator')
        ET.SubElement(item, "content:encoded").text = f"<![CDATA[{wp_content}]]>"
        ET.SubElement(item, "excerpt:encoded").text = f"<![CDATA[{meta_desc}]]>"
        ET.SubElement(item, "wp:post_type").text = "post"
        ET.SubElement(item, "wp:status").text = "draft"
        ET.SubElement(item, "wp:post_date").text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Add categories/tags if specified
        if options.get('categories'):
            for category in options['categories']:
                cat_elem = ET.SubElement(item, "category")
                cat_elem.set("domain", "category")
                cat_elem.set("nicename", category.lower().replace(' ', '-'))
                cat_elem.text = category
        
        return ET.tostring(root, encoding='unicode', xml_declaration=True)
    
    def export_medium(self, content: Dict, options: Dict = None) -> str:
        """Export content formatted for Medium import"""
        options = options or {}
        
        title = content.get('title', 'Untitled Article')
        article_content = content.get('content', '')
        meta_desc = content.get('meta_description', '')
        
        # Medium-specific HTML formatting
        medium_content = self.format_for_medium(article_content)
        
        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta name="description" content="{meta_desc}">
</head>
<body>
    <article>
        <h1>{title}</h1>
        {f'<p><em>{meta_desc}</em></p>' if meta_desc and options.get('include_subtitle', True) else ''}
        {medium_content}
    </article>
</body>
</html>"""
        
        return html_template
    
    def export_linkedin(self, content: Dict, options: Dict = None) -> str:
        """Export content formatted for LinkedIn articles"""
        options = options or {}
        
        title = content.get('title', 'Untitled Article')
        article_content = content.get('content', '')
        
        # LinkedIn has character limits and formatting restrictions
        linkedin_content = self.format_for_linkedin(article_content, options.get('max_length', 3000))
        
        output = f"{title}\n\n{linkedin_content}"
        
        if options.get('include_hashtags', True):
            # Generate relevant hashtags
            hashtags = self.generate_hashtags(content)
            if hashtags:
                output += f"\n\n{' '.join(hashtags)}"
        
        return output
    
    def export_social_media_package(self, content: Dict, options: Dict = None) -> bytes:
        """Export a complete social media package as ZIP file"""
        options = options or {}
        
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            
            # Main article content
            markdown_content = self.export_markdown(content, {'include_footer': False})
            zip_file.writestr("article.md", markdown_content)
            
            # Social media posts
            social_posts = self.generate_social_media_posts(content)
            
            # Twitter threads
            if 'twitter' in social_posts:
                zip_file.writestr("twitter_thread.txt", social_posts['twitter'])
            
            # Facebook post
            if 'facebook' in social_posts:
                zip_file.writestr("facebook_post.txt", social_posts['facebook'])
            
            # LinkedIn post
            if 'linkedin' in social_posts:
                zip_file.writestr("linkedin_post.txt", social_posts['linkedin'])
            
            # Instagram caption
            if 'instagram' in social_posts:
                zip_file.writestr("instagram_caption.txt", social_posts['instagram'])
            
            # Email newsletter version
            email_content = self.export_email_template(content)
            zip_file.writestr("email_newsletter.html", email_content)
            
            # Summary/excerpt
            summary = self.generate_content_summary(content, max_words=150)
            zip_file.writestr("summary.txt", summary)
            
            # Metadata file
            metadata = {
                "title": content.get('title', ''),
                "word_count": content.get('word_count', 0),
                "reading_time": max(1, round(content.get('word_count', 0) / 225)),
                "primary_keyword": content.get('primary_keyword', ''),
                "generated_at": content.get('generated_at', ''),
                "exported_at": datetime.now().isoformat()
            }
            zip_file.writestr("metadata.json", json.dumps(metadata, indent=2))
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    
    def export_email_template(self, content: Dict, options: Dict = None) -> str:
        """Export content as email newsletter template"""
        options = options or {}
        
        title = content.get('title', 'Untitled Article')
        article_content = content.get('content', '')
        meta_desc = content.get('meta_description', '')
        
        # Convert to email-friendly HTML
        email_content = self.format_for_email(article_content)
        
        # Email template with inline CSS
        email_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    
    <header style="text-align: center; margin-bottom: 30px; border-bottom: 2px solid #eee; padding-bottom: 20px;">
        <h1 style="color: #2c3e50; margin: 0;">{title}</h1>
        {f'<p style="color: #7f8c8d; font-style: italic; margin: 10px 0 0 0;">{meta_desc}</p>' if meta_desc else ''}
    </header>
    
    <main style="margin-bottom: 30px;">
        {email_content}
    </main>
    
    <footer style="border-top: 1px solid #eee; padding-top: 20px; text-align: center; color: #7f8c8d; font-size: 14px;">
        <p>Generated by SEO Content Generator</p>
        {f'<p>Reading time: {max(1, round(content.get("word_count", 0) / 225))} minutes</p>' if content.get('word_count') else ''}
    </footer>
    
</body>
</html>"""
        
        return email_template
    
    def export_analytics_csv(self, content: Dict, options: Dict = None) -> str:
        """Export content analytics as CSV"""
        options = options or {}
        
        seo_analysis = content.get('seo_analysis', {})
        
        csv_lines = [
            "Metric,Value,Description"
        ]
        
        # Basic metrics
        csv_lines.extend([
            f"Title,\"{content.get('title', '')}\",Article title",
            f"Word Count,{content.get('word_count', 0)},Total words in content",
            f"Reading Time,{max(1, round(content.get('word_count', 0) / 225))},Estimated reading time in minutes",
            f"Generated Date,{content.get('generated_at', '')},Content generation timestamp"
        ])
        
        # SEO metrics
        if seo_analysis:
            csv_lines.extend([
                f"SEO Score,{seo_analysis.get('score', 0)},Overall SEO score (0-100)",
                f"SEO Grade,{seo_analysis.get('grade', 'N/A')},SEO letter grade",
                f"Keyword Density,{seo_analysis.get('keyword_density', 0):.1f}%,Primary keyword density",
                f"H2 Count,{seo_analysis.get('h2_count', 0)},Number of H2 headings"
            ])
        
        # Keywords
        primary_keyword = content.get('primary_keyword', '')
        secondary_keywords = content.get('secondary_keywords', [])
        
        if primary_keyword:
            csv_lines.append(f"Primary Keyword,\"{primary_keyword}\",Main target keyword")
        
        if secondary_keywords:
            csv_lines.append(f"Secondary Keywords,\"{'; '.join(secondary_keywords)}\",Additional target keywords")
        
        return '\n'.join(csv_lines)
    
    def clean_markdown_content(self, content: str) -> str:
        """Clean and optimize markdown content"""
        # Remove excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        # Ensure proper heading spacing
        content = re.sub(r'\n(#{1,6}\s)', r'\n\n\1', content)
        content = re.sub(r'(#{1,6}\s.+)\n([^\n#])', r'\1\n\n\2', content)
        
        # Clean up list formatting
        content = re.sub(r'\n([•\-\*]\s)', r'\n\1', content)
        content = re.sub(r'\n(\d+\.\s)', r'\n\1', content)
        
        return content.strip()
    
    def markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown content to HTML"""
        html_content = markdown_content
        
        # Headers
        html_content = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html_content, flags=re.MULTILINE)
        
        # Bold and italic
        html_content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html_content)
        html_content = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html_content)
        
        # Links
        html_content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', html_content)
        
        # Bullet points
        html_content = re.sub(r'^[•\-\*] (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
        html_content = re.sub(r'(<li>.*</li>)', r'<ul>\1</ul>', html_content, flags=re.DOTALL)
        html_content = re.sub(r'</li>\n<li>', r'</li><li>', html_content)
        
        # Numbered lists
        html_content = re.sub(r'^\d+\. (.+)$', r'<li>\1</li>', html_content, flags=re.MULTILINE)
        
        # Paragraphs
        paragraphs = html_content.split('\n\n')
        formatted_paragraphs = []
        
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('<'):
                para = f'<p>{para}</p>'
            formatted_paragraphs.append(para)
        
        return '\n\n'.join(formatted_paragraphs)
    
    def get_html_css_style(self, theme: str = 'modern') -> str:
        """Get CSS styles for HTML export"""
        
        styles = {
            'modern': """
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: #fff;
                }
                
                .main-content {
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    padding: 40px;
                }
                
                h1 {
                    color: #2c3e50;
                    font-size: 2.5em;
                    margin-bottom: 0.5em;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 0.3em;
                }
                
                h2 {
                    color: #34495e;
                    font-size: 1.8em;
                    margin-top: 2em;
                    margin-bottom: 1em;
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                }
                
                h3 {
                    color: #34495e;
                    font-size: 1.4em;
                    margin-top: 1.5em;
                    margin-bottom: 0.8em;
                }
                
                p {
                    margin-bottom: 1.2em;
                    text-align: justify;
                }
                
                ul, ol {
                    margin-bottom: 1.2em;
                    padding-left: 2em;
                }
                
                li {
                    margin-bottom: 0.5em;
                }
                
                strong {
                    color: #2c3e50;
                    font-weight: 600;
                }
                
                .meta-description {
                    font-style: italic;
                    color: #7f8c8d;
                    font-size: 1.1em;
                    margin-bottom: 2em;
                    border-left: 3px solid #95a5a6;
                    padding-left: 15px;
                }
                
                .footer {
                    margin-top: 3em;
                    padding-top: 2em;
                    border-top: 1px solid #ecf0f1;
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 0.9em;
                }
            """,
            
            'minimal': """
                body {
                    font-family: Georgia, serif;
                    line-height: 1.8;
                    color: #333;
                    max-width: 700px;
                    margin: 0 auto;
                    padding: 40px 20px;
                }
                
                h1, h2, h3 {
                    color: #000;
                    font-weight: normal;
                }
                
                h1 {
                    font-size: 2.2em;
                    margin-bottom: 1em;
                }
                
                h2 {
                    font-size: 1.6em;
                    margin-top: 2em;
                    margin-bottom: 1em;
                }
                
                p {
                    margin-bottom: 1.5em;
                }
            """,
            
            'professional': """
                body {
                    font-family: 'Times New Roman', serif;
                    line-height: 1.6;
                    color: #000;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: #fff;
                }
                
                h1 {
                    font-size: 2.2em;
                    text-align: center;
                    margin-bottom: 1em;
                    font-weight: bold;
                }
                
                h2 {
                    font-size: 1.5em;
                    margin-top: 2em;
                    margin-bottom: 1em;
                    font-weight: bold;
                }
                
                p {
                    text-align: justify;
                    margin-bottom: 1em;
                }
            """
        }
        
        return styles.get(theme, styles['modern'])
    
    def generate_social_meta_tags(self, content: Dict) -> str:
        """Generate social media meta tags"""
        title = content.get('title', '')
        description = content.get('meta_description', '')
        
        meta_tags = f"""
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="{title}">
    <meta property="twitter:description" content="{description}">
        """
        
        return meta_tags.strip()
    
    def generate_html_footer(self, content: Dict, options: Dict) -> str:
        """Generate HTML footer"""
        footer_items = []
        
        if options.get('include_generation_date', True):
            gen_date = content.get('generated_at', datetime.now().isoformat())
            try:
                date_obj = datetime.fromisoformat(gen_date.replace('Z', '+00:00'))
                formatted_date = date_obj.strftime('%B %d, %Y')
                footer_items.append(f"Generated on {formatted_date}")
            except:
                footer_items.append(f"Generated on {gen_date}")
        
        if options.get('include_word_count', True):
            word_count = content.get('word_count', 0)
            reading_time = max(1, round(word_count / 225))
            footer_items.append(f"{word_count} words • {reading_time} min read")
        
        if options.get('include_seo_score', False):
            seo_analysis = content.get('seo_analysis', {})
            if seo_analysis:
                score = seo_analysis.get('score', 0)
                grade = seo_analysis.get('grade', 'N/A')
                footer_items.append(f"SEO Score: {score}/100 ({grade})")
        
        footer_content = " • ".join(footer_items)
        
        return f'<footer class="footer"><p>{footer_content}</p></footer>' if footer_content else ''
    
    def format_for_medium(self, content: str) -> str:
        """Format content specifically for Medium platform"""
        # Medium prefers certain formatting
        formatted = self.markdown_to_html(content)
        
        # Medium-specific adjustments
        formatted = formatted.replace('<h1>', '<h2>')  # Medium uses h1 for title
        formatted = formatted.replace('</h1>', '</h2>')
        
        return formatted
    
    def format_for_linkedin(self, content: str, max_length: int = 3000) -> str:
        """Format content for LinkedIn with length restrictions"""
        # Convert to plain text
        text_content = re.sub(r'#{1,6}\s', '', content)  # Remove markdown headers
        text_content = re.sub(r'\*\*(.+?)\*\*', r'\1', text_content)  # Remove bold
        text_content = re.sub(r'\*(.+?)\*', r'\1', text_content)  # Remove italic
        
        # Truncate if too long
        if len(text_content) > max_length:
            text_content = text_content[:max_length-3] + "..."
        
        return text_content
    
    def format_for_email(self, content: str) -> str:
        """Format content for email with inline styles"""
        html_content = self.markdown_to_html(content)
        
        # Add inline styles for email compatibility
        html_content = html_content.replace('<h2>', '<h2 style="color: #2c3e50; margin-top: 30px; margin-bottom: 15px;">')
        html_content = html_content.replace('<h3>', '<h3 style="color: #34495e; margin-top: 25px; margin-bottom: 12px;">')
        html_content = html_content.replace('<p>', '<p style="margin-bottom: 15px; line-height: 1.6;">')
        html_content = html_content.replace('<strong>', '<strong style="color: #2c3e50;">')
        html_content = html_content.replace('<ul>', '<ul style="margin-bottom: 15px; padding-left: 25px;">')
        html_content = html_content.replace('<ol>', '<ol style="margin-bottom: 15px; padding-left: 25px;">')
        html_content = html_content.replace('<li>', '<li style="margin-bottom: 8px;">')
        
        return html_content
    
    def generate_social_media_posts(self, content: Dict) -> Dict[str, str]:
        """Generate social media posts for different platforms"""
        title = content.get('title', '')
        meta_desc = content.get('meta_description', '')
        primary_keyword = content.get('primary_keyword', '')
        
        posts = {}
        
        # Twitter thread (280 chars per tweet)
        twitter_thread = self.create_twitter_thread(title, meta_desc, content.get('content', ''))
        posts['twitter'] = twitter_thread
        
        # Facebook post (longer format)
        facebook_post = f"{title}\n\n{meta_desc}\n\n"
        facebook_post += self.generate_content_summary(content, max_words=100)
        if primary_keyword:
            facebook_post += f"\n\n#{primary_keyword.replace(' ', '')}"
        posts['facebook'] = facebook_post
        
        # LinkedIn post (professional format)
        linkedin_post = f"📝 {title}\n\n{meta_desc}\n\n"
        linkedin_post += "Key insights from this article:\n"
        linkedin_post += self.extract_key_points(content.get('content', ''), max_points=3)
        posts['linkedin'] = linkedin_post
        
        # Instagram caption
        instagram_caption = f"{title}\n\n{meta_desc[:100]}..."
        hashtags = self.generate_hashtags(content)
        if hashtags:
            instagram_caption += f"\n\n{' '.join(hashtags[:10])}"  # Instagram limit
        posts['instagram'] = instagram_caption
        
        return posts
    
    def create_twitter_thread(self, title: str, description: str, content: str) -> str:
        """Create a Twitter thread from content"""
        tweets = []
        
        # First tweet - hook
        tweet1 = f"🧵 {title}\n\n{description[:200]}..."
        tweets.append(f"1/{len(tweets)+3} {tweet1}")
        
        # Extract key points for subsequent tweets
        key_points = self.extract_key_points(content, max_points=5)
        
        for i, point in enumerate(key_points.split('\n')[:4], 2):
            if point.strip():
                tweet = f"{i}/{len(tweets)+2} {point.strip()[:250]}"
                tweets.append(tweet)
        
        # Final tweet - CTA
        final_tweet = f"{len(tweets)+1}/{len(tweets)+1} What do you think about this? Share your thoughts below! 👇"
        tweets.append(final_tweet)
        
        return '\n\n---\n\n'.join(tweets)
    
    def extract_key_points(self, content: str, max_points: int = 5) -> str:
        """Extract key points from content"""
        # Look for bullet points or numbered lists first
        bullet_points = re.findall(r'^[•\-\*] (.+), content, re.MULTILINE)
        if bullet_points:
            return '\n'.join([f"• {point}" for point in bullet_points[:max_points]])
        
        # Extract from headings
        headings = re.findall(r'^## (.+), content, re.MULTILINE)
        if headings:
            return '\n'.join([f"• {heading}" for heading in headings[:max_points]])
        
        # Extract from paragraphs (simplified)
        paragraphs = content.split('\n\n')
        key_sentences = []
        
        for para in paragraphs[:max_points]:
            sentences = para.split('.')
            if sentences and len(sentences[0]) > 20:
                key_sentences.append(f"• {sentences[0].strip()}")
        
        return '\n'.join(key_sentences[:max_points])
    
    def generate_hashtags(self, content: Dict) -> List[str]:
        """Generate relevant hashtags from content"""
        hashtags = []
        
        # From primary keyword
        primary_keyword = content.get('primary_keyword', '')
        if primary_keyword:
            hashtags.append(f"#{primary_keyword.replace(' ', '')}")
        
        # From secondary keywords
        secondary_keywords = content.get('secondary_keywords', [])
        for keyword in secondary_keywords[:3]:
            hashtags.append(f"#{keyword.replace(' ', '')}")
        
        # Content type hashtags
        content_type = content.get('content_type', '')
        type_hashtags = {
            'blog_post': ['#blogging', '#content'],
            'how_to_guide': ['#howto', '#tutorial'],
            'review': ['#review', '#recommendation'],
            'landing_page': ['#marketing', '#conversion']
        }
        
        if content_type in type_hashtags:
            hashtags.extend(type_hashtags[content_type])
        
        # General hashtags
        hashtags.extend(['#SEO', '#contentmarketing'])
        
        return hashtags[:15]  # Reasonable limit
    
    def generate_content_summary(self, content: Dict, max_words: int = 150) -> str:
        """Generate a concise summary of the content"""
        full_content = content.get('content', '')
        
        # Extract first paragraph or introduction
        paragraphs = full_content.split('\n\n')
        
        for para in paragraphs:
            if len(para.split()) > 20:  # Skip very short paragraphs
                words = para.split()
                if len(words) <= max_words:
                    return para.strip()
                else:
                    return ' '.join(words[:max_words]) + "..."
        
        # Fallback to meta description
        meta_desc = content.get('meta_description', '')
        if meta_desc:
            return meta_desc
        
        # Last resort - create from title
        title = content.get('title', '')
        return f"An in-depth article about {title.lower()}."
    
    def clean_json_data(self, data: Any) -> Any:
        """Recursively remove None values from JSON data"""
        if isinstance(data, dict):
            return {k: self.clean_json_data(v) for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [self.clean_json_data(item) for item in data if item is not None]
        else:
            return data

def render_download_interface():
    """Render the comprehensive download and export interface"""
    st.markdown("## 📥 Download & Export")
    st.markdown("Export your content in multiple formats for various platforms and use cases.")
    
    # Check if we have content to download
    if 'generated_article' not in st.session_state or not st.session_state.generated_article:
        st.warning("⚠️ No content available for download. Please generate an article first.")
        
        if st.button("🚀 Go to Content Generation", type="primary"):
            st.session_state.current_page = "generate"
            st.rerun()
        return
    
    # Initialize download manager
    download_manager = DownloadManager()
    content = st.session_state.generated_article
    
    # Download interface tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Document Formats", "🌐 Publishing Platforms", "📱 Social Media", "📊 Analytics & Data"
    ])
    
    with tab1:
        render_document_formats(download_manager, content)
    
    with tab2:
        render_publishing_platforms(download_manager, content)
    
    with tab3:
        render_social_media_exports(download_manager, content)
    
    with tab4:
        render_analytics_exports(download_manager, content)
    
    # Bulk download option
    render_bulk_download_section(download_manager, content)

def render_document_formats(download_manager: DownloadManager, content: Dict):
    """Render document format downloads"""
    st.markdown("### 📄 Document Formats")
    st.markdown("Download your content in various document formats for different uses.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Text Formats")
        
        # Markdown export options
        with st.expander("📋 Markdown Options"):
            md_include_meta = st.checkbox("Include metadata", value=True, key="md_meta")
            md_include_footer = st.checkbox("Include footer", value=True, key="md_footer")
            md_clean_format = st.checkbox("Clean formatting", value=True, key="md_clean")
            md_include_seo = st.checkbox("Include SEO info", value=False, key="md_seo")
        
        md_options = {
            'include_meta': md_include_meta,
            'include_footer': md_include_footer,
            'clean_markdown': md_clean_format,
            'include_seo_info': md_include_seo
        }
        
        markdown_content = download_manager.export_markdown(content, md_options)
        filename = download_manager.generate_filename(content, 'markdown')
        
        st.download_button(
            "📝 Download Markdown",
            data=markdown_content,
            file_name=filename,
            mime="text/markdown",
            use_container_width=True
        )
        
        # Plain text export
        plain_text = content.get('content', '').replace('#', '').replace('*', '')
        txt_filename = download_manager.generate_filename(content, 'txt')
        
        st.download_button(
            "📄 Download Plain Text",
            data=plain_text,
            file_name=txt_filename,
            mime="text/plain",
            use_container_width=True
        )
    
    with col2:
        st.markdown("#### 🌐 Web Formats")
        
        # HTML export options
        with st.expander("🎨 HTML Styling Options"):
            html_theme = st.selectbox("Style theme:", ['modern', 'minimal', 'professional'], key="html_theme")
            html_include_schema = st.checkbox("Include schema markup", value=True, key="html_schema")
            html_include_social = st.checkbox("Include social meta tags", value=True, key="html_social")
            html_include_footer = st.checkbox("Include footer", value=True, key="html_footer")
            html_show_meta = st.checkbox("Show meta description in content", value=False, key="html_meta_content")
        
        html_options = {
            'style_theme': html_theme,
            'include_schema': html_include_schema,
            'include_social_meta': html_include_social,
            'include_footer': html_include_footer,
            'show_meta_in_content': html_show_meta
        }
        
        html_content = download_manager.export_html(content, html_options)
        html_filename = download_manager.generate_filename(content, 'html')
        
        st.download_button(
            "🌐 Download HTML",
            data=html_content,
            file_name=html_filename,
            mime="text/html",
            use_container_width=True
        )
        
        # PDF-ready HTML
        pdf_html = download_manager.export_html(content, {
            'style_theme': 'professional',
            'include_schema': False,
            'include_social_meta': False
        })
        pdf_filename = download_manager.generate_filename(content, 'pdf_ready')
        
        st.download_button(
            "📄 Download PDF-Ready HTML",
            data=pdf_html,
            file_name=pdf_filename,
            mime="text/html",
            use_container_width=True,
            help="Optimized for PDF conversion tools"
        )
    
    # Preview section
    st.markdown("#### 👁️ Format Preview")
    
    preview_format = st.selectbox("Preview format:", ['Markdown', 'HTML'], key="preview_format")
    
    if preview_format == 'Markdown':
        with st.expander("📋 Markdown Preview"):
            st.code(markdown_content[:1000] + "..." if len(markdown_content) > 1000 else markdown_content, language="markdown")
    
    else:  # HTML
        with st.expander("🌐 HTML Preview"):
            st.components.v1.html(html_content[:2000] + "..." if len(html_content) > 2000 else html_content, height=400, scrolling=True)

def render_publishing_platforms(download_manager: DownloadManager, content: Dict):
    """Render publishing platform specific exports"""
    st.markdown("### 🌐 Publishing Platforms")
    st.markdown("Export content optimized for specific publishing platforms.")
    
    platform_col1, platform_col2 = st.columns(2)
    
    with platform_col1:
        st.markdown("#### 📰 Blog Platforms")
        
        # WordPress export
        st.markdown("**WordPress**")
        wp_author = st.text_input("Author name:", value="Content Creator", key="wp_author")
        wp_categories = st.text_input("Categories (comma-separated):", key="wp_categories")
        
        wp_options = {
            'author': wp_author,
            'categories': [cat.strip() for cat in wp_categories.split(',') if cat.strip()]
        }
        
        wp_content = download_manager.export_wordpress(content, wp_options)
        wp_filename = download_manager.generate_filename(content, 'wordpress')
        
        st.download_button(
            "📱 WordPress WXR",
            data=wp_content,
            file_name=wp_filename,
            mime="application/xml",
            use_container_width=True,
            help="Import this file in WordPress admin"
        )
        
        # Medium export
        st.markdown("**Medium**")
        medium_include_subtitle = st.checkbox("Include subtitle", value=True, key="medium_subtitle")
        
        medium_options = {'include_subtitle': medium_include_subtitle}
        medium_content = download_manager.export_medium(content, medium_options)
        medium_filename = download_manager.generate_filename(content, 'medium')
        
        st.download_button(
            "📝 Medium HTML",
            data=medium_content,
            file_name=medium_filename,
            mime="text/html",
            use_container_width=True
        )
    
    with platform_col2:
        st.markdown("#### 💼 Professional Platforms")
        
        # LinkedIn export
        st.markdown("**LinkedIn Articles**")
        linkedin_max_length = st.slider("Max length (characters):", 1000, 5000, 3000, key="linkedin_length")
        linkedin_hashtags = st.checkbox("Include hashtags", value=True, key="linkedin_hashtags")
        
        linkedin_options = {
            'max_length': linkedin_max_length,
            'include_hashtags': linkedin_hashtags
        }
        
        linkedin_content = download_manager.export_linkedin(content, linkedin_options)
        linkedin_filename = download_manager.generate_filename(content, 'linkedin')
        
        st.download_button(
            "💼 LinkedIn Article",
            data=linkedin_content,
            file_name=linkedin_filename,
            mime="text/plain",
            use_container_width=True
        )
        
        # Email newsletter
        st.markdown("**Email Newsletter**")
        email_content = download_manager.export_email_template(content)
        email_filename = download_manager.generate_filename(content, 'email')
        
        st.download_button(
            "📧 Email Template",
            data=email_content,
            file_name=email_filename,
            mime="text/html",
            use_container_width=True,
            help="Ready for email marketing platforms"
        )
    
    # Platform-specific tips
    st.markdown("#### 💡 Platform Tips")
    
    tips_col1, tips_col2, tips_col3 = st.columns(3)
    
    with tips_col1:
        st.info("""
        **WordPress:**
        • Import via Tools > Import
        • Content will be saved as draft
        • Review before publishing
        """)
    
    with tips_col2:
        st.info("""
        **Medium:**
        • Use import feature in settings
        • Add featured image after import
        • Adjust formatting as needed
        """)
    
    with tips_col3:
        st.info("""
        **LinkedIn:**
        • Paste into article editor
        • Add relevant hashtags
        • Engage with comments
        """)

def render_social_media_exports(download_manager: DownloadManager, content: Dict):
    """Render social media specific exports"""
    st.markdown("### 📱 Social Media Content")
    st.markdown("Generate content optimized for different social media platforms.")
    
    # Generate social media posts
    social_posts = download_manager.generate_social_media_posts(content)
    
    social_col1, social_col2 = st.columns(2)
    
    with social_col1:
        st.markdown("#### 🐦 Twitter")
        
        if 'twitter' in social_posts:
            st.text_area(
                "Twitter Thread:",
                value=social_posts['twitter'],
                height=200,
                key="twitter_preview"
            )
            
            st.download_button(
                "📱 Download Twitter Thread",
                data=social_posts['twitter'],
                file_name=f"twitter_thread_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        st.markdown("#### 📘 Facebook")
        
        if 'facebook' in social_posts:
            st.text_area(
                "Facebook Post:",
                value=social_posts['facebook'],
                height=150,
                key="facebook_preview"
            )
            
            st.download_button(
                "📘 Download Facebook Post",
                data=social_posts['facebook'],
                file_name=f"facebook_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    with social_col2:
        st.markdown("#### 💼 LinkedIn")
        
        if 'linkedin' in social_posts:
            st.text_area(
                "LinkedIn Post:",
                value=social_posts['linkedin'],
                height=200,
                key="linkedin_social_preview"
            )
            
            st.download_button(
                "💼 Download LinkedIn Post",
                data=social_posts['linkedin'],
                file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        st.markdown("#### 📸 Instagram")
        
        if 'instagram' in social_posts:
            st.text_area(
                "Instagram Caption:",
                value=social_posts['instagram'],
                height=150,
                key="instagram_preview"
            )
            
            st.download_button(
                "📸 Download Instagram Caption",
                data=social_posts['instagram'],
                file_name=f"instagram_caption_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    # Complete social media package
    st.markdown("#### 📦 Complete Social Media Package")
    
    st.info("📱 Download all social media content in one convenient package")
    
    if st.button("🎁 Generate Social Media Package", type="primary"):
        social_package = download_manager.export_social_media_package(content)
        package_filename = download_manager.generate_filename(content, 'social_media')
        
        st.download_button(
            "📦 Download Complete Package",
            data=social_package,
            file_name=package_filename,
            mime="application/zip",
            use_container_width=True,
            help="Contains posts for all platforms plus email template and metadata"
        )

def render_analytics_exports(download_manager: DownloadManager, content: Dict):
    """Render analytics and data exports"""
    st.markdown("### 📊 Analytics & Data")
    st.markdown("Export content analytics and structured data for analysis.")
    
    analytics_col1, analytics_col2 = st.columns(2)
    
    with analytics_col1:
        st.markdown("#### 📈 Content Analytics")
        
        # CSV analytics export
        csv_content = download_manager.export_analytics_csv(content)
        csv_filename = download_manager.generate_filename(content, 'csv')
        
        st.download_button(
            "📊 Download Analytics CSV",
            data=csv_content,
            file_name=csv_filename,
            mime="text/csv",
            use_container_width=True
        )
        
        # Preview analytics
        with st.expander("📋 Analytics Preview"):
            st.text(csv_content)
        
        # Schema markup export
        schema_data = content.get('schema_markup', {})
        if schema_data:
            schema_json = json.dumps(schema_data, indent=2)
            schema_filename = download_manager.generate_filename(content, 'schema')
            
            st.download_button(
                "🏷️ Download Schema Markup",
                data=schema_json,
                file_name=schema_filename,
                mime="application/json",
                use_container_width=True
            )
    
    with analytics_col2:
        st.markdown("#### 🗄️ Structured Data")
        
        # JSON export options
        with st.expander("⚙️ JSON Export Options"):
            json_include_html = st.checkbox("Include HTML content", value=True, key="json_html")
            json_include_seo = st.checkbox("Include SEO analysis", value=True, key="json_seo")
            json_include_settings = st.checkbox("Include generation settings", value=False, key="json_settings")
            json_include_schema = st.checkbox("Include schema markup", value=True, key="json_schema")
            json_clean = st.checkbox("Clean JSON (remove nulls)", value=True, key="json_clean")
        
        json_options = {
            'include_html': json_include_html,
            'include_seo': json_include_seo,
            'include_settings': json_include_settings,
            'include_schema': json_include_schema,
            'clean_json': json_clean
        }
        
        json_content = download_manager.export_json(content, json_options)
        json_filename = download_manager.generate_filename(content, 'json')
        
        st.download_button(
            "📄 Download JSON Data",
            data=json_content,
            file_name=json_filename,
            mime="application/json",
            use_container_width=True
        )
        
        # JSON preview
        with st.expander("👁️ JSON Preview"):
            preview_data = json.loads(json_content)
            st.json(preview_data)

def render_bulk_download_section(download_manager: DownloadManager, content: Dict):
    """Render bulk download options"""
    st.markdown("---")
    st.markdown("## 📦 Bulk Download Options")
    st.markdown("Download multiple formats or create custom packages.")
    
    bulk_col1, bulk_col2 = st.columns(2)
    
    with bulk_col1:
        st.markdown("#### 🎯 Quick Packages")
        
        # Blogger package
        if st.button("📝 Blogger Package", use_container_width=True):
            st.info("Creating blogger package: Markdown + HTML + Social posts")
            # This would create a zip with multiple formats
        
        # Marketer package  
        if st.button("📈 Marketer Package", use_container_width=True):
            st.info("Creating marketer package: All social media + Email + Analytics")
        
        # Developer package
        if st.button("👨‍💻 Developer Package", use_container_width=True):
            st.info("Creating developer package: JSON + Schema + Raw data")
    
    with bulk_col2:
        st.markdown("#### 🛠️ Custom Package")
        
        st.markdown("**Select formats to include:**")
        
        format_options = {
            'markdown': st.checkbox("📝 Markdown", value=True, key="bulk_md"),
            'html': st.checkbox("🌐 HTML", value=True, key="bulk_html"), 
            'json': st.checkbox("📄 JSON", value=False, key="bulk_json"),
            'social': st.checkbox("📱 Social Media", value=True, key="bulk_social"),
            'email': st.checkbox("📧 Email Template", value=False, key="bulk_email"),
            'analytics': st.checkbox("📊 Analytics", value=False, key="bulk_analytics")
        }
        
        selected_formats = [fmt for fmt, selected in format_options.items() if selected]
        
        if selected_formats and st.button("🎁 Create Custom Package", type="primary", use_container_width=True):
            st.success(f"✅ Creating package with {len(selected_formats)} formats...")
            # This would create a custom zip file
    
    # Download history
    with st.expander("📚 Download History"):
        st.info("Download history feature will track your exports and allow re-downloading previous packages.")

# Main interface function
def render_complete_download_manager():
    """Render complete download management interface"""
    render_download_interface()
