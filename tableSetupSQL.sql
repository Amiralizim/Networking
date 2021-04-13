-- ------------------------------------------------
-- Networking Database
-- ip-network-traffic-flows-labeled-with-87-apps -------------------------------------------------------------------
create table Dataset1 (
	  Flow_ID varchar(46), 
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
	  Active_Mean decimal(10),  
	  Active_Std decimal(10), 
	  Active_Max decimal(10),
	  Active_Min decimal(10),
	  Idle_Mean decimal(10),
	  Idle_Std decimal(10),
	  Idle_Max decimal(10),
	  Idle_Min decimal(10),
	  Label varchar(6),
	  L7Protocol decimal(3),
	  ProtocolName varchar(20)
);
load data infile '/var/lib/mysql-files/21-Network-Traffic/Dataset-Unicauca-Version2-87Atts.csv' ignore into table Dataset1
		fields terminated by ','
		enclosed by '"'
		lines terminated by '\n'
		ignore 3477296 lines;

-- parse the data in the table
-- This includes: 
-- 1) reformat the timestamp field and store it in Flow_Start
-- 2) reformat Link_ID -> soureIp-SourcePort-DestinationIp-DestinationPort
-- 3) flow_index -> a uniqueue identifier for each flow
--				 -> flowId-flowDuration-flowStart

ALTER TABLE Dataset1
	ADD Link_ID varchar(60);

UPDATE Dataset1 d1
	SET d1.Link_ID = CONCAT(d1.Source_IP, '-', d1.Source_Port, '-', d1.Destination_IP, '-', d1.Destination_Port);

ALTER TABLE Dataset1
	ADD Flow_Start varchar(60);

UPDATE Dataset1 d1
	SET d1.Flow_Start = DATE_FORMAT((CONCAT(SUBSTRING(d1.Timestamp, 7, 4), '-', SUBSTRING(d1.Timestamp,4, 2), '-',  SUBSTRING(d1.Timestamp,1,2), ' ',SUBSTRING(d1.Timestamp,11,8))), "%Y-%m-%d %h:%i:%s");


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
		ignore 2604839 lines;

-- parse the data in the table
-- This includes: 
-- 1) reformat the flowDuration field and store it in Flow_Duration
-- 2) reformat Link_ID -> soureIp-SourcePort-DestinationIp-DestinationPort
-- 3) flow_index -> a uniqueue identifier for each flow
--				 -> flowId-flowDuration-flowStart

ALTER TABLE Dataset2
	ADD Link_ID varchar(60);

UPDATE Dataset2 d2
	SET d2.Link_ID = CONCAT(d2.src_ip, '-', d2.src_port, '-', d2.dst_ip, '-', d2.dst_port);

ALTER TABLE Dataset2
	ADD Flow_Start varchar(60);

UPDATE Dataset2 d2
	SET d2.Flow_Start = FROM_UNIXTIME(flowStart, "%Y-%m-%d %h:%i:%s");

ALTER TABLE Dataset2
	ADD Flow_Duration decimal(10);

UPDATE Dataset2 d2
	SET d2.Flow_Duration = TIME_TO_SEC(timediff(FROM_UNIXTIME(d2.flowDuration), FROM_UNIXTIME(0)));

------------------------------------------------------------- aggregate dataset -----------------------------------------------------------------------
-- this table combines both datasets and produce a unqiue id: Flow_index 
DROP TABLE IF EXISTS aggregate_dataset;

