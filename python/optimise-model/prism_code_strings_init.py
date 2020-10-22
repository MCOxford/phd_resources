honest_init = """
init

c1=0&c2=0&c3=0&c4=0&c5=0 &
c1s=0&c2s=0&c3s=0&c4s=0&c5s=0 &
c1_skip=false&c2_skip=false&c3_skip=false&c4_skip=false&c5_skip=false &
((c1_sth=true & c2_sth=false & c3_sth=false & c4_sth=false & c5_sth=false) |
 (c1_sth=false & c2_sth=true & c3_sth=false & c4_sth=false & c5_sth=false) |
 (c1_sth=false & c2_sth=false & c3_sth=true & c4_sth=false & c5_sth=false) |
 (c1_sth=false & c2_sth=false & c3_sth=false & c4_sth=true & c5_sth=false) |
 (c1_sth=false & c2_sth=false & c3_sth=false & c4_sth=false & c5_sth=true)) &
((s1_sth=true & s2_sth=false & s3_sth=false & s4_sth=false & s5_sth=false) |
 (s1_sth=false & s2_sth=true & s3_sth=false & s4_sth=false & s5_sth=false) |
 (s1_sth=false & s2_sth=false & s3_sth=true & s4_sth=false & s5_sth=false) |
 (s1_sth=false & s2_sth=false & s3_sth=false & s4_sth=true & s5_sth=false) |
 (s1_sth=false & s2_sth=false & s3_sth=false & s4_sth=false & s5_sth=true))

endinit
"""

split_init = """
init

c1=0&c2=0&c3=0&c4=0&c5=0 &
c1s=0&c2s=0&c3s=0&c4s=0&c5s=0 &
c1_skip=false&c2_skip=false&c3_skip=false&c4_skip=false&c5_skip=false &
c1d=false&c2d=false&c3d=false&c4d=false&c5d=false &
((c1_sth=0|c1_sth=2) & (c2_sth=0|c2_sth=2) & (c3_sth=0|c3_sth=2) & (c4_sth=0|c4_sth=2) & (c5_sth=0|c5_sth=2)) &
c1_sth+c2_sth+c3_sth+c4_sth+c5_sth=2 &
s1_sth+s2_sth+s3_sth+s4_sth+s5_sth=1 &
s1d=false&s2d=false&s3d=false&s4d=false&s5d=false

endinit
"""

