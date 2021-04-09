import mysql.connector
import click
from mysql.connector import Error
import hashlib

'''
This class is specifically used for login related functionalities
'''
class Protocol:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def converter(self, attribute):
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

    def get_protocol_name(self):
        """
        Determines the distinct protocol names
        """
        result = []
        try: 
            query = ('SELECT DISTINCT ProtocolName FROM Protocol1;')
            self.cursor.execute(query)
        except Error:
            return result
        query_result = self.cursor.fetchall()
        for x in query_result:
            result.append(x[0])
        return result 

    def get_webservice_names(self):
        """
        Determines the distinct web service names
        """
        result = []
        try:
            query = ('SELECT DISTINCT web_service FROM Protocol2;')
            self.cursor.execute(query)
        except Error:
            return result
        query_result = self.cursor.fetchall()
        for x in query_result:
            result.append(x[0])
        return result 

    
    def fetchFlowByPN(self,protocolName):
        """
        Determines the totla number of flows with matching protocolName
        input: protocolName
        output: total number of flows
        """

        query = ('SELECT COUNT(*) FROM Protocol1 WHERE ProtocolName = "{}"; ').format(protocolName)
        self.cursor.execute(query)
        query_result = self.cursor.fetchone()
        return query_result[0]

    def fetchFlowByWeb(self, web_service):
        """
        Determines the total number of flows with matching web_service
        input: web_service
        output: total number of flows
        """

        query = ('SELECT COUNT(*) FROM Protocol2 WHERE web_service = "{}"; ').format(web_service)
        self.cursor.execute(query)
        query_result = self.cursor.fetchone()
        return query_result[0]

    def fetchInfoByPN(self, attribute, pn):
        """
        Determine the max/min/avg of the attribute where flows are sorted by protocol name
        input: attribute (1,2,3,4 are for min, max, avg, std packet size, 5,6,7,8 are for min, max, avg, std packet interarrival time)
        """
        attributeName = self.converter(attribute)
        query = ('WITH temp(flow_index) AS (SELECT flow_index FROM Protocol1 WHERE ProtocolName = "{}") SELECT MAX({}), MIN({}), AVG({}), temp.Flow_index FROM temp INNER JOIN Packets on temp.flow_index = Packets.Flow_index;').format(pn, attributeName, attributeName, attributeName)
        self.cursor.execute(query)
        query_result = self.cursor.fetchone()
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

    def fetchInfoByWeb(self, attribute, ws):
        """
        Determine the max/min/avg of the attribute where flows are sorted by web services
        input: attribute (1,2,3,4 are for min, max, avg, std packet size, 5,6,7,8 are for min, max, avg, std packet interarrival time)
        """

        attributeName = self.converter(attribute)
        query = ('WITH temp(flow_index) AS (SELECT flow_index FROM Protocol2 WHERE web_service = "{}") SELECT MAX({}), MIN({}), AVG({}), temp.Flow_index FROM temp INNER JOIN Packets on temp.flow_index = Packets.Flow_index;').format(ws, attributeName, attributeName, attributeName)
        self.cursor.execute(query)
        query_result = self.cursor.fetchone()
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