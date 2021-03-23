-- ------------------------------------------------
--
-- Networking Database

-- ip-network-traffic-flows-labeled-with-87-apps -------------------------------------------------------------------
create table dataset1 (
	  Flow.ID varchar(40), -- SourceIP-DestinationIP-SourcePort-DestinationPort 12*2+2+5*2+2+1=
	  Source.IP varchar(15),
	  Source.Port varchar(5), 
	  Destination.IP varchar(15), 
	  Destination.Port varchar(5), 
	  Protocol varchar(1), 
	  Timestamp SmallDateTime, -- YYYY-MM-DD hh:mm:ss
	  Flow.Duration decimal(100000000), -- maximum 120000000
	  Total.Fwd.Packets decimal(1000000), -- maximum 453k 
	  Total.Backward.Packets decimal(1000000), -- maximum 542k
	  Total.Length.of.Fwd.Packets decimal(1000000000), -- maximum 678023588
	  Total.Length.of.Bwd.Packets decimal(1000000000), -- maximum 1,345,795,830
	  Fwd.Packet.Length.Max, 
	  Fwd.Packet.Length.Min, 
	  Fwd.Packet.Length.Mean, 
	  Fwd.Packet.Length.Std, 
	  Bwd.Packet.Length.Max, 
	  Bwd.Packet.Length.Min, 
	  Bwd.Packet.Length.Mean, 
	  Bwd.Packet.Length.Std, 
	  Flow.Bytes.s, 
	  Flow.Packets.s, 
	  Flow.IAT.Mean, 
	  Flow.IAT.Std, 
	  Flow.IAT.Max, 
	  Flow.IAT.Min, 
	  Fwd.IAT.Total, 
	  Fwd.IAT.Mean, 
	  Fwd.IAT.Std, 
	  Fwd.IAT.Max, 
	  Fwd.IAT.Min, 
	  Bwd.IAT.Total, 
	  Bwd.IAT.Mean, 
	  Bwd.IAT.Std, 
	  Bwd.IAT.Max, 
	  Bwd.IAT.Min, 
	  Fwd.PSH.Flags, 
	  Bwd.PSH.Flags, 
	  Fwd.URG.Flags, 
	  Bwd.URG.Flags, 
	  Fwd.Header.Length, 
	  Bwd.Header.Length, 
	  Fwd.Packets.s, 
	  Bwd.Packets.s, 
	  Min.Packet.Length, 
	  Max.Packet.Length, 
	  Packet.Length.Mean, 
	  Packet.Length.Std, 
	  Packet.Length.Variance, 
	  FIN.Flag.Count, 
	  SYN.Flag.Count, 
	  RST.Flag.Count, 
	  PSH.Flag.Count, 
	  ACK.Flag.Count, 
	  URG.Flag.Count, 
	  CWE.Flag.Count, 
	  ECE.Flag.Count, 
	  Down.Up.Ratio, 
	  Average.Packet.Size, 
	  Avg.Fwd.Segment.Size, 
	  Avg.Bwd.Segment.Size, 
	  Fwd.Header.Length.1, 
	  Fwd.Avg.Bytes.Bulk, 
	  Fwd.Avg.Packets.Bulk, 
	  Fwd.Avg.Bulk.Rate, 
	  Bwd.Avg.Bytes.Bulk, 
	  Bwd.Avg.Packets.Bulk, 
	  Bwd.Avg.Bulk.Rate, 
	  Subflow.Fwd.Packets, 
	  Subflow.Fwd.Bytes, 
	  Subflow.Bwd.Packets, 
	  Subflow.Bwd.Bytes, 
	  Init_Win_bytes_forward, 
	  Init_Win_bytes_backward, 
	  act_data_pkt_fwd, 
	  min_seg_size_forward,
	  Label, 
	  L7Protocol, 
	  ProtocolName
)
load data infile '/var/lib/mysql-files/21-Network-Traffic/ip-network-traffic-flows-labeled-with-87-apps.csv' ignore into table dataset1
		fields terminated by ','
		enclosed by '"'
		lines terminated by '\r\n'
		ignore 1 lines;


-- Unicauca-dataset-April-June-2019-Network-flows  -------------------------------------------------------------------
create table dataset1 (
	flow_key,
	 src_ip_numeric,
	 src_ip,
	 src_port,
	 dst_i,
	 dst_port,
	 proto,
	 pktTotalCount,
	 octetTotalCount,
	 min_ps,
	 max_ps,
	 avg_ps,
	 std_dev_ps,
	 flowStart,
	 flowEnd,
	 flowDuration,
	 min_piat,
	 max_piat,
	 avg_piat,
	 std_dev_piat,
	 f_pktTotalCount,
	 f_octetTotalCount,
	 f_min_ps,
	 f_max_ps,
	 f_avg_ps,
	 f_std_dev_ps,
	 f_flowStart,
	 f_flowEnd,
	 f_flowDuration,
	 f_min_piat,
	 f_max_piat,
	 f_avg_piat,
	 f_std_dev_piat,
	 b_pktTotalCount,
	 b_octetTotalCount,
	 b_min_ps, 
	 b_max_ps, 
	 b_avg_ps, 
	 b_std_dev_ps, 
	 b_flowStart, 
	 b_flowEnd, 
	 b_flowDuration, 
	 b_min_piat, 
	 b_max_piat, 
	 b_avg_piat, 
	 b_std_dev_piat, 
	 flowEndReason, 
	 category, 
	 application_protocol, 
	 web_service
)
load data infile '/var/lib/mysql-files/21-Network-Traffic/Unicauca-dataset-April-June-2019-Network-flows.csv' ignore into table dataset2
		fields terminated by ','
		enclosed by '"'
		lines terminated by '\r\n'
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