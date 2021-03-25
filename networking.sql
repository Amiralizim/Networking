-- ------------------------------------------------
--
-- Networking Database

-- ip-network-traffic-flows-labeled-with-87-apps -------------------------------------------------------------------
create table Dataset1 (
	  Flow_ID varchar(40), 
	  Source_IP varchar(15),
	  Source_Port varchar(5), 
	  Destination_IP varchar(15), 
	  Destination_Port varchar(5), 
	  Protocol varchar(1),  
	  Timestamp varchar(30),
	  Flow_Duration decimal(9), 
	  Total_Fwd_Packets decimal(6),
	  Total_Backward_Packets decimal(6), 
	  Total_Length_of_Fwd_Packets decimal(9), 
	  Total_Length_of_Bwd_Packets decimal(10), 
	  Fwd_Packet_Length_Max decimal(5), 
	  Fwd_Packet_Length_Min decimal(5), 
	  Fwd_Packet_Length_Mean decimal(5), 
	  Fwd_Packet_Length_Std decimal(4), 
	  Bwd_Packet_Length_Max decimal(5), 
	  Bwd_Packet_Length_Min decimal(5), 
	  Bwd_Packet_Length_Mean decimal(5), 
	  Bwd_Packet_Length_Std decimal(4), 
	  Flow_Bytes_s decimal(11), 
	  Flow_Packets_s decimal(7), 
	  Flow_IAT_Mean decimal(9), 
	  Flow_IAT_Std decimal(8), 
	  Flow_IAT_Max decimal(9),
	  Flow_IAT_Min decimal(9), 
	  Fwd_IAT_Total decimal(9),
	  Fwd_IAT_Mean decimal(9),
	  Fwd_IAT_Std decimal(8), 
	  Fwd_IAT_Max decimal(9), 
	  Fwd_IAT_Min decimal(9), 
	  Bwd_IAT_Total decimal(9), 
	  Bwd_IAT_Mean decimal(9), 
	  Bwd_IAT_Std decimal(8), 
	  Bwd_IAT_Max decimal(9),
	  Bwd_IAT_Min decimal(9), 
	  Fwd_PSH_Flags decimal(1), 
	  Bwd_PSH_Flags decimal(1), 
	  Fwd_URG_Flags decimal(1), 
	  Bwd_URG_Flags decimal(1), 
	  Fwd_Header_Length decimal(8), 
	  Bwd_Header_Length decimal(8), 
	  Fwd_Packets_s decimal(7),
	  Bwd_Packets_s decimal(7),
	  Min_Packet_Length decimal(4),
	  Max_Packet_Length decimal(5), 
	  Packet_Length_Mean decimal(5), 
	  Packet_Length_Std decimal(4), 
	  Packet_Length_Variance decimal(8), 
	  FIN_Flag_Count decimal(1), 
	  SYN_Flag_Count decimal(1), 
	  RST_Flag_Count decimal(1), 
	  PSH_Flag_Count decimal(1), 
	  ACK_Flag_Count decimal(1),
	  URG_Flag_Count decimal(1), 
	  CWE_Flag_Count decimal(1), 
	  ECE_Flag_Count decimal(1), 
	  Down_Up_Ratio decimal(3), 
	  Average_Packet_Size decimal(5), 
	  Avg_Fwd_Segment_Size decimal(5), 
	  Avg_Bwd_Segment_Size decimal(5), 
	  Fwd_Header_Length_1 decimal(8), 
	  Fwd_Avg_Bytes_Bulk decimal(1),
	  Fwd_Avg_Packets_Bulk decimal(1), 
	  Fwd_Avg_Bulk_Rate decimal(1), 
	  Bwd_Avg_Bytes_Bulk decimal(1), 
	  Bwd_Avg_Packets_Bulk decimal(1), 
	  Bwd_Avg_Bulk_Rate decimal(1), 
	  Subflow_Fwd_Packets decimal(6),
	  Subflow_Fwd_Bytes decimal(9),
	  Subflow_Bwd_Packets decimal(6), 
	  Subflow_Bwd_Bytes decimal(10), 
	  Init_Win_bytes_forward decimal(5), 
	  Init_Win_bytes_backward decimal(5), 
	  act_data_pkt_fwd decimal(6), 
	  min_seg_size_forward decimal(3),
	  Label varchar(6),
	  L7Protocol decimal(3),
	  ProtocolName varchar(15)
);
load data infile '/var/lib/mysql-files/21-Network-Traffic/Dataset-Unicauca-Version2-87Atts.csv' ignore into table Dataset1
		fields terminated by ','
		enclosed by '"'
		lines terminated by '\n'
		ignore 1 lines;


-- Unicauca-dataset-April-June-2019-Network-flows  -------------------------------------------------------------------
create table Dataset2 (
	 flow_key varchar(33), 
	 src_ip_numeric decimal(10), 
	 src_ip varchar(15), 
	 src_port decimal(6), 
	 dst_ip varchar(15), 
	 dst_port decimal(6), 
	 proto decimal(2), 
	 pktTotalCount decimal(8), 
	 octetTotalCount decimal(10), 
	 min_ps decimal(6), 
	 max_ps decimal(6), 
	 avg_ps decimal(6), 
	 std_dev_ps decimal(4), 
	 flowStart decimal(10), 
	 flowEnd decimal(10), 
	 flowDuration decimal(4), 
	 min_piat decimal(4), 
	 max_piat decimal(4), 
	 avg_piat decimal(4), 
	 std_dev_piat decimal(3), 
	 f_pktTotalCount decimal(8), 
	 f_octetTotalCount decimal(10), 
	 f_min_ps decimal(5), 
	 f_max_ps decimal(5), 
	 f_avg_ps decimal(5), 
	 f_std_dev_ps decimal(4), 
	 f_flowStart decimal(10),
	 f_flowEnd decimal(12), 
	 f_flowDuration decimal(4),
	 f_min_piat decimal(4), 
	 f_max_piat decimal(4), 
	 f_avg_piat decimal(4), 
	 f_std_dev_piat decimal(3),
	 b_pktTotalCount decimal(8), 
	 b_octetTotalCount decimal(10), 
	 b_min_ps decimal(5),  
	 b_max_ps decimal(5),  
	 b_avg_ps decimal(5),  
	 b_std_dev_ps decimal(5), 
	 b_flowStart decimal(10), 
	 b_flowEnd decimal(10), 
	 b_flowDuration decimal(12),  
	 b_min_piat decimal(5),  
	 b_max_piat decimal(5),  
	 b_avg_piat decimal(5),  
	 b_std_dev_piat decimal(3), 
	 flowEndReason decimal(1),  
	 category varchar(7), 
	 application_protocol varchar(6), 
	 web_service varchar(20) 
);
load data infile '/var/lib/mysql-files/21-Network-Traffic/Unicauca-dataset-April-June-2019-Network-flows.csv' ignore into table Dataset2
		fields terminated by ','
		enclosed by '"'
		lines terminated by '\n'
		ignore 1 lines;


-- Links Table -------------------------------------------------------------------
-- select '----------------------------------------------------------------' as '';
-- select 'Create Links' as '';

-- create table Links

-- create table Links (srcIP varchar(15), -- max: 255.255.255.255 -> 12+3
-- 				    srcPort varchar(5),
-- 					dstIP varchar(15),
-- 					dstPort varchar(15),
-- -- Constraints
-- 					primary key (flowID)
-- );