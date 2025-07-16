import logging
from datetime import datetime
from typing import List, Dict, Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

from config import GOOGLE_API_KEY


class PersonaGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.llm = ChatGoogleGenerativeAI(
            google_api_key=GOOGLE_API_KEY,
            model="models/gemini-1.5-pro",
            temperature=0.3
        )

    def generate_persona(self, analysis: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        personal_info = self._generate_personal_info(analysis, user_data)
        personality_section = self._generate_personality_section(analysis)
        behavior_section = self._generate_behavior_section(analysis)
        motivations_section = self._generate_motivations_section(analysis)
        frustrations_section = self._generate_frustrations_section(analysis)
        goals_section = self._generate_goals_section(analysis)
        citations = self._generate_citations(analysis, user_data)

        return self._format_persona(
            username=user_data['username'],
            personal_info=personal_info,
            personality=personality_section,
            behavior=behavior_section,
            motivations=motivations_section,
            frustrations=frustrations_section,
            goals=goals_section,
            citations=citations
        )

    def _invoke_prompt(self, prompt: PromptTemplate, **kwargs) -> str:
        try:
            content = prompt.format(**kwargs)
            return self.llm.invoke(content)
        except Exception as e:
            self.logger.error(f"LLM invocation failed: {str(e)}")
            return "Unable to generate content"

    def _generate_personal_info(self, analysis: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["username", "stats", "demographics", "interests"],
            template="""
            You are a user persona analyst. Based on the following Reddit user analysis, generate personal information:
            
            Username: {username}
            Statistics: {stats}
            Demographics: {demographics}
            Interests: {interests}
            
            Please generate the following information:
            1. Estimated age range (be conservative)
            2. Possible occupation/status
            3. Location hints (if any)
            4. User archetype (e.g., Lurker, Contributor, Expert)
            5. Tier classification (Early Adopter, Creator, Casual User, etc.)
            
            Be conservative in your estimates and clearly indicate uncertainty levels. Format your response in a clear, structured manner.
            """
        )

        personal_info = self._invoke_prompt(
            prompt,
            username=user_data['username'],
            stats=str(analysis['basic_stats']),
            demographics=str(analysis['demographic_hints']),
            interests=str(analysis['interests'])
        )

        return {
            'generated_info': personal_info,
            'activity_level': self._classify_activity_level(analysis['basic_stats']),
            'primary_communities': list(analysis['basic_stats']['top_subreddits'].keys())[:3]
        }

    def _generate_personality_section(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["analysis", "communication"],
            template="""
            You are a personality analyst. Based on the personality analysis, create personality trait scores:
            
            Analysis: {analysis}
            Communication: {communication}
            
            Generate scores (1-10 scale) for these personality dimensions:
            1. Introvert (1) ← → Extrovert (10)
            2. Intuition (1) ← → Sensing (10)
            3. Feeling (1) ← → Thinking (10)
            4. Perceiving (1) ← → Judging (10)
            
            Also provide:
            - Key personality traits (3-5 main traits)
            - Communication style description
            - Social behavior patterns
            
            Format as structured data with clear scores and explanations for each dimension.
            """
        )

        traits = self._invoke_prompt(
            prompt,
            analysis=analysis['personality_traits']['personality_analysis'],
            communication=str(analysis['communication_style'])
        )

        return {
            'traits': traits,
            'communication_style': analysis['communication_style'],
            'social_patterns': analysis['behavioral_patterns']
        }

    def _generate_behavior_section(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["patterns", "stats"],
            template="""
            You are a behavioral analyst. Based on the behavioral analysis, describe user habits and behaviors:
            
            Patterns: {patterns}
            Statistics: {stats}
            
            Describe the following aspects:
            1. Daily/weekly habits and routines
            2. Online behavior patterns
            3. Content consumption habits
            4. Social interaction patterns
            5. Engagement preferences
            
            Make it specific and actionable for persona understanding. Focus on observable behaviors and patterns.
            """
        )

        behavior = self._invoke_prompt(
            prompt,
            patterns=str(analysis['behavioral_patterns']),
            stats=str(analysis['basic_stats'])
        )

        return {
            'description': behavior,
            'activity_patterns': analysis['basic_stats']['activity_pattern'],
            'engagement_metrics': analysis['behavioral_patterns']['engagement_metrics']
        }

    def _generate_motivations_section(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["interests", "personality"],
            template="""
            You are a motivation analyst. Based on interests and personality, identify key motivations:
            
            Interests: {interests}
            Personality: {personality}
            
            Identify and score (1-10 scale) motivations for:
            1. Convenience
            2. Wellness
            3. Speed
            4. Preferences
            5. Comfort
            6. Dietary needs
            7. Social connection
            8. Achievement
            9. Learning
            10. Entertainment

            Provide scores (1-10) and brief explanations for each motivation category.
            """
        )

        motivations = self._invoke_prompt(
            prompt,
            interests=str(analysis['interests']),
            personality=str(analysis['personality_traits'])
        )

        return {
            'analysis': motivations,
            'primary_drivers': self._extract_primary_motivations(analysis)
        }

    def _generate_frustrations_section(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["behavior", "communication"],
            template="""
            You are a user experience analyst. Based on behavior and communication patterns, identify likely frustrations:

            Behavior: {behavior}
            Communication: {communication}

            Identify common frustrations related to:
            1. Technology issues
            2. Time management
            3. Information overload
            4. Social interactions
            5. Content quality
            6. Platform limitations

            Make them specific and relatable.
            """
        )

        frustrations = self._invoke_prompt(
            prompt,
            behavior=str(analysis['behavioral_patterns']),
            communication=str(analysis['communication_style'])
        )

        return {
            'analysis': frustrations,
            'behavioral_indicators': self._extract_frustration_indicators(analysis)
        }

    def _generate_goals_section(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        prompt = PromptTemplate(
            input_variables=["interests", "motivations"],
            template="""
            You are a goals and needs analyst. Based on interests and motivations, identify goals and needs:

            Interests: {interests}
            Motivations: {motivations}

            Identify:
            1. Short-term goals
            2. Long-term aspirations
            3. Immediate needs
            4. Desired outcomes
            5. Success metrics

            Be specific and measurable.
            """
        )

        goals = self._invoke_prompt(
            prompt,
            interests=str(analysis['interests']),
            motivations=str(analysis.get('motivations', {}))
        )

        return {
            'analysis': goals,
            'priority_areas': self._identify_priority_areas(analysis)
        }

    


    def _generate_citations(self, analysis: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate citations mapping characteristics to source content."""
        citations = {}
        
        # Map characteristics to specific posts/comments
        posts = user_data['posts']
        comments = user_data['comments']
        
        # Top subreddits citations
        top_subreddits = analysis['basic_stats']['top_subreddits']
        citations['interests'] = []
        
        for subreddit in list(top_subreddits.keys())[:5]:
            relevant_posts = [p for p in posts if p['subreddit'] == subreddit][:2]
            relevant_comments = [c for c in comments if c['subreddit'] == subreddit][:2]
            
            for post in relevant_posts:
                citations['interests'].append({
                    'type': 'post',
                    'id': post['id'],
                    'title': post['title'],
                    'subreddit': post['subreddit'],
                    'content_preview': post['content'][:200] + "..." if len(post['content']) > 200 else post['content']
                })
            
            for comment in relevant_comments:
                citations['interests'].append({
                    'type': 'comment',
                    'id': comment['id'],
                    'subreddit': comment['subreddit'],
                    'content_preview': comment['body'][:200] + "..." if len(comment['body']) > 200 else comment['body']
                })
        
        # Communication style citations
        citations['communication_style'] = []
        long_posts = [p for p in posts if len(p['content']) > 500][:3]
        long_comments = [c for c in comments if len(c['body']) > 200][:3]
        
        for post in long_posts:
            citations['communication_style'].append({
                'type': 'post',
                'id': post['id'],
                'title': post['title'],
                'characteristic': 'detailed_communication',
                'evidence': f"Long post with {len(post['content'])} characters"
            })
        
        for comment in long_comments:
            citations['communication_style'].append({
                'type': 'comment',
                'id': comment['id'],
                'characteristic': 'detailed_communication',
                'evidence': f"Long comment with {len(comment['body'])} characters"
            })
        
        # Personality trait citations
        citations['personality'] = []
        question_posts = [p for p in posts if '?' in p['title']][:3]
        
        for post in question_posts:
            citations['personality'].append({
                'type': 'post',
                'id': post['id'],
                'title': post['title'],
                'characteristic': 'inquisitive_nature',
                'evidence': 'Asks questions in post titles'
            })
        
        return citations
    
    def _classify_activity_level(self, basic_stats: Dict[str, Any]) -> str:
        """Classify user activity level."""
        total_activity = basic_stats['total_activity']
        
        if total_activity > 200:
            return "Very Active"
        elif total_activity > 100:
            return "Active"
        elif total_activity > 50:
            return "Moderate"
        elif total_activity > 20:
            return "Light"
        else:
            return "Minimal"
    
    def _extract_primary_motivations(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract primary motivations from analysis."""
        interests = analysis['interests']
        
        # Simple heuristic based on subreddit categories
        motivations = []
        
        if 'interest_analysis' in interests:
            # This would be more sophisticated in a real implementation
            motivations = ["Learning", "Community", "Entertainment", "Problem-solving"]
        
        return motivations
    
    def _extract_frustration_indicators(self, analysis: Dict[str, Any]) -> List[str]:
        """Extract frustration indicators from analysis."""
        behavior = analysis['behavioral_patterns']
        
        indicators = []
        
        # Low engagement scores might indicate frustration
        if behavior['engagement_metrics']['avg_post_score'] < 5:
            indicators.append("Low post engagement")
        
        if behavior['engagement_metrics']['avg_comment_score'] < 2:
            indicators.append("Low comment engagement")
        
        return indicators
    
    def _identify_priority_areas(self, analysis: Dict[str, Any]) -> List[str]:
        """Identify priority areas from analysis."""
        interests = analysis['interests']
        
        # Extract from top subreddits
        top_subreddits = analysis['basic_stats']['top_subreddits']
        priority_areas = list(top_subreddits.keys())[:5]
        
        return priority_areas
    
    def _format_persona(self, username: str, personal_info: Dict[str, Any], 
                       personality: Dict[str, Any], behavior: Dict[str, Any],
                       motivations: Dict[str, Any], frustrations: Dict[str, Any],
                       goals: Dict[str, Any], citations: Dict[str, Any]) -> str:
        """Format the complete persona."""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        persona = f"""
# USER PERSONA: {username}
Generated on: {timestamp}

## PERSONAL INFORMATION
Username: {username}
Activity Level: {personal_info['activity_level']}
Primary Communities: {', '.join(personal_info['primary_communities'])}

{personal_info['generated_info']}

## PERSONALITY TRAITS
{personality['traits']}

## BEHAVIOR & HABITS
{behavior['description']}

### Activity Patterns
{self._format_activity_patterns(behavior['activity_patterns'])}

### Engagement Metrics
{self._format_engagement_metrics(behavior['engagement_metrics'])}

## MOTIVATIONS
{motivations['analysis']}

Primary Drivers: {', '.join(motivations['primary_drivers'])}

## FRUSTRATIONS
{frustrations['analysis']}

Behavioral Indicators: {', '.join(frustrations['behavioral_indicators'])}

## GOALS & NEEDS
{goals['analysis']}

Priority Areas: {', '.join(goals['priority_areas'])}

## CITATIONS & EVIDENCE

### Interest Evidence
{self._format_citations(citations.get('interests', []))}

### Communication Style Evidence
{self._format_citations(citations.get('communication_style', []))}

### Personality Evidence
{self._format_citations(citations.get('personality', []))}

---
Generated by Reddit User Persona Generator (Powered by Google Gemini)
"""
        
        return persona
    
    def _format_activity_patterns(self, patterns: Dict[str, Any]) -> str:
        """Format activity patterns section."""
        if not patterns:
            return "No activity patterns available"
        
        formatted = ""
        if 'peak_hours' in patterns:
            formatted += f"Peak Hours: {patterns['peak_hours']}\n"
        if 'peak_days' in patterns:
            formatted += f"Peak Days: {patterns['peak_days']}\n"
        if 'activity_consistency' in patterns:
            formatted += f"Activity Consistency: {patterns['activity_consistency']:.2f}\n"
        
        return formatted
    
    def _format_engagement_metrics(self, metrics: Dict[str, Any]) -> str:
        """Format engagement metrics section."""
        if not metrics:
            return "No engagement metrics available"
        
        formatted = ""
        for key, value in metrics.items():
            formatted += f"{key.replace('_', ' ').title()}: {value}\n"
        
        return formatted
    
    def _format_citations(self, citations: List[Dict[str, Any]]) -> str:
        """Format citations section."""
        if not citations:
            return "No citations available"
        
        formatted = ""
        for i, citation in enumerate(citations, 1):
            formatted += f"\n{i}. {citation['type'].upper()}"
            if 'title' in citation:
                formatted += f" - {citation['title']}"
            if 'subreddit' in citation:
                formatted += f" (r/{citation['subreddit']})"
            if 'characteristic' in citation:
                formatted += f"\n   Characteristic: {citation['characteristic']}"
            if 'evidence' in citation:
                formatted += f"\n   Evidence: {citation['evidence']}"
            if 'content_preview' in citation:
                formatted += f"\n   Content: {citation['content_preview']}"
            formatted += "\n"
        
        return formatted