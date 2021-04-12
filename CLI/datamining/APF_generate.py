import pandas as pd
import csv
# -------------------------------------------------------------- APF --------------------------------------------------------------
# description: calculate the APF (average packets per flow) for dataset 1, 2 and combined. The result is then written on a new csv.
# NOTE: before using, please modify line 15, 35 to reflect the path of the csv for dataset 1 and 2
#                      please modify line 58 to reflect the path for the output file
# usage: after installing the corresponding modules, simply run the python script.

# dataset 1 get totalPktCount
ds1_totalPktCount = 0
ds1_totalFlowCount = 0
ds1_avgPktPerFlow = 0

ds1_column_names = ["Flow_ID", "Source_IP", "Source_Port", "Destination_IP", "Destination_Port", "Protocol", "Timestamp", "Flow_Duration","Total_Fwd_Packets","Total_Backward_Packets","Total_Length_of_Fwd_Packets","Total_Length_of_Bwd_Packets","Fwd_Packet_Length_Max","Fwd_Packet_Length_Min","Fwd_Packet_Length_Mean","Fwd_Packet_Length_Std","Bwd_Packet_Length_Max","Bwd_Packet_Length_Min","Bwd_Packet_Length_Mean","Bwd_Packet_Length_Std","Flow_Bytes_s","Flow_Packets_s","Flow_IAT_Mean","Flow_IAT_Std","Flow_IAT_Max","Flow_IAT_Min","Fwd_IAT_Total","Fwd_IAT_Mean","Fwd_IAT_Std","Fwd_IAT_Max","Fwd_IAT_Min","Bwd_IAT_Total","Bwd_IAT_Mean","Bwd_IAT_Std","Bwd_IAT_Max","Bwd_IAT_Min","Fwd_PSH_Flags","Bwd_PSH_Flags","Fwd_URG_Flags","Bwd_URG_Flags","Fwd_Header_Length","Bwd_Header_Length","Fwd_Packets_s","Bwd_Packets_s","Min_Packet_Length","Max_Packet_Length","Packet_Length_Mean","Packet_Length_Std","Packet_Length_Variance","FIN_Flag_Count","SYN_Flag_Count","RST_Flag_Count","PSH_Flag_Count","ACK_Flag_Count","URG_Flag_Count","CWE_Flag_Count","ECE_Flag_Count","Down_Up_Ratio","Average_Packet_Size","Avg_Fwd_Segment_Size","Avg_Bwd_Segment_Size","Fwd_Header_Length_1","Fwd_Avg_Bytes_Bulk","Fwd_Avg_Packets_Bulk","Fwd_Avg_Bulk_Rate","Bwd_Avg_Bytes_Bulk","Bwd_Avg_Packets_Bulk","Bwd_Avg_Bulk_Rate","Subflow_Fwd_Packets","Subflow_Fwd_Bytes","Subflow_Bwd_Packets","Subflow_Bwd_Bytes","Init_Win_bytes_forward","Init_Win_bytes_backward","act_data_pkt_fwd","min_seg_size_forward","Active_Mean","Active_Std","Active_Max","Active_Min","Idle_Mean","Idle_Std","Idle_Max","Idle_Min","Label","L7Protocol","ProtocolName"]
df1 = pd.read_csv("/Users/zzzh/Documents/Winter2021/ECE356/LAB/Data/Networking_dataset_temp/21-Network-Traffic/Dataset-Unicauca-Version2-87Atts.csv", names = ds1_column_names)
ds1_totalFwdCount = df1.Total_Fwd_Packets.to_list()
ds1_totalBwdCount = df1.Total_Backward_Packets.to_list()
# range start from 1 (excluding attribute name), stops at len(df) (excluding it), step size: 1
for i in range(1, len(df1), 1):
    ds1_totalPktCount += int(ds1_totalFwdCount[i])
    ds1_totalPktCount += int(ds1_totalBwdCount[i])
ds1_totalFlowCount = len(df1) - 1
ds1_avgPktPerFlow = ds1_totalPktCount / ds1_totalFlowCount
print("--------------- dataset 1 ---------------")                  # --------------- dataset 1 ---------------
print("total packet counts: %i" % ds1_totalPktCount)                # total packet counts: 456888033
print("total flow counts: %i" % ds1_totalFlowCount)                 # total flow counts: 3577296
print("average packets per flow: %f" % ds1_avgPktPerFlow)           # average packets per flow: 127.718823