honest_original_client_init = """
module Client1 

	//global state.
	c1 : [0..4];
	//connectivity state.
	c1s : [0..5];
	//current STH data stored by the client. 'True' means the client has the latest STH.
	c1_sth : bool;
	//skip the round?
	c1_skip : bool;

	//client decides randomly to participate in the round.
	[connect] c1=0 -> g1 : (c1'=1) + 1-g1 : (c1'=1) & (c1_skip'=true);
	//client randomly chooses a server if participating in the round.
	[choose] c1_skip=false & c1=1 -> p_1_1 : (c1'=2)&(c1s'=1) + p_1_2 : (c1'=2)&(c1s'=2) + p_1_3 : (c1'=2)&(c1s'=3) + 
					 p_1_4 : (c1'=2)&(c1s'=4) + p_1_5 : (c1'=2)&(c1s'=5);
	[choose] c1_skip=true & c1=1 -> (c1'=2);
	//client updates itself using data retrieved from server so long as c1_skip=false or c1_sth=true.
	[update] c1_skip=false & c1=2 & connected_server_has_sth  -> (c1'=3) & (c1_sth'=true);
	[update] c1=2 & ((c1_skip=false & !connected_server_has_sth) | c1_skip=true) -> (c1'=3);
	//round complete - reset if there is a client who is not yet updated. Otherwise, stop.
	[round_complete] c1=3 & !clients_all_updated -> (c1'=0) & (c1s'=0) & (c1_skip'=false);
	[round_complete] c1=3 & clients_all_updated -> (c1'=4);
	//self-looping state - go here when every client is updated.
	[END] c1=4 -> true;

endmodule

formula connected_server_has_sth = ((c1s=1 & s1_sth) | (c1s=2 & s2_sth) | (c1s=3 & s3_sth) | (c1s=4 & s4_sth) | (c1s=5 & s5_sth));
formula clients_all_updated = c1_sth&c2_sth&c3_sth&c4_sth&c5_sth;
label "clients_all_updated" = c1_sth&c2_sth&c3_sth&c4_sth&c5_sth;

module Client2=Client1[p_1_1=p_2_1,p_1_2=p_2_2,p_1_3=p_2_3,p_1_4=p_2_4,p_1_5=p_2_5,
g1=g2,c1=c2,c1s=c2s, c1_sth=c2_sth, c2_sth=c1_sth, c1_skip=c2_skip, c1_sth_init = c2_sth_init] endmodule

module Client3=Client1[p_1_1=p_3_1,p_1_2=p_3_2,p_1_3=p_3_3,p_1_4=p_3_4,p_1_5=p_3_5,
g1=g3,c1=c3,c1s=c3s, c1_sth=c3_sth, c3_sth=c1_sth, c1_skip=c3_skip, c1_sth_init = c3_sth_init] endmodule

module Client4=Client1[p_1_1=p_4_1,p_1_2=p_4_2,p_1_3=p_4_3,p_1_4=p_4_4,p_1_5=p_4_5,
g1=g4,c1=c4,c1s=c4s, c1_sth=c4_sth, c4_sth=c1_sth, c1_skip=c4_skip, c1_sth_init = c4_sth_init] endmodule

module Client5=Client1[p_1_1=p_5_1,p_1_2=p_5_2,p_1_3=p_5_3,p_1_4=p_5_4,p_1_5=p_5_5,
g1=g5,c1=c5,c1s=c5s, c1_sth=c5_sth, c5_sth=c1_sth, c1_skip=c5_skip, c1_sth_init = c5_sth_init] endmodule
"""

honest_original_server_init = """
//needed for module relabelling
const int S1 = 1;
const int S2 = 2;
const int S3 = 3;
const int S4 = 4;
const int S5 = 5;

module Server1

	//does the server have the latest STH?
	s1_sth : bool;

	//update if a connected client has the latest STH
	[update] !s1_sth & connected_client_has_sth -> (s1_sth'=true);
	[update] s1_sth | (!s1_sth & !connected_client_has_sth) -> true;
	//server-to-server gossip - this is done during the 'connect' phase to make data spreading more effective
	//[connect] !s1_sth -> get_data : (s1_sth'=true) + 1-get_data : true;
	//[connect] s1_sth -> true;
	//end when every client is updated
	[END] true -> true;

endmodule

formula connected_client_has_sth = (c1s=S1 & c1_sth) | (c2s=S1 & c2_sth) | (c3s=S1 & c3_sth) | (c4s=S1 & c4_sth) | (c5s=S1 & c5_sth);

module Server2=Server1[s1_sth=s2_sth, s2_sth=s1_sth, S1=S2, s1_init=s2_init] endmodule
module Server3=Server1[s1_sth=s3_sth, s3_sth=s1_sth, S1=S3, s1_init=s3_init] endmodule
module Server4=Server1[s1_sth=s4_sth, s4_sth=s1_sth, S1=S4, s1_init=s4_init] endmodule
module Server5=Server1[s1_sth=s5_sth, s5_sth=s1_sth, S1=S5, s1_init=s5_init] endmodule
"""

