import streamlit as st
import re
import json
import math
from datetime import datetime
from typing import Dict, List, Tuple, Any
from collections import Counter
from urllib.parse import urlparse
import nltk
from textstat import flesch_reading_ease, flesch_kincaid_grade

class SEOAnalyzer:
    """Advanced SEO analysis and scoring system"""

    def __init__(self):
        self.scoring_weights = {
            'title_optimization': 15,
            'meta_description': 10,
            'keyword_optimization': 20,
            'content_structure': 15,
            'readability': 10,
            'content_length': 10,
            'internal_links': 5,
            'image_optimization': 5,
            'schema_markup': 5,
            'technical_seo': 5
        }

        self.keyword_density_targets = {
            'primary': {'min': 1.0, 'max': 3.0, 'optimal': 1.5},
            'secondary': {'min': 0.5, 'max': 2.0, 'optimal': 1.0},
            'related': {'min': 0.2, 'max': 1.0, 'optimal': 0.5}
        }

        self.content_length_targets = {
            'blog_post': {'min': 800, 'optimal': 1500, 'max': 3000},
            'how_to_guide': {'min': 1200, 'optimal': 2000, 'max': 4000},
            'review': {'min': 1000, 'optimal': 1800, 'max': 3500},
            'landing_page': {'min': 600, 'optimal': 1200, 'max': 2000}
        }

        self.stop_words = {
            'en': ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is',
                   'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                   'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
                   'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them']
        }

    def analyze_content_comprehensive(self, content_data: Dict, seo_settings: Dict) -> Dict:
        """Perform comprehensive SEO analysis of content"""
        results = {
            'overall_score': 0,
            'grade': 'F',
            'category_scores': {},
            'recommendations': [],
            'issues': [],
            'strengths': [],
            'detailed_analysis': {},
            'competitive_analysis': {},
            'optimization_opportunities': [],
            'technical_metrics': {},
            'analyzed_at': datetime.now().isoformat()
        }
        try:
            title = content_data.get('title', '')
            content = content_data.get('content', '')
            meta_desc = content_data.get('meta_description', '')
            primary_kw = seo_settings.get('primary_keyword', '')
            secondary_kws = seo_settings.get('secondary_keywords', [])
            content_type = seo_settings.get('content_type', 'blog_post')

            # Individual analyses
            title_a = self.analyze_title_optimization(title, primary_kw)
            meta_a = self.analyze_meta_description(meta_desc, primary_kw)
            kw_a = self.analyze_keyword_optimization(content, primary_kw, secondary_kws)
            struct_a = self.analyze_content_structure(content, content_type)
            read_a = self.analyze_readability(content)
            length_a = self.analyze_content_length(content, content_type)
            links_a = self.analyze_links(content)
            img_a = self.analyze_images(content_data)
            schema_a = self.analyze_schema_markup(content_data)
            tech_a = self.analyze_technical_seo(content_data, seo_settings)

            detailed = {
                'title_optimization': title_a,
                'meta_description': meta_a,
                'keyword_optimization': kw_a,
                'content_structure': struct_a,
                'readability': read_a,
                'content_length': length_a,
                'internal_links': links_a,
                'image_optimization': img_a,
                'schema_markup': schema_a,
                'technical_seo': tech_a
            }
            results['detailed_analysis'] = detailed

            for cat, analy in detailed.items():
                results['category_scores'][cat] = analy.get('score', 0)
            overall = self.calculate_overall_score(results['category_scores'])
            results['overall_score'] = overall
            results['grade'] = self.score_to_grade(overall)

            results['recommendations'] = self.generate_recommendations(detailed)
            results['issues'] = self.identify_issues(detailed)
            results['strengths'] = self.identify_strengths(detailed)
            results['optimization_opportunities'] = self.identify_optimization_opportunities(detailed, seo_settings)
            results['technical_metrics'] = self.calculate_technical_metrics(content, content_data)
            results['competitive_analysis'] = self.perform_basic_competitive_analysis(
                primary_kw, content_type, len(content.split())
            )
        except Exception as e:
            results['error'] = str(e)
        return results

    # Readability
    def analyze_readability(self, content: str) -> Dict:
        """Analyze content readability"""
        analysis = {'score': 0, 'max_score': 100, 'issues': [], 'recommendations': [], 'metrics': {}}
        if not content:
            analysis['issues'].append("No content to analyze")
            return analysis
        try:
            flesch = flesch_reading_ease(content)
            fk = flesch_kincaid_grade(content)
            analysis['metrics']['flesch_reading_ease'] = flesch
            analysis['metrics']['flesch_kincaid_grade'] = fk
            if flesch >= 80:
                analysis['score'] += 100
            elif flesch >= 70:
                analysis['score'] += 80
            elif flesch >= 60:
                analysis['score'] += 60
            elif flesch >= 50:
                analysis['score'] += 40
                analysis['recommendations'].append("Consider simplifying language for better readability")
            else:
                analysis['issues'].append("Content is difficult to read")
                analysis['recommendations'].append("Significantly simplify language and sentence structure")
                analysis['score'] += 20
            if fk <= 8:
                analysis['score'] = min(analysis['score'] + 20, 100)
            elif fk <= 12:
                analysis['score'] = min(analysis['score'] + 10, 100)
            else:
                analysis['recommendations'].append("Lower reading grade level for broader audience")
        except Exception as e:
            analysis['issues'].append(f"Readability analysis failed: {str(e)}")
        sentences = re.split(r'[.!?]+', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        if sentences:
            sentence_lengths = [len(s.split()) for s in sentences]
            avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
            max_sentence_length = max(sentence_lengths)
            analysis['metrics']['avg_sentence_length'] = avg_sentence_length
            analysis['metrics']['max_sentence_length'] = max_sentence_length
            analysis['metrics']['sentence_count'] = len(sentences)
            if avg_sentence_length <= 15:
                analysis['score'] = min(analysis['score'] + 15, 100)
            elif avg_sentence_length <= 20:
                analysis['score'] = min(analysis['score'] + 10, 100)
            else:
                analysis['recommendations'].append("Use shorter sentences for better readability")
            if max_sentence_length > 30:
                analysis['recommendations'].append("Break up very long sentences")
        # Transition words
        transitions = ['however', 'therefore', 'moreover', 'furthermore', 'consequently', 'meanwhile',
                       'nevertheless', 'additionally', 'similarly']
        transition_count = sum(content.lower().count(word) for word in transitions)
        word_count = len(content.split())
        transition_ratio = (transition_count / word_count) * 100 if word_count > 0 else 0
        analysis['metrics']['transition_words_ratio'] = transition_ratio
        if transition_ratio >= 0.3:
            analysis['score'] = min(analysis['score'] + 10, 100)
        else:
            analysis['recommendations'].append("Add more transition words to improve flow")
        return analysis

    # Remaining methods omitted for brevity (no changes needed)

# Streamlit interface functions omitted
