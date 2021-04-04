import hashlib
import mysql.connector
import click
from mysql.connector import Error


cursor = None
connection = None

def create_connection(host_name, user_name, user_password):
    #connection = None
    global connection
    try:
        connection = mysql.connector.connect(
            host=host_name,
            port = '3307',
            user=user_name,
            passwd=user_password,
            database = 'Networking'
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print("The error '{e}' occurred")

    return connection

def initialize_db():
    connection = create_connection('localhost', 'root', 'root')
    cursor = connection.cursor()


def find_links(sourceip, sourceport, destinationip, destinationport):
    """
    Fetch Link_ID from table Links.
    inputs: source ip, port, destination ip, port
    output: corresponding Link_ID 
    """

    result = ""
    link_id = ("{}-{}-{}-{}").format(sourceip, sourceport, destinationip, destinationport)
    try:
        query = ("SELECT Link_ID FROM Links WHERE Link_ID = \'{}\'; ").format(link_id)
        cursor.execute(query)
    except Error:
        return result
    for x in cursor.fetchall():
        #print (x)
        result += x[0]            # x is a tuple type, Link_ID is a string type

    # cursor.close()
    # connection.close()
    return result

def find_flows(Link_ID):
    """
    Fetch Flow_index from table Flows.
    input: Link_ID
    outputs: corresponding Flow_index associated with the Link_ID
    """

    result = []
    try:
        query = ("SELECT Flow_index FROM Flows WHERE Link_ID = \'{}\'; ").format(Link_ID)
        cursor.execute(query)
    except Error:
        return result

    for x in cursor.fetchall():
        #print (x)
        result.append(x[0])           # x is a tuple type, Flow_index is an INT
    
    return result
    
def display_total(Flow_index):
    """
    Display generic packet information from table Packets based on Flow_index
    input: Flow_index
    output: None (print statements)
    """
    record = []
    try:
        query = ("SELECT * FROM Packets WHERE Flow_index = \'{}\'; ").format(Flow_index)
        cursor.execute(query)
    except Error:
        return record
    record = cursor.fetchone()        # use fetchone to fetch only one row, then each attribute from that row would be record[0] [1] and so on
    return record
    
def display_forward(Flow_index):
    """
    Display forward packet information from table ForwardFlows based on Flow_index
    input: Flow_index
    output: None (print statements)
    """
    record = []
    try:
        query = ("SELECT * FROM ForwardFlows WHERE Flow_index = \'{}\'; ").format(Flow_index)
        cursor.execute(query)
    except Error:
        return record
    record = cursor.fetchone()  
    return record

def display_backward(Flow_index):
    """
    Display backward packet information from table BackwardFlows based on Flow_index
    input: Flow_index
    output: None (print statements)
    """
    record = []
    try: 
        query = ("SELECT * FROM BackwardFlows WHERE Flow_index = \'{}\'; ").format(Flow_index)
        cursor.execute(query)
    except Error:
        return record 
    record = cursor.fetchone()  
    return record

def display_protocol(Flow_index):
    """
    Display protocol info from the table Protocol based on Flow_index
    NOTE: flows from origin 1 will have different protocol info. than origin 2
    input: Flow_index
    output: None (print statements)
    """
    
    # check if Flow_index is from origin 1 or 2
    query = ("SELECT origin FROM Flows WHERE Flow_index = \'{}\'; ").format(Flow_index)
    cursor.execute(query)
    record = cursor.fetchone() 

    if (record[0] == "1"):
        query = ("SELECT * FROM Protocol1 WHERE Flow_index = \'{}\'; ").format(Flow_index)
        cursor.execute(query)
        record = cursor.fetchone()

        click.secho("This flow is from origin 1!", fg="red")
        click.secho("Flow_index:    ", fg="yellow", nl=False)
        click.echo(record[0])
        click.secho("protocol number:    ", fg="yellow", nl=False)
        click.echo(record[1])           # proto
        click.secho("code number the layer 7 protocol:    ", fg="yellow", nl=False)
        click.echo(record[2])           # L7Protocol
        click.secho("protocol name:    ", fg="yellow", nl=False)
        click.echo(record[3])           # ProtocolName

    elif (record[0] == "2"):
        query = ("SELECT * FROM Protocol2 WHERE Flow_index = \'{}\'; ").format(Flow_index)
        cursor.execute(query)
        record = cursor.fetchone()

        click.secho("This flow is from origin 2!", fg="red")
        click.secho("Flow_index:    ", fg="yellow", nl=False)
        click.echo(record[0])
        click.secho("protocol number:    ", fg="yellow", nl=False)
        click.echo(record[1])           # proto
        click.secho("category delivered by nDPI:    ", fg="yellow", nl=False)
        click.echo(record[2])           # category  
        click.secho("application protocol detected by nDPI:    ", fg="yellow", nl=False)
        click.echo(record[3])           # application_protocol
        click.secho("web service detected by nDPI:    ", fg="yellow", nl=False)
        click.echo(record[4])           # web_service
    

def display_flag(Flow_index):
    """
    Display flag info from the table Flags based on Flow_index 
    NOTE: ONLY flows from origin 1 have this information 
    input: Flow_index
    output: None (print statements)
    """

    # check if Flow_index is from origin 1 or 2
    query = ("SELECT origin FROM Flows WHERE Flow_index = \'{}\'; ").format(Flow_index)
    cursor.execute(query)
    record = cursor.fetchone() 

    if (record[0] == "1"):
        query = ("SELECT * FROM Flags WHERE Flow_index = \'{}\'; ").format(Flow_index)
        cursor.execute(query)
        record = cursor.fetchone()
        click.secho("Flow_index:    ", fg="yellow", nl=False)
        click.echo(record[0])
        click.secho("FIN_Flag_Count:    ", fg="yellow", nl=False)
        click.echo(record[1])           # FIN_Flag_Count
        click.secho("SYN_Flag_Count:    ", fg="yellow", nl=False)
        click.echo(record[2])           # SYN_Flag_Count
        click.secho("RST_Flag_Count:    ", fg="yellow", nl=False)
        click.echo(record[3])           # RST_Flag_Count
        click.secho("PSH_Flag_Count:    ", fg="yellow", nl=False)
        click.echo(record[4])           # PSH_Flag_Count
        click.secho("ACK_Flag_Count:    ", fg="yellow", nl=False)
        click.echo(record[5])           # ACK_Flag_Count
        click.secho("URG_Flag_Count:    ", fg="yellow", nl=False)
        click.echo(record[6])           # URG_Flag_Count
        click.secho("CWE_Flag_Count:    ", fg="yellow", nl=False)
        click.echo(record[7])           # CWE_Flag_Count
        click.secho("ECE_Flag_Count:    ", fg="yellow", nl=False)
        click.echo(record[8])           # ECE_Flag_Count

    elif (record[0] == "2"):
        click.secho("This flow doesn't have flag information available!", fg="red")

def hash_password(password):
    result = hashlib.sha256(password.encode())
    return result.hexdigest()

def authenticate(username, password):
    query = ("SELECT passwd FROM userinfo WHERE userID = \'{}\';").format(username)
    cursor.execute(query)
    query_result = cursor.fetchall()
    if len(query_result) == 0:
        return False
    hashed_password_input = hash_password(password)
    for x in query_result:
        if x[0] == hashed_password_input:
            return True 
    return False

def get_session_token(username):
    query = ("SELECT isadmin FROM userinfo WHERE userID = \'{}\'").format(username)
    cursor.execute(query)
    query_result = cursor.fetchall()
    return query_result[0][0]

def add_annotation(username, flow_id, annotation):
    query = ("INSERT INTO annotations VALUES ({}, \'{}\', \'{}\');").format(flow_id, username, annotation)
    cursor.execute(query)
    count = cursor.rowcount
    connection.commit() #WHENEVER MAKING CHANGES TO THE DATABASE REMEMBER TO COMMIT TO THE CONNECTION OTHERWISE THEY WILL NOT BE SAVED
    return count

def mode_helper(mode):
    """
    Determines if the private_ips or public_ips view has to be used
    """
    view_name = ""
    if(mode == "private"):
        view_name = "private_ips"
    elif(mode == "public"):
        view_name = "public_ips"
    return view_name

def get_first_ip_range(mode):
    """
    Determines the different IP ranges of the first three digits based on previous values and mode
    """
    result = []
    try: 
        query = ('SELECT DISTINCT CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) FROM {};').format(mode_helper(mode))
        cursor.execute(query)
    except Error as e:
        return result
    query_result = cursor.fetchall()
    for x in query_result:
        result.append(x[0])
    return result

def get_second_ip_range(mode, ipvalue):
    """
    Determines the different IP ranges of the second three digits based on previous values and mode
    """
    result = []
    try:
        query = ('SELECT DISTINCT CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int) FROM {} WHERE CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int)={}').format(mode_helper(mode), ipvalue)
        cursor.execute(query)
    except Error:
        return result
    query_result = cursor.fetchall()
    for x in query_result:
        result.append(x[0])
    return result

def get_third_ip_range(mode, ipvalue):
    """
    Determines the different IP ranges of the third three digits based on previous values and mode
    """
    result = []
    try:
        query = ('SELECT DISTINCT CAST(SUBSTRING_INDEX(srcIP, ".", -2) AS int) FROM {} WHERE CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int)={}').format(mode_helper(mode), ipvalue)
        cursor.execute(query)
    except Error:
        return result
    query_result = cursor.fetchall()
    for x in query_result:
        result.append(x[0])
    return result

def get_fourth_ip_range(mode, ipvalue):
    """
    Determines the different IP ranges of the fourth three digits based on previous values and mode
    """
    result = []
    try:
        query = ('SELECT DISTINCT CAST(SUBSTRING_INDEX(srcIP, ".", -1) AS int) FROM {} WHERE CAST(SUBSTRING_INDEX(srcIP, ".", -2) AS int)={}').format(mode_helper(mode), ipvalue)
        cursor.execute(query)
    except Error:
        return result
    query_result = cursor.fetchall()
    for x in query_result:
        result.append(x[0])
    return result

def get_source_ports(mode, srcIP):
    """
    Determines the source port based on the provided srcIP
    """
    result = []
    try:
        query = ('SELECT distinct srcPort FROM {} WHERE srcIP="{}";').format(mode_helper(mode), str(srcIP))
        cursor.execute(query)
    except Error:
        return result    
    query_result = cursor.fetchall()
    for x in query_result:
        result.append(x[0])
    return result

def get_dst_ips(mode, srcIP, srcPort):
    """
    Determines the destination IP based on the provided srcIP and srcPort
    """
    result = []
    try:
        query = ('SELECT distinct dstIP FROM {} WHERE srcIP="{}" AND srcPort="{}";').format(mode_helper(mode), str(srcIP), str(srcPort))
        cursor.execute(query)
    except Error:
        return result
    query_result = cursor.fetchall()
    for x in query_result:
        result.append(x[0])
    return result

def get_dst_ports(mode, srcIP, srcPort, dstIP):
    """
    Determines the destination IP based on the provided srcIP, srcPort and destination IP
    """
    result = []
    try:
        query = ('SELECT distinct dstPort FROM {} WHERE srcIP="{}" AND srcPort="{}" AND dstIP="{}";').format(mode_helper(mode), str(srcIP), str(srcPort), str(dstIP))
        cursor.execute(query)
    except Error:
        return result
    query_result = cursor.fetchall()
    for x in query_result:
        result.append(x[0])
    return result

def get_protocol_name():
    """
    Determines the distinct protocol names
    """
    result = []
    try: 
        query = ('SELECT DISTINCT ProtocolName FROM Protocol1;')
        cursor.execute(query)
    except Error:
        return result
    query_result = cursor.fetchall()
    for x in query_result:
        result.append(x[0])
    return result 

def get_webservice_names():
    """
    Determines the distinct web service names
    """
    result = []
    try:
        query = ('SELECT DISTINCT web_service FROM Protocol2;')
        cursor.execute(query)
    except Error:
        return result
    query_result = cursor.fetchall()
    for x in query_result:
        result.append(x[0])
    return result 

connection = create_connection('localhost', 'root', 'root')
cursor = connection.cursor()

