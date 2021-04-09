import mysql.connector
from mysql.connector import Error
import click

class Link:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

    def mode_helper(self, mode):
        """
        Determines if the private_ips or public_ips view has to be used
        """
        view_name = ""
        if(mode == "private"):
            view_name = "private_ips"
        elif(mode == "public"):
            view_name = "public_ips"
        return view_name
    
    def get_source_ports(self, mode, srcIP):
        """
        Determines the source port based on the provided srcIP
        """
        result = []
        try:
            query = ('SELECT distinct srcPort FROM {} WHERE srcIP="{}";').format(self.mode_helper(mode), str(srcIP))
            self.cursor.execute(query)
        except Error:
            return result    
        query_result = self.cursor.fetchall()
        for x in query_result:
            result.append(x[0])
        return result
    
    def get_dst_ips(self, mode, srcIP, srcPort):
        """
        Determines the destination IP based on the provided srcIP and srcPort
        """
        result = []
        try:
            query = ('SELECT distinct dstIP FROM {} WHERE srcIP="{}" AND srcPort="{}";').format(self.mode_helper(mode), str(srcIP), str(srcPort))
            self.cursor.execute(query)
        except Error:
            return result
        query_result = self.cursor.fetchall()
        for x in query_result:
            result.append(x[0])
        return result

    def get_dst_ports(self, mode, srcIP, srcPort, dstIP):
        """
        Determines the destination IP based on the provided srcIP, srcPort and destination IP
        """
        result = []
        try:
            query = ('SELECT distinct dstPort FROM {} WHERE srcIP="{}" AND srcPort="{}" AND dstIP="{}";').format(self.mode_helper(mode), str(srcIP), str(srcPort), str(dstIP))
            self.cursor.execute(query)
        except Error:
            return result
        query_result = self.cursor.fetchall()
        for x in query_result:
            result.append(x[0])
        return result

    def get_links(self, sourceip, sourceport, destinationip, destinationport):
        """
        Fetch Link_ID from table Links.
        inputs: source ip, port, destination ip, port
        output: corresponding Link_ID 
        """

        result = ""
        link_id = ("{}-{}-{}-{}").format(sourceip, sourceport, destinationip, destinationport)
        try:
            query = ("SELECT Link_ID FROM Links WHERE Link_ID = \'{}\'; ").format(link_id)
            self.cursor.execute(query)
        except Error:
            return result
        for x in self.cursor.fetchall():
            result += x[0]            # x is a tuple type, Link_ID is a string type

        return result