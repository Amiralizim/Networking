import hashlib
import mysql.connector
import click
from mysql.connector import Error


cursor = None
connection = None

#Constants
DUPLICATE_PRIMARY_KEY_ERRNO = 1062
CLIENT_ORIGIN = 3
QUERY_ERR = -1
QUERY_OK = 0

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

# INSERT QUERIES
def insert_new_flow(srcIP, srcPort, dstIP, dstPort):
    Link_ID = ('{}-{}-{}-{}').format(srcIP, srcPort, dstIP, dstPort)
    #Step 1: Insert the Link into the Links table so the FK is satisfied
    query = 'INSERT INTO Links (Link_ID, srcIP, srcPort, dstIP, dstPort) VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(Link_ID, srcIP, srcPort, dstIP, dstPort)
    print(query)
    try:
        cursor.execute(query)
    except mysql.connector.Error as err:
        if (err.errno == DUPLICATE_PRIMARY_KEY_ERRNO):
            errmsg = 'Error: This link already exists, you can query the link and update its contents instead'
            return (QUERY_ERR,errmsg)
        else:
            errmsg = ('Unexpected Error: {}').format(err.msg)
            return (QUERY_ERR,errmsg)
    connection.commit()
    #Step 2: Get the max Flow_index so we can iterate it further, as this is the PK
    flow_index_query = 'SELECT MAX(Flow_index) FROM Flows'
    cursor.execute(flow_index_query)
    result = cursor.fetchall()
    flow_index = int(result[0][0])+1
    #Step 3: Insert just the Flow_index and the Link_ID into the flows table so now all a user has to do is update from the given flow index
    query = 'INSERT INTO Flows(Flow_index,Link_ID,origin) VALUES ({},\'{}\',{})'.format(flow_index,Link_ID, CLIENT_ORIGIN)
    cursor.execute(query)
    connection.commit()
    msg = ('Success, flow was added with Flow_index: {}').format(flow_index)
    return (QUERY_OK, msg)

# UPDATE QUERIES
def update_packet_table(packet_information):
    query1 = 'SELECT COUNT(*) FROM Packets WHERE Flow_index = {};'.format(packet_information[0]) #Check if the row exists, if it does update otherwise insert
    print(query1)
    cursor.execute(query1)
    result = cursor.fetchall()
    if result[0][0] == 0:
        print('add new column first')
        insert_query = 'INSERT INTO Packets(Flow_index, min_ps, max_ps, avg_ps, std_dev_ps, min_piat, max_piat, avg_piat, std_dev_piat) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
            packet_information[0], packet_information[1], packet_information[2], packet_information[3], packet_information[4], packet_information[4], packet_information[5], packet_information[6], packet_information[7], packet_information[8])
        print(insert_query)
        try:
            cursor.execute(insert_query)
        except mysql.connector.Error as err:
            errmsg = ('Unexpected error: {}').format(err.msg)
            return (QUERY_ERR,errmsg)
        connection.commit()
        msg = 'Succesfully inserted new row in Packets data with Flow_index = {}'.format(packet_information[0])
        return (QUERY_OK, msg)
    elif result[0][0] == 1:
        update_query = 'UPDATE Packets SET min_ps = {}, max_ps = {}, avg_ps = {}, std_dev_ps = {}, min_piat = {}, max_piat = {}, avg_piat = {}, std_dev_piat = {} WHERE Flow_index = {};'.format(
            packet_information[1], packet_information[2], packet_information[3], packet_information[4], packet_information[5], packet_information[6], packet_information[7], packet_information[8], packet_information[0]
        )
        print(update_query)
        print('row is already present use update instead')
        try:
            cursor.execute(update_query)
        except mysql.connector.Error as err:
            errmsg = ('Unexpected error: {}').format(err.msg)
            return(QUERY_ERR, errmsg)
        connection.commit()
        msg = 'Succesfully updated new row in Packets data with Flow_index = {}'.format(packet_information[0])
        return(QUERY_OK, msg)
    return