# dataset 2 get totalPktCount
ds2_totalPktCount = 0
ds2_totalFlowCount = 0
ds2_avgPktPerFlow = 0

ds2_column_names = ["flow_key",	"src_ip_numeric",	"src_ip",	"src_port",	"dst_ip",	"dst_port",	"proto",	"pktTotalCount",	"octetTotalCount",	"min_ps",	"max_ps",	"avg_ps",	"std_dev_ps",	"flowStart",	"flowEnd",	"flowDuration",	"min_piat",	"max_piat",	"avg_piat",	"std_dev_piat",	"f_pktTotalCount",	"f_octetTotalCount",	"f_min_ps",	"f_max_ps",	"f_avg_ps",	"f_std_dev_ps",	"f_flowStart",	"f_flowEnd",	"f_flowDuration",	"f_min_piat",	"f_max_piat",	"f_avg_piat",	"f_std_dev_piat",	"b_pktTotalCount",	"b_octetTotalCount",	"b_min_ps",	"b_max_ps",	"b_avg_ps",	"b_std_dev_ps",	"b_flowStart",	"b_flowEnd",	"b_flowDuration",	"b_min_piat",	"b_max_piat",	"b_avg_piat",	"b_std_dev_piat",	"flowEndReason",	"category",	"application_protocol",	"web_service"]
df2 = pd.read_csv("/Users/zzzh/Documents/Winter2021/ECE356/LAB/Data/Networking_dataset_temp/21-Network-Traffic/Unicauca-dataset-April-June-2019-Network-flows.csv", names = ds2_column_names)
ds2_packetCount = df2.pktTotalCount.to_list()

for i in range(1, len(df2), 1):
    ds2_totalPktCount += int(ds2_packetCount[i])
ds2_totalFlowCount = len(df2) - 1
ds2_avgPktPerFlow = ds2_totalPktCount / ds2_totalFlowCount
print("--------------- dataset 2 ---------------")                     # --------------- dataset 2 ---------------
print("total packet counts: %i" % ds2_totalPktCount)                   # total packet counts: 241188599    
print("total flow counts: %i" % ds2_totalFlowCount)                    # total flow counts: 2704839
print("average packets per flow: %f" % ds2_avgPktPerFlow)              # average packets per flow: 89.169300 

# dataset 1 + 2
totalPktCount = ds1_totalPktCount + ds2_totalPktCount
totalFlowCount = ds1_totalFlowCount + ds2_totalFlowCount
avgPktPerFlow = totalPktCount / totalFlowCount

print("--------------- dataset 1&2 ---------------")                    # --------------- dataset 1&2 ---------------
print("total packet counts: %i" % totalPktCount)                        # total packet counts: 698076632
print("total flow counts: %i" % totalFlowCount)                         # total flow counts: 6282135
print("average packets per flow: %f" % avgPktPerFlow)                   # average packets per flow: 111.120922

# write into a csv file that CLI can fetch later
with open('/Users/zzzh/Documents/Winter2021/ECE356/LAB/Networking_dataset/datamining/APF.csv', mode='w') as csv_file:
    fieldnames = ["ds1_totalPktCount", "ds1_totalFlowCount", "ds1_avgPktPerFlow", "ds2_totalPktCount", "ds2_totalFlowCount", "ds2_avgPktPerFlow", "totalPktCount", "totalFlowCount", "avgPktPerFlow"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    # write column name
    writer.writerow({"ds1_totalPktCount":"ds1_totalPktCount", "ds1_totalFlowCount":"ds1_totalFlowCount", "ds1_avgPktPerFlow":"ds1_avgPktPerFlow", "ds2_totalPktCount":"ds2_totalPktCount", "ds2_totalFlowCount":"ds2_totalFlowCount", "ds2_avgPktPerFlow":"ds2_avgPktPerFlow", "totalPktCount":"totalPktCount", "totalFlowCount":"totalFlowCount", "avgPktPerFlow":"avgPktPerFlow"})
    # write data
    writer.writerow({"ds1_totalPktCount":ds1_totalPktCount, "ds1_totalFlowCount":ds1_totalFlowCount, "ds1_avgPktPerFlow":ds1_avgPktPerFlow, "ds2_totalPktCount":ds2_totalPktCount, "ds2_totalFlowCount":ds2_totalFlowCount, "ds2_avgPktPerFlow":ds2_avgPktPerFlow, "totalPktCount":totalPktCount, "totalFlowCount":totalFlowCount, "avgPktPerFlow":avgPktPerFlow})

