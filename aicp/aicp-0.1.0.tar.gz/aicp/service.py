import typer
import os

app = typer.Typer()


@app.command('create')
def create_service(name: str):
    typer.echo(f"Create service: {name}")


@app.command('import')
def import_service():
    typer.echo(f"Import service")
    
    # get current directory
    current_dir = os.getcwd()
    print(current_dir)
    
    # get all files in current directory
    files = os.listdir(current_dir)
    print(files)
