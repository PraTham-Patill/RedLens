

import requests
import json
import time
import re
import os
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import argparse
from urllib.parse import urlparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('reddit_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class RedditPost:
    """Data class for Reddit posts"""
    title: str
    content: str
    subreddit: str
    score: int
    created_utc: float
    url: str
    num_comments: int
    post_type: str = "post"


@dataclass
class RedditComment:
    """Data class for Reddit comments"""
    content: str
    subreddit: str
    score: int
    created_utc: float
    post_title: str
    url: str
    post_type: str = "comment"


class RedditScraper:
    """Scrapes Reddit user data using Reddit's JSON API"""
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extract_username(self, profile_url: str) -> str:
        """Extract username from Reddit profile URL"""
        try:
            # Handle different URL formats
            if '/user/' in profile_url:
                username = profile_url.split('/user/')[-1].rstrip('/')
            elif '/u/' in profile_url:
                username = profile_url.split('/u/')[-1].rstrip('/')
            else:
                raise ValueError("Invalid Reddit profile URL format")
            
            # Clean username
            username = username.split('/')[0]  # Remove any trailing paths
            return username
        except Exception as e:
            logger.error(f"Error extracting username from {profile_url}: {e}")
            raise
    
    def fetch_user_data(self, username: str, limit: int = 100) -> Dict[str, List]:
        """Fetch user's posts and comments from Reddit JSON API"""
        posts = []
        comments = []
        
        try:
            # Fetch posts
            logger.info(f"Fetching posts for user: {username}")
            posts_url = f"https://www.reddit.com/user/{username}/submitted.json?limit={limit}"
            posts_response = self.session.get(posts_url)
            
            if posts_response.status_code == 200:
                posts_data = posts_response.json()
                for post in posts_data.get('data', {}).get('children', []):
                    post_data = post['data']
                    reddit_post = RedditPost(
                        title=post_data.get('title', ''),
                        content=post_data.get('selftext', ''),
                        subreddit=post_data.get('subreddit', ''),
                        score=post_data.get('score', 0),
                        created_utc=post_data.get('created_utc', 0),
                        url=f"https://reddit.com{post_data.get('permalink', '')}",
                        num_comments=post_data.get('num_comments', 0)
                    )
                    posts.append(reddit_post)
                    
            time.sleep(self.delay)
            
            # Fetch comments
            logger.info(f"Fetching comments for user: {username}")
            comments_url = f"https://www.reddit.com/user/{username}/comments.json?limit={limit}"
            comments_response = self.session.get(comments_url)
            
            if comments_response.status_code == 200:
                comments_data = comments_response.json()
                for comment in comments_data.get('data', {}).get('children', []):
                    comment_data = comment['data']
                    reddit_comment = RedditComment(
                        content=comment_data.get('body', ''),
                        subreddit=comment_data.get('subreddit', ''),
                        score=comment_data.get('score', 0),
                        created_utc=comment_data.get('created_utc', 0),
                        post_title=comment_data.get('link_title', ''),
                        url=f"https://reddit.com{comment_data.get('permalink', '')}"
                    )
                    comments.append(reddit_comment)
                    
        except Exception as e:
            logger.error(f"Error fetching data for user {username}: {e}")
            raise
            
        logger.info(f"Fetched {len(posts)} posts and {len(comments)} comments for {username}")
        return {"posts": posts, "comments": comments}


class PersonaAnalyzer:
    """Analyzes Reddit data to generate user personas using LLM techniques"""
    
    def __init__(self):
        self.persona_template = {
            "Basic Information": {
                "Username": "",
                "Account Age Estimate": "",
                "Activity Level": ""
            },
            "Demographics": {
                "Age Range": "",
                "Gender": "",
                "Location": "",
                "Education Level": "",
                "Occupation": ""
            },
            "Interests and Hobbies": [],
            "Personality Traits": [],
            "Communication Style": {
                "Tone": "",
                "Formality": "",
                "Humor Style": "",
                "Engagement Pattern": ""
            },
            "Values and Beliefs": [],
            "Technology Usage": {
                "Tech Savviness": "",
                "Preferred Platforms": [],
                "Digital Behavior": ""
            },
            "Goals and Motivations": [],
            "Pain Points and Challenges": [],
            "Community Engagement": {
                "Favorite Subreddits": [],
                "Interaction Style": "",
                "Content Preference": ""
            }
        }
    
    def analyze_activity_patterns(self, posts: List[RedditPost], comments: List[RedditComment]) -> Dict[str, Any]:
        """Analyze user activity patterns"""
        if not posts and not comments:
            return {}
            
        all_content = posts + comments
        
        # Activity level
        total_content = len(all_content)
        if total_content > 100:
            activity_level = "Very Active"
        elif total_content > 50:
            activity_level = "Active"
        elif total_content > 20:
            activity_level = "Moderate"
        else:
            activity_level = "Light"
        
        # Popular subreddits
        subreddit_counts = {}
        for item in all_content:
            subreddit = item.subreddit
            subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
        
        top_subreddits = sorted(subreddit_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Average scores
        scores = [item.score for item in all_content if hasattr(item, 'score')]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        return {
            "activity_level": activity_level,
            "total_posts": len(posts),
            "total_comments": len(comments),
            "top_subreddits": top_subreddits,
            "average_score": avg_score
        }
    
    def extract_interests_from_subreddits(self, subreddit_data: List[tuple]) -> List[str]:
        """Extract interests based on subreddit participation"""
        interest_mapping = {
            # Technology
            'programming': 'Programming/Software Development',
            'python': 'Python Programming',
            'javascript': 'JavaScript Programming',
            'webdev': 'Web Development',
            'technology': 'Technology',
            'gadgets': 'Technology/Gadgets',
            'apple': 'Apple Products',
            'android': 'Android Technology',
            
            # Gaming
            'gaming': 'Video Gaming',
            'pcgaming': 'PC Gaming',
            'nintendo': 'Nintendo Gaming',
            'playstation': 'PlayStation Gaming',
            'xbox': 'Xbox Gaming',
            
            # Entertainment
            'movies': 'Movies/Cinema',
            'television': 'Television Shows',
            'music': 'Music',
            'books': 'Reading/Literature',
            'netflix': 'Streaming Entertainment',
            
            # Sports
            'sports': 'Sports',
            'nfl': 'American Football',
            'nba': 'Basketball',
            'soccer': 'Soccer/Football',
            'baseball': 'Baseball',
            
            # Lifestyle
            'food': 'Food/Cooking',
            'cooking': 'Cooking',
            'fitness': 'Fitness/Health',
            'travel': 'Travel',
            'photography': 'Photography',
            'art': 'Art',
            'diy': 'DIY/Crafts',
            
            # Education/Career
            'askscience': 'Science Interest',
            'explainlikeimfive': 'Learning/Education',
            'personalfinance': 'Personal Finance',
            'entrepreneur': 'Entrepreneurship',
            'jobs': 'Career/Employment',
            
            # Social
            'askreddit': 'Social Discussion',
            'relationships': 'Relationships/Dating',
            'parenting': 'Parenting',
            'pets': 'Pet Ownership'
        }
        
        interests = []
        for subreddit, count in subreddit_data:
            subreddit_lower = subreddit.lower()
            if subreddit_lower in interest_mapping:
                interests.append(f"{interest_mapping[subreddit_lower]} (active in r/{subreddit})")
            else:
                # Generic interest based on subreddit name
                interests.append(f"Interest in {subreddit.replace('_', ' ').title()}")
        
        return interests[:10]  # Return top 10 interests
    
    def analyze_communication_style(self, posts: List[RedditPost], comments: List[RedditComment]) -> Dict[str, str]:
        """Analyze communication style from content"""
        all_text = []
        
        # Collect all text content
        for post in posts:
            if post.content:
                all_text.append(post.content)
            if post.title:
                all_text.append(post.title)
        
        for comment in comments:
            if comment.content:
                all_text.append(comment.content)
        
        if not all_text:
            return {
                "tone": "Unknown",
                "formality": "Unknown",
                "humor_style": "Unknown",
                "engagement_pattern": "Unknown"
            }
        
        # Join all text for analysis
        full_text = " ".join(all_text).lower()
        
        # Analyze tone
        positive_words = ['great', 'awesome', 'love', 'amazing', 'excellent', 'wonderful', 'fantastic']
        negative_words = ['hate', 'terrible', 'awful', 'horrible', 'worst', 'sucks', 'annoying']
        
        positive_count = sum(full_text.count(word) for word in positive_words)
        negative_count = sum(full_text.count(word) for word in negative_words)
        
        if positive_count > negative_count * 1.5:
            tone = "Generally Positive"
        elif negative_count > positive_count * 1.5:
            tone = "Generally Negative"
        else:
            tone = "Balanced/Neutral"
        
        # Analyze formality
        informal_indicators = ['lol', 'lmao', 'wtf', 'omg', 'tbh', 'imo', 'btw']
        formal_indicators = ['however', 'therefore', 'furthermore', 'consequently', 'nevertheless']
        
        informal_count = sum(full_text.count(indicator) for indicator in informal_indicators)
        formal_count = sum(full_text.count(indicator) for indicator in formal_indicators)
        
        if informal_count > formal_count:
            formality = "Casual/Informal"
        elif formal_count > informal_count:
            formality = "Formal/Professional"
        else:
            formality = "Mixed"
        
        # Analyze humor
        humor_indicators = ['lol', 'haha', 'funny', 'joke', 'hilarious', '/s', 'sarcasm']
        humor_count = sum(full_text.count(indicator) for indicator in humor_indicators)
        
        if humor_count > len(all_text) * 0.1:
            humor_style = "Humorous/Sarcastic"
        else:
            humor_style = "Serious/Straightforward"
        
        # Engagement pattern
        avg_length = sum(len(text) for text in all_text) / len(all_text)
        if avg_length > 200:
            engagement_pattern = "Detailed/Comprehensive responses"
        elif avg_length > 50:
            engagement_pattern = "Moderate-length responses"
        else:
            engagement_pattern = "Brief/Concise responses"
        
        return {
            "tone": tone,
            "formality": formality,
            "humor_style": humor_style,
            "engagement_pattern": engagement_pattern
        }
    
    def extract_demographics_clues(self, posts: List[RedditPost], comments: List[RedditComment]) -> Dict[str, str]:
        """Extract demographic clues from content"""
        all_text = []
        
        # Collect all text content
        for post in posts:
            if post.content:
                all_text.append(post.content.lower())
            if post.title:
                all_text.append(post.title.lower())
        
        for comment in comments:
            if comment.content:
                all_text.append(comment.content.lower())
        
        full_text = " ".join(all_text)
        
        demographics = {
            "age_range": "Unknown",
            "gender": "Unknown",
            "location": "Unknown",
            "education_level": "Unknown",
            "occupation": "Unknown"
        }
        
        # Age indicators
        age_indicators = {
            "teenager": ["high school", "teenager", "teen", "grade 12", "grade 11"],
            "young_adult": ["college", "university", "dorm", "freshman", "sophomore", "junior", "senior"],
            "adult": ["work", "job", "career", "mortgage", "married", "spouse"],
            "older_adult": ["retirement", "grandchildren", "pension", "medicare"]
        }
        
        for age_group, indicators in age_indicators.items():
            if any(indicator in full_text for indicator in indicators):
                demographics["age_range"] = age_group.replace("_", " ").title()
                break
        
        # Gender indicators (note: this is based on self-identification in text)
        if any(term in full_text for term in ["i'm a guy", "i'm male", "as a man", "i'm a dude"]):
            demographics["gender"] = "Likely Male (self-identified)"
        elif any(term in full_text for term in ["i'm a girl", "i'm female", "as a woman", "i'm a gal"]):
            demographics["gender"] = "Likely Female (self-identified)"
        
        # Location indicators
        location_patterns = [
            r'\bi live in ([a-zA-Z\s]+)',
            r'\bfrom ([a-zA-Z\s]+)',
            r'\bin ([a-zA-Z\s]+) here',
            r'\bhere in ([a-zA-Z\s]+)'
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, full_text)
            if matches:
                demographics["location"] = f"Possibly {matches[0].title()}"
                break
        
        # Education indicators
        education_keywords = {
            "High School": ["high school", "grade 12", "grade 11", "grade 10"],
            "College/University": ["college", "university", "bachelor", "masters", "phd", "dissertation"],
            "Graduate": ["masters", "phd", "doctorate", "graduate school"]
        }
        
        for level, keywords in education_keywords.items():
            if any(keyword in full_text for keyword in keywords):
                demographics["education_level"] = level
                break
        
        # Occupation indicators
        job_keywords = {
            "Technology": ["programmer", "developer", "software", "coding", "tech", "engineer"],
            "Healthcare": ["doctor", "nurse", "medical", "hospital", "patient"],
            "Education": ["teacher", "professor", "student", "education"],
            "Business": ["manager", "sales", "marketing", "business", "corporate"],
            "Service": ["retail", "restaurant", "customer service", "server"]
        }
        
        for field, keywords in job_keywords.items():
            if any(keyword in full_text for keyword in keywords):
                demographics["occupation"] = f"Possibly {field}"
                break
        
        return demographics
    
    def generate_persona(self, username: str, posts: List[RedditPost], comments: List[RedditComment]) -> Dict[str, Any]:
        """Generate comprehensive user persona"""
        activity_data = self.analyze_activity_patterns(posts, comments)
        communication_style = self.analyze_communication_style(posts, comments)
        demographics = self.extract_demographics_clues(posts, comments)
        interests = self.extract_interests_from_subreddits(activity_data.get('top_subreddits', []))
        
        persona = self.persona_template.copy()
        
        # Basic Information
        persona["Basic Information"]["Username"] = username
        persona["Basic Information"]["Activity Level"] = activity_data.get('activity_level', 'Unknown')
        
        # Demographics
        persona["Demographics"]["Age Range"] = demographics.get('age_range', 'Unknown')
        persona["Demographics"]["Gender"] = demographics.get('gender', 'Unknown')
        persona["Demographics"]["Location"] = demographics.get('location', 'Unknown')
        persona["Demographics"]["Education Level"] = demographics.get('education_level', 'Unknown')
        persona["Demographics"]["Occupation"] = demographics.get('occupation', 'Unknown')
        
        # Interests
        persona["Interests and Hobbies"] = interests
        
        # Communication Style
        persona["Communication Style"]["Tone"] = communication_style.get('tone', 'Unknown')
        persona["Communication Style"]["Formality"] = communication_style.get('formality', 'Unknown')
        persona["Communication Style"]["Humor Style"] = communication_style.get('humor_style', 'Unknown')
        persona["Communication Style"]["Engagement Pattern"] = communication_style.get('engagement_pattern', 'Unknown')
        
        # Community Engagement
        top_subreddits = activity_data.get('top_subreddits', [])
        persona["Community Engagement"]["Favorite Subreddits"] = [f"r/{sub} ({count} posts/comments)" for sub, count in top_subreddits[:5]]
        
        # Determine content preference
        if len(posts) > len(comments):
            content_pref = "Prefers creating original posts"
        elif len(comments) > len(posts):
            content_pref = "Prefers commenting on others' content"
        else:
            content_pref = "Balanced between posting and commenting"
        
        persona["Community Engagement"]["Content Preference"] = content_pref
        
        return persona


class CitationGenerator:
    """Generates citations for persona characteristics"""
    
    def __init__(self):
        pass
    
    def generate_citations(self, username: str, posts: List[RedditPost], comments: List[RedditComment], persona: Dict[str, Any]) -> Dict[str, List[str]]:
        """Generate citations for each persona characteristic"""
        citations = {}
        
        # Combine all content for searching
        all_content = []
        for post in posts:
            all_content.append({
                'type': 'post',
                'title': post.title,
                'content': post.content,
                'subreddit': post.subreddit,
                'url': post.url,
                'score': post.score
            })
        
        for comment in comments:
            all_content.append({
                'type': 'comment',
                'content': comment.content,
                'subreddit': comment.subreddit,
                'url': comment.url,
                'score': comment.score,
                'post_title': comment.post_title
            })
        
        # Generate citations for different characteristics
        citations.update(self._cite_interests(persona.get("Interests and Hobbies", []), all_content))
        citations.update(self._cite_communication_style(persona.get("Communication Style", {}), all_content))
        citations.update(self._cite_demographics(persona.get("Demographics", {}), all_content))
        citations.update(self._cite_community_engagement(persona.get("Community Engagement", {}), all_content))
        
        return citations
    
    def _cite_interests(self, interests: List[str], content: List[Dict]) -> Dict[str, List[str]]:
        """Generate citations for interests"""
        citations = {}
        
        for interest in interests:
            interest_citations = []
            
            # Extract subreddit from interest if present
            if "r/" in interest:
                subreddit = interest.split("r/")[1].split(")")[0]
                relevant_content = [item for item in content if item['subreddit'].lower() == subreddit.lower()]
                
                for item in relevant_content[:3]:  # Top 3 examples
                    if item['type'] == 'post':
                        citation = f"Post in r/{item['subreddit']}: '{item['title']}' - {item['url']}"
                    else:
                        citation = f"Comment in r/{item['subreddit']}: '{item.get('post_title', 'Unknown post')}' - {item['url']}"
                    interest_citations.append(citation)
            
            if interest_citations:
                citations[f"Interest: {interest}"] = interest_citations
        
        return citations
    
    def _cite_communication_style(self, comm_style: Dict[str, str], content: List[Dict]) -> Dict[str, List[str]]:
        """Generate citations for communication style"""
        citations = {}
        
        # Find examples of tone
        tone = comm_style.get("Tone", "")
        if "Positive" in tone:
            positive_examples = []
            for item in content:
                text = (item.get('content', '') + ' ' + item.get('title', '')).lower()
                if any(word in text for word in ['great', 'awesome', 'love', 'amazing', 'excellent']):
                    if item['type'] == 'post':
                        citation = f"Positive tone in post: '{item['title']}' - {item['url']}"
                    else:
                        citation = f"Positive tone in comment: '{item.get('post_title', 'Unknown post')}' - {item['url']}"
                    positive_examples.append(citation)
                    if len(positive_examples) >= 3:
                        break
            if positive_examples:
                citations["Communication Style - Positive Tone"] = positive_examples
        
        return citations
    
    def _cite_demographics(self, demographics: Dict[str, str], content: List[Dict]) -> Dict[str, List[str]]:
        """Generate citations for demographic information"""
        citations = {}
        
        # This would require more sophisticated NLP to find specific mentions
        # For now, we'll provide general citations for demographic indicators
        
        return citations
    
    def _cite_community_engagement(self, community_eng: Dict[str, Any], content: List[Dict]) -> Dict[str, List[str]]:
        """Generate citations for community engagement patterns"""
        citations = {}
        
        favorite_subs = community_eng.get("Favorite Subreddits", [])
        if favorite_subs:
            sub_citations = []
            for sub_info in favorite_subs[:3]:
                subreddit = sub_info.split()[0].replace('r/', '')
                relevant_content = [item for item in content if item['subreddit'].lower() == subreddit.lower()]
                
                if relevant_content:
                    item = relevant_content[0]  # Take first example
                    if item['type'] == 'post':
                        citation = f"Active in {sub_info}: Post '{item['title']}' - {item['url']}"
                    else:
                        citation = f"Active in {sub_info}: Comment on '{item.get('post_title', 'Unknown post')}' - {item['url']}"
                    sub_citations.append(citation)
            
            if sub_citations:
                citations["Community Engagement - Favorite Subreddits"] = sub_citations
        
        return citations


class PersonaOutputGenerator:
    """Generates formatted output for user personas"""
    
    def __init__(self):
        pass
    
    def generate_text_output(self, username: str, persona: Dict[str, Any], citations: Dict[str, List[str]]) -> str:
        """Generate formatted text output for persona"""
        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append(f"USER PERSONA ANALYSIS FOR: u/{username}")
        output_lines.append("=" * 80)
        output_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append("")
        
        # Basic Information
        output_lines.append("BASIC INFORMATION")
        output_lines.append("-" * 40)
        basic_info = persona.get("Basic Information", {})
        for key, value in basic_info.items():
            if value:
                output_lines.append(f"{key}: {value}")
        output_lines.append("")
        
        # Demographics
        output_lines.append("DEMOGRAPHICS")
        output_lines.append("-" * 40)
        demographics = persona.get("Demographics", {})
        for key, value in demographics.items():
            if value and value != "Unknown":
                output_lines.append(f"{key}: {value}")
        output_lines.append("")
        
        # Interests and Hobbies
        interests = persona.get("Interests and Hobbies", [])
        if interests:
            output_lines.append("INTERESTS AND HOBBIES")
            output_lines.append("-" * 40)
            for i, interest in enumerate(interests, 1):
                output_lines.append(f"{i}. {interest}")
            output_lines.append("")
        
        # Communication Style
        output_lines.append("COMMUNICATION STYLE")
        output_lines.append("-" * 40)
        comm_style = persona.get("Communication Style", {})
        for key, value in comm_style.items():
            if value and value != "Unknown":
                output_lines.append(f"{key}: {value}")
        output_lines.append("")
        
        # Community Engagement
        output_lines.append("COMMUNITY ENGAGEMENT")
        output_lines.append("-" * 40)
        community = persona.get("Community Engagement", {})
        
        fav_subs = community.get("Favorite Subreddits", [])
        if fav_subs:
            output_lines.append("Most Active Subreddits:")
            for sub in fav_subs:
                output_lines.append(f"  • {sub}")
        
        content_pref = community.get("Content Preference", "")
        if content_pref:
            output_lines.append(f"Content Preference: {content_pref}")
        output_lines.append("")
        
        # Citations
        if citations:
            output_lines.append("SUPPORTING EVIDENCE & CITATIONS")
            output_lines.append("=" * 80)
            output_lines.append("")
            
            for characteristic, cite_list in citations.items():
                output_lines.append(f"{characteristic}:")
                output_lines.append("-" * len(characteristic))
                for citation in cite_list:
                    output_lines.append(f"  • {citation}")
                output_lines.append("")
        
        # Footer
        output_lines.append("=" * 80)
        output_lines.append("End of User Persona Analysis")
        output_lines.append("Generated by Reddit Persona Analyzer")
        output_lines.append("=" * 80)
        
        return "\n".join(output_lines)


def main():
    """Main function to run the Reddit persona analyzer"""
    parser = argparse.ArgumentParser(
        description="Analyze Reddit user profiles and generate personas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/
  python reddit_persona_analyzer.py https://www.reddit.com/user/Hungry-Move-6603/
  python reddit_persona_analyzer.py --profile-url https://www.reddit.com/user/username/ --output custom_output.txt
        """
    )
    
    parser.add_argument(
        "profile_url",
        nargs="?",
        help="Reddit profile URL (e.g., https://www.reddit.com/user/username/)"
    )
    
    parser.add_argument(
        "--profile-url",
        dest="profile_url_alt",
        help="Alternative way to specify profile URL"
    )
    
    parser.add_argument(
        "--output",
        default=None,
        help="Output filename (default: {username}_persona.txt)"
    )
    
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum number of posts/comments to fetch (default: 100)"
    )
    
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Delay between API requests in seconds (default: 1.0)"
    )
    
    args = parser.parse_args()
    
    # Get profile URL
    profile_url = args.profile_url or args.profile_url_alt
    
    if not profile_url:
        print("Error: Please provide a Reddit profile URL")
        print("Usage: python reddit_persona_analyzer.py <profile_url>")
        print("Example: python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/")
        sys.exit(1)
    
    try:
        # Initialize components
        scraper = RedditScraper(delay=args.delay)
        analyzer = PersonaAnalyzer()
        citation_generator = CitationGenerator()
        output_generator = PersonaOutputGenerator()
        
        # Extract username
        logger.info(f"Processing profile: {profile_url}")
        username = scraper.extract_username(profile_url)
        logger.info(f"Extracted username: {username}")
        
        # Scrape user data
        logger.info("Starting data collection...")
        user_data = scraper.fetch_user_data(username, limit=args.limit)
        posts = user_data["posts"]
        comments = user_data["comments"]
        
        if not posts and not comments:
            logger.warning(f"No data found for user {username}. User may not exist or have no public posts/comments.")
            sys.exit(1)
        
        # Generate persona
        logger.info("Analyzing user data and generating persona...")
        persona = analyzer.generate_persona(username, posts, comments)
        
        # Generate citations
        logger.info("Generating citations...")
        citations = citation_generator.generate_citations(username, posts, comments, persona)
        
        # Generate output
        output_text = output_generator.generate_text_output(username, persona, citations)
        
        # Save to file
        output_filename = args.output or f"{username}_persona.txt"
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(output_text)
        
        logger.info(f"Persona analysis completed successfully!")
        logger.info(f"Output saved to: {output_filename}")
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"ANALYSIS COMPLETE FOR u/{username}")
        print(f"{'='*60}")
        print(f"Posts analyzed: {len(posts)}")
        print(f"Comments analyzed: {len(comments)}")
        print(f"Output file: {output_filename}")
        print(f"{'='*60}")
        
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
