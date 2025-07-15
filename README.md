# Reddit User Persona Analyzer

A Python script that scrapes Reddit user profiles and generates comprehensive user personas using web scraping and data analysis techniques.

## 📋 Assignment Description

This project was developed as part of the BeyondChats AI/LLM Engineer Intern assignment. The script takes a Reddit user's profile URL, scrapes their posts and comments, and generates a detailed user persona with supporting citations.

## 🚀 Features

- **Profile Scraping**: Fetches posts and comments from Reddit users using Reddit's JSON API
- **Persona Generation**: Creates comprehensive user personas including:
  - Basic information and activity level
  - Demographics analysis (age, gender, location, education, occupation)
  - Interests and hobbies based on subreddit participation
  - Communication style analysis
  - Community engagement patterns
  - Technology usage patterns
- **Citation System**: Provides evidence and links to specific posts/comments that support each persona characteristic
- **Professional Output**: Generates well-formatted text files with complete analysis
- **Error Handling**: Robust error handling and logging
- **Rate Limiting**: Respectful API usage with configurable delays

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Internet connection

### Installation Steps

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd reddit-persona-analyzer
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python reddit_persona_analyzer.py --help
   ```

## 📖 Usage

### Basic Usage

```bash
python reddit_persona_analyzer.py <reddit_profile_url>
```

### Examples

```bash
# Analyze the sample users from the assignment
python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/
python reddit_persona_analyzer.py https://www.reddit.com/user/Hungry-Move-6603/

# Using alternative syntax
python reddit_persona_analyzer.py --profile-url https://www.reddit.com/user/username/

# Custom output filename
python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/ --output kojied_analysis.txt

# Adjust number of posts/comments to analyze
python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/ --limit 150

# Adjust delay between requests (be respectful to Reddit's servers)
python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/ --delay 2.0
```

### Command Line Options

- `profile_url`: Reddit profile URL (required)
- `--output`: Custom output filename (default: `{username}_persona.txt`)
- `--limit`: Maximum posts/comments to fetch (default: 100)
- `--delay`: Delay between API requests in seconds (default: 1.0)

## 📊 Output Format

The script generates a comprehensive text file containing:

1. **Basic Information**
   - Username
   - Activity level
   - Account statistics

2. **Demographics**
   - Age range (estimated)
   - Gender (if self-identified)
   - Location (if mentioned)
   - Education level
   - Occupation (estimated)

3. **Interests and Hobbies**
   - Derived from subreddit participation
   - Ranked by activity level

4. **Communication Style**
   - Tone analysis (positive/negative/neutral)
   - Formality level
   - Humor style
   - Engagement patterns

5. **Community Engagement**
   - Most active subreddits
   - Content preferences (posting vs. commenting)
   - Interaction style

6. **Supporting Evidence & Citations**
   - Direct links to posts/comments that support each characteristic
   - Specific examples with URLs for verification

## 🏗️ Project Structure

```
reddit-persona-analyzer/
├── reddit_persona_analyzer.py    # Main script
├── requirements.txt              # Python dependencies
├── README.md                    # This file
├── kojied_persona.txt           # Sample output for kojied user
├── Hungry-Move-6603_persona.txt # Sample output for Hungry-Move-6603 user
└── reddit_analyzer.log         # Log file (generated when script runs)
```

## 🔧 Technical Details

### How It Works

1. **URL Parsing**: Extracts username from various Reddit URL formats
2. **Data Collection**: Uses Reddit's JSON API endpoints to fetch public posts and comments
3. **Text Analysis**: Analyzes content for patterns, keywords, and linguistic features
4. **Pattern Recognition**: Identifies interests, demographics, and behavior patterns
5. **Citation Generation**: Maps persona characteristics back to specific content
6. **Output Generation**: Creates formatted, professional reports

### API Usage

The script uses Reddit's public JSON API endpoints:
- `https://www.reddit.com/user/{username}/submitted.json` for posts
- `https://www.reddit.com/user/{username}/comments.json` for comments

No authentication is required as it only accesses public data.

### Privacy & Ethics

- Only analyzes publicly available Reddit content
- Does not store user data permanently
- Respects Reddit's rate limits
- Provides clear citations for transparency

## 🧪 Testing

The script has been tested with various Reddit profiles including:
- Active users with diverse content
- Users with different activity levels
- Users from different communities
- Edge cases (deleted content, private profiles, etc.)

### Sample Test Cases

```bash
# Test with provided sample users
python reddit_persona_analyzer.py https://www.reddit.com/user/kojied/
python reddit_persona_analyzer.py https://www.reddit.com/user/Hungry-Move-6603/

# Test with your own Reddit profile
python reddit_persona_analyzer.py https://www.reddit.com/user/yourusername/
```

## 🔍 Sample Output Files

This repository includes sample outputs for the assignment's test users:
- `kojied_persona.txt` - Analysis of u/kojied
- `Hungry-Move-6603_persona.txt` - Analysis of u/Hungry-Move-6603

## ⚠️ Limitations

- Relies on publicly available Reddit content only
- Demographic analysis is based on text patterns and may not be 100% accurate
- Some characteristics require manual verification
- Limited by Reddit's API rate limits
- Cannot analyze private or deleted content

## 🚀 Future Enhancements

Potential improvements for future versions:
- Integration with advanced NLP models (GPT, BERT) for better analysis
- Sentiment analysis using machine learning
- Temporal analysis of behavior changes
- Visual persona representations
- Support for other social media platforms
- Real-time persona updates

## 📝 Code Quality

The code follows Python best practices:
- PEP 8 style guidelines
- Comprehensive error handling
- Detailed logging
- Type hints where applicable
- Modular, object-oriented design
- Comprehensive documentation

## 🤝 Contributing

This project was created for the BeyondChats internship assignment. While this specific implementation is for evaluation purposes, the concepts and techniques used here can be adapted for other applications.

## 📄 License

This code is submitted as part of the BeyondChats internship assignment. As stated in the assignment requirements, the code remains the property of the author unless selected for the paid internship position.

## 🙋‍♂️ Support

For questions about this implementation or the assignment, please contact through the appropriate channels as specified in the internship posting.

---

**Assignment Submission Details:**
- **Position**: AI/LLM Engineer Intern at BeyondChats
- **Completion Time**: Within 48-hour deadline
- **Technologies Used**: Python, Web Scraping, Data Analysis, Text Processing
- **Assignment Requirements**: ✅ All completed as specified

**Date**: July 15, 2025  
**Assignment Deadline**: 48 hours from assignment receipt  
**GitHub Repository**: https://github.com/PraTham-Patill/RedLens
