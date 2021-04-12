import numpy as np 
import pandas as pd
import csv
import matplotlib.pyplot as plt 
from sklearn.cluster import KMeans
import mysql.connector
from mysql.connector import Error 
from instances.login import Login

class K_means_cluster: 
    def __init__(self):
        login_instance = Login()
        self.connection = login_instance.initialize_db()
        self.cursor = self.connection.cursor()

    def generate_csv(self):
        """
        Generate csv of total packet size data
        """
        result = []
        try:
            # 2002 is the total number of flows, as a result we calculate the total average
            query = ('SELECT F1.Flow_Duration, (F.f_pktTotalCount + B.b_pktTotalCount)/200002 AS Total_Packet_PerFlow FROM ForwardFlows F join BackwardFlows B ON F.Flow_index = B.Flow_index JOIN Flows F1 ON F1.Flow_index = F.Flow_index Order By Flow_Duration')
            self.cursor.execute(query)
        except Error:
            return result
        query_result = self.cursor.fetchall()
        with open('total_packet_count.csv', mode='w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            row_index = 0
            for x in query_result:
                if x[1] == 'NULL':
                    continue
                csv_writer.writerow([row_index, x[1]])
                row_index += 1
        return result
    
    def perform_clustering(self, cluster_num):
        """
        Cluster the data generated in the csv
        """
        df = pd.read_csv('total_packet_count.csv')
        x = df.iloc[:, [0, 1]].values
        print(x)
        kmeans = KMeans(n_clusters=cluster_num)
        y_kmeans5 = kmeans.fit_predict(x)
        print(y_kmeans5)
        kmeans.cluster_centers_
        plt.scatter(x[:, 0], x[:, 1], c=y_kmeans5, cmap='rainbow')
        plt.show()

############################
#           Main           #
############################
K_mean = K_means_cluster()
K_mean.generate_csv()
K_mean.perform_clustering(5)



