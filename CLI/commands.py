import click
from query import *

'''Mantain this token to keep track is session is admin session or user session'''
is_admin_session = 0

@click.group()
def cli():
    pass


@click.command()
@click.option("--username", prompt="Please enter your username:", help="Provide the username", default = "")
@click.option("--password", prompt = "Please enter your password:", help = "Provide the password", default = "", hide_input = True)
def login(username, password):
    if authenticate(username, password) == True:
        click.secho("Succesfully logged in!", fg = 'green')
        is_admin_session = get_session_token(username)
        generate_flow_id()
    else:
        click.secho("ERROR: INCORRECT CREDENTIALS", fg = 'red')



''' Use this command to get the source details and destiantion details which can be used to generate our flow_id '''
@click.command()
@click.option("--sourceip", prompt="Enter the sourceip", help="Provide the sourceip", default = "")
@click.option("--sourceport", prompt="Enter the sourceport", help="Provide the sourceport", default = "")
@click.option("--destinationip", prompt="Enter the destinationip", help="Provide the destinationip", default = "")
@click.option("--destinationport", prompt="Enter the destinationport", help="Provide the destinationport", default = "")
def generate_flow_id(sourceip, destinationip, sourceport, destinationport):
    source = sourceip + ":" + sourceport
    click.secho(source, fg = 'blue')
    destination = destinationip + ":" + destinationport
    click.secho(destination, fg = 'green')
    click.secho("The found flows are: ")
    click.secho("Flow_index, Link_ID, srcIP, srcPort, dstPort", fg = 'yellow')
    find_flows(sourceip, sourceport, destinationip, destinationport)


cli.add_command(login)
cli.add_command(generate_flow_id)
