------------------------------------------------

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
	  Label varchar(6),
	  L7Protocol decimal(3),
	  ProtocolName varchar(15)
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

ALTER TABLE Dataset1	
	ADD Flow_index varchar(100);

UPDATE Dataset1 d1
	SET d1.Flow_index = CONCAT(d1.Link_ID, '-', d1.Flow_Start, '-',  d1.Flow_Duration, '-', d1.Protocol);


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

ALTER TABLE Dataset2	
	ADD Flow_index varchar(100);

UPDATE Dataset2 d2
	SET d2.Flow_index = CONCAT(d2.Link_ID, '-', d2.Flow_Start, '-',  d2.Flow_Duration, '-', d2.proto);

-- Links table -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Links' as '';

create table Links (Link_ID varchar(60),
	    			srcIP varchar(15),
 				    srcPort varchar(5),
 					dstIP varchar(15),
 					dstPort varchar(15)
);

create view temp as 
	(SELECT Link_ID, Source_IP AS srcIP, Source_Port AS srcPort, Destination_IP AS dstIP, Destination_Port AS dstPort
	FROM  Dataset1
	GROUP BY Link_ID, Source_IP, Source_Port, Destination_IP, Destination_Port)
	union 
	(SELECT Link_ID, src_ip AS srcIP, src_port AS srcPort, dst_ip AS dstIP, dst_port AS dstPort
	FROM  Dataset2
	GROUP BY Link_ID, src_ip, src_port, dst_ip, dst_port);

insert into Links
	SELECT Link_ID, srcIP, srcPort, dstIP, dstPort
	FROM  temp;

drop view temp;

-- get rid of duplicates

alter table Links
ADD CONSTRAINT Pk_Link_ID primary key (Link_ID);

-- Flows table -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Flows' as '';

create table Flows (Flow_index char(100),
					Link_ID varchar(60),
					Flow_Start varchar(60),
					Flow_Duration decimal(10),
					Protocol decimal(2),
					primary key (Flow_index)
					);

create view temp as 
	(SELECT DISTINCT Flow_index, Link_ID, Flow_Start , Flow_Duration, Protocol
	FROM  Dataset1)
	union 
	(SELECT DISTINCT Flow_index, Link_ID, Flow_Start , Flow_Duration, proto AS Protocol
	FROM  Dataset2);

insert into Flows
	SELECT Flow_index, Link_ID, Flow_Start, Flow_Duration, Protocol
	FROM  temp;

drop view temp;

alter table Flows
ADD CONSTRAINT fk_Link_ID foreign key (Link_ID) references Links(Link_ID);

-- Forward Flows table -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create ForwardFlows' as '';
-- using the naming convention of dataset 2 as they are easier to understand

create table ForwardFlows(Flow_index char(100),
						   f_pktTotalCount decimal(8),
						   f_octetTotalCount decimal(10),
						   f_min_ps decimal(5),
						   f_max_ps decimal(5),
						   f_avg_ps decimal(5),
						   f_std_dev_ps decimal(4),
						   f_min_piat decimal(9), 
						   f_max_piat decimal(9), 
						   f_avg_piat decimal(9), 
						   f_std_dev_piat decimal(8)
						   );

create view temp as 
	(SELECT Flow_index, 
			Total_Fwd_Packets AS f_pktTotalCount, 
			Total_Length_of_Fwd_Packets AS f_octetTotalCount, 
			Fwd_Packet_Length_Min AS f_min_ps, 
			Fwd_Packet_Length_Max AS f_max_ps,
			Fwd_Packet_Length_Mean AS f_avg_ps,
			Fwd_Packet_Length_Std AS f_std_dev_ps,
			Fwd_IAT_Min AS f_min_piat,
			Fwd_IAT_Max AS f_max_piat,
			Fwd_IAT_Mean AS f_avg_piat,
			Fwd_IAT_Std AS f_std_dev_piat
	FROM  Dataset1)
	union 
	(SELECT Flow_index, 
			f_pktTotalCount, 
			f_octetTotalCount, 
			f_min_ps, 
			f_max_ps,
			f_avg_ps,
			f_std_dev_ps,
			f_min_piat,
			f_max_piat,
			f_avg_piat,
			f_std_dev_piat
	FROM  Dataset2);

-- we use max here because there are bad data in the dataset, sometimes for duplicated individual flows the inccorect value of 0 is shown for the fields
insert into ForwardFlows
	SELECT Flow_index, MAX(f_pktTotalCount), MAX(f_octetTotalCount), MAX(f_min_ps), MAX(f_max_ps), MAX(f_avg_ps), MAX(f_std_dev_ps), MAX(f_min_piat), MAX(f_max_piat), MAX(f_avg_piat), MAX(f_std_dev_piat)
	FROM  temp
	GROUP BY Flow_index;

drop view temp;

alter table ForwardFlows
ADD CONSTRAINT Pk_Flow_ID primary key (Flow_index);

alter table ForwardFlows	
ADD CONSTRAINT fk_Flow_index foreign key (Flow_index) references Flows(Flow_index);			

-- Backwards Flows table -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create BackwardFlows' as '';

