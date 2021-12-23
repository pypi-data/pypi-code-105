from pathlib import Path
import typer
import bcml.util
from bcml.install import install_mod

app = typer.Typer()

@app.command()
def install(bnp: Path):
    print(f'Installing {bnp} . . .')
    install_mod(mod=Path(bnp), merge_now=True)

if __name__ == '__main__':
    app()