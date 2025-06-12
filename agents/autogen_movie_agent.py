import autogen
from typing import List, Dict, Any
from config.config import settings
import json
from tmdbv3api import TMDb, Movie

class AutoGenMovieAgent:
    def __init__(self):
        # Initialize TMDB client
        self.tmdb = TMDb()
        self.tmdb.api_key = settings.TMDB_API_KEY
        self.movie_api = Movie()
        
        # Configure AutoGen agents
        self.config_list = [
            {
                "model": settings.GROQ_MODEL,
                "api_key": settings.GROQ_API_KEY,
                "api_type": "groq"
            }
        ]
        
        # Create the movie expert agent
        self.movie_expert = autogen.AssistantAgent(
            name="Movie_Expert",
            llm_config={
                "config_list": self.config_list,
                "temperature": settings.TEMPERATURE,
                "max_tokens": settings.MAX_TOKENS,
            },
            system_message="""You are a movie expert with extensive knowledge of films across all genres and eras.
            Your role is to understand user preferences and provide detailed movie recommendations.
            You can discuss plot details, themes, and cinematic elements of movies.
            When recommending movies, consider:
            1. User's stated preferences
            2. Similar movies they've enjoyed
            3. Current trends and critically acclaimed films
            4. Different genres that might appeal to them"""
        )
        
        # Create the preference analyzer agent
        self.preference_analyzer = autogen.AssistantAgent(
            name="Preference_Analyzer",
            llm_config={
                "config_list": self.config_list,
                "temperature": 0.3,  # Lower temperature for more consistent analysis
                "max_tokens": settings.MAX_TOKENS,
            },
            system_message="""You are a movie preference analyzer.
            Your role is to extract and analyze user preferences from their messages.
            Focus on identifying:
            1. Preferred genres
            2. Favorite actors/directors
            3. Time period preferences
            4. Specific themes or elements they enjoy
            Return your analysis in a structured JSON format."""
        )
        
        # Create the user proxy agent
        self.user_proxy = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            llm_config=False,
            system_message="A user looking for movie recommendations."
        )
        
        # Initialize the group chat
        self.groupchat = autogen.GroupChat(
            agents=[self.user_proxy, self.movie_expert, self.preference_analyzer],
            messages=[],
            max_round=10
        )
        
        # Create the manager
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config={
                "config_list": self.config_list,
                "temperature": settings.TEMPERATURE,
                "max_tokens": settings.MAX_TOKENS,
            }
        )
        
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
    
    def process_message(self, message: str) -> str:
        """
        Process a user message using AutoGen agents.
        
        Args:
            message (str): The user's message
            
        Returns:
            str: The agent's response
        """
        # Initialize the chat with the manager
        self.user_proxy.initiate_chat(
            self.manager,
            message=message
        )
        
        # Get the last message from the chat
        last_message = self.user_proxy.last_message()
        
        # Check if we need to get movie recommendations
        if any(keyword in message.lower() for keyword in ["recommend", "suggest", "find", "looking for"]):
            # Extract preferences using the preference analyzer
            preferences = self._extract_preferences(message)
            recommendations = self.get_recommendations(preferences)
            
            if recommendations:
                formatted_recommendations = self._format_recommendations(recommendations)
                # Add the recommendations to the chat
                self.user_proxy.send(
                    recipient=self.manager,
                    message=f"Based on your preferences, here are some recommendations:\n\n{formatted_recommendations}"
                )
                return formatted_recommendations
            else:
                return "I couldn't find any movies matching your preferences. Could you try being more specific?"
        
        return last_message.get("content", "I apologize, but I'm having trouble processing your request right now.")
    
    def _extract_preferences(self, message: str) -> Dict[str, Any]:
        """
        Extract movie preferences from the user's message using the preference analyzer.
        
        Args:
            message (str): The user's message
            
        Returns:
            Dict[str, Any]: Extracted preferences
        """
        extraction_prompt = f"""Extract movie preferences from this message: "{message}"
        Return a JSON object with keys: genres, year_range, keywords, and any other relevant preferences."""
        
        # Use the preference analyzer to extract preferences
        self.user_proxy.initiate_chat(
            self.preference_analyzer,
            message=extraction_prompt
        )
        
        try:
            response = self.user_proxy.last_message().get("content", "{}")
            return json.loads(response)
        except:
            return {"query": message}  # Fallback to using the message as a query 