import logging
from typing import Dict, List, Any
from collections import Counter
import re
from datetime import datetime

from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from config import GOOGLE_API_KEY


class PersonaAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=GOOGLE_API_KEY,
            model="models/gemini-1.5-pro",
            temperature=0.3
        )

    def analyze_user_content(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'basic_stats': self._analyze_basic_stats(user_data),
            'interests': self._analyze_interests(user_data),
            'personality_traits': self._analyze_personality(user_data),
            'behavioral_patterns': self._analyze_behavior(user_data),
            'communication_style': self._analyze_communication(user_data),
            'demographic_hints': self._analyze_demographics(user_data),
            'citations': {}
        }

    def _analyze_basic_stats(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        posts = user_data['posts']
        comments = user_data['comments']
        total_activity = len(posts) + len(comments)
        post_to_comment_ratio = len(posts) / len(comments) if comments else float('inf')

        subreddits = [p['subreddit'] for p in posts] + [c['subreddit'] for c in comments]
        subreddit_counts = Counter(subreddits)

        activity_times = [datetime.fromtimestamp(p['created_utc']) for p in posts] + \
                         [datetime.fromtimestamp(c['created_utc']) for c in comments]

        return {
            'total_posts': len(posts),
            'total_comments': len(comments),
            'total_activity': total_activity,
            'post_to_comment_ratio': post_to_comment_ratio,
            'top_subreddits': dict(subreddit_counts.most_common(10)),
            'activity_pattern': self._analyze_activity_pattern(activity_times)
        }

    def _analyze_interests(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        all_content = [f"POST: {p['title']} {p['content']}" for p in user_data['posts']] + \
                      [f"COMMENT: {c['body']}" for c in user_data['comments']]

        prompt = PromptTemplate(
            input_variables=["content"],
            template="""
            Analyze the following Reddit posts and comments to identify the user's interests and hobbies.

            Content:
            {content}

            Please identify:
            1. Main interests/hobbies
            2. Professional interests
            3. Entertainment preferences
            4. Lifestyle interests

            Format your response as a structured analysis with clear categories and specific examples from the content.
            """
        )

        content_chunks = [all_content[i:i+8] for i in range(0, len(all_content), 8)]
        interest_analyses = []

        for chunk in content_chunks:
            chunk_content = "\n".join(chunk)
            if len(chunk_content) > 100:
                try:
                    if len(chunk_content) > 8000:
                        chunk_content = chunk_content[:8000] + "..."
                    formatted_prompt = prompt.format(content=chunk_content)
                    analysis = self.llm.invoke(formatted_prompt)
                    interest_analyses.append(analysis)
                except Exception as e:
                    self.logger.error(f"Error analyzing interests: {str(e)}")

        return {
            'interest_analysis': interest_analyses,
            'subreddit_interests': self._categorize_subreddits(user_data)
        }

    def _analyze_personality(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        recent_content = [f"POST: {p['title']} {p['content']}" for p in user_data['posts'][:15]] + \
                         [f"COMMENT: {c['body']}" for c in user_data['comments'][:25]]

        prompt = PromptTemplate(
            input_variables=["content"],
            template="""
            Analyze the following Reddit posts and comments to determine personality traits.

            Content:
            {content}

            Please analyze and provide insights on:
            1. Introversion vs Extroversion tendencies
            2. Intuitive vs Sensing preferences
            3. Feeling vs Thinking approach
            4. Perceiving vs Judging style
            5. Openness to experience
            6. Conscientiousness level
            7. Agreeableness patterns
            8. Emotional stability

            Also identify:
            - Communication style
            - Emotional tendencies
            - Social behavior patterns

            Provide specific examples from the content to support your analysis. Be thorough but concise.
            """
        )

        try:
            content_text = "\n".join(recent_content)
            if len(content_text) > 100:
                if len(content_text) > 8000:
                    content_text = content_text[:8000] + "..."
                formatted_prompt = prompt.format(content=content_text)
                personality_analysis = self.llm.invoke(formatted_prompt)
            else:
                personality_analysis = "Insufficient content for personality analysis"
        except Exception as e:
            self.logger.error(f"Error analyzing personality: {str(e)}")
            personality_analysis = "Error in personality analysis"

        return {
            'personality_analysis': personality_analysis,
            'communication_patterns': self._analyze_communication_patterns(user_data)
        }

    def _analyze_demographics(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        demo_content = [f"POST: {p['title']} {p['content']}" for p in user_data['posts'][:8]] + \
                       [f"COMMENT: {c['body']}" for c in user_data['comments'][:15]]

        prompt = PromptTemplate(
            input_variables=["content"],
            template="""
            Analyze the following Reddit content to infer demographic information.

            Content:
            {content}

            Please infer (only if there are clear indicators):
            1. Approximate age range
            2. Possible location/region
            3. Education level indicators
            4. Professional field hints
            5. Lifestyle indicators

            IMPORTANT: Only make inferences if there are clear indicators in the content.
            Be conservative and indicate uncertainty levels. Explain your reasoning for each inference.
            """
        )

        try:
            content_text = "\n".join(demo_content)
            if len(content_text) > 100:
                if len(content_text) > 6000:
                    content_text = content_text[:6000] + "..."
                formatted_prompt = prompt.format(content=content_text)
                demographic_analysis = self.llm.invoke(formatted_prompt)
            else:
                demographic_analysis = "Insufficient content for demographic analysis"
        except Exception as e:
            self.logger.error(f"Error analyzing demographics: {str(e)}")
            demographic_analysis = "Error in demographic analysis"

        return {
            'demographic_analysis': demographic_analysis,
            'activity_timezone': self._infer_timezone(user_data)
        }

    # All other helper methods remain unchanged below...

    
    def _analyze_behavior(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze behavioral patterns."""
        posts = user_data['posts']
        comments = user_data['comments']
        
        # Engagement patterns
        avg_post_score = sum(post['score'] for post in posts) / len(posts) if posts else 0
        avg_comment_score = sum(comment['score'] for comment in comments) / len(comments) if comments else 0
        
        # Content patterns
        question_posts = len([p for p in posts if '?' in p['title']])
        long_posts = len([p for p in posts if len(p['content']) > 500])
        
        # Interaction patterns
        reply_comments = len([c for c in comments if c['parent_id'].startswith('t1_')])
        
        return {
            'engagement_metrics': {
                'avg_post_score': avg_post_score,
                'avg_comment_score': avg_comment_score,
                'question_posts': question_posts,
                'long_posts': long_posts,
                'reply_comments': reply_comments
            },
            'content_style': self._analyze_content_style(user_data),
            'interaction_style': self._analyze_interaction_style(user_data)
        }
    
    def _analyze_communication(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze communication style."""
        all_text = []
        
        for post in user_data['posts']:
            all_text.append(post['title'] + " " + post['content'])
        
        for comment in user_data['comments']:
            all_text.append(comment['body'])
        
        combined_text = " ".join(all_text)
        
        # Basic text analysis
        word_count = len(combined_text.split())
        sentence_count = len(re.findall(r'[.!?]+', combined_text))
        avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0
        
        # Emoji and punctuation usage
        emoji_count = len(re.findall(r'[😀-🿿]', combined_text))
        exclamation_count = combined_text.count('!')
        question_count = combined_text.count('?')
        
        return {
            'text_metrics': {
                'total_words': word_count,
                'avg_words_per_sentence': avg_words_per_sentence,
                'emoji_usage': emoji_count,
                'exclamation_usage': exclamation_count,
                'question_usage': question_count
            },
            'language_style': self._analyze_language_style(combined_text)
        }
    
    
    def _analyze_activity_pattern(self, activity_times: List[datetime]) -> Dict[str, Any]:
        """Analyze activity patterns."""
        if not activity_times:
            return {}
        
        hours = [dt.hour for dt in activity_times]
        days = [dt.weekday() for dt in activity_times]
        
        hour_counts = Counter(hours)
        day_counts = Counter(days)
        
        return {
            'peak_hours': dict(hour_counts.most_common(5)),
            'peak_days': dict(day_counts.most_common(7)),
            'activity_consistency': len(set(hours)) / 24  # Spread across hours
        }
    
    def _categorize_subreddits(self, user_data: Dict[str, Any]) -> Dict[str, List[str]]:
        """Categorize subreddits by interest areas."""
        subreddits = []
        for post in user_data['posts']:
            subreddits.append(post['subreddit'])
        for comment in user_data['comments']:
            subreddits.append(comment['subreddit'])
        
        subreddit_counts = Counter(subreddits)
        
        # Expanded categorization
        categories = {
            'Technology': ['programming', 'python', 'javascript', 'MachineLearning', 'technology', 'coding', 'webdev'],
            'Gaming': ['gaming', 'Games', 'pcgaming', 'nintendo', 'playstation', 'xbox', 'steam'],
            'Lifestyle': ['fitness', 'cooking', 'DIY', 'productivity', 'minimalism', 'health', 'selfimprovement'],
            'Entertainment': ['movies', 'television', 'music', 'books', 'netflix', 'anime', 'comics'],
            'News': ['news', 'worldnews', 'politics', 'UpliftingNews', 'science'],
            'Education': ['explainlikeimfive', 'todayilearned', 'askscience', 'learnprogramming'],
            'Finance': ['investing', 'personalfinance', 'stocks', 'cryptocurrency', 'financialindependence'],
            'Career': ['jobs', 'careeradvice', 'entrepreneur', 'cscareerquestions']
        }
        
        categorized = {}
        for category, keywords in categories.items():
            categorized[category] = [sub for sub in subreddit_counts.keys() 
                                   if any(keyword.lower() in sub.lower() for keyword in keywords)]
        
        return categorized
    
    def _analyze_communication_patterns(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze communication patterns."""
        posts = user_data['posts']
        comments = user_data['comments']
        
        # Length analysis
        post_lengths = [len(post['content']) for post in posts if post['content']]
        comment_lengths = [len(comment['body']) for comment in comments]
        
        avg_post_length = sum(post_lengths) / len(post_lengths) if post_lengths else 0
        avg_comment_length = sum(comment_lengths) / len(comment_lengths) if comment_lengths else 0
        
        return {
            'avg_post_length': avg_post_length,
            'avg_comment_length': avg_comment_length,
            'verbosity_score': (avg_post_length + avg_comment_length) / 2,
            'engagement_preference': 'posts' if len(posts) > len(comments) else 'comments'
        }
    
    def _analyze_content_style(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content style."""
        posts = user_data['posts']
        
        # Content type analysis
        text_posts = len([p for p in posts if p['is_self']])
        link_posts = len([p for p in posts if not p['is_self']])
        
        # Title analysis
        question_titles = len([p for p in posts if '?' in p['title']])
        caps_titles = len([p for p in posts if p['title'].isupper()])
        
        return {
            'content_types': {
                'text_posts': text_posts,
                'link_posts': link_posts
            },
            'title_patterns': {
                'question_titles': question_titles,
                'caps_titles': caps_titles
            }
        }
    
    def _analyze_interaction_style(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze interaction style."""
        comments = user_data['comments']
        
        # Response patterns
        direct_replies = len([c for c in comments if c['parent_id'].startswith('t1_')])
        post_replies = len([c for c in comments if c['parent_id'].startswith('t3_')])
        
        return {
            'response_patterns': {
                'direct_replies': direct_replies,
                'post_replies': post_replies,
                'interaction_ratio': direct_replies / len(comments) if comments else 0
            }
        }
    
    def _analyze_language_style(self, text: str) -> Dict[str, Any]:
        """Analyze language style."""
        # Basic language metrics
        words = text.split()
        unique_words = len(set(words))
        vocabulary_diversity = unique_words / len(words) if words else 0
        
        # Formality indicators
        formal_words = ['therefore', 'however', 'furthermore', 'nevertheless', 'consequently']
        informal_words = ['lol', 'haha', 'omg', 'btw', 'tbh', 'ngl', 'fr']
        
        formal_count = sum(text.lower().count(word) for word in formal_words)
        informal_count = sum(text.lower().count(word) for word in informal_words)
        
        return {
            'vocabulary_diversity': vocabulary_diversity,
            'formality_score': formal_count / (formal_count + informal_count + 1),
            'total_words': len(words),
            'unique_words': unique_words
        }
    
    def _infer_timezone(self, user_data: Dict[str, Any]) -> str:
        """Infer timezone from activity patterns."""
        activity_times = []
        
        for post in user_data['posts']:
            activity_times.append(datetime.fromtimestamp(post['created_utc']))
        for comment in user_data['comments']:
            activity_times.append(datetime.fromtimestamp(comment['created_utc']))
        
        if not activity_times:
            return "Unknown"
        
        # Simple heuristic based on peak activity hours
        hours = [dt.hour for dt in activity_times]
        peak_hour = Counter(hours).most_common(1)[0][0]
        
        # Very basic timezone inference
        if 6 <= peak_hour <= 12:
            return "Likely US Eastern/Central"
        elif 13 <= peak_hour <= 19:
            return "Likely US Pacific/Mountain"
        elif 20 <= peak_hour <= 23:
            return "Likely European"
        else:
            return "Unknown pattern"