import groq
from typing import List, Dict, Any
from config.config import settings
import json
from tmdbv3api import TMDb, Movie
import streamlit as st

class GroqAgent:
    def __init__(self, api_key: str, model: str):
        self.client = groq.Groq(api_key=api_key)
        self.model = model
        
    def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 1000) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now."

class MovieRecommendationAgent:
    def __init__(self):
        # Initialize Groq client
        self.groq_agent = GroqAgent(
            api_key=settings.GROQ_API_KEY,
            model=settings.GROQ_MODEL
        )
        
        # Initialize TMDB client
        self.tmdb = TMDb()
        self.tmdb.api_key = settings.TMDB_API_KEY
        self.movie_api = Movie()
        
        self.conversation_history = []
        
    def start_conversation(self, initial_message: str) -> None:
        """
        Start a conversation with the movie recommendation agent.
        
        Args:
            initial_message (str): The initial message from the user
        """
        self.conversation_history = [
            {"role": "system", "content": settings.SYSTEM_MESSAGE},
            {"role": "user", "content": initial_message}
        ]
        response = self.groq_agent.generate_response(
            messages=self.conversation_history,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS
        )
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
    
    def process_message(self, message: str) -> str:
        """
        Process a single message and return the agent's response.
        
        Args:
            message (str): The user's message
            
        Returns:
            str: The agent's response
        """
        self.conversation_history.append({"role": "user", "content": message})
        
        # Check if the message is about movie recommendations
        if any(keyword in message.lower() for keyword in ["recommend", "suggest", "find", "looking for"]):
            # Extract preferences from the conversation
            preferences = self._extract_preferences(message)
            recommendations = self.get_recommendations(preferences)
            
            # Format recommendations into a response
            if recommendations:
                response = self._format_recommendations(recommendations)
                # Store recommendations in session state for Streamlit
                st.session_state.last_recommendations = recommendations
            else:
                response = "I couldn't find any movies matching your preferences. Could you try being more specific?"
        else:
            # Generate a general response using Groq
            response = self.groq_agent.generate_response(
                messages=self.conversation_history,
                temperature=settings.TEMPERATURE,
                max_tokens=settings.MAX_TOKENS
            )
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response
    
    def _extract_preferences(self, message: str) -> Dict[str, Any]:
        """
        Extract movie preferences from the user's message.
        
        Args:
            message (str): The user's message
            
        Returns:
            Dict[str, Any]: Extracted preferences
        """
        # Use Groq to extract preferences
        extraction_prompt = f"""Extract movie preferences from this message: "{message}"
        Return a JSON object with keys: genres, year_range, keywords, and any other relevant preferences."""
        
        try:
            response = self.groq_agent.generate_response(
                messages=[{"role": "user", "content": extraction_prompt}],
                temperature=0.3,  # Lower temperature for more consistent extraction
                max_tokens=500
            )
            return json.loads(response)
        except:
            return {"query": message}  # Fallback to using the message as a query
    
    def _format_recommendations(self, recommendations: List[Dict[str, Any]]) -> str:
        """
        Format movie recommendations into a readable response.
        
        Args:
            recommendations (List[Dict[str, Any]]): List of movie recommendations
            
        Returns:
            str: Formatted response
        """
        if not recommendations:
            return "I couldn't find any movies matching your preferences."
        
        response = "Here are some movies you might enjoy:\n\n"
        for movie in recommendations:
            response += f"🎬 {movie['title']} ({movie['year']})\n"
            response += f"⭐ Rating: {movie['rating']}/10\n"
            response += f"📝 {movie['description'][:200]}...\n"
            response += f"🎭 Genres: {', '.join(movie['genres'])}\n\n"
        
        return response
    
    def get_recommendations(self, preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get movie recommendations based on user preferences.
        
        Args:
            preferences (Dict[str, Any]): User preferences for movies
            
        Returns:
            List[Dict[str, Any]]: List of movie recommendations
        """
        try:
            # Search for movies based on preferences
            search_results = self.movie_api.search(preferences.get('query', ''))
            
            # Get detailed information for each movie
            recommendations = []
            for movie in search_results[:5]:  # Limit to top 5 results
                movie_details = self.movie_api.details(movie.id)
                recommendations.append({
                    "title": movie_details.title,
                    "year": movie_details.release_date.split('-')[0] if movie_details.release_date else "N/A",
                    "description": movie_details.overview,
                    "rating": movie_details.vote_average,
                    "genres": [genre.name for genre in movie_details.genres],
                    "poster_path": movie_details.poster_path,
                    "backdrop_path": movie_details.backdrop_path,
                    "id": movie_details.id
                })
            
            return recommendations
        except Exception as e:
            print(f"Error fetching movie recommendations: {str(e)}")
            return [] 