def update_flag_table(flag_information):
    query1 = 'SELECT COUNT(*) FROM Flags WHERE Flow_index = {};'.format(flag_information[0]) #Check if the row exists, if it does update otherwise insert
    print(query1)
    cursor.execute(query1)
    result = cursor.fetchall()
    if result[0][0] == 0:
        print('add new row first')
        insert_query = 'INSERT INTO Flags(Flow_index, FIN_Flag_Count, SYN_Flag_Count, RST_Flag_Count, PSH_Flag_Count, ACK_Flag_Count, URG_Flag_Count, CWE_Flag_Count, ECE_Flag_Count) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
            flag_information[0], flag_information[1], flag_information[2], flag_information[3], flag_information[4], flag_information[5], flag_information[6], flag_information[7], flag_information[8]
        )
        print(insert_query)
        try:
            cursor.execute(insert_query)
        except mysql.connector.Error as err:
            errmsg = ('Unexpected Error: {}').format(err.msg)
            print(errmsg)
            return (QUERY_ERR, errmsg)
        connection.commit()
        msg = 'Succesfully inserted new row in flags table with Flow_index = {}'.format(flag_information[0])
        print(msg)
        return (QUERY_OK, msg)
    elif result[0][0] == 1:
        print('update existing row')
        update_query = 'UPDATE Flags SET FIN_Flag_Count = {}, SYN_Flag_Count = {}, RST_Flag_Count = {}, PSH_Flag_Count = {}, ACK_Flag_Count = {}, URG_Flag_Count = {}, CWE_Flag_Count = {}, ECE_Flag_Count = {} WHERE Flow_index = {}'.format(
            flag_information[1], flag_information[2], flag_information[3], flag_information[4], flag_information[5], flag_information[6], flag_information[7], flag_information[8], flag_information[0]
        )
        print(update_query)
        try:
            cursor.execute(update_query)
        except mysql.connector.Error as err:
            errmsg = ('Unexpected Error: {}').format(err.msg)
            print(errmsg)
            return (QUERY_ERR, errmsg)
        connection.commit()
        msg = 'Succesfully updated row in flags table with Flow_index = {}'.format(flag_information[0])
        print(msg)
        return(QUERY_OK, msg)

def update_protocol_table(protocol_information):
    count_query = 'SELECT COUNT(*) FROM Protocol2 WHERE Flow_index = {};'.format(protocol_information[0])
    print(count_query)
    cursor.execute(count_query)
    result = cursor.fetchall()
    if result[0][0] == 0:
        print('Add new row first')
        main_query = 'INSERT INTO Protocol2(Flow_index, proto, category, application_protocol, web_service) VALUES ({}, {}, \'{}\', \'{}\', \'{}\'); '.format(
            protocol_information[0], protocol_information[1], protocol_information[2], protocol_information[3], protocol_information[4]
        )
        msg = 'Succesfully inserted new row in the table Protocol with Flow_index = {}'.format(protocol_information[0])
    elif result[0][0] == 1:
        print('Update existing row')
        main_query = 'UPDATE Protocol2 SET proto = {}, category = \'{}\', application_protocol = \'{}\', web_service = \'{}\' WHERE Flow_index = {};'.format(
            protocol_information[1], protocol_information[2], protocol_information[3], protocol_information[4], protocol_information[0]
        )
        msg = 'Succesfully updated row in the table Protocol with Flow_index = {}'.format(protocol_information[0])
    print(main_query)
    try:
        cursor.execute(main_query)
    except mysqlconnector.Error as err:
        errmsg = ('Unexpected Error: {}').format(err.msg)
        print(errmsg)
        return (QUERY_ERR, errmsg)
    connection.commit()
    return(QUERY_OK, msg)

