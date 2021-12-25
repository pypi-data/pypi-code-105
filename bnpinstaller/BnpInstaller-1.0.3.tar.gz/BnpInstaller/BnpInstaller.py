from pathlib import Path
import typer
import bcml.util
from bcml.install import install_mod

app = typer.Typer()

@app.command()
def install(bnp: Path, update: bool = False, remerge: bool = False):
    print(f'Installing {bnp} . . .')
    install_mod(mod=Path(bnp), updated=bool(update), merge_now=bool(remerge))

if __name__ == '__main__':
    app()