honest_extended_server_init = """
//needed for module relabelling
const int S1 = 1;
const int S2 = 2;
const int S3 = 3;
const int S4 = 4;
const int S5 = 5;

module Server1

	//does the server have the latest STH?
	s1_sth : bool;

	//update if a connected client has the latest STH
	[update] !s1_sth & connected_client_has_sth -> (s1_sth'=true);
	[update] s1_sth | (!s1_sth & !connected_client_has_sth) -> true;
	//server-to-server gossip - this is done during the 'connect' phase to make data spreading more effective
	[connect] !s1_sth -> get_data : (s1_sth'=true) + 1-get_data : true;
	[connect] s1_sth -> true;
	//end when every client is updated
	[END] true -> true;

endmodule

formula connected_client_has_sth = (c1s=S1 & c1_sth) | (c2s=S1 & c2_sth) | (c3s=S1 & c3_sth) | (c4s=S1 & c4_sth) | (c5s=S1 & c5_sth);

module Server2=Server1[s1_sth=s2_sth, s2_sth=s1_sth, S1=S2, s1_init=s2_init] endmodule
module Server3=Server1[s1_sth=s3_sth, s3_sth=s1_sth, S1=S3, s1_init=s3_init] endmodule
module Server4=Server1[s1_sth=s4_sth, s4_sth=s1_sth, S1=S4, s1_init=s4_init] endmodule
module Server5=Server1[s1_sth=s5_sth, s5_sth=s1_sth, S1=S5, s1_init=s5_init] endmodule
"""

splitworld_original_client_init = """
module Client1 

	//global state
	c1 : [0..4];
	//connectivity state
	c1s : [0..5];
	//Record which root hash this node currently has.
	c1_sth : [0..2];
	//detection state
	c1d : bool;
	//skip the round?
	c1_skip : bool;

	//client decides randomly to participate in the round
	[connect] c1=0 -> g1 : (c1'=1) + 1-g1 : (c1'=1) & (c1_skip'=true);
	//client randomly chooses a server if participating in the round
	[choose] !c1_skip & c1=1 -> p_1_1 : (c1'=2)&(c1s'=1) + p_1_2 : (c1'=2)&(c1s'=2) + p_1_3 : (c1'=2)&(c1s'=3) + 
			            p_1_4 : (c1'=2)&(c1s'=4) + p_1_5 : (c1'=2)&(c1s'=5);
	[choose] c1_skip & c1=1 -> (c1'=2);
	//client updates itself using data retrieved from server, checking that no issues are present (so long as c1_skip=false).
	[update] !c1_skip & c1=2 & s_data_ok -> (c1_sth'=c_update) & (c1'=3);
	[update] !c1_skip & c1=2 & !s_data_ok -> (c1d'=true) & (c1'=3);
 	[update] c1_skip & c1=2 -> (c1'=3);
	//round complete - start the next round if there no client has found an issue with the log. Otherwise, go to self-looping state and stop.
	[round_complete] c1=3 & !detect -> (c1'=0) & (c1s'=0) & (c1_skip'=false);
	[round_complete] c1=3 & detect -> (c1'=4) & (c1s'=0) & (c1_skip'=false);
	//self-looping state
	[END] c1=4 -> true;

endmodule

//pr_req_successful is true if either a) log returns a valid proof or 
//b) client does not need to contact log in the first place 

formula pr_req_successful = (c1s=1 & s1_sth+c1_sth!=3) | (c1s=2 & s2_sth+c1_sth!=3) |
        	            (c1s=3 & s3_sth+c1_sth!=3) | (c1s=4 & s4_sth+c1_sth!=3) |
          		    (c1s=5 & s5_sth+c1_sth!=3);

// Warning messages are used when someone has already found an inconsistency and starts to report this to other nodes through gossiping.
formula warn_msg = (c1s=1 & s1d) | (c1s=2 & s2d) | (c1s=3 & s3d) | (c1s=4 & s4d) | (c1s=5 & s5d);

// Clients update when given brand new data via a server
formula c_update = c1_sth + ((c1s=1 & s1_sth>c1_sth)?s1_sth-c1_sth:0) + ((c1s=2 & s2_sth>c1_sth)?s2_sth-c1_sth:0) + 
		   ((c1s=3 & s3_sth>c1_sth)?s3_sth-c1_sth:0) + ((c1s=4 & s4_sth>c1_sth)?s4_sth-c1_sth:0) + 
		   ((c1s=5 & s5_sth>c1_sth)?s5_sth-c1_sth:0);

// An issue will be found in the data if either a) log cannot provide a valid proof or b) client gets a warning message.
formula s_data_ok = pr_req_successful & !warn_msg;

formula detect = c1d | c2d | c3d | c4d | c5d;
label "detect" = c1d | c2d | c3d | c4d | c5d;

module Client2=Client1[p_1_1=p_2_1, p_1_2=p_2_2, p_1_3=p_2_3, p_1_4=p_2_4, p_1_5=p_2_5, 
g1=g2,
c1=c2, c1s=c2s, c1_sth=c2_sth, c1_skip=c2_skip, c1d=c2d, c2d=c1d,
c1_sth_init = c2_sth_init] endmodule

module Client3=Client1[p_1_1=p_3_1, p_1_2=p_3_2, p_1_3=p_3_3, p_1_4=p_3_4, p_1_5=p_3_5, 
g1=g3,
c1=c3, c1s=c3s, c1_sth=c3_sth, c1_skip=c3_skip, c1d=c3d, c3d=c1d,
c1_sth_init = c3_sth_init] endmodule

module Client4=Client1[p_1_1=p_4_1, p_1_2=p_4_2, p_1_3=p_4_3, p_1_4=p_4_4, p_1_5=p_4_5, 
g1=g4,
c1=c4, c1s=c4s, c1_sth=c4_sth, c1_skip=c4_skip, c1d=c4d, c4d=c1d,
c1_sth_init = c4_sth_init] endmodule

module Client5=Client1[p_1_1=p_5_1, p_1_2=p_5_2, p_1_3=p_5_3, p_1_4=p_5_4, p_1_5=p_5_5, 
g1=g5,
c1=c5, c1s=c5s, c1_sth=c5_sth, c1_skip=c5_skip, c1d=c5d, c5d=c1d,
c1_sth_init = c5_sth_init] endmodule
"""

