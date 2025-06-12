# AI Movie Recommendation System with AutoGen

## Overview
This project implements an intelligent movie recommendation system using AutoGen's multi-agent framework. The system uses multiple specialized agents to provide personalized movie recommendations through natural conversation. Each agent has a specific role in understanding user preferences and providing detailed movie suggestions.

## Features
- Multi-agent conversation system using AutoGen
- Specialized agents for different aspects of movie recommendations:
  - Movie Expert: Provides detailed movie knowledge and recommendations
  - Preference Analyzer: Extracts and analyzes user preferences
  - User Proxy: Manages user interaction
- Natural language understanding of movie preferences
- Integration with TMDB API for movie data
- Rich command-line interface with colored output
- Group chat capabilities for collaborative recommendations

## Technical Architecture
The system is built using:
- Python 3.9+
- AutoGen framework for multi-agent conversations
- Groq LLM for natural language processing
- TMDB API for movie data
- Rich library for terminal formatting

## Agent Roles

### Movie Expert Agent
- Provides detailed movie recommendations
- Discusses plot details, themes, and cinematic elements
- Considers user preferences and similar movies
- Suggests different genres that might appeal to the user

### Preference Analyzer Agent
- Extracts and analyzes user preferences
- Identifies preferred genres, actors, and directors
- Determines time period preferences
- Recognizes specific themes or elements users enjoy

### User Proxy Agent
- Manages the conversation flow
- Coordinates between different agents
- Handles user input and output
- Maintains conversation context

## Setup Instructions

1. Clone the repository:
```bash
git clone [repository-url]
cd movie-recommendation-system
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
movie-recommendation-system/
├── agents/
│   └── autogen_movie_agent.py
├── config/
│   └── config.py
├── app.py
├── main.py
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
Movie Expert: I'd be happy to help! Could you tell me what kind of movies you usually enjoy?

You: I like action movies with some comedy
Preference Analyzer: I've analyzed your preferences. You seem to enjoy action-comedy films. Would you prefer recent releases or are you open to older classics as well?

Movie Expert: Based on your preference for action-comedy, I'd recommend "Bullet Train" (2022). It's a perfect blend of action and humor, starring Brad Pitt as a reluctant assassin on a high-speed train in Japan. The movie features intense action sequences, witty dialogue, and an ensemble cast.

[System provides formatted recommendations with details]
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