CREATE TABLE aggregate_dataset (
	 Flow_index int NOT NULL AUTO_INCREMENT,
	 src_ip varchar(15), 
	 src_port decimal(6), 
	 dst_ip varchar(15), 
	 dst_port decimal(6), 
	 proto decimal(2), 
	 min_ps decimal(6), 
	 max_ps decimal(6), 
	 avg_ps decimal(6), 
	 std_dev_ps decimal(4), 
	 flowStart varchar(60), 
	 flowDuration decimal(10), 
	 min_piat decimal(9), 
	 max_piat decimal(9), 
	 avg_piat decimal(9), 
	 std_dev_piat decimal(8), 
	 f_pktTotalCount decimal(8), 
	 f_octetTotalCount decimal(10), 
	 f_min_ps decimal(5), 
	 f_max_ps decimal(5), 
	 f_avg_ps decimal(5), 
	 f_std_dev_ps decimal(4), 
	 f_min_piat decimal(9), 
	 f_max_piat decimal(9), 
	 f_avg_piat decimal(9), 
	 f_std_dev_piat decimal(8),
	 b_pktTotalCount decimal(8), 
	 b_octetTotalCount decimal(10), 
	 b_min_ps decimal(5),  
	 b_max_ps decimal(5),  
	 b_avg_ps decimal(5),  
	 b_std_dev_ps decimal(5), 
	 b_min_piat decimal(9),  
	 b_max_piat decimal(9),  
	 b_avg_piat decimal(9),  
	 b_std_dev_piat decimal(8), 
	 category varchar(7) DEFAULT NULL,  				-- dataset2
	 application_protocol varchar(6) DEFAULT NULL, 		-- dataset2
	 web_service varchar(20) DEFAULT NULL,				-- dataset2
     L7Protocol decimal(3) DEFAULT NULL,                -- dataset1
	 ProtocolName varchar(20) DEFAULT NULL,             -- dataset1
	 FIN_Flag_Count decimal(1) DEFAULT NULL, 			-- dataset1
	 SYN_Flag_Count decimal(1) DEFAULT NULL, 			-- dataset1
	 RST_Flag_Count decimal(1) DEFAULT NULL, 			-- dataset1
	 PSH_Flag_Count decimal(1) DEFAULT NULL, 			-- dataset1
	 ACK_Flag_Count decimal(1) DEFAULT NULL,			-- dataset1
 	 URG_Flag_Count decimal(1) DEFAULT NULL, 			-- dataset1
	 CWE_Flag_Count decimal(1) DEFAULT NULL, 			-- dataset1
	 ECE_Flag_Count decimal(1) DEFAULT NULL,			-- dataset1
	 origin varchar(1),                                 -- specifies if from dataset 1 or 2
	 PRIMARY KEY (Flow_index)
);

-- load data from dataset1 
INSERT INTO aggregate_dataset (src_ip, src_port, dst_ip, dst_port, proto, min_ps, max_ps, avg_ps, std_dev_ps, flowStart,  
	 						   flowDuration, min_piat, max_piat, avg_piat, std_dev_piat, f_pktTotalCount, f_octetTotalCount, f_min_ps, f_max_ps, f_avg_ps, 
	 						   f_std_dev_ps, f_min_piat, f_max_piat, f_avg_piat, f_std_dev_piat,b_pktTotalCount, 
							   b_octetTotalCount, b_min_ps,  b_max_ps,  b_avg_ps,  b_std_dev_ps, b_min_piat,  b_max_piat,  
							   b_avg_piat,  b_std_dev_piat, L7Protocol, ProtocolName, origin, 
							   FIN_Flag_Count, SYN_Flag_Count, RST_Flag_Count, PSH_Flag_Count, ACK_Flag_Count, URG_Flag_Count, CWE_Flag_Count, ECE_Flag_Count)
SELECT Source_IP, Source_Port, Destination_IP, Destination_Port, Protocol, Min_Packet_Length, Max_Packet_Length, Packet_Length_Mean, Packet_Length_Std, Flow_Start,
	    Flow_Duration, Flow_IAT_Min, Flow_IAT_Max, Flow_IAT_Mean, Flow_IAT_Std, Total_Fwd_Packets, Total_Length_of_Fwd_Packets, Fwd_Packet_Length_Min, Fwd_Packet_Length_Max, Fwd_Packet_Length_Mean,
		Fwd_Packet_Length_Std, Fwd_IAT_Min, Fwd_IAT_Max, Fwd_IAT_Mean, Fwd_IAT_Std, Total_Backward_Packets,
		Total_Length_of_Bwd_Packets, Bwd_Packet_Length_Min, Bwd_Packet_Length_Max, Bwd_Packet_Length_Mean, Bwd_Packet_Length_Std, Bwd_IAT_Min, Bwd_IAT_Max,
		Bwd_IAT_Mean, Bwd_IAT_Std, L7Protocol, ProtocolName, 1, FIN_Flag_Count, SYN_Flag_Count, RST_Flag_Count, PSH_Flag_Count, ACK_Flag_Count, URG_Flag_Count, CWE_Flag_Count, ECE_Flag_Count
FROM Dataset1;

-- load data from dataset2
INSERT INTO aggregate_dataset (src_ip, src_port, dst_ip, dst_port, proto, min_ps, max_ps, avg_ps, std_dev_ps, flowStart,  
	 						   flowDuration, min_piat, max_piat, avg_piat, std_dev_piat, f_pktTotalCount, f_octetTotalCount, f_min_ps, f_max_ps, f_avg_ps, 
	 						   f_std_dev_ps, f_min_piat, f_max_piat, f_avg_piat, f_std_dev_piat,b_pktTotalCount, 
							   b_octetTotalCount, b_min_ps,  b_max_ps,  b_avg_ps,  b_std_dev_ps, b_min_piat,  b_max_piat,  
							   b_avg_piat,  b_std_dev_piat, category, application_protocol, web_service, origin)
