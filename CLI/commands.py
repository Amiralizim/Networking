import click
from query import *

'''Mantain this token to keep track is session is admin session or user session'''
is_admin_session = 0
current_user = None
src_ip = ""
src_port = ""
dst_ip = ""
dst_port = ""
# this global variable is used for private or public modes
mode = ""


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
@click.option("--clientchoice", prompt="Please one of the following options to recieve information: privateIps, publicIps, protocolName, webServices")
def client_option(clientchoice):
    global current_user
    global mode
    if(clientchoice == "privateIps"):
        # get the first range
        click.secho("The first ip range options are: ", fg="green", nl=False)
        mode = "private"
        defaults = get_first_ip_range(mode)
        for x in defaults:
            click.secho(str(x), fg="blue", nl=False)
            click.secho(", ", fg="blue", nl=False) 
        click.secho(" ", nl=True)
        privateIps_first(None)
    elif(clientchoice == "publicIps"):
        # get the first range
        click.secho("The first ip range options are: ", fg="green", nl=False)
        mode = "public"
        defaults = get_first_ip_range(mode)
        for x in defaults:
            click.secho(str(x), fg="blue", nl=False)
            click.secho(", ", fg="blue", nl=False) 
        click.secho(" ", nl=True)
        # for x in defaults:
        #     click.secho(x,fg="blue")
        privateIps_first(None)
    elif(clientchoice == "protocolName"):
        click.secho("Different protocolName options are: ", fg="green", nl=False)
        defaults = get_protocol_name()
        for x in defaults:
            click.secho(str(x), fg="blue", nl=False)
            click.secho(", ", fg="blue", nl=False) 
        click.secho(" ", nl=True)
    elif(clientchoice == "webServices"):
        defaults = get_webservice_names()
        for x in defaults:
            click.secho(str(x), fg="blue", nl=False)
            click.secho(", ", fg="blue", nl=False) 
        click.secho(" ", nl=True)
        

''' Use this command to choose the client option'''
@click.command()
@click.option("--firstiprange", prompt="Please choose one of the above options", default = "")
def privateIps_first(firstiprange):
    global src_ip
    global mode
    src_ip = firstiprange
    click.secho("The second ip range options are: ", fg="green", nl=False)
    defaults = get_second_ip_range(mode, firstiprange)
    for x in defaults:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    privateIps_second(None)


@click.command()
@click.option("--secondiprange", prompt="Please choose one of the above options", default = "")
def privateIps_second(secondiprange):
    global src_ip
    global mode
    src_ip = src_ip + "." + secondiprange
    click.secho("The third ip range options are: ", fg="green", nl=False)
    defaults = get_third_ip_range(mode, secondiprange)
    for x in defaults:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    privateIps_third(None)

@click.command()
@click.option("--thirdiprange", prompt="Please choose one of the above options", default = "")
def privateIps_third(thirdiprange):
    global src_ip
    global mode
    src_ip = src_ip + "." + thirdiprange
    click.secho("The fourth ip range options are: ", fg="green", nl=False)
    defaults = get_fourth_ip_range(mode, thirdiprange)
    for x in defaults:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    privateIps_fourth(None)

@click.command()
@click.option("--fourthiprange", prompt="Please choose one of the above options", default = "")
def privateIps_fourth(fourthiprange):
    global src_ip
    global mode
    src_ip = src_ip + "." + fourthiprange
    defaults = get_fourth_ip_range(mode, fourthiprange)
    for x in defaults:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    src_port_options = get_source_ports(src_ip)
    click.secho("The source port options for private ip {} are: ".format(src_ip), fg="green", nl=False)
    for y in src_port_options:
        click.secho(str(y), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    src_port_selection(None)


@click.command()
@click.option("--sourceport", prompt="Please choose one of the above port options", default="")
def src_port_selection(sourceport):
    global src_port
    global src_ip
    src_port = sourceport
    dst_ip_options = get_dst_ips(src_ip, src_port)
    click.secho("The destination ip options for private source ip {} and source port {} are: ".format(src_ip, src_port), fg="green", nl=False)
    for x in dst_ip_options:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    dst_ip_selection(None)

@click.command()
@click.option("--dstip", prompt="Please choose one of the above destination ip options", default="")
def dst_ip_selection(dstip):
    global src_port
    global src_ip
    global dst_ip
    dst_ip = dstip
    click.secho("The destination port options for private source ip {}, source port {} and destination ip {} are: ".format(src_ip, src_port, dst_ip), fg="green", nl=False)
    dst_port_options = get_dst_ports(src_ip, src_port, dst_ip)
    for x in dst_port_options:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    dst_port_selection(None)

@click.command()
@click.option("--dstport", prompt="Please choose one of the above destination ip options", default="")
def dst_port_selection(dstport):
    global src_port
    global src_ip
    global dst_port
    global dst_ip
    dst_port = dstport
    click.secho("The destination port options for private source ip {}, source port {}, destination ip {} and destination port {} are: ".format(src_ip, src_port, dst_ip, dst_port), fg="green", nl=False)
    generate_flow_index(src_ip, dst_ip, src_port, dst_port)
    


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
@click.option("--flow_index", prompt="Enter the Flow_index of a flow you wish to operate upon", help="Provide the Flow_index", default = "")
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


