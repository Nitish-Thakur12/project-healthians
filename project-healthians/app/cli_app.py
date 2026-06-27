import sys
import os
# This ensures Python can find the 'src' and 'data' folders from the root directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.nlp_engine import extract_symptoms
from src.matcher import load_knowledge_base, find_conditions

console = Console()
kb = load_knowledge_base()

def main():
    # Displaying the critical medical disclaimer as required
    console.print(Panel("[bold cyan]Healthcare Symptom Assistant[/]\n[dim]For educational use only. Does NOT provide medical diagnoses.[/]"))
    
    user_input = console.input("\n[yellow]Describe your symptoms: [/]")
    symptoms = extract_symptoms(user_input)
    
    if not symptoms:
        console.print("[red]No matching symptoms detected in our database. Please try again.[/]")
        return

    console.print(f"[green]Detected symptoms:[/] {symptoms}")
    results = find_conditions(symptoms, kb)
    
    if not results:
        console.print("[red]No matching conditions found.[/]")
        return

    for r in results:
        console.print("\n")
        tbl = Table(title="Possible Conditions", style="cyan")
        tbl.add_column("Condition")
        tbl.add_column("Confidence")
        
        for c in r["conditions"]:
            tbl.add_row(c["name"], c["confidence"])
        console.print(tbl)
        
        # Color-coding the urgency flag
        urgency_color = {"HOME": "green", "DOCTOR": "yellow", "EMERGENCY": "red"}
        color = urgency_color.get(r["urgency"], "white")
        console.print(f"Urgency: [{color}]{r['urgency']}[/]")
        
        console.print("[bold]Recommendations:[/]")
        for rec in r["recommendations"]:
            console.print(f" - [dim]{rec}[/]")

if __name__ == "__main__":
    main()
    