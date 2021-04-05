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
@click.option("--username", prompt="Please enter your username", help="Provide the username")
@click.option("--password", prompt = "Please enter your password", help = "Provide the password", hide_input = True)
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
        login(None, None)

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
        privateIps_first(None)
    elif(clientchoice == "protocolName"):
        protocol()
    elif(clientchoice == "webServices"):
        web_service()
        

''' Use this command to choose the client option'''
@click.command()
@click.option("--firstiprange", prompt="Please choose one of the above options")
def privateIps_first(firstiprange):
    global src_ip
    global mode
    defaults = get_second_ip_range(mode, firstiprange)
    # invalid case
    if(not defaults):
        click.secho("incorrect value, try again!", fg="red")
        privateIps_first(None)
    src_ip = firstiprange
    click.secho("The second ip range options are: ", fg="green", nl=False)
    for x in defaults:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    privateIps_second(None)


@click.command()
@click.option("--secondiprange", prompt="Please choose one of the above options")
def privateIps_second(secondiprange):
    global src_ip
    global mode
    defaults = get_third_ip_range(mode, secondiprange)
    if(not defaults):
        click.secho("incorrect value, try again!", fg="red")
        privateIps_second(None)
    src_ip = src_ip + "." + secondiprange
    click.secho("The third ip range options are: ", fg="green", nl=False)
    for x in defaults:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    privateIps_third(None)

@click.command()
@click.option("--thirdiprange", prompt="Please choose one of the above options")
def privateIps_third(thirdiprange):
    global src_ip
    global mode
    defaults = get_fourth_ip_range(mode, thirdiprange)
    if(not defaults):
        click.secho("incorrect value, try again!", fg="red")
        privateIps_third(None)
    src_ip = src_ip + "." + thirdiprange
    click.secho("The fourth ip range options are: ", fg="green", nl=False)
    for x in defaults:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    privateIps_fourth(None)

@click.command()
@click.option("--fourthiprange", prompt="Please choose one of the above options")
def privateIps_fourth(fourthiprange):
    global src_ip
    global mode
    src_ip_t = src_ip + "." + fourthiprange
    src_port_options = get_source_ports(mode, src_ip_t)
    if(not src_port_options):
        click.secho("incorrect value, try again!", fg="red")
        privateIps_fourth(None)
    src_ip = src_ip + "." + fourthiprange
    click.secho("The source port options for private ip {} are: ".format(src_ip), fg="green", nl=False)
    for y in src_port_options:
        click.secho(str(y), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    src_port_selection(None)


@click.command()
@click.option("--sourceport", prompt="Please choose one of the above port options")
def src_port_selection(sourceport):
    global src_port
    global src_ip
    global mode
    src_port = sourceport
    dst_ip_options = get_dst_ips(mode, src_ip, src_port)
    if(not dst_ip_options):
        click.secho("incorrect value, try again!", fg="red")
        src_port_selection(None)
    click.secho("The destination ip options for private source ip {} and source port {} are: ".format(src_ip, src_port), fg="green", nl=False)
    for x in dst_ip_options:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    dst_ip_selection(None)

@click.command()
@click.option("--dstip", prompt="Please choose one of the above destination ip options")
def dst_ip_selection(dstip):
    global mode
    global src_port
    global src_ip
    global dst_ip
    dst_ip = dstip
    dst_port_options = get_dst_ports(mode, src_ip, src_port, dst_ip)
    if(not dst_port_options):
        click.secho("incorrect value, try again!", fg="red")
        dst_ip_selection(None)
    click.secho("The destination port options for private source ip {}, source port {} and destination ip {} are: ".format(src_ip, src_port, dst_ip), fg="green", nl=False)
    for x in dst_port_options:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False)
    click.secho(" ", nl=True)
    dst_port_selection(None)

