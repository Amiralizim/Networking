import click
from query import *

'''Mantain this token to keep track is session is admin session or user session'''
is_admin_session = 0
current_user = None
current_date = None
current_time = None
current_date_time = None



@click.command()
@click.option("--username", prompt="Please enter your username:", help="Provide the username", default = "")
@click.option("--password", prompt = "Please enter your password:", help = "Provide the password", default = "", hide_input = True)
def login(username, password):
    global current_user
    if authenticate(username, password) == True:
        current_user = username
        click.secho("Succesfully logged in!", fg = 'green')
        is_admin_session = get_session_token(username)
        # annotate(None, None)
        client_option(None)
    else:
        click.secho("ERROR: INCORRECT CREDENTIALS", fg = 'red')

''' Use this command to choose the client option '''
@click.command()
@click.option("--clientchoice", prompt="Please one of the following options to recieve information: time, links, protocol")
def client_option(clientchoice):
    global current_user
    if(clientchoice == "time"):
        date_option(None, None)
    if(clientchoice == "protocol"):
        print("TO BE IMPLEMENTED")
    if(clientchoice == "links"):
        #generate_flow_index("10.200.1.118", "0", "10.200.7.194", "0") # test purpose
        generate_flow_index(None, None, None, None)

''' Use this command to annotate a particular time '''
@click.command()
@click.option("--time1", prompt="Please enter the first year begining for the range")
@click.option("--time2", prompt="Please enter the second year end for the range")
def date_option(time1, time2):
    global current_date
    click.secho("The available dates in the system for the provided range are: ")
    current_date = get_flow_dates(time1, time2)
    click.secho("Dates: {}".format(current_date), fg = 'yellow')
    time_option(None)

@click.command()
@click.option("--time1", prompt="Please select a specific date from the covered range of dates in the system")
def time_option(time1):
    global current_time
    click.secho("The available times in the system for the provided date are: ")
    current_time = get_flow_times(time1)
    click.secho("Times: {}".format(current_time), fg='yellow')
    # concat the specific date and time string
    
    flow_based_on_time_option(None)

@click.command()
@click.option("--chosentime", prompt="Please select a specific time from the covered range of times in the system")
def flow_based_on_time_option(chosentime):
    global current_date_time
    current_date_time = current_date + ' ' + chosentime 
    click.secho("FlowIDs: {}".format(get_flows_based_on_time(current_date_time)))
    client_option(None)



''' Use this command to annotate a particular flowID , a non admin user can annotate'''
@click.command()
@click.option("--flowid", prompt="Please enter the flowid which you wish to annotate", help = "Provide the flowid", default = "")
@click.option("--annotation", prompt = "Please provide the annotation text")
def annotate(flowid, annotation):
    global current_user

    if add_annotation(current_user, flowid, annotation) == 1:
        click.secho("Succesfully added in annotation", fg = 'green')
    else:
        click.secho("Error adding annotation", fg = 'red')


''' Use this command to get the source details and destiantion details which can be used to generate our flow_id '''
@click.command()
@click.option("--sourceip", prompt="Enter the sourceip", help="Provide the sourceip", default = "10.200.1.118")
@click.option("--sourceport", prompt="Enter the sourceport", help="Provide the sourceport", default = "0")
@click.option("--destinationip", prompt="Enter the destinationip", help="Provide the destinationip", default = "10.200.7.194")
@click.option("--destinationport", prompt="Enter the destinationport", help="Provide the destinationport", default = "0")
def generate_flow_index(sourceip, destinationip, sourceport, destinationport):
    source = sourceip + ":" + sourceport
    click.secho(source, fg = 'blue')
    destination = destinationip + ":" + destinationport
    click.secho(destination, fg = 'green')

    Link_ID = find_links(sourceip, sourceport, destinationip, destinationport)
    Flow_indexes = find_flows(Link_ID)  # Flow_index is a [] where each element is a Flow_index (int)

    click.secho("The Link_ID is:           ", fg="green", nl=False)
    click.echo(Link_ID)
    click.secho("The found Flow_index are: ", fg="green", nl=False)
    click.echo(Flow_indexes)

    display_or_annotate(None)


''' Use this command to get the Flow_index of a flow that its information will be provided '''
@click.command()
@click.option("--flow_index", prompt="Enter the Flow_index of a flow you wish to operate upon", help="Provide the Flow_index", default = "92612")
def display_or_annotate(flow_index):
    choice = ""
    while (choice != "7"):
        click.secho("(1) check total packet information")
        click.secho("(2) check forward packet information")
        click.secho("(3) check backward packet information")
        click.secho("(4) check protocol packet information")
        click.secho("(5) check flag packet information")
        click.secho("(6) add an annotation")
        click.secho("(7) exit")
        choice = click.prompt('Please choose one of the options (1/2/3/4/5/6/7)')  # choice is string 

        # TODO: implement each of these print functions, for protocol and flag need to check if its from origin 1 or 2 before printing
        if (choice == "1"):
            display_total(flow_index)
        elif (choice == "2"):
            display_forward(flow_index)
        elif (choice == "3"):
            display_backward(flow_index)
        elif (choice == "4"):
            display_protocol(flow_index)
        elif (choice == "5"):
            display_flag(flow_index)
        # elif (choice == "6"):
        #     annotate(flow_index, None)         # TODO for ppt: this will still ask the user for the Flow_index, which is redundant


