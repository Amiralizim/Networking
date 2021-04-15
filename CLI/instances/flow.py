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

    def display_annotations(self, Flow_index):
        query = 'SELECT comments FROM annotations WHERE Flow_index = {};'.format(Flow_index)
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for x in results:
            click.secho(x[0], fg = 'magenta')
    
    def client_display_annotations(self, Flow_index):
        record = []
        try: 
            query = 'SELECT comments FROM annotations WHERE Flow_index = {};'.format(Flow_index)
            self.cursor.execute(query)
        except Error:
            return record
        record = self.cursor.fetchall()
        return record