@click.command()
@click.option("--dstport", prompt="Please choose one of the above destination port options")
def dst_port_selection(dstport):
    global src_port
    global src_ip
    global dst_port
    global dst_ip
    dst_port = dstport
    generate_flow_index(src_ip, dst_ip, src_port, dst_port)
    


''' Use this command to annotate a particular flowID , a non admin user can annotate'''
@click.command()
@click.option("--flowid", prompt="Please enter the flowid which you wish to annotate", help = "Provide the flowid")
@click.option("--annotation", prompt = "Please provide the annotation text")
def annotate(flowid, annotation):
    global current_user

    if add_annotation(current_user, flowid, annotation) == 1:
        click.secho("Succesfully added in annotation", fg = 'green')
    else:
        click.secho("Error adding annotation", fg = 'red')


''' Use this command to get the source details and destiantion details which can be used to generate our flow_id '''
def generate_flow_index(sourceip, destinationip, sourceport, destinationport):
    Link_ID = find_links(sourceip, sourceport, destinationip, destinationport)
    if(not Link_ID):
        click.secho("incorrect value, try again!", fg="red")
        dst_port_selection(None)
    Flow_indexes = find_flows(Link_ID)
    if(not Flow_indexes):
        click.secho("inccorect value, try again!", fg="red")
        dst_port_selection(None)
    source = sourceip + ":" + sourceport
    click.secho(source, fg = 'blue')
    destination = destinationip + ":" + destinationport
    click.secho(destination, fg = 'green')
    click.secho("The Link_ID is:           ", fg="green", nl=False)
    click.echo(Link_ID)
    click.secho("The found Flow_index are: ", fg="green", nl=False)
    click.echo(Flow_indexes)

    display_or_annotate(None)


