from agents.autogen_movie_agent import AutoGenMovieAgent
from config.config import settings
import json
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt

def main():
    console = Console()
    
    # Initialize the movie recommendation agent
    agent = AutoGenMovieAgent()
    
    # Welcome message
    console.print(Panel.fit(
        "[bold blue]🎬 Movie Recommendation Assistant[/bold blue]\n\n"
        "Welcome to your personal movie recommendation assistant!\n"
        "Tell me what kind of movies you like, and I'll help you discover your next favorite film.",
        title="Welcome",
        border_style="blue"
    ))
    
    # Help message
    console.print("\n[bold]How to use:[/bold]")
    console.print("1. Tell me what kind of movies you like")
    console.print("2. Share your preferences (genres, actors, etc.)")
    console.print("3. Get personalized recommendations")
    console.print("4. Type 'quit' or 'exit' to end the conversation\n")
    
    # Main conversation loop
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
            
            # Check for exit command
            if user_input.lower() in ['quit', 'exit', 'bye']:
                console.print("\n[bold green]Goodbye! Hope you found a great movie to watch![/bold green]")
                break
            
            # Get agent's response
            response = agent.process_message(user_input)
            
            # Display response
            console.print(f"\n[bold yellow]Assistant:[/bold yellow]")
            console.print(Markdown(response))
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Session terminated by user.[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred: {str(e)}[/bold red]")
            continue

if __name__ == "__main__":
    main() 