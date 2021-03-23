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
	  Protocol varchar(1),                             --can 17 fit in varchar(1)?
	  Timestamp SmallDateTime, -- YYYY-MM-DD hh:mm:ss
	  Flow.Duration decimal(9), -- maximum 120000000
	  Total.Fwd.Packets decimal(6), -- maximum 453k 
	  Total.Backward.Packets decimal(6), -- maximum 542k
	  Total.Length.of.Fwd.Packets decimal(9), -- maximum 678023588
	  Total.Length.of.Bwd.Packets decimal(10), -- maximum 1,345,795,830
	  Fwd.Packet.Length.Max decimal(5), -- 32.8k
	  Fwd.Packet.Length.Min decimal(5), -- 16.1k
	  Fwd.Packet.Length.Mean decimal(5), -- 16.1k 
	  Fwd.Packet.Length.Std decimal(4), -- 6.23k
	  Bwd.Packet.Length.Max decimal(5), -- 37.6k
	  Bwd.Packet.Length.Min decimal(5), -- 13k
	  Bwd.Packet.Length.Mean decimal(5), -- 13k
	  Bwd.Packet.Length.Std decimal(4), -- 8.43k
	  Flow.Bytes.s decimal(11), -- 14.4b
	  Flow.Packets.s decimal(7), -- 6m
	  Flow.IAT.Mean decimal(9), -- 120m
	  Flow.IAT.Std decimal(8), -- 84.9m
	  Flow.IAT.Max decimal(9), -- 120m
	  Flow.IAT.Min decimal(9), -- 120m
	  Fwd.IAT.Total decimal(9), -- 120m
	  Fwd.IAT.Mean decimal(9), -- 120m
	  Fwd.IAT.Std decimal(8), -- 84.9m
	  Fwd.IAT.Max decimal(9), --120m
	  Fwd.IAT.Min decimal(9), -- 120m
	  Bwd.IAT.Total decimal(9), -- 120m
	  Bwd.IAT.Mean decimal(9), -- 120m
	  Bwd.IAT.Std decimal(8), -- 84.9m
	  Bwd.IAT.Max decimal(9), -- 120m
	  Bwd.IAT.Min decimal(9), -- 120m
	  Fwd.PSH.Flags decimal(1), -- 1
	  Bwd.PSH.Flags decimal(1), -- 0
	  Fwd.URG.Flags decimal(1), -- 0
	  Bwd.URG.Flags decimal(1), -- 0
	  Fwd.Header.Length decimal(8), -- 15.4m
	  Bwd.Header.Length decimal(8), -- 12.8m
	  Fwd.Packets.s decimal(7), -- 6m
	  Bwd.Packets.s decimal(7), -- 5m
	  Min.Packet.Length decimal(4), -- 7063
	  Max.Packet.Length decimal(5), -- 37.6k
	  Packet.Length.Mean decimal(5), -- 10.7k
	  Packet.Length.Std decimal(4), -- 9.27k
	  Packet.Length.Variance decimal(8), -- 85.9m
	  FIN.Flag.Count decimal(1), -- 1
	  SYN.Flag.Count decimal(1), -- 1
	  RST.Flag.Count decimal(1), -- 1
	  PSH.Flag.Count decimal(1), -- 1
	  ACK.Flag.Count decimal(1), -- 1
	  URG.Flag.Count decimal(1), -- 1
	  CWE.Flag.Count decimal(1), -- 1
	  ECE.Flag.Count decimal(1), -- 1
	  Down.Up.Ratio decimal(3), -- 293
	  Average.Packet.Size decimal(5), -- 16.1k
	  Avg.Fwd.Segment.Size decimal(5), -- 16.1k
	  Avg.Bwd.Segment.Size decimal(5), -- 13k
	  Fwd.Header.Length.1 decimal(8), -- 15.4m
	  Fwd.Avg.Bytes.Bulk decimal(1), -- 0
	  Fwd.Avg.Packets.Bulk decimal(1), -- 0
	  Fwd.Avg.Bulk.Rate decimal(1), -- 0
	  Bwd.Avg.Bytes.Bulk decimal(1), -- 0
	  Bwd.Avg.Packets.Bulk decimal(1), -- 0
	  Bwd.Avg.Bulk.Rate decimal(1), -- 0
	  Subflow.Fwd.Packets decimal(6), -- 453k
	  Subflow.Fwd.Bytes decimal(9), -- 678m
	  Subflow.Bwd.Packets decimal(6), -- 542k
	  Subflow.Bwd.Bytes decimal(10), -- 1.35b
	  Init_Win_bytes_forward decimal(5), -- 65.5k
	  Init_Win_bytes_backward decimal(5), -- 65.5k
	  act_data_pkt_fwd decimal(6), -- 329k
	  min_seg_size_forward decimal(3),-- 523
	  Label varchar(6), -- BENIGH OR MALIGN
	  L7Protocol decimal(3), -- 222
	  ProtocolName varchar(15) -- WINDOWS_UPDATE
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