''' Use this command to get the Flow_index of a flow that its information will be provided '''
@click.command()
@click.option("--flow_index", prompt="Enter the Flow_index of a flow you wish to operate upon", help="Provide the Flow_index")
def display_or_annotate(flow_index):
    choice = ""
    while (choice != "8"):
        click.secho("(1) check total packet information")
        click.secho("(2) check forward packet information")
        click.secho("(3) check backward packet information")
        click.secho("(4) check protocol packet information")
        click.secho("(5) check flag packet information")
        click.secho("(6) add an annotation")
        click.secho("(7) start from begining")
        click.secho("(8) exit")
        choice = click.prompt('Please choose one of the options (1/2/3/4/5/6/7)')  # choice is string 

        if (choice == "1"):
            record = display_total(flow_index)
            if not record:
                click.secho("no data present!", fg="red")
                dst_port_selection(None)
            click.secho("Flow_index:    ", fg="yellow", nl=False)
            click.echo(record[0])
            click.secho("minimum packet size:    ", fg="yellow", nl=False)
            click.echo(record[1])           # min_ps
            click.secho("maximum packet size:    ", fg="yellow", nl=False)
            click.echo(record[2])           # max_ps 
            click.secho("average packet size:    ", fg="yellow", nl=False)
            click.echo(record[3])           # avg_ps
            click.secho("standard deviation packet size:    ", fg="yellow", nl=False)
            click.echo(record[4])           # std_dev_ps
            click.secho("minimum packet interarrival time:    ", fg="yellow", nl=False)
            click.echo(record[5])           # min_piat
            click.secho("maximum packet interarrival time:    ", fg="yellow", nl=False)
            click.echo(record[6])           # max_piat
            click.secho("average packet interarrival time:    ", fg="yellow", nl=False)
            click.echo(record[7])           # avg_piat
            click.secho("standard deviation packet interarrival time:    ", fg="yellow", nl=False)
            click.echo(record[8])           # std_dev_piat
        elif (choice == "2"):
            record = display_forward(flow_index)
            if not record:
                click.secho("no data present!", fg="red")
                dst_ip_selection(None)
            click.secho("The following attributes are in representing packets in the FORWARD direction!", fg="red")
            click.secho("Flow_index:    ", fg="yellow", nl=False)
            click.echo(record[0])
            click.secho("number of packets (F):    ", fg="yellow", nl=False)
            click.echo(record[1])           # f_pktTotalCount
            click.secho("total of bytes exchanged (F):     ", fg="yellow", nl=False)
            click.echo(record[2])           # f_octetTotalCount
            click.secho("minimum packet size (F):    ", fg="yellow", nl=False)
            click.echo(record[3])           # f_min_ps
            click.secho("maximum packet size (F):    ", fg="yellow", nl=False)
            click.echo(record[4])           # f_max_ps 
            click.secho("average packet size (F):    ", fg="yellow", nl=False)
            click.echo(record[5])           # f_avg_ps
            click.secho("standard deviation packet size (F):    ", fg="yellow", nl=False)
            click.echo(record[6])           # f_std_dev_ps
            click.secho("minimum packet interarrival time (F):    ", fg="yellow", nl=False)
            click.echo(record[7])           # f_min_piat
            click.secho("maximum packet interarrival time (F):    ", fg="yellow", nl=False)
            click.echo(record[8])           # f_max_piat
            click.secho("average packet interarrival time (F):    ", fg="yellow", nl=False)
            click.echo(record[9])           # f_avg_piat
            click.secho("standard deviation packet interarrival time (F):    ", fg="yellow", nl=False)
            click.echo(record[10])          # f_std_dev_piat
        elif (choice == "3"):
            record = display_backward(flow_index)
            if not record:
                click.secho("no data present!", fg="red")
                dst_ip_selection(None)
            click.secho("The following attributes are in representing packets in the BACKWARD direction!", fg="red")
            click.secho("Flow_index:    ", fg="yellow", nl=False)
            click.echo(record[0])
            click.secho("number of packets (B):    ", fg="yellow", nl=False)
            click.echo(record[1])           # b_pktTotalCount
            click.secho("total of bytes exchanged (B):     ", fg="yellow", nl=False)
            click.echo(record[2])           # b_octetTotalCount
            click.secho("minimum packet size (B):    ", fg="yellow", nl=False)
            click.echo(record[3])           # b_min_ps
            click.secho("maximum packet size (B):    ", fg="yellow", nl=False)
            click.echo(record[4])           # b_max_ps 
            click.secho("average packet size (B):    ", fg="yellow", nl=False)
            click.echo(record[5])           # b_avg_ps
            click.secho("standard deviation packet size (B):    ", fg="yellow", nl=False)
            click.echo(record[6])           # b_std_dev_ps
            click.secho("minimum packet interarrival time (B):    ", fg="yellow", nl=False)
            click.echo(record[7])           # b_min_piat
            click.secho("maximum packet interarrival time (B):    ", fg="yellow", nl=False)
            click.echo(record[8])           # b_max_piat
            click.secho("average packet interarrival time (B):    ", fg="yellow", nl=False)
            click.echo(record[9])           # b_avg_piat
            click.secho("standard deviation packet interarrival time (B):    ", fg="yellow", nl=False)
            click.echo(record[10])          # b_std_dev_piat
        elif (choice == "4"):
            display_protocol(flow_index)
        elif (choice == "5"):
            display_flag(flow_index)
        # elif (choice == "6"):
        #     annotate(flow_index, None)         # TODO for ppt: this will still ask the user for the Flow_index, which is redundant
        elif (choice == "7"):
            client_option(None)

''' Use this command to insert new data into our database, this can only be done by the admin account '''
''' This method is used to add minimal required data to flows and links so that the PKs and FKs can be satisfied '''
@click.command()
def insert_new_data():
    #if (is_admin_session == 0):
        #Non admin can not insert so return back to the client_option menu
    #    client_option(None)
    srcIP = click.prompt('Enter the source IP')
    srcPort = click.prompt('Enter the source port')
    dstIP = click.prompt('Enter the destination IP')
    dstPort = click.prompt('Enter the destination Port')
    result = insert_new_flow(srcIP, srcPort, dstIP, dstPort)
    if result[0] == -1:
        click.secho(result[1], fg= 'red')
        insert_new_data()
    else:
        click.secho(result[1], fg= 'green')

