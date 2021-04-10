''' This file is used to generate all update queries '''
import mysql.connector
from mysql.connector import Error

DUPLICATE_PRIMARY_KEY_ERRNO = 1062
CLIENT_ORIGIN = 3
QUERY_ERR = -1
QUERY_OK = 0

class Update_Result:
    def __init__(self, QUERY_OK, msg, is_new_row, row_before, row_after):
        self.QUERY_OK = QUERY_OK
        self.msg = msg
        self.is_new_row = is_new_row
        self.row_before = row_before
        self.row_after = row_after

class Delete_Result:
    def __init__(self, QUERY_OK, msg):
        self.QUERY_OK = QUERY_OK
        self.msg = msg

class Update_Queries:
    def __init__(self, count_query, get_query, insert_query, update_query):
        self.count_query = count_query
        self.get_query = get_query
        self.insert_query = insert_query
        self.update_query = update_query

class Update:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()
    
    def delete_from_table(self, table_name, Flow_id):
        delete_query = 'DELETE FROM {} WHERE Flow_index = {};'.format(table_name, Flow_id)
        print(delete_query)
        try:
            self.cursor.execute(delete_query)
        except mysql.connector.Error as err:
            errmsg = ('Unexpected error {}').format(err.msg)
            return Delete_Result(-1, errmsg)
        self.connection.commit()
        msg = 'Succesfully deleted From Table {} data with Flow_id: {}'.format(table_name, Flow_id)
        return Delete_Result(0, msg)
    
    def update_table(self, table_name, table_data):
        update_queries = self.get_update_queries(table_name, table_data)
        count_query = update_queries.count_query
        print(count_query)
        self.cursor.execute(count_query)
        count_result = self.cursor.fetchall()
        before_update = ""
        after_update = ""
        is_new_row = 0
        if count_result[0][0] == 0:
            is_new_row = 1
            main_query = update_queries.insert_query
            print(main_query)
            msg = 'Succesfully inserted new row in the {} table with Flow_index = {}'.format(table_name, table_data[0])
        elif count_result[0][0] == 1:
            self.cursor.execute(update_queries.get_query)
            before_result = self.cursor.fetchall()
            before_update = before_result[0]
            main_query = update_queries.update_query
            print(main_query)
            msg = 'Succesfully updated the row in the {} table with Flow_index = {}'.format(table_name, table_data[0])
        
        try:
            self.cursor.execute(main_query)
        except mysqlconnector.Error as err:
            errmsg = ('Unexpected Error: {}').format(err.msg)
            print(errmsg)
            return Update_Result(-1, errmsg, is_new_row, before_updat, after_update)
        self.connection.commit()
        self.cursor.execute(update_queries.get_query)
        after_result = self.cursor.fetchall()
        after_update = after_result[0]
        return Update_Result(1, msg, is_new_row, before_update, after_update)

    def get_update_queries(self, table_name, table_information):
        Flow_index = table_information[0]
        count_query = 'SELECT COUNT(*) FROM {} WHERE Flow_index = {};'.format(table_name, table_information[0])
        get_query = 'SELECT * FROM {} WHERE Flow_index = {};'.format(table_name, table_information[0])

        if table_name == 'Packets':
            insert_query = 'INSERT INTO Packets(Flow_index, min_ps, max_ps, avg_ps, std_dev_ps, min_piat, max_piat, avg_piat, std_dev_piat) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
                table_information[0], table_information[1], table_information[2], table_information[3], table_information[4], table_information[4], table_information[5], table_information[6], table_information[7], table_information[8])
            update_query = 'UPDATE Packets SET min_ps = {}, max_ps = {}, avg_ps = {}, std_dev_ps = {}, min_piat = {}, max_piat = {}, avg_piat = {}, std_dev_piat = {} WHERE Flow_index = {};'.format(
                table_information[1], table_information[2], table_information[3], table_information[4], table_information[5], table_information[6], table_information[7], table_information[8], table_information[0]
            )
        elif table_name == 'Flags':
            insert_query = 'INSERT INTO Flags(Flow_index, FIN_Flag_Count, SYN_Flag_Count, RST_Flag_Count, PSH_Flag_Count, ACK_Flag_Count, URG_Flag_Count, CWE_Flag_Count, ECE_Flag_Count) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
                table_information[0], table_information[1], table_information[2], table_information[3], table_information[4], table_information[5], table_information[6], table_information[7], table_information[8]
            )
            update_query = 'UPDATE Flags SET FIN_Flag_Count = {}, SYN_Flag_Count = {}, RST_Flag_Count = {}, PSH_Flag_Count = {}, ACK_Flag_Count = {}, URG_Flag_Count = {}, CWE_Flag_Count = {}, ECE_Flag_Count = {} WHERE Flow_index = {}'.format(
                table_information[1], table_information[2], table_information[3], table_information[4], table_information[5], table_information[6], table_information[7], table_information[8], table_information[0]
            )
        elif table_name == 'Protocol2':
            insert_query = 'INSERT INTO Protocol2(Flow_index, proto, category, application_protocol, web_service) VALUES ({}, {}, \'{}\', \'{}\', \'{}\'); '.format(
                table_information[0], table_information[1], table_information[2], table_information[3], table_information[4]
            )
            update_query = 'UPDATE Protocol2 SET proto = {}, category = \'{}\', application_protocol = \'{}\', web_service = \'{}\' WHERE Flow_index = {};'.format(
                table_information[1], table_information[2], table_information[3], table_information[4], table_information[0]
            )
        elif table_name == 'ForwardFlows':
            insert_query = 'INSERT INTO ForwardFlows(Flow_index, f_pktTotalCount, f_octetTotalCount, f_min_ps, f_max_ps, f_avg_ps, f_std_dev_ps, f_min_piat, f_max_piat, f_avg_piat, f_std_dev_piat) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
                table_information[0], table_information[1], table_information[2], table_information[3], table_information[4], table_information[5], table_information[6], table_information[7], table_information[8], table_information[9], table_information[10]
            )
            update_query = 'UPDATE ForwardFlows SET f_pktTotalCount = {}, f_octetTotalCount = {}, f_min_ps = {}, f_max_ps = {}, f_avg_ps = {}, f_std_dev_ps = {}, f_min_piat = {}, f_max_piat = {}, f_avg_piat = {}, f_std_dev_piat = {} WHERE Flow_index = {};'.format(
                table_information[1], table_information[2], table_information[3], table_information[4], table_information[5], table_information[6], table_information[7], table_information[8], table_information[9], table_information[10], table_information[0]
            )
        elif table_name == 'BackwardFlows':
            insert_query = 'INSERT INTO BackwardFlows(Flow_index, b_pktTotalCount, b_octetTotalCount, b_min_ps, b_max_ps, b_avg_ps, b_std_dev_ps, b_min_piat, b_max_piat, b_avg_piat, b_std_dev_piat) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});'.format(
                table_information[0], table_information[1], table_information[2], table_information[3], table_information[4], table_information[5], table_information[6], table_information[7], table_information[8], table_information[9], table_information[10]
            )
            update_query = 'UPDATE BackwardFlows SET b_pktTotalCount = {}, b_octetTotalCount = {}, b_min_ps = {}, b_max_ps = {}, b_avg_ps = {}, b_std_dev_ps = {}, b_min_piat = {}, b_max_piat = {}, b_avg_piat = {}, b_std_dev_piat = {} WHERE Flow_index = {};'.format(
                table_information[1], table_information[2], table_information[3], table_information[4], table_information[5], table_information[6], table_information[7], table_information[8], table_information[9], table_information[10], table_information[0]
            )

        update_queries = Update_Queries(count_query, get_query, insert_query, update_query)
        return update_queries
    
    def insert_new_flow(self, srcIP, srcPort, dstIP, dstPort):
        Link_ID = ('{}-{}-{}-{}').format(srcIP, srcPort, dstIP, dstPort)
        #Step 1: Insert the Link into the Links table so the FK is satisfied
        query = 'INSERT INTO Links (Link_ID, srcIP, srcPort, dstIP, dstPort) VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\');'.format(Link_ID, srcIP, srcPort, dstIP, dstPort)
        print(query)
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            if (err.errno == DUPLICATE_PRIMARY_KEY_ERRNO):
                errmsg = 'Error: This link already exists, you can query the link and update its contents instead'
                return (QUERY_ERR,errmsg)
            else:
                errmsg = ('Unexpected Error: {}').format(err.msg)
                return (QUERY_ERR,errmsg)
        self.connection.commit()
        #Step 2: Get the max Flow_index so we can iterate it further, as this is the PK
        flow_index_query = 'SELECT MAX(Flow_index) FROM Flows'
        self.cursor.execute(flow_index_query)
        result = self.cursor.fetchall()
        flow_index = int(result[0][0])+1
        #Step 3: Insert just the Flow_index and the Link_ID into the flows table so now all a user has to do is update from the given flow index
        query = 'INSERT INTO Flows(Flow_index,Link_ID,origin) VALUES ({},\'{}\',{})'.format(flow_index,Link_ID, 3)
        self.cursor.execute(query)
        self.connection.commit()
        msg = ('Success, flow was added with Flow_index: {}').format(flow_index)
        return (0, msg)
    
    def update_flow_timing_table(self, date_time_information):
        count_query = 'SELECT COUNT(*) FROM Flows WHERE Flow_index = {};'.format(date_time_information[0])
        print(count_query)
        self.cursor.execute(count_query)
        result = self.cursor.fetchall()
        if result[0][0] == 0:
            errmsg = 'This flow does not exist in our system, Please insert the flow first'
            return (QUERY_ERR, errmsg)
        elif result[0][0] == 1:
            main_query = 'UPDATE Flows SET Flow_Start = \'{}\', Flow_Duration = {} WHERE Flow_index = {};'.format(
                date_time_information[1], date_time_information[2], date_time_information[0]
            )
        try:
            self.cursor.execute(main_query)
        except mysqlconnector.Error as err:
            errmsg = ('Unexpected Error: {}').format(err.msg)
            return (QUERY_ERR, errmsg)
        self.connection.commit()
        msg = 'Succesfully updated date time information of flow with Flow_index = {}'.format(date_time_information[0])
        return(QUERY_OK, msg)
    