splitworld_original_server_init = """
//needed for module relabelling
const int S1 = 1;
const int S2 = 2;
const int S3 = 3;
const int S4 = 4;
const int S5 = 5;

module Server1

	//does the server have the latest STH?
	s1_sth : [0..2];
	//detection state
	s1d : bool;

	//If any clients sends inconsistent data, cease protocol execution and go into detection state.
	[update] !s1d & c_data_ok -> (s1_sth'=s_update);
	[update] !s1d & !c_data_ok -> (s1d'=true) & (s1_sth'=0);
	[update] s1d -> true;
	//self-looping state
	[END] true -> true;

endmodule

//The following formulae is used for the 'update' stage in server 1.
// Server-side, an issue will be found in the data if either a) log cannot provide a valid proof or b) a pair of clients connect with inconsistent data.
formula server_pr_req_fail = (c1s=S1 & s1_sth+c1_sth=3) | (c2s=S1 & s1_sth+c2_sth=3) | (c3s=S1 & s1_sth+c3_sth=3) | 
			     (c4s=S1 & s1_sth+c4_sth=3) | (c5s=S1 & s1_sth+c5_sth=3);
formula pairwise_inconsistency = ((c1s=S1 & c1_sth=1) | (c2s=S1 & c2_sth=1) | (c3s=S1 & c3_sth=1) | 
				  (c4s=S1 & c4_sth=1) | (c5s=S1 & c5_sth=1)) & 
				 ((c1s=S1 & c1_sth=2) | (c2s=S1 & c2_sth=2) | (c3s=S1 & c3_sth=2) | 
				  (c4s=S1 & c4_sth=2) | (c5s=S1 & c5_sth=2));
formula c_data_ok = !server_pr_req_fail & !pairwise_inconsistency;

// Servers update when given brand new data via a connected client. 
formula s_update = s1_sth + max((c1s=S1&c1_sth>s1_sth?c1_sth-s1_sth:0),(c2s=S1&c2_sth>s1_sth?c2_sth-s1_sth:0),(c3s=S1&c3_sth>s1_sth?c3_sth-s1_sth:0),
				(c4s=S1&c4_sth>s1_sth?c4_sth-s1_sth:0),(c5s=S1&c5_sth>s1_sth?c5_sth-s1_sth:0));

module Server2=Server1[s1_sth=s2_sth, s2_sth=s1_sth, s1d=s2d, s2d=s1d, S1=S2, s1_init=s2_init] endmodule
module Server3=Server1[s1_sth=s3_sth, s3_sth=s1_sth, s1d=s3d, s3d=s1d, S1=S3, s1_init=s3_init] endmodule
module Server4=Server1[s1_sth=s4_sth, s4_sth=s1_sth, s1d=s4d, s4d=s1d, S1=S4, s1_init=s4_init] endmodule
module Server5=Server1[s1_sth=s5_sth, s5_sth=s1_sth, s1d=s5d, s5d=s1d, S1=S5, s1_init=s5_init] endmodule
"""