@click.command()
def update_menu():
    choice = ""
    while (choice != "7"):
        click.secho("(1) Update flow timing information", fg='yellow')
        click.secho("(2) Update flow forward packet information", fg='yellow')
        click.secho("(3) Update flow backward packet information", fg='yellow')
        click.secho("(4) Update flow protocol information", fg='yellow')
        click.secho("(5) Update flow packet information", fg='yellow')
        click.secho("(6) Update flow flag information", fg='yellow')
        click.secho("(7) Exit", fg='yellow')
        choice = click.prompt('Please choose one of the options (1/2/3/4/5/6/7)') 
        if (choice == '5'):
            update_packet_information()
        elif (choice == '6'):
            update_flag_information()
        elif (choice == '4'):
            update_protocol_information()
        elif (choice == '2'):
            update_forward_flows_information()
        elif (choice == '3'):
            update_backward_flows_information()
        elif (choice == '1'):
            update_date_time_information()

@click.command()
@click.option("--flow_index", prompt = "Enter the flow index you wish to update", default = "")
def update_packet_information(flow_index):
    min_ps = click.prompt('Enter the minmimum packet size: ')
    max_ps = click.prompt('Enter the maximum packet size: ')
    avg_ps = click.prompt('Enter the average packet size: ')
    std_dev_ps = click.prompt('Enter the packet size standard deviation: ')
    min_piat = click.prompt('Enter the min inter packet arrival time: ')
    max_piat = click.prompt('Enter the max inter packet arrival time: ')
    avg_piat = click.prompt('Enter the avg inter packet arrival time: ')
    std_dev_piat = click.prompt('Enter the standard deviation inter packet arrival time : ')
    packet_information = (flow_index ,min_ps, max_ps, avg_ps, std_dev_ps, min_piat, max_piat, avg_piat, std_dev_piat)
    result = update_packet_table(packet_information)
    if result[0] == -1:
        click.secho(result[1], fg='red')
        update_packet_information()
    else:
        click.secho(result[1], fg = 'green')
        update_menu()

@click.command()
@click.option("--flow_index", prompt = "Enter the flow index you wish to update", default = "")
def update_flag_information(flow_index):
    FIN_flag_count = click.prompt('Enter number of times flow had FIN flag bit set to 1: ')
    SYN_flag_count = click.prompt('Enter number of times flow had SYN flag bit set to 1: ')
    RST_flag_count = click.prompt('Enter number of times flow had RST flag bit set to 1: ')
    PSH_flag_count = click.prompt('Enter number of times flow had PSH flag bit set to 1: ')
    ACK_flag_count = click.prompt('Enter number of times flow had ACK flag bit set to 1: ')
    URG_flag_count = click.prompt('Enter number of times flow had URG flag bit set to 1: ')
    CWE_flag_count = click.prompt('Enter number of times flow had CWE flag bit set to 1: ')
    ECE_flag_count = click.prompt('Enter number of times flow had ECE flag bit set to 1: ')
    flag_information = (flow_index, FIN_flag_count, SYN_flag_count, RST_flag_count, PSH_flag_count, ACK_flag_count, URG_flag_count, CWE_flag_count, ECE_flag_count)
    result = update_flag_table(flag_information)
    if result[0] == -1:
        click.secho(result[1], fg= 'red')
        update_flag_information()
    else:
        click.secho(result[1], fg = 'green')
        update_menu()