def update_forward_flows_table(forward_flow_information):
    count_query = 'SELECT COUNT(*) FROM ForwardFlows WHERE Flow_index = {}; '.format(forward_flow_information[0])
    print(count_query)
    cursor.execute(count_query)
    result = cursor.fetchall()
    if result[0][0] == 0:
        print('Add new row first')
        main_query = 'INSERT INTO ForwardFlows(Flow_index, f_pktTotalCount, f_octetTotalCount, f_min_ps, f_max_ps, f_avg_ps, f_std_dev_ps, f_min_piat, f_max_piat, f_avg_piat, f_std_dev_piat) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
            forward_flow_information[0], forward_flow_information[1], forward_flow_information[2], forward_flow_information[3], forward_flow_information[4], forward_flow_information[5], forward_flow_information[6], forward_flow_information[7], forward_flow_information[8], forward_flow_information[9], forward_flow_information[10]
        )
        msg = 'Succesfully inserted new row in the forward flows table with Flow_index = {}'.format(forward_flow_information[0])
    elif result[0][0] == 1:
        print('Update existing row')
        main_query = 'UPDATE ForwardFlows SET f_pktTotalCount = {}, f_octetTotalCount = {}, f_min_ps = {}, f_max_ps = {}, f_avg_ps = {}, f_std_dev_ps = {}, f_min_piat = {}, f_max_piat = {}, f_avg_piat = {}, f_std_dev_piat = {} WHERE Flow_index = {};'.format(
            forward_flow_information[1], forward_flow_information[2], forward_flow_information[3], forward_flow_information[4], forward_flow_information[5], forward_flow_information[6], forward_flow_information[7], forward_flow_information[8], forward_flow_information[9], forward_flow_information[10], forward_flow_information[0]
        )
        msg = 'Succesfully updated existing row in the forward flows table with Flow_index = {}'.format(forward_flow_information[0])
    print(main_query)
    try:
        cursor.execute(main_query)
    except mysqlconnector.Error as err:
        errmsg = ('Unexpected Error: {}').format(err.msg)
        print(errmsg)
        return(QUERY_ERR, errmsg)
    connection.commit()
    return(QUERY_OK, msg)

def update_backward_flows_table(backward_flow_information):
    count_query = 'SELECT COUNT(*) FROM BackwardFlows WHERE Flow_index = {}; '.format(backward_flow_information[0])
    print(count_query)
    cursor.execute(count_query)
    result = cursor.fetchall()
    if result[0][0] == 0:
        print('Add new row first')
        main_query = 'INSERT INTO BackwardFlows(Flow_index, b_pktTotalCount, b_octetTotalCount, b_min_ps, b_max_ps, b_avg_ps, b_std_dev_ps, b_min_piat, b_max_piat, b_avg_piat, b_std_dev_piat) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
            backward_flow_information[0], backward_flow_information[1], backward_flow_information[2], backward_flow_information[3], backward_flow_information[4], backward_flow_information[5], backward_flow_information[6], backward_flow_information[7], backward_flow_information[8], backward_flow_information[9], backward_flow_information[10]
        )
        msg = 'Succesfully inserted new row in the backward flows table with Flow_index = {}'.format(backward_flow_information[0])
    elif result[0][0] == 1:
        print('Update existing row')
        main_query = 'UPDATE BackwardFlows SET b_pktTotalCount = {}, b_octetTotalCount = {}, b_min_ps = {}, b_max_ps = {}, b_avg_ps = {}, b_std_dev_ps = {}, b_min_piat = {}, b_max_piat = {}, b_avg_piat = {}, b_std_dev_piat = {} WHERE Flow_index = {};'.format(
            backward_flow_information[1], backward_flow_information[2], backward_flow_information[3], backward_flow_information[4], backward_flow_information[5], backward_flow_information[6], backward_flow_information[7], backward_flow_information[8], backward_flow_information[9], backward_flow_information[10], backward_flow_information[0]
        )
        msg = 'Succesfully updated existing row in the backward flows table with Flow_index = {}'.format(backward_flow_information[0])
    print(main_query)
    try:
        cursor.execute(main_query)
    except mysqlconnector.Error as err:
        errmsg = ('Unexpected Error: {}').format(err.msg)
        print(errmsg)
        return(QUERY_ERR, errmsg)
    connection.commit()
    return(QUERY_OK, msg)
    
def update_flow_timing_table(date_time_information):
    count_query = 'SELECT COUNT(*) FROM Flows WHERE Flow_index = {};'.format(date_time_information[0])
    print(count_query)
    cursor.execute(count_query)
    result = cursor.fetchall()
    if result[0][0] == 0:
        errmsg = 'This flow does not exist in our system, Please insert the flow first'
        return (QUERY_ERR, errmsg)
    elif result[0][0] == 1:
        main_query = 'UPDATE Flows SET Flow_Start = \'{}\', Flow_Duration = {} WHERE Flow_index = {};'.format(
            date_time_information[1], date_time_information[2], date_time_information[0]
        )
    try:
        cursor.execute(main_query)
    except mysqlconnector.Error as err:
        errmsg = ('Unexpected Error: {}').format(err.msg)
        return (QUERY_ERR, errmsg)
    connection.commit()
    msg = 'Succesfully updated date time information of flow with Flow_index = {}'.format(date_time_information[0])
    return(QUERY_OK, msg)