splitworld_extended_server_init = """
//needed for module relabelling
const int S1 = 1;
const int S2 = 2;
const int S3 = 3;
const int S4 = 4;
const int S5 = 5;

//server-to-server gossiping is done using a "spread-and-forget" approach: A server randomly gossips to a subset of servers uniformly by sending 
//them a message but gets nothing in return. We assume that the channels used for this communication are secure.
//
//in cases b) and c), the server will either update or find an inconsistency with the data they already have. In case d),
//the server will always go into the detection state. The probability of getting a data type can be computed using the 
//inclusion-exclusion principle (note that it is possible that a server can get real data, for example, from at least two other servers at the 
//same time so we must avoid cases of double counting!)
formula real_5c1 = (s1_sth=1?1/5:0)+(s2_sth=1?1/5:0)+(s3_sth=1?1/5:0)+(s4_sth=1?1/5:0)+(s5_sth=1?1/5:0);
formula real_5c2 = (s1_sth=1?1/5:0)*(s2_sth=1?1/5:0)+(s1_sth=1?1/5:0)*(s3_sth=1?1/5:0)+(s1_sth=1?1/5:0)*(s4_sth=1?1/5:0)+
	   	   (s1_sth=1?1/5:0)*(s5_sth=1?1/5:0)+(s2_sth=1?1/5:0)*(s3_sth=1?1/5:0)+(s2_sth=1?1/5:0)*(s4_sth=1?1/5:0)+
  		   (s2_sth=1?1/5:0)*(s5_sth=1?1/5:0)+(s3_sth=1?1/5:0)*(s4_sth=1?1/5:0)+(s3_sth=1?1/5:0)*(s5_sth=1?1/5:0)+
		   (s4_sth=1?1/5:0)*(s5_sth=1?1/5:0);
formula real_5c3 = (s2_sth=1?1/5:0)*(s4_sth=1?1/5:0)*(s5_sth=1?1/5:0)+(s1_sth=1?1/5:0)*(s2_sth=1?1/5:0)*(s3_sth=1?1/5:0)+
		   (s1_sth=1?1/5:0)*(s2_sth=1?1/5:0)*(s4_sth=1?1/5:0)+(s1_sth=1?1/5:0)*(s2_sth=1?1/5:0)*(s5_sth=1?1/5:0)+
		   (s2_sth=1?1/5:0)*(s3_sth=1?1/5:0)*(s4_sth=1?1/5:0)+(s2_sth=1?1/5:0)*(s3_sth=1?1/5:0)*(s5_sth=1?1/5:0)+
		   (s3_sth=1?1/5:0)*(s1_sth=1?1/5:0)*(s4_sth=1?1/5:0)+(s3_sth=1?1/5:0)*(s1_sth=1?1/5:0)*(s5_sth=1?1/5:0)+
		   (s3_sth=1?1/5:0)*(s4_sth=1?1/5:0)*(s5_sth=1?1/5:0)+(s1_sth=1?1/5:0)*(s4_sth=1?1/5:0)*(s5_sth=1?1/5:0);
formula real_5c4 = (s1_sth=1?1/5:0)*(s2_sth=1?1/5:0)*(s3_sth=1?1/5:0)*(s4_sth=1?1/5:0)+
		   (s1_sth=1?1/5:0)*(s2_sth=1?1/5:0)*(s3_sth=1?1/5:0)*(s5_sth=1?1/5:0)+
		   (s1_sth=1?1/5:0)*(s2_sth=1?1/5:0)*(s4_sth=1?1/5:0)*(s5_sth=1?1/5:0)+
		   (s1_sth=1?1/5:0)*(s3_sth=1?1/5:0)*(s4_sth=1?1/5:0)*(s5_sth=1?1/5:0)+
		   (s2_sth=1?1/5:0)*(s3_sth=1?1/5:0)*(s4_sth=1?1/5:0)*(s5_sth=1?1/5:0);
formula real_5c5 = (s1_sth=1?1/5:0)*(s2_sth=1?1/5:0)*(s3_sth=1?1/5:0)*(s4_sth=1?1/5:0)*(s5_sth=1?1/5:0);

formula fake_5c1 = (s1_sth=2?1/5:0)+(s2_sth=2?1/5:0)+(s3_sth=2?1/5:0)+(s4_sth=2?1/5:0)+(s5_sth=2?1/5:0);
formula fake_5c2 = (s1_sth=2?1/5:0)*(s2_sth=2?1/5:0)+(s1_sth=2?1/5:0)*(s3_sth=2?1/5:0)+(s1_sth=2?1/5:0)*(s4_sth=2?1/5:0)+
	           (s1_sth=2?1/5:0)*(s5_sth=2?1/5:0)+(s2_sth=2?1/5:0)*(s3_sth=2?1/5:0)+(s2_sth=2?1/5:0)*(s4_sth=2?1/5:0)+
	 	   (s2_sth=2?1/5:0)*(s5_sth=2?1/5:0)+(s3_sth=2?1/5:0)*(s4_sth=2?1/5:0)+(s3_sth=2?1/5:0)*(s5_sth=2?1/5:0)+
	   	   (s4_sth=2?1/5:0)*(s5_sth=2?1/5:0);
formula fake_5c3 = (s2_sth=2?1/5:0)*(s4_sth=2?1/5:0)*(s5_sth=2?1/5:0)+(s1_sth=2?1/5:0)*(s2_sth=2?1/5:0)*(s3_sth=2?1/5:0)+
	  	   (s1_sth=2?1/5:0)*(s2_sth=2?1/5:0)*(s4_sth=2?1/5:0)+(s1_sth=2?1/5:0)*(s2_sth=2?1/5:0)*(s5_sth=2?1/5:0)+
	  	   (s2_sth=2?1/5:0)*(s3_sth=2?1/5:0)*(s4_sth=2?1/5:0)+(s2_sth=2?1/5:0)*(s3_sth=2?1/5:0)*(s5_sth=2?1/5:0)+
	   	   (s3_sth=2?1/5:0)*(s1_sth=2?1/5:0)*(s4_sth=2?1/5:0)+(s3_sth=2?1/5:0)*(s1_sth=2?1/5:0)*(s5_sth=2?1/5:0)+
	   	   (s3_sth=2?1/5:0)*(s4_sth=2?1/5:0)*(s5_sth=2?1/5:0)+(s1_sth=2?1/5:0)*(s4_sth=2?1/5:0)*(s5_sth=2?1/5:0);
formula fake_5c4 = (s1_sth=2?1/5:0)*(s2_sth=2?1/5:0)*(s3_sth=2?1/5:0)*(s4_sth=2?1/5:0)+
	   	   (s1_sth=2?1/5:0)*(s2_sth=2?1/5:0)*(s3_sth=2?1/5:0)*(s5_sth=2?1/5:0)+
	 	   (s1_sth=2?1/5:0)*(s2_sth=2?1/5:0)*(s4_sth=2?1/5:0)*(s5_sth=2?1/5:0)+
	 	   (s1_sth=2?1/5:0)*(s3_sth=2?1/5:0)*(s4_sth=2?1/5:0)*(s5_sth=2?1/5:0)+
		   (s2_sth=2?1/5:0)*(s3_sth=2?1/5:0)*(s4_sth=2?1/5:0)*(s5_sth=2?1/5:0);
formula fake_5c5 = (s1_sth=2?1/5:0)*(s2_sth=2?1/5:0)*(s3_sth=2?1/5:0)*(s4_sth=2?1/5:0)*(s5_sth=2?1/5:0);

formula mssg_5c1 = (s1d?1/5:0)+(s2d?1/5:0)+(s3d?1/5:0)+(s4d?1/5:0)+(s5d?1/5:0);
formula mssg_5c2 = (s1d?1/5:0)*(s2d?1/5:0)+(s1d?1/5:0)*(s3d?1/5:0)+(s1d?1/5:0)*(s4d?1/5:0)+
		   (s1d?1/5:0)*(s5d?1/5:0)+(s2d?1/5:0)*(s3d?1/5:0)+(s2d?1/5:0)*(s4d?1/5:0)+
		   (s2d?1/5:0)*(s5d?1/5:0)+(s3d?1/5:0)*(s4d?1/5:0)+(s3d?1/5:0)*(s5d?1/5:0)+
		   (s4d?1/5:0)*(s5d?1/5:0);
formula mssg_5c3 = (s2d?1/5:0)*(s4d?1/5:0)*(s5d?1/5:0)+(s1d?1/5:0)*(s2d?1/5:0)*(s3d?1/5:0)+
		   (s1d?1/5:0)*(s2d?1/5:0)*(s4d?1/5:0)+(s1d?1/5:0)*(s2d?1/5:0)*(s5d?1/5:0)+
		   (s2d?1/5:0)*(s3d?1/5:0)*(s4d?1/5:0)+(s2d?1/5:0)*(s3d?1/5:0)*(s5d?1/5:0)+
		   (s3d?1/5:0)*(s1d?1/5:0)*(s4d?1/5:0)+(s3d?1/5:0)*(s1d?1/5:0)*(s5d?1/5:0)+
		   (s3d?1/5:0)*(s4d?1/5:0)*(s5d?1/5:0)+(s1d?1/5:0)*(s4d?1/5:0)*(s5d?1/5:0);
formula mssg_5c4 = (s1d?1/5:0)*(s2d?1/5:0)*(s3d?1/5:0)*(s4d?1/5:0)+
		   (s1d?1/5:0)*(s2d?1/5:0)*(s3d?1/5:0)*(s5d?1/5:0)+
		   (s1d?1/5:0)*(s2d?1/5:0)*(s4d?1/5:0)*(s5d?1/5:0)+
		   (s1d?1/5:0)*(s3d?1/5:0)*(s4d?1/5:0)*(s5d?1/5:0)+
		   (s2d?1/5:0)*(s3d?1/5:0)*(s4d?1/5:0)*(s5d?1/5:0);
formula mssg_5c5 = (s1d?1/5:0)*(s2d?1/5:0)*(s3d?1/5:0)*(s4d?1/5:0)*(s5d?1/5:0);

formula get_real_data = real_5c1 - real_5c2 + real_5c3 - real_5c4 + real_5c5;
formula get_fake_data = fake_5c1 - fake_5c2 + fake_5c3 - fake_5c4 + fake_5c5; 
formula get_message   = mssg_5c1 - mssg_5c2 + mssg_5c3 - mssg_5c4 + mssg_5c5;

module Server1

	//does the server have the latest STH?
	s1_sth : [0..2];
	//detection state
	s1d : bool;

	//ORIGINAL DESIGN - PERRIG ET AL RPOTOCOLS
	//If any clients sends inconsistent data, cease protocol execution and go into detection state.
	[update] !s1d & c_data_ok -> (s1_sth'=s_update);
	[update] !s1d & !c_data_ok -> (s1d'=true) & (s1_sth'=0);
	[update] s1d -> true;
	//NEW DESIGN MODIFICATION - SERVER-TO-SERVER GOSSIP (comment this section if analysing only the original Perrig et al. design)
	//
	//Between the 'update' stages, each server will spread their data to every other server (including itself). The genuine data is shared first,
	//then afterwards the fake data and warning messages, in that order.
	//We set the probability of server i gossiping to server j at 0.2. The probabilities used in the transitions were calculated 
	//using the I-E principle. If a server goes into detection mode, set si_sth=0 to correct probabilities for the next round.
	//
	//'connect' stage - servers with the real data gossip.
	[connect] !s1d & s1_sth=0 -> get_real_data : (s1_sth'=1) + 1-get_real_data : true;
	[connect] !s1d & s1_sth=1 -> true;
	[connect] !s1d & s1_sth=2 -> get_real_data : (s1d'=true) & (s1_sth'=0) + 1-get_real_data : true;
	[connect] s1d -> true;
	//'choose' stage - servers with the fake data gossip.
	[choose] !s1d & s1_sth=0 -> get_fake_data : (s1_sth'=2) + 1-get_fake_data : true;
	[choose] !s1d & s1_sth=1 -> get_fake_data : (s1d'=true) & (s1_sth'=0) + 1-get_fake_data : true;
	[choose] !s1d & s1_sth=2 -> true;
	[choose] s1d -> true;
	//'round complete' stage - servers in detection mode gossip warning messages.
	[round_complete] true -> get_message : (s1d'=true) & (s1_sth'=0) + 1-get_message : true;
	//self-looping state
	[END] true -> true;

endmodule

//The following formulae is used for the 'update' stage in server 1.
// Server-side, an issue will be found in the data if either a) log cannot provide a valid proof or b) a pair of clients connect with inconsistent data.
formula server_pr_req_fail = (c1s=S1 & s1_sth+c1_sth=3) | (c2s=S1 & s1_sth+c2_sth=3) | (c3s=S1 & s1_sth+c3_sth=3) | 
			     (c4s=S1 & s1_sth+c4_sth=3) | (c5s=S1 & s1_sth+c5_sth=3);
formula pairwise_inconsistency = ((c1s=S1 & c1_sth=1) | (c2s=S1 & c2_sth=1) | (c3s=S1 & c3_sth=1) | 
				  (c4s=S1 & c4_sth=1) | (c5s=S1 & c5_sth=1)) & 
				 ((c1s=S1 & c1_sth=2) | (c2s=S1 & c2_sth=2) | (c3s=S1 & c3_sth=2) | 
				  (c4s=S1 & c4_sth=2) | (c5s=S1 & c5_sth=2));
formula c_data_ok = !server_pr_req_fail & !pairwise_inconsistency;

// Servers update when given brand new data via a connected client. 
formula s_update = s1_sth + max((c1s=S1&c1_sth>s1_sth?c1_sth-s1_sth:0),(c2s=S1&c2_sth>s1_sth?c2_sth-s1_sth:0),(c3s=S1&c3_sth>s1_sth?c3_sth-s1_sth:0),
				(c4s=S1&c4_sth>s1_sth?c4_sth-s1_sth:0),(c5s=S1&c5_sth>s1_sth?c5_sth-s1_sth:0));

module Server2=Server1[s1_sth=s2_sth, s2_sth=s1_sth, s1d=s2d, s2d=s1d, S1=S2, s1_init=s2_init] endmodule
module Server3=Server1[s1_sth=s3_sth, s3_sth=s1_sth, s1d=s3d, s3d=s1d, S1=S3, s1_init=s3_init] endmodule
module Server4=Server1[s1_sth=s4_sth, s4_sth=s1_sth, s1d=s4d, s4d=s1d, S1=S4, s1_init=s4_init] endmodule
module Server5=Server1[s1_sth=s5_sth, s5_sth=s1_sth, s1d=s5d, s5d=s1d, S1=S5, s1_init=s5_init] endmodule
"""