@click.command()
@click.option("--flow_index", prompt = "Enter the flow index you wish to update", default = "")
def update_protocol_information(flow_index):
    proto = click.prompt('Enter the protocol number')
    category = click.prompt('Enter the protocol category')
    application_protocol = click.prompt('Enter the application protocol ')
    web_service = click.prompt('Enter the web service')
    protocol_information = (flow_index, proto, category, application_protocol, web_service)
    result = update_protocol_table(protocol_information)
    if result[0] == -1:
        click.secho(result[1], fg = 'red')
        update_protocol_information()
    else:
        click.secho(result[1], fg = 'green')
        update_menu()

@click.command()
@click.option("--flow_index", prompt = "Enter the flow index you wish to update", default = "")
def update_forward_flows_information(flow_index):
    f_pktTotalCount = click.prompt('Enter the total number of packets in the forward direction')
    f_octetTotalCount = click.prompt('Enter the total number of octet in the forward direection') #TODO: Figure out what this field means and update prompt
    f_min_ps = click.prompt('Enter the minimum packet size in the fwd direction')
    f_max_ps = click.prompt('Enter the maximum packet size in the fwd direction')
    f_avg_ps = click.prompt('Enter the avg packet size in the forward direction')
    f_std_dev_ps = click.prompt('Enter the standard deviaton of the packet size')
    f_min_piat = click.prompt('Enter the minimum inter arrival packet time in the forward direction')
    f_max_piat = click.prompt('Enter the maximum inter arrival packet time in the forward direction')
    f_avg_piat = click.prompt('Enter the average inter arrival packet time in the forward direction')
    f_std_dev_piat = click.prompt('Enter the standard deviation of the inter arrival packet size in the forward direction')
    forward_flow_information = (flow_index, f_pktTotalCount, f_octetTotalCount, f_min_ps, f_max_ps, f_avg_ps, f_std_dev_ps, f_min_piat, f_max_piat, f_avg_piat, f_std_dev_piat)
    result = update_forward_flows_table(forward_flow_information)
    if result[0] == -1:
        click.secho(result[1], fg = 'red')
        update_forward_flows_information()
    else:
        click.secho(result[1], fg = 'green')
        update_menu()

@click.command()
@click.option("--flow_index", prompt = "Enter the flow index you wish to update", default = "")
def update_backward_flows_information(flow_index):
    b_pktTotalCount = click.prompt('Enter the total number of packets in the backward direction')
    b_octetTotalCount = click.prompt('Enter the total number of octet in the backward direection') #TODO: Figure out what this field means and update prompt
    b_min_ps = click.prompt('Enter the minimum packet size in the backward direction')
    b_max_ps = click.prompt('Enter the maximum packet size in the backward direction')
    b_avg_ps = click.prompt('Enter the avg packet size in the backward direction')
    b_std_dev_ps = click.prompt('Enter the standard deviaton of the packet size in the backward direction')
    b_min_piat = click.prompt('Enter the minimum inter arrival packet time in the backward direction')
    b_max_piat = click.prompt('Enter the maximum inter arrival packet time in the backward direction')
    b_avg_piat = click.prompt('Enter the average inter arrival packet time in the backward direction')
    b_std_dev_piat = click.prompt('Enter the standard deviation of the inter arrival packet size in the backward direction')
    backward_flow_informtion = (flow_index, b_pktTotalCount, b_octetTotalCount, b_min_ps, b_max_ps, b_avg_ps, b_std_dev_ps, b_min_piat, b_max_piat, b_avg_piat, b_std_dev_piat)
    result = update_backward_flows_table(backward_flow_informtion)
    if result[0] == -1:
        click.secho(result[1], fg = 'red')
        update_backward_flows_information()
    else:
        click.secho(result[1], fg = 'green')
        update_menu()

