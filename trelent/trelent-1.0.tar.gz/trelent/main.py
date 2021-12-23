# Copyright (c) 2021 Trelent Inc.

# External modules
import click

# Internal modules
import trelent.auth_module as auth_module
import trelent.docgen as docgen

@click.group()
def trelent():
    pass

@click.command()
@click.password_option(prompt='Your API Key')
def auth(password):
    if auth_module.set_api_key(password) and auth_module.is_valid_api_key(password):
        click.echo(u'\u001b[32;1mAdded API Key Successfully!')
    else:
        click.echo(u'\u001b[31;1mThe API Key you used is invalid. Please copy your API Key from our dashboard.')

@click.command()
@click.option('--key', '-k', help="Provide an API Key directly without storing in plaintext within a config file.")
@click.option('--verbose', '-v', is_flag=True, help="Should we print verbose logs?")
@click.option('--insert', '-i', is_flag=True, help="Should we automatically insert the docstrings?")
@click.argument('folder')
def document(folder, insert, verbose, key):
    click.echo(u'\u001b[33;1mAttempting to document python files in ' + folder + u'\u001b[33;1m  ...')

    # Check for authentication
    if(key != None):
        # Use provided api key
        api_key = key

    else:
        # Check config file
        api_key = auth_module.get_api_key()
        if(api_key == None):
            click.echo(u"\u001b[31;1mYou have not added your API Key yet! Try running 'trelent auth' or provide your api key directly using the '--key' option")
            return

    if(not auth_module.is_valid_api_key(api_key)):
        click.echo(u"\u001b[31;1mThe API Key you used is invalid. Please copy your API Key from our dashboard.")
        return

    try:
        docgen.document_folder(api_key, insert, folder, verbose)
        click.echo(u'\u001b[32;1mSuccessfully documented ' + folder + u'\u001b[32;1m!')
    except Exception as e:
        click.echo(u'\u001b[31;1mError: ' + str(e))
        click.echo(u'\u001b[31;1mAn error occured while documenting the provided folder')

trelent.add_command(auth)
trelent.add_command(document)

if __name__ == '__main__':
    trelent()