# AI Conversational Agent - Movie Recommendation System

## Overview
This project implements an intelligent conversational agent that helps users discover and get recommendations for movies based on their preferences and interests. The agent uses a multi-turn conversation approach to understand user preferences and provide personalized movie recommendations.

## Features
- Natural language understanding of movie preferences
- Multi-turn conversation capability
- Personalized movie recommendations
- Fallback handling for unclear requests
- Context-aware responses
- Integration with movie database API
- Rich command-line interface with colored output

## Technical Architecture
The system is built using:
- Python 3.9+
- Groq LLM for natural language processing
- TMDB API for movie data
- Rich library for terminal formatting
- SQLite for conversation state management

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd movie-recommendation-agent
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys:
# - GROQ_API_KEY: Your Groq API key
# - TMDB_API_KEY: Your TMDB API key
```

5. Run the application:
```bash
python app.py
```

## Project Structure
```
movie-recommendation-agent/
├── agents/
│   ├── __init__.py
│   └── movie_agent.py
├── config/
│   └── config.py
├── database/
│   └── conversation_store.py
├── services/
│   ├── movie_service.py
│   └── conversation_service.py
├── utils/
│   ├── logger.py
│   └── helpers.py
├── app.py
├── requirements.txt
└── README.md
```

## Usage Guide

### Starting the Application
Run the application using:
```bash
python app.py
```

### Basic Commands
- Type your movie preferences or questions
- Type 'quit', 'exit', or 'bye' to end the conversation
- Press Ctrl+C to terminate the session

### Example Interaction
```
Welcome to Movie Recommendation Assistant!

How to use:
1. Tell me what kind of movies you like
2. Share your preferences (genres, actors, etc.)
3. Get personalized recommendations
4. Type 'quit' or 'exit' to end the conversation

You: I'm looking for a good movie to watch tonight
Assistant: I'd be happy to help you find a movie! Could you tell me what kind of movies you usually enjoy?

You: I like action movies with some comedy
Assistant: Great choice! Would you prefer recent releases or are you open to older classics as well?

You: Recent ones would be better
Assistant: I have a few recommendations for you. How about "Bullet Train" (2022) - it's an action-comedy with Brad Pitt, or "The Unbearable Weight of Massive Talent" (2022) starring Nicolas Cage?

You: Tell me more about Bullet Train
Assistant: "Bullet Train" is a 2022 action-comedy directed by David Leitch. It follows five assassins aboard a bullet train in Japan, with Brad Pitt playing a reluctant assassin. The movie features intense action sequences, witty dialogue, and an ensemble cast. Would you like to know more about the cast or the plot?
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

