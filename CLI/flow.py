import mysql.connector
from mysql.connector import Error
import click

class Flow:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.DUPLICATE_PRIMARY_KEY_ERRNO = 1062
        self.CLIENT_ORIGIN = 3
        self.QUERY_ERR = -1
        self.QUERY_OK = 0


    def find_flows(self, Link_ID):
        """
        Fetch Flow_index from table Flows.
        input: Link_ID
        outputs: corresponding Flow_index associated with the Link_ID
        """
        result = []
        try:
            query = ("SELECT Flow_index FROM Flows WHERE Link_ID = \'{}\'; ").format(Link_ID)
            self.cursor.execute(query)
        except Error:
            return result
        for x in self.cursor.fetchall():
            #print (x)
            result.append(x[0])           # x is a tuple type, Flow_index is an INT
        return result


    def display_total(self, Flow_index):
        """
        Display generic packet information from table Packets based on Flow_index
        input: Flow_index
        output: None (print statements)
        """
        record = []
        try:
            query = ("SELECT * FROM Packets WHERE Flow_index = \'{}\'; ").format(Flow_index)
            self.cursor.execute(query)
        except Error:
            return record
        record = self.cursor.fetchone()        # use fetchone to fetch only one row, then each attribute from that row would be record[0] [1] and so on
        return record


    def display_forward(self, Flow_index):
        """
        Display forward packet information from table ForwardFlows based on Flow_index
        input: Flow_index
        output: None (print statements)
        """
        record = []
        try:
            query = ("SELECT * FROM ForwardFlows WHERE Flow_index = \'{}\'; ").format(Flow_index)
            self.cursor.execute(query)
        except Error:
            return record
        record = self.cursor.fetchone()  
        return record


    def display_backward(self, Flow_index):
        """
        Display backward packet information from table BackwardFlows based on Flow_index
        input: Flow_index
        output: None (print statements)
        """
        record = []
        try: 
            query = ("SELECT * FROM BackwardFlows WHERE Flow_index = \'{}\'; ").format(Flow_index)
            self.cursor.execute(query)
        except Error:
            return record 
        record = self.cursor.fetchone()  
        return record


    def display_protocol(self, Flow_index):
        """
        Display protocol info from the table Protocol based on Flow_index
        NOTE: flows from origin 1 will have different protocol info. than origin 2
        input: Flow_index
        output: None (print statements)
        """
        # check if Flow_index is from origin 1 or 2
        record = []
        query = ("SELECT origin FROM Flows WHERE Flow_index = \'{}\'; ").format(Flow_index)
        self.cursor.execute(query)
        record = self.cursor.fetchone()
        if (record[0] == "1"):
            query = ("SELECT * FROM Protocol1 WHERE Flow_index = \'{}\'; ").format(Flow_index)
            self.cursor.execute(query)
            record = self.cursor.fetchone()
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
            self.cursor.execute(query)
            record = self.cursor.fetchone()
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

    def display_flag(self, Flow_index):
        """
        Display flag info from the table Flags based on Flow_index 
        NOTE: ONLY flows from origin 1 have this information 
        input: Flow_index
        output: None (print statements)
        """
        # check if Flow_index is from origin 1 or 2
        query = ("SELECT origin FROM Flows WHERE Flow_index = \'{}\'; ").format(Flow_index)
        self.cursor.execute(query)
        record = self.cursor.fetchone() 
        if (record[0] == "1"):
            query = ("SELECT * FROM Flags WHERE Flow_index = \'{}\'; ").format(Flow_index)
            self.cursor.execute(query)
            record = self.cursor.fetchone()
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

    # UPDATE METHODS
    def insert_new_flow(self, srcIP, srcPort, dstIP, dstPort):
        Link_ID = ('{}-{}-{}-{}').format(srcIP, srcPort, dstIP, dstPort)
        #Step 1: Insert the Link into the Links table so the FK is satisfied
        query = 'INSERT INTO Links (Link_ID, srcIP, srcPort, dstIP, dstPort) VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(Link_ID, srcIP, srcPort, dstIP, dstPort)
        print(query)
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            if (err.errno == self.DUPLICATE_PRIMARY_KEY_ERRNO):
                errmsg = 'Error: This link already exists, you can query the link and update its contents instead'
                return (self.QUERY_ERR,errmsg)
            else:
                errmsg = ('Unexpected Error: {}').format(err.msg)
                return (self.QUERY_ERR,errmsg)
        self.connection.commit()
        #Step 2: Get the max Flow_index so we can iterate it further, as this is the PK
        flow_index_query = 'SELECT MAX(Flow_index) FROM Flows'
        self.cursor.execute(flow_index_query)
        result = self.cursor.fetchall()
        flow_index = int(result[0][0])+1
        #Step 3: Insert just the Flow_index and the Link_ID into the flows table so now all a user has to do is update from the given flow index
        query = 'INSERT INTO Flows(Flow_index,Link_ID,origin) VALUES ({},\'{}\',{})'.format(flow_index,Link_ID, self.CLIENT_ORIGIN)
        self.cursor.execute(query)
        self.connection.commit()
        msg = ('Success, flow was added with Flow_index: {}').format(flow_index)
        return (self.QUERY_OK, msg)

    # UPDATE QUERIES
    def update_packet_table(self, packet_information):
        query1 = 'SELECT COUNT(*) FROM Packets WHERE Flow_index = {};'.format(packet_information[0]) #Check if the row exists, if it does update otherwise insert
        print(query1)
        self.cursor.execute(query1)
        result = self.cursor.fetchall()
        if result[0][0] == 0:
            print('add new column first')
            insert_query = 'INSERT INTO Packets(Flow_index, min_ps, max_ps, avg_ps, std_dev_ps, min_piat, max_piat, avg_piat, std_dev_piat) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
                packet_information[0], packet_information[1], packet_information[2], packet_information[3], packet_information[4], packet_information[4], packet_information[5], packet_information[6], packet_information[7], packet_information[8])
            print(insert_query)
            try:
                self.cursor.execute(insert_query)
            except mysql.connector.Error as err:
                errmsg = ('Unexpected error: {}').format(err.msg)
                return (self.QUERY_ERR,errmsg)
            self.connection.commit()
            msg = 'Succesfully inserted new row in Packets data with Flow_index = {}'.format(packet_information[0])
            return (self.QUERY_OK, msg)
        elif result[0][0] == 1:
            update_query = 'UPDATE Packets SET min_ps = {}, max_ps = {}, avg_ps = {}, std_dev_ps = {}, min_piat = {}, max_piat = {}, avg_piat = {}, std_dev_piat = {} WHERE Flow_index = {};'.format(
                packet_information[1], packet_information[2], packet_information[3], packet_information[4], packet_information[5], packet_information[6], packet_information[7], packet_information[8], packet_information[0]
            )
            print(update_query)
            print('row is already present use update instead')
            try:
                self.cursor.execute(update_query)
            except mysql.connector.Error as err:
                errmsg = ('Unexpected error: {}').format(err.msg)
                return(self.QUERY_ERR, errmsg)
            self.connection.commit()
            msg = 'Succesfully updated new row in Packets data with Flow_index = {}'.format(packet_information[0])
            return(self.QUERY_OK, msg)
        return

    def update_flag_table(self, flag_information):
        query1 = 'SELECT COUNT(*) FROM Flags WHERE Flow_index = {};'.format(flag_information[0]) #Check if the row exists, if it does update otherwise insert
        print(query1)
        self.cursor.execute(query1)
        result = self.cursor.fetchall()
        if result[0][0] == 0:
            print('add new row first')
            insert_query = 'INSERT INTO Flags(Flow_index, FIN_Flag_Count, SYN_Flag_Count, RST_Flag_Count, PSH_Flag_Count, ACK_Flag_Count, URG_Flag_Count, CWE_Flag_Count, ECE_Flag_Count) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
                flag_information[0], flag_information[1], flag_information[2], flag_information[3], flag_information[4], flag_information[5], flag_information[6], flag_information[7], flag_information[8]
            )
            print(insert_query)
            try:
                self.cursor.execute(insert_query)
            except mysql.connector.Error as err:
                errmsg = ('Unexpected Error: {}').format(err.msg)
                print(errmsg)
                return (self.QUERY_ERR, errmsg)
            self.connection.commit()
            msg = 'Succesfully inserted new row in flags table with Flow_index = {}'.format(flag_information[0])
            print(msg)
            return (self.QUERY_OK, msg)
        elif result[0][0] == 1:
            print('update existing row')
            update_query = 'UPDATE Flags SET FIN_Flag_Count = {}, SYN_Flag_Count = {}, RST_Flag_Count = {}, PSH_Flag_Count = {}, ACK_Flag_Count = {}, URG_Flag_Count = {}, CWE_Flag_Count = {}, ECE_Flag_Count = {} WHERE Flow_index = {}'.format(
                flag_information[1], flag_information[2], flag_information[3], flag_information[4], flag_information[5], flag_information[6], flag_information[7], flag_information[8], flag_information[0]
            )
            print(update_query)
            try:
                self.cursor.execute(update_query)
            except mysql.connector.Error as err:
                errmsg = ('Unexpected Error: {}').format(err.msg)
                print(errmsg)
                return (self.QUERY_ERR, errmsg)
            self.connection.commit()
            msg = 'Succesfully updated row in flags table with Flow_index = {}'.format(flag_information[0])
            print(msg)
            return(self.QUERY_OK, msg)

    def update_protocol_table(self, protocol_information):
        count_query = 'SELECT COUNT(*) FROM Protocol2 WHERE Flow_index = {};'.format(protocol_information[0])
        print(count_query)
        self.cursor.execute(count_query)
        result = self.cursor.fetchall()
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
            self.cursor.execute(main_query)
        except mysqlconnector.Error as err:
            errmsg = ('Unexpected Error: {}').format(err.msg)
            print(errmsg)
            return (self.QUERY_ERR, errmsg)
        self.connection.commit()
        return(self.QUERY_OK, msg)


        def update_forward_flows_table(self, forward_flow_information):
            count_query = 'SELECT COUNT(*) FROM ForwardFlows WHERE Flow_index = {}; '.format(forward_flow_information[0])
            print(count_query)
            self.cursor.execute(count_query)
            result = self.cursor.fetchall()
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
                self.cursor.execute(main_query)
            except mysqlconnector.Error as err:
                errmsg = ('Unexpected Error: {}').format(err.msg)
                print(errmsg)
                return(self.QUERY_ERR, errmsg)
            self.connection.commit()
            return(self.QUERY_OK, msg)

        def update_backward_flows_table(self, backward_flow_information):
            count_query = 'SELECT COUNT(*) FROM BackwardFlows WHERE Flow_index = {}; '.format(backward_flow_information[0])
            print(count_query)
            self.cursor.execute(count_query)
            result = self.cursor.fetchall()
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
                self.cursor.execute(main_query)
            except mysqlconnector.Error as err:
                errmsg = ('Unexpected Error: {}').format(err.msg)
                print(errmsg)
                return(self.QUERY_ERR, errmsg)
            self.connection.commit()
            return(self.QUERY_OK, msg)
            
        def update_flow_timing_table(self, date_time_information):
            count_query = 'SELECT COUNT(*) FROM Flows WHERE Flow_index = {};'.format(date_time_information[0])
            print(count_query)
            self.cursor.execute(count_query)
            result = self.cursor.fetchall()
            if result[0][0] == 0:
                errmsg = 'This flow does not exist in our system, Please insert the flow first'
                return (self.QUERY_ERR, errmsg)
            elif result[0][0] == 1:
                main_query = 'UPDATE Flows SET Flow_Start = \'{}\', Flow_Duration = {} WHERE Flow_index = {};'.format(
                    date_time_information[1], date_time_information[2], date_time_information[0]
                )
            try:
                self.cursor.execute(main_query)
            except mysqlconnector.Error as err:
                errmsg = ('Unexpected Error: {}').format(err.msg)
                return (self.QUERY_ERR, errmsg)
            self.connection.commit()
            msg = 'Succesfully updated date time information of flow with Flow_index = {}'.format(date_time_information[0])
            return(self.QUERY_OK, msg)