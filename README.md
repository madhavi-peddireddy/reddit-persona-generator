# Reddit User Persona Generator

A Python application that generates comprehensive user personas from Reddit profiles by analyzing posts, comments, and behavioral patterns using LLMs.

## Features

- **Reddit Data Scraping**: Extracts posts and comments from user profiles
- **AI-Powered Analysis**: Uses LLMs to analyze personality traits, interests, and behaviors
- **Comprehensive Personas**: Generates detailed user personas with citations
- **Citation System**: Links each characteristic to specific Reddit content
- **Flexible Output**: Structured text format with clear sections

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/reddit-persona-generator.git
cd reddit-persona-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory:
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=PersonaGenerator/1.0
GOOGLE_API_KEY=your_google_api_key
```

## Reddit API Setup

1. Go to https://www.reddit.com/prefs/apps
2. Create a new application (script type)
3. Note your client ID and secret
4. Add these to your `.env` file

## Usage

### Basic Usage
```bash
python main.py "https://www.reddit.com/user/kojied/"
```

### With Custom Output Directory
```bash
python main.py "https://www.reddit.com/user/kojied/" --output-dir custom_output
```

### With Verbose Logging
```bash
python main.py "https://www.reddit.com/user/kojied/" --verbose
```

## Output Format

The generated persona includes:

### Personal Information
- Username and activity level
- Estimated demographics
- Primary communities
- User archetype

### Personality Traits
- MBTI-style personality scores
- Communication patterns
- Social behavior analysis

### Behavior & Habits
- Activity patterns
- Engagement metrics
- Content preferences

### Motivations
- Key driving factors
- Scored motivations (1-10)

### Frustrations
- Common pain points
- Behavioral indicators

### Goals & Needs
- Short and long-term objectives
- Priority areas

### Citations
- Specific posts/comments supporting each characteristic
- Evidence linking analysis to source content

## Project Structure

```
reddit_persona_generator/
├── main.py                 # Main execution script
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── src/
│   ├── reddit_scraper.py  # Reddit data scraping
│   ├── persona_analyzer.py # Content analysis
│   ├── persona_generator.py # Persona generation
│   └── utils.py           # Utility functions
├── output/                # Generated personas
└── data/                  # Scraped data cache
```

## Sample Output

See `output/kojied_persona.txt` and `output/Hungry-Move-6603_persona.txt` for example personas generated from the provided sample users.

## Configuration

Edit `config.py` to adjust:
- Maximum posts/comments to scrape
- Request delays (rate limiting)
- LLM parameters
- Output formatting

## Error Handling

The application handles:
- Private/non-existent users
- API rate limits
- Network errors
- Invalid URLs
- Insufficient content

## Rate Limiting

The scraper includes built-in rate limiting to respect Reddit's API guidelines. Default delay is 1 second between requests.

## Privacy & Ethics

- Only processes publicly available Reddit content
- No personal information is stored beyond the session
- Respects Reddit's terms of service
- Code is provided for educational purposes

## Requirements

- Python 3.8+
- Reddit API credentials
- Google Gemini API key
- Internet connection

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please ensure compliance with Reddit's API terms and user privacy guidelines.

## Troubleshooting

### Common Issues

1. **Reddit API errors**: Check your credentials and rate limits
2. **Google Gemini API errors**: Verify your API key and quota
3. **Empty results**: User might be private or have no content
4. **Installation issues**: Use Python 3.8+ and install all dependencies

### Debugging

Use the `--verbose` flag to see detailed logging:
```bash
python main.py "https://www.reddit.com/user/kojied/" --verbose
```

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `persona_generator.log`
3. Create an issue on GitHub

---



## .env (template)
```
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=PersonaGenerator/1.0
GOOGLE_API_KEY=your_google_api_key_here