def fetchFlowByPN(protocolName):
    """
    Determines the totla number of flows with matching protocolName
    input: protocolName
    output: total number of flows
    """

    query = ('SELECT COUNT(*) FROM Protocol1 WHERE ProtocolName = "{}"; ').format(protocolName)
    cursor.execute(query)
    query_result = cursor.fetchone()
    return query_result[0]

def fetchFlowByWeb(web_service):
    """
    Determines the total number of flows with matching web_service
    input: web_service
    output: total number of flows
    """

    query = ('SELECT COUNT(*) FROM Protocol2 WHERE web_service = "{}"; ').format(web_service)
    cursor.execute(query)
    query_result = cursor.fetchone()
    return query_result[0]

def fetchInfoByPN(attribute, pn):
    """
    Determine the max/min/avg of the attribute where flows are sorted by protocol name
    input: attribute (1,2,3,4 are for min, max, avg, std packet size, 5,6,7,8 are for min, max, avg, std packet interarrival time)
    """
    attributeName = converter(attribute)
    query = ('WITH temp(flow_index) AS (SELECT flow_index FROM Protocol1 WHERE ProtocolName = "{}") SELECT MAX({}), MIN({}), AVG({}), temp.Flow_index FROM temp INNER JOIN Packets on temp.flow_index = Packets.Flow_index;').format(pn, attributeName, attributeName, attributeName)
    cursor.execute(query)
    query_result = cursor.fetchone()
    result = []
    result.append(query_result[0])
    result.append(query_result[1])
    result.append(query_result[2])

    click.secho("For the Protocol Name: ", fg="yellow", nl=False)
    click.echo(pn)
    click.secho("The MAX(%s):    " % attributeName, fg="yellow", nl=False)
    click.echo(result[0])
    click.secho("The MIN(%s):    " % attributeName, fg="yellow", nl=False)
    click.echo(result[1])
    click.secho("The AVG(%s):    " % attributeName, fg="yellow", nl=False)
    click.echo(result[2])

def fetchInfoByWeb(attribute, ws):
    """
    Determine the max/min/avg of the attribute where flows are sorted by web services
    input: attribute (1,2,3,4 are for min, max, avg, std packet size, 5,6,7,8 are for min, max, avg, std packet interarrival time)
    """

    attributeName = converter(attribute)
    query = ('WITH temp(flow_index) AS (SELECT flow_index FROM Protocol2 WHERE web_service = "{}") SELECT MAX({}), MIN({}), AVG({}), temp.Flow_index FROM temp INNER JOIN Packets on temp.flow_index = Packets.Flow_index;').format(ws, attributeName, attributeName, attributeName)
    cursor.execute(query)
    query_result = cursor.fetchone()
    result = []
    result.append(query_result[0])
    result.append(query_result[1])
    result.append(query_result[2])
   
    click.secho("For the Web Service: ", fg="yellow", nl=False)
    click.echo(ws)
    click.secho("The MAX(%s):    " % attributeName, fg="yellow", nl=False)
    click.echo(result[0])
    click.secho("The MIN(%s):    " % attributeName, fg="yellow", nl=False)
    click.echo(result[1])
    click.secho("The AVG(%s):    " % attributeName, fg="yellow", nl=False)
    click.echo(result[2])


def converter(attribute):
    attributeName = ""
    aggregationName = ""
    if (attribute == 1):
        attributeName = "min_ps"
    elif (attribute == 2):
        attributeName = "max_ps"
    elif (attribute == 3):
        attributeName = "avg_ps"
    elif (attribute == 4):
        attributeName = "std_dev_ps"
    elif (attribute == 5):
        attributeName = "min_piat"
    elif (attribute == 6):
        attributeName = "max_piat"
    elif (attribute == 7):
        attributeName = "avg_piat"
    elif (attribute == 8):
        attributeName = "std_dev_piat"

    return attributeName


connection = create_connection('localhost', 'root', 'root')
cursor = connection.cursor()