create table BackwardFlows(Flow_index char(100),
						   b_pktTotalCount decimal(8),
						   b_octetTotalCount decimal(10),
						   b_min_ps decimal(5),
						   b_max_ps decimal(5),
						   b_avg_ps decimal(5),
						   b_std_dev_ps decimal(4),
						   b_min_piat decimal(9), 
						   b_max_piat decimal(9), 
						   b_avg_piat decimal(9), 
						   b_std_dev_piat decimal(8)
						   );

create view temp as 
	(SELECT Flow_index, 
			Total_Backward_Packets AS b_pktTotalCount, 
			Total_Length_of_Bwd_Packets AS b_octetTotalCount, 
			Bwd_Packet_Length_Min AS b_min_ps, 
			Bwd_Packet_Length_Max AS b_max_ps,
			Bwd_Packet_Length_Mean AS b_avg_ps,
			Bwd_Packet_Length_Std AS b_std_dev_ps,
			Bwd_IAT_Min AS b_min_piat,
			Bwd_IAT_Max AS b_max_piat,
			Bwd_IAT_Mean AS b_avg_piat,
			Bwd_IAT_Std AS b_std_dev_piat
	FROM  Dataset1)
	union 
	(SELECT Flow_index, 
			b_pktTotalCount, 
			b_octetTotalCount, 
			b_min_ps, 
			b_max_ps,
			b_avg_ps,
			b_std_dev_ps,
			b_min_piat,
			b_max_piat,
			b_avg_piat,
			b_std_dev_piat
	FROM  Dataset2);

insert into BackwardFlows
	SELECT Flow_index, MAX(b_pktTotalCount), MAX(b_octetTotalCount), MAX(b_min_ps), MAX(b_max_ps), MAX(b_avg_ps), MAX(b_std_dev_ps), MAX(b_min_piat), MAX(b_max_piat), MAX(b_avg_piat), MAX(b_std_dev_piat)
	FROM  temp
	GROUP BY Flow_index;

drop view temp;

alter table BackwardFlows
ADD CONSTRAINT Pk_B_Flow_ID primary key (Flow_index);

alter table BackwardFlows	
ADD CONSTRAINT fk_B_Flow_index foreign key (Flow_index) references Flows(Flow_index);		


-- Packets Flows table -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Packets' as '';

create table Packets(Flow_index char(100),
					 Min_Packet_Length decimal(4),
					 Max_Packet_Length decimal(5), 
					 Packet_Length_Mean decimal(5),
					 Packet_Length_Std decimal(4), 
					 Flow_IAT_Mean decimal(9), 
					 Flow_IAT_Std decimal(8), 
					 Flow_IAT_Max decimal(9),
					 Flow_IAT_Min decimal(9));

create view temp as 
	(SELECT Flow_index, 
			Min_Packet_Length,
			Max_Packet_Length,
			Packet_Length_Mean,
			Packet_Length_Std,
			Flow_IAT_Mean,
			Flow_IAT_Std,
			Flow_IAT_Max,
			Flow_IAT_Min
	FROM  Dataset1)
	union 
	(SELECT Flow_index, 
			min_ps AS Min_Packet_Length, 
			max_ps AS Max_Packet_Length, 
			avg_ps AS Packet_Length_Mean, 
			std_dev_ps AS Packet_Length_Std,
			avg_piat AS Flow_IAT_Mean,
			std_dev_piat AS Flow_IAT_Std,
			max_piat AS Flow_IAT_Max,
			max_piat AS Flow_IAT_Min
	FROM  Dataset2);

insert into Packets
SELECT Flow_index,
		MAX(Min_Packet_Length),
		MAX(Max_Packet_Length), 
		MAX(Packet_Length_Mean),
		MAX(Packet_Length_Std), 
		MAX(Flow_IAT_Mean), 
		MAX(Flow_IAT_Std), 
		MAX(Flow_IAT_Max),
		MAX(Flow_IAT_Min)
	FROM  temp
	GROUP BY Flow_index;

drop view temp;

alter table Packets
ADD CONSTRAINT Pk_P_Flow_ID primary key (Flow_index);

alter table Packets	
ADD CONSTRAINT fk_P_Flow_index foreign key (Flow_index) references Flows(Flow_index);	

-- Flags table -------------------------------------------------------------------
select '----------------------------------------------------------------' as '';
select 'Create Flags' as '';

create table Flags(Flow_index char(100),
					FIN_Flag_Count decimal(1), 
					SYN_Flag_Count decimal(1), 
					RST_Flag_Count decimal(1), 
					PSH_Flag_Count decimal(1), 
					ACK_Flag_Count decimal(1),
					URG_Flag_Count decimal(1), 
					CWE_Flag_Count decimal(1), 
					ECE_Flag_Count decimal(1));

insert into Flags
SELECT Flow_index,
	MAX(FIN_Flag_Count), 
	MAX(SYN_Flag_Count), 
	MAX(RST_Flag_Count), 
	MAX(PSH_Flag_Count), 
	MAX(ACK_Flag_Count),
	MAX(URG_Flag_Count), 
	MAX(CWE_Flag_Count), 
	MAX(ECE_Flag_Count)
from Dataset1
GROUP BY Flow_index;

alter table Flags
ADD CONSTRAINT Pk_F_Flow_ID primary key (Flow_index);