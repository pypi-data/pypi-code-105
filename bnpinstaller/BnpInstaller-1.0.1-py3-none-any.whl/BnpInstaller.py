from pathlib import Path
import typer
import bcml.util
from bcml.install import install_mod

app = typer.Typer()

@app.command()
def install(bnp: Path, is_update: bool = True, remerge: bool = True):
    print(f'Installing {bnp} . . .')
    install_mod(mod=Path(bnp), is_update=is_update, merge_now=remerge)

if __name__ == '__main__':
    app()