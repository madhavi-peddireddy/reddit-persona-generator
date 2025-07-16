# 🧠 Reddit User Persona Generator

🚀 A Python application that generates **deep user personas** from Reddit profiles by analyzing their posts, comments, and behavioral patterns — all powered by **LLMs** 🔍.

---

## ✨ Features

- 🔗 **Reddit Data Scraping**: Extracts user posts & comments
- 🤖 **AI-Powered Analysis**: Uses LLMs (via Gemini API) to understand traits & behavior
- 📋 **Detailed Personas**: Outputs structured profiles with sections like personality, motivations, and goals
- 📎 **Citations**: Links insights to specific Reddit content
- 🧱 **Flexible Output**: Saves personas in clean text format

---

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/reddit-persona-generator.git
cd reddit-persona-generator


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

## 🧾 Reddit API Setup
### 🔐 You'll need Reddit API credentials:

1. Go to https://www.reddit.com/prefs/apps
2. Create a new application (script type)
3. Note your client ID and secret
4. Add these to your `.env` file

## ▶️ Usage

### Basic Usage
```bash
python main.py "https://www.reddit.com/user/kojied/"
```
### With Verbose Logging
```bash
python main.py "https://www.reddit.com/user/kojied/" --verbose
```

## 📽️ Demo

Watch the demo on [Loom](https://www.loom.com/share/3bfb14a5b13d4415b03eb2a8451b607b?sid=bfa05d79-b093-4138-85b1-14fe6d5f0e8c)


## 🧠 Output Format

The generated persona includes:

### 👤 Personal Information
- Username and activity level
- Estimated demographics
- Primary communities
- User archetype

### 🧬 Personality Traits
- MBTI-style personality scores
- Communication patterns
- Social behavior analysis

### ⏱️ Behavior & Habits
- Activity patterns
- Engagement metrics
- Content preferences

### 🎯 Motivations
- Key driving factors
- Scored motivations (1-10)

### 😤 Frustrations
- Common pain points
- Behavioral indicators

### 🏆 Goals & Needs
- Short and long-term objectives
- Priority areas

### 📌 Citations
- Specific posts/comments supporting each characteristic
- Evidence linking analysis to source content

## 📁 Project Structure

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

## 📄 Sample Output

See `output/kojied_persona.txt` and `output/Hungry-Move-6603_persona.txt` for example personas generated from the provided sample users.

## ⚙️ Configuration

Edit `config.py` to adjust:
- Maximum posts/comments to scrape
- Request delays (rate limiting)
- LLM parameters
- Output formatting options


## 🚦 Rate Limiting

The scraper includes built-in rate limiting to respect Reddit's API guidelines. Default delay is 1 second between requests.

## 🔒 Privacy & Ethics

- Only processes publicly available Reddit content
- No personal information is stored beyond the session
- Respects Reddit's terms of service
- Code is provided for educational purposes

## 🧰 Requirements

- Python 3.8+
- Reddit API credentials
- Google Gemini API key
- Internet connection


## 🧯 Common Issues

1. **Reddit API errors**: Check your credentials and rate limits
2. **Google Gemini API errors**: Verify your API key and quota
3. **Empty results**: User might be private or have no content
4. **Installation issues**: Use Python 3.8+ and install all dependencies


## 🧪 .env (template)
```
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=PersonaGenerator/1.0
GOOGLE_API_KEY=your_google_api_key_here
