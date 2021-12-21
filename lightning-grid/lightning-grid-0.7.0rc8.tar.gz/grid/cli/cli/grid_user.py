import click

from grid.cli import rich_click
from grid.cli.client import credentials_from_env
from grid.cli.core.team import Team
from grid.sdk._gql.queries import get_user_info
from grid.sdk import user as sdk_user, list_clusters


@rich_click.group(invoke_without_command=True)
@click.pass_context
def user(ctx):
    """Show the user information of the authorized user for this CLI instance."""
    if ctx.invoked_subcommand is not None:
        return

    creds = credentials_from_env()
    user_info = get_user_info()

    email = user_info['email']
    email = email if email is not None else "N/A"

    click.echo(f"Display name: {user_info['firstName']} {user_info['lastName']}")
    click.echo(f"UserID      : {creds.user_id}")
    click.echo(f"Username    : {user_info['username']}")
    click.echo(f"Email       : {email}")

    teams = Team.get_all()
    if teams:
        click.echo("Teams:\n-")
        for t in teams:
            click.echo(f"  {t.name} - Role: {t.role}")


@user.command()
@click.argument('cluster_name', type=str)
def set_default_cluster(cluster_name: str):
    """Specify the default CLUSTER_ID which all operations should be run against.
    """
    cluster_resp = list_clusters()
    for cluster in cluster_resp.clusters:
        if cluster_name == cluster.name:
            cluster_id = cluster.id
            break
    else:
        raise click.ClickException(f"Cluster with name {cluster_name} not found")
    sdk_user.set_default_cluster(cluster_id)
