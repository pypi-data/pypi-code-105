import typer
import service
import solution

app = typer.Typer()
app.add_typer(service.app, name="service")
app.add_typer(solution.app, name="solution")