SELECT src_ip, src_port, dst_ip, dst_port, proto, min_ps, max_ps, avg_ps, std_dev_ps, Flow_Start,  
	 						   flowDuration, min_piat, max_piat, avg_piat, std_dev_piat, f_pktTotalCount, f_octetTotalCount, f_min_ps, f_max_ps, f_avg_ps, 
	 						   f_std_dev_ps, f_min_piat, f_max_piat, f_avg_piat, f_std_dev_piat,b_pktTotalCount, 
							   b_octetTotalCount, b_min_ps,  b_max_ps,  b_avg_ps,  b_std_dev_ps, b_min_piat,  b_max_piat,  
							   b_avg_piat,  b_std_dev_piat, category, application_protocol, web_service, 2
FROM Dataset2;

-- link ID stuff
ALTER TABLE aggregate_dataset
	ADD Link_ID varchar(60);

UPDATE aggregate_dataset d2
	SET d2.Link_ID = CONCAT(d2.src_ip, '-', d2.src_port, '-', d2.dst_ip, '-', d2.dst_port);

------------------------------------------------------------- Links -----------------------------------------------------------------------
DROP TABLE IF EXISTS Links;

create table Links (Link_ID varchar(60),
	    			srcIP varchar(15),
 				    srcPort varchar(5),
 					dstIP varchar(15),
 					dstPort varchar(15),
					PRIMARY KEY (Link_ID)
);

INSERT INTO Links
SELECT Link_ID, src_ip, src_port, dst_ip, dst_port 
FROM aggregate_dataset
GROUP BY Link_ID, src_ip, src_port, dst_ip, dst_port;

------------------------------------------------------------- Flows ----------------------------------------------------------------------
DROP TABLE IF EXISTS Flows;

CREATE TABLE Flows (Flow_index int,
					Link_ID varchar(60),
					Flow_Start varchar(60),
					Flow_Duration decimal(10),
					origin varchar(1),
					PRIMARY KEY (Flow_index),
					FOREIGN KEY (Link_ID) REFERENCES Links(Link_ID)
					);

INSERT INTO Flows
SELECT Flow_index, Link_ID, flowStart, flowDuration, origin
FROM aggregate_dataset;

------------------------------------------------------------- ForwardFlows -----------------------------------------------------------------------
DROP TABLE IF EXISTS ForwardFlows;

create table ForwardFlows(Flow_index int,
						   f_pktTotalCount decimal(8),
						   f_octetTotalCount decimal(10),
						   f_min_ps decimal(5),
						   f_max_ps decimal(5),
						   f_avg_ps decimal(5),
						   f_std_dev_ps decimal(4),
						   f_min_piat decimal(9), 
						   f_max_piat decimal(9), 
						   f_avg_piat decimal(9), 
						   f_std_dev_piat decimal(8),
						   PRIMARY KEY (Flow_index),
						   FOREIGN KEY (Flow_index) REFERENCES Flows(Flow_index)
						   );

INSERT INTO ForwardFlows
SELECT Flow_index, f_pktTotalCount, f_octetTotalCount, f_min_ps, f_max_ps, f_avg_ps, f_std_dev_ps,
													   f_min_piat, f_max_piat, f_avg_piat, f_std_dev_piat
FROM aggregate_dataset;

------------------------------------------------------------- BackwardFlows -----------------------------------------------------------------------
DROP TABLE IF EXISTS BackwardFlows;

create table BackwardFlows(Flow_index int,
						   b_pktTotalCount decimal(8),
						   b_octetTotalCount decimal(10),
						   b_min_ps decimal(5),
						   b_max_ps decimal(5),
						   b_avg_ps decimal(5),
						   b_std_dev_ps decimal(4),
						   b_min_piat decimal(9), 
						   b_max_piat decimal(9), 
						   b_avg_piat decimal(9), 
						   b_std_dev_piat decimal(8),
						   PRIMARY KEY (Flow_index),
						   FOREIGN KEY (Flow_index) REFERENCES Flows(Flow_index)
						   );

INSERT INTO BackwardFlows
SELECT Flow_index, b_pktTotalCount, b_octetTotalCount, b_min_ps, b_max_ps, b_avg_ps, b_std_dev_ps,
													   b_min_piat, b_max_piat, b_avg_piat, b_std_dev_piat
FROM aggregate_dataset;

------------------------------------------------------------- Packets -----------------------------------------------------------------------
DROP TABLE IF EXISTS Packets;

