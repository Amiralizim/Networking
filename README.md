# Networking_dataset
ECE356 project
ER relationship diagram: draw.io
# Datasets:
https://www.kaggle.com/jsrojas/ip-network-traffic-flows-labeled-with-87-apps
https://www.kaggle.com/jsrojas/labeled-network-traffic-flows-114-applications

# Notes:

## Flows Table

This is in reference to Flows table located in the first dataset (87-attributes)

__Purpose:__
This table should allow for us to uniquely indentify flows , Hence everytime we need to use a unique flow we will start by querying this table and get whatever information is required

__Notes:__
* The primary key can't just be the flowId and the timestamp, first 2 values are duplicates in that case
* Use flowId, timestamp and flow.duration as the primary key together
* Make sure we actually need this key to be primary?? makes sense for us to uniquely identify flows but we should check with our client requirements
* Load this table inside of SQL with the PK as defined in second point and check if we are getting primary key warnings
* The fields in this table ending with a .s means they are defined per second as per kaggle
* Anything that needs to be referenced as a FK to here needs all three fields that are in the PK


## Forward Flows Table

__Purpose:__ This table should allow us to get all the information regarding flows in the forward direction

__Notes:__
* No primary key for the table as it stands
* Getting rid of column Fwd.Header.Length.1 as it is same information as Fwd.Header.Length
* Subflow columns seem to be redunant. For example Total.Fwd.Packets has same information as Subflow.Fwd.Packets
* This table looks like it has a lot of columns which are not going to be used, Get rid of those
* See if we can combine the forward tables of both the datasets together


## Backward Flows Table

__Purpose:__ Same as forwards but in other direction

__Notes:__
* Basically the same things as forward
* There is only difference in two column compared to fwd_counterpart. ie there is no such column called act_data_pkt_bwd but there is act_data_pkt_fwd similarly for min_seg_size_forward
* We should name the columns in fwd and bwd tables the exact same for easy querying. Remove all the fwd. bwd. etc etc
* we can relate this directly to the fwd table as every fwd flow should have backward counterpart

## Flags

__Purpose:__ Tells us how many times a certain type of flag was sent across the whole flow 

__Notes:__ N/A Seems straightforward

## Packets

__Purpose:__ Packet stats for the overall flow (forward and backward)

__Notes:__
* Technically this table shouldnt be required as we can extract mins and maxs from the fwd and bwd and compare them to get an overall min and max
* Above does not hold true though??? When compared values from fwd.min bwd.min and packets.min, it does not add up , maybe I am not understanding what these fields mean correctly or the data is BS


## Active and Idle

__Purpose:__ Stats for idle and active time in a flow

__Notes:__
* Took the active and idle tables and combined them together , pretty sure its safe to do so. They are both related too so it makes sense

## Protocol

__Purpose:__ Find what protocol is being used

__Notes:__ N/A