@click.command()
@click.option("--flow_index", prompt = "Enter the flow index you wish to update", default = "")
def update_date_time_information(flow_index):
    flow_date = click.prompt('Enter the date of the flow in the format YYYY-MM-DD')
    flow_time = click.prompt('Enter the time of flow in the format HH:MM:SS')
    Flow_Start = '{} {}'.format(flow_date, flow_time)
    flow_Duration = click.prompt('Enter the duration of the flow in milliseconds') 
    #Leaving protocol out for now, seems like the column is redundant
    date_time_information = (flow_index, Flow_Start, flow_Duration)
    result = update_flow_timing_table(date_time_information)
    if result[0] == -1:
        click.secho(result[1], fg = 'red')
        update_date_time_information()
    else:
        click.secho(result[1], fg = 'green')
        update_menu()

def protocol():
    click.secho("Different protocolName options are: ", fg="green", nl=False)
    defaults = get_protocol_name()
    for x in defaults:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False) 
    click.secho(" ", nl=True)

    pn = click.prompt("Enter the protocol name of the flows you wish to inspect upon")
    while pn not in defaults:
        click.secho("incorrect value, try again!", fg="red")
        pn = click.prompt("Enter the protocol name of the flows you wish to inspect upon")

    numFlows = fetchFlowByPN(pn)
    print("Number of flows matching the protocol name %s is %i" % (pn, numFlows))

    attribute = 0
    aggregation = 0

    while(1):
        attribute, aggregation = get_att_agg()
        if attribute == 9 or aggregation == 4:
            break
        fetchInfoByPN(attribute, aggregation, pn)
    client_option(None)


def web_service():
    defaults = get_webservice_names()
    for x in defaults:
        click.secho(str(x), fg="blue", nl=False)
        click.secho(", ", fg="blue", nl=False) 
    click.secho(" ", nl=True)

    ws = click.prompt("Enter the web service of the flows you wish to inspect upon")
    while ws not in defaults: # reiterate until user provides valid web service
        click.secho("incorrect value, try again!", fg="red")
        ws = click.prompt("Enter the web service of the flows you wish to inspect upon")

    numFlows = fetchFlowByWeb(ws)
    print("Number of flows matching the web service %s is %i" % (ws, numFlows))
        
    attribute = 0
    aggregation = 0

    while 1:
        attribute, aggregation = get_att_agg()
        if attribute == 9 or aggregation == 4:
            break
        fetchInfoByWeb(attribute, aggregation, ws)

    client_option(None)

def get_att_agg():
    """
    Get attribute and aggregation from user
    input: None
    output: attribute name, aggregation method
    """
    attribute = 0
    aggregation = 0
    click.secho("Which of the following attributes would you like to check?")
    click.secho("(1) minimum packet size", fg="blue")
    click.secho("(2) maximum packet size", fg="blue")
    click.secho("(3) average packet size", fg="blue")
    click.secho("(4) standard deviation packet size", fg="blue")
    click.secho("(5) minimum packet interarrival time", fg="blue")
    click.secho("(6) maximum packet interarrival time", fg="blue")
    click.secho("(7) average packet interarrival time", fg="blue")
    click.secho("(8) standard deviation packet interarrival time", fg="blue")
    click.secho("(9) exit", fg="blue")
    attribute = click.prompt("Please enter one of the options (1/2/3/4/5/6/7/8/9)", type=int)
    while attribute not in range(1,10):
        click.secho("incorrect value, try again!", fg="red")
        attribute = click.prompt("Please enter one of the options (1/2/3/4/5/6/7/8/9)", type=int)
    if attribute == 9:
        return 9, 4

    click.secho("Which of the following aggregation method would you like to use?")
    click.secho("(1) minimum", fg="blue")
    click.secho("(2) maximum", fg="blue")
    click.secho("(3) average", fg="blue")
    click.secho("(4) exit", fg="blue")
    aggregation = click.prompt("Please enter one of the options (1/2/3/4)", type=int)
    while aggregation not in range(1,5):
        click.secho("incorrect value, try again!", fg="red")
        aggregation = click.prompt("Please enter one of the options (1/2/3/4)", type=int)

    return attribute, aggregation