CREATE TABLE Packets(Flow_index int,
					 min_ps decimal(6),
					 max_ps decimal(6),
					 avg_ps decimal(6),
					 std_dev_ps decimal(4),
					 min_piat decimal(9),
					 max_piat decimal(9),
					 avg_piat decimal(9),
					 std_dev_piat decimal(8),
					 PRIMARY KEY (Flow_index),
					 FOREIGN KEY (Flow_index) REFERENCES Flows(Flow_index)
);

INSERT INTO Packets
SELECT Flow_index, min_ps, max_ps, avg_ps, std_dev_ps, min_piat, max_piat, avg_piat, std_dev_piat
FROM aggregate_dataset;


------------------------------------------------------------- Flags -----------------------------------------------------------------------
DROP TABLE IF EXISTS Flags;

create table Flags(Flow_index int,
					FIN_Flag_Count decimal(1), 
					SYN_Flag_Count decimal(1), 
					RST_Flag_Count decimal(1), 
					PSH_Flag_Count decimal(1), 
					ACK_Flag_Count decimal(1),
					URG_Flag_Count decimal(1), 
					CWE_Flag_Count decimal(1), 
					ECE_Flag_Count decimal(1),
					PRIMARY KEY (Flow_index),
					FOREIGN KEY (Flow_index) REFERENCES Flows(Flow_index)
					);

INSERT INTO Flags
SELECT Flow_index, FIN_Flag_Count, SYN_Flag_Count, RST_Flag_Count, PSH_Flag_Count, ACK_Flag_Count,URG_Flag_Count, CWE_Flag_Count, ECE_Flag_Count
FROM aggregate_dataset 
WHERE origin = '1'; -- only load dataset 1

------------------------------------------------------------- Protocol1 -----------------------------------------------------------------------
DROP TABLE IF EXISTS Protocol1;

CREATE TABLE Protocol1(Flow_index int,
					 proto decimal(2),
					 L7Protocol decimal(3),
	 				 ProtocolName varchar(20),
					 PRIMARY KEY (Flow_index),
					 FOREIGN KEY (Flow_index) REFERENCES Flows(Flow_index)
);

INSERT INTO Protocol1
SELECT Flow_index, proto, L7Protocol, ProtocolName
FROM aggregate_dataset
WHERE origin = '1';


------------------------------------------------------------- Protocol2 -----------------------------------------------------------------------
DROP TABLE IF EXISTS Protocol2;

create table Protocol2(Flow_index int,
					proto decimal(2),
					category varchar(7),
				    application_protocol varchar(6),
	 				web_service varchar(20),
					PRIMARY KEY (Flow_index),
					FOREIGN KEY (Flow_index) REFERENCES Flows(Flow_index)
					);

INSERT INTO Protocol2
SELECT Flow_index, proto, category, application_protocol, web_service
FROM aggregate_dataset 
WHERE origin = '2'; 


------------------------------------------------------------- USERS -----------------------------------------------------------------------
DROP TABLE IF EXISTS userinfo;

CREATE TABLE userinfo (userID varchar(100),
					passwd char(64),
					isadmin decimal(1),
					primary key (userID)
					);
--Hardcode two users one with admin rights and one without
--Password123
--Password456
INSERT INTO userinfo (userID, passwd, isadmin)  
VALUES ('admin','ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f',1), 
('user', 'c6ba91b90d922e159893f46c387e5dc1b3dc5c101a5a4522f03b987177a24a91', 0); 


------------------------------------------------------------- ANNOTATIONS -----------------------------------------------------------------------
DROP TABLE IF EXISTS annotations;

CREATE TABLE annotations (Flow_index INT,
					userID CHAR(64),
					comments VARCHAR(1000)
					); 
-- Figure out which PKs and FKs to use here, also add this to ER 

------------------------------------------------------------- private_ips VIEW -----------------------------------------------------------------------
CREATE VIEW private_ips AS 
SELECT srcIP, srcPort, dstIP, dstPort 
FROM Links 
WHERE
((CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 10) OR
(CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 192 AND CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int) = 168) OR
(CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 172 AND 16 < CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int) < 31))
GROUP BY srcIP, srcPort, dstIP, dstPort;

-------------------------------------------------------------  public_ips VIEW  -----------------------------------------------------------------------
CREATE VIEW public_ips AS 
SELECT srcIP, srcPort, dstIP, dstPort 
FROM Links 
WHERE
NOT ((CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 10) OR
(CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 192 AND CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int) = 168) OR
(CAST(SUBSTRING_INDEX(srcIP, ".", -4) AS int) = 172 AND 16 < CAST(SUBSTRING_INDEX(srcIP, ".", -3) AS int) < 31))
GROUP BY srcIP, srcPort, dstIP, dstPort;
