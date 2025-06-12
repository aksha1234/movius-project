import typer
from rich.console import Console
from rich.prompt import Prompt
from agents.autogen_movie_agent import AutoGenMovieAgent
from config.config import settings

app = typer.Typer()
console = Console()

@app.command()
def start():
    """Start the movie recommendation agent."""
    console.print("[bold green]Welcome to the Movie Recommendation Agent![/bold green]")
    console.print("I'm here to help you find the perfect movie to watch.")
    
    agent = AutoGenMovieAgent()
    
    while True:
        try:
            user_input = Prompt.ask("\n[bold blue]You[/bold blue]")
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                console.print("[bold green]Goodbye! Hope you found a great movie to watch![/bold green]")
                break
                
            response = agent.process_message(user_input)
            console.print(f"\n[bold yellow]Agent[/bold yellow]: {response}")
            
        except KeyboardInterrupt:
            console.print("\n[bold red]Session terminated by user.[/bold red]")
            break
        except Exception as e:
            console.print(f"[bold red]An error occurred: {str(e)}[/bold red]")
            continue

if __name__ == "__main__":
    app() 