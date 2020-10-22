dtmc

formula c1_connected_server_has_sth = (c1s=1 & s1_sth)|(c1s=2 & s2_sth)|(c1s=3 & s3_sth)|(c1s=4 & s4_sth)|(c1s=5 & s5_sth);
formula c2_connected_server_has_sth = (c2s=1 & s1_sth)|(c2s=2 & s2_sth)|(c2s=3 & s3_sth)|(c2s=4 & s4_sth)|(c2s=5 & s5_sth);
formula c3_connected_server_has_sth = (c3s=1 & s1_sth)|(c3s=2 & s2_sth)|(c3s=3 & s3_sth)|(c3s=4 & s4_sth)|(c3s=5 & s5_sth);
formula c4_connected_server_has_sth = (c4s=1 & s1_sth)|(c4s=2 & s2_sth)|(c4s=3 & s3_sth)|(c4s=4 & s4_sth)|(c4s=5 & s5_sth);
formula c5_connected_server_has_sth = (c5s=1 & s1_sth)|(c5s=2 & s2_sth)|(c5s=3 & s3_sth)|(c5s=4 & s4_sth)|(c5s=5 & s5_sth);
formula updated_client_gossips = (c1_sth & !c1_skip)|(c2_sth & !c2_skip)|(c3_sth & !c3_skip)|(c4_sth & !c4_skip)|(c5_sth & !c5_skip);
formula nonupdated_client_gossips = (!c1_sth & !c1_skip)|(!c2_sth & !c2_skip)|(!c3_sth & !c3_skip)|(!c4_sth & !c4_skip)|(!c5_sth & !c5_skip);
formula s1_connected_client_has_sth = (c1s=1 & c1_sth)|(c2s=1 & c2_sth)|(c3s=1 & c3_sth)|(c4s=1 & c4_sth)|(c5s=1 & c5_sth);
formula s2_connected_client_has_sth = (c1s=2 & c1_sth)|(c2s=2 & c2_sth)|(c3s=2 & c3_sth)|(c4s=2 & c4_sth)|(c5s=2 & c5_sth);
formula s3_connected_client_has_sth = (c1s=3 & c1_sth)|(c2s=3 & c2_sth)|(c3s=3 & c3_sth)|(c4s=3 & c4_sth)|(c5s=3 & c5_sth);
formula s4_connected_client_has_sth = (c1s=4 & c1_sth)|(c2s=4 & c2_sth)|(c3s=4 & c3_sth)|(c4s=4 & c4_sth)|(c5s=4 & c5_sth);
formula s5_connected_client_has_sth = (c1s=5 & c1_sth)|(c2s=5 & c2_sth)|(c3s=5 & c3_sth)|(c4s=5 & c4_sth)|(c5s=5 & c5_sth);

formula abs_c1_sth = ((c1=2 & ( (!c1_sth & c1_connected_server_has_sth) | c1_sth )) | (c1!=2 & c1_sth)?1:0);
formula abs_c2_sth = ((c2=2 & ( (!c2_sth & c2_connected_server_has_sth) | c2_sth )) | (c2!=2 & c2_sth)?1:0);
formula abs_c3_sth = ((c3=2 & ( (!c3_sth & c3_connected_server_has_sth) | c3_sth )) | (c3!=2 & c3_sth)?1:0);
formula abs_c4_sth = ((c4=2 & ( (!c4_sth & c4_connected_server_has_sth) | c4_sth )) | (c4!=2 & c4_sth)?1:0);
formula abs_c5_sth = ((c5=2 & ( (!c5_sth & c5_connected_server_has_sth) | c5_sth )) | (c5!=2 & c5_sth)?1:0);

formula abs_s1_sth = 0 + ( ( c1!=2 & s1_sth ) | ( c1=2 & (!s1_sth & s1_connected_client_has_sth) | s1_sth )?1:0);
formula abs_s2_sth = 0 + ( ( c1!=2 & s2_sth ) | ( c1=2 & (!s2_sth & s2_connected_client_has_sth) | s2_sth )?1:0);
formula abs_s3_sth = 0 + ( ( c1!=2 & s3_sth ) | ( c1=2 & (!s3_sth & s3_connected_client_has_sth) | s3_sth )?1:0);
formula abs_s4_sth = 0 + ( ( c1!=2 & s4_sth ) | ( c1=2 & (!s4_sth & s4_connected_client_has_sth) | s4_sth )?1:0);
formula abs_s5_sth = 0 + ( ( c1!=2 & s5_sth ) | ( c1=2 & (!s5_sth & s5_connected_client_has_sth) | s5_sth )?1:0);

formula abs_stage = 0 + (c1=1 & updated_client_gossips & !nonupdated_client_gossips?1:0) +
(c1=1 & !updated_client_gossips & nonupdated_client_gossips?2:0) +
(c1=1 & updated_client_gossips & nonupdated_client_gossips?3:0) +
(c1=1 & !updated_client_gossips & !nonupdated_client_gossips?4:0) +
(c1=2?5:0) +
(c1=3?6:0) +
(c1=4?7:0);

label "abs_t" = abs_c1_sth+abs_c2_sth+abs_c3_sth+abs_c4_sth+abs_c5_sth=5 & abs_stage>=6;

const bool c1_sth_init = false;
const bool c2_sth_init = false;
const bool c3_sth_init = false;
const bool c4_sth_init = false;
const bool c5_sth_init = true;

prob g1_L = 0.6618291704203741;
prob g1_H = 0.6818291704203742;
prob g2_L = 0.5903077579304304;
prob g2_H = 0.6103077579304305;
prob g3_L = 0.11997299592744239;
prob g3_H = 0.1399729959274424;
prob g4_L = 0.5822001141087131;
prob g4_H = 0.6022001141087131;
prob g5_L = 0.15267966953026899;
prob g5_H = 0.172679669530269;

prob p_1_1_L = 0.1641352982897128;
prob p_1_1_H = 0.1841352982897128;
prob p_1_2_L = 0.11669412854654933;
prob p_1_2_H = 0.13669412854654933;
prob p_1_3_L = 0.24054451688988787;
prob p_1_3_H = 0.2605445168898879;
prob p_1_4_L = 0.20028560952328525;
prob p_1_4_H = 0.22028560952328527;
prob p_1_5_L = 0.22834044675056472;
prob p_1_5_H = 0.24834044675056474;

prob p_2_1_L = 0.1625813331601667;
prob p_2_1_H = 0.18258133316016673;
prob p_2_2_L = 0.17450951239052584;
prob p_2_2_H = 0.19450951239052586;
prob p_2_3_L = 0.23653945014041997;
prob p_2_3_H = 0.25653945014041996;
prob p_2_4_L = 0.18506400424488464;
prob p_2_4_H = 0.20506400424488466;
prob p_2_5_L = 0.19130570006400285;
prob p_2_5_H = 0.21130570006400287;

prob p_3_1_L = 0.24286142694634694;
prob p_3_1_H = 0.26286142694634695;
prob p_3_2_L = 0.2251244945248801;
prob p_3_2_H = 0.2451244945248801;
prob p_3_3_L = 0.22403949287691885;
prob p_3_3_H = 0.24403949287691887;
prob p_3_4_L = 0.1511902265120986;
prob p_3_4_H = 0.17119022651209861;
prob p_3_5_L = 0.10678435913975547;
prob p_3_5_H = 0.12678435913975547;

prob p_4_1_L = 0.2096478195193796;
prob p_4_1_H = 0.22964781951937963;
prob p_4_2_L = 0.20095412019899586;
prob p_4_2_H = 0.22095412019899588;
prob p_4_3_L = 0.173389010810975;
prob p_4_3_H = 0.193389010810975;
prob p_4_4_L = 0.21380786036793334;
prob p_4_4_H = 0.23380786036793336;
prob p_4_5_L = 0.15220118910271613;
prob p_4_5_H = 0.17220118910271615;

prob p_5_1_L = 0.1588415984351136;
prob p_5_1_H = 0.17884159843511363;
prob p_5_2_L = 0.1637785835235843;
prob p_5_2_H = 0.1837785835235843;
prob p_5_3_L = 0.1484352906029249;
prob p_5_3_H = 0.16843529060292492;
prob p_5_4_L = 0.3186368368058043;
prob p_5_4_H = 0.3386368368058043;
prob p_5_5_L = 0.16030769063257289;
prob p_5_5_H = 0.1803076906325729;

module Client1

	c1 : [0..4] init 0;
	c1s : [0..5] init 0;
	c1_sth : bool init c1_sth_init;
	c1_skip : bool init false;
	[connect] c1=0 -> [g1_L, g1_H] : (c1'=1) + [1-g1_H, 1-g1_L] : (c1'=1) & (c1_skip'=true);
	[choose] c1_skip=false & c1=1 -> [p_1_1_L, p_1_1_H] : (c1'=2)&(c1s'=1) +
					 [p_1_2_L, p_1_2_H] : (c1'=2)&(c1s'=2) +
					 [p_1_3_L, p_1_3_H] : (c1'=2)&(c1s'=3) +
					 [p_1_4_L, p_1_4_H] : (c1'=2)&(c1s'=4) +
					 [p_1_5_L, p_1_5_H] : (c1'=2)&(c1s'=5);
	[choose] c1_skip=true & c1=1-> (c1'=2);
	[update] !c1_skip & c1=2 & connected_server_has_sth  -> (c1'=3) & (c1_sth'=true);
	[update] c1=2 & ((!c1_skip & !connected_server_has_sth) | c1_skip) -> (c1'=3);
	[round_complete] c1=3 & !clients_all_updated -> (c1'=0) & (c1s'=0) & (c1_skip'=false);
	[round_complete] c1=3 & clients_all_updated -> (c1'=4);
	[END] c1=4 -> true;

endmodule

formula connected_server_has_sth = ((c1s=1 & s1_sth) | (c1s=2 & s2_sth) | (c1s=3 & s3_sth) | (c1s=4 & s4_sth) | (c1s=5 & s5_sth));
formula clients_all_updated = c1_sth&c2_sth&c3_sth&c4_sth&c5_sth;
label "clients_all_updated" = c1_sth&c2_sth&c3_sth&c4_sth&c5_sth;


module Client2=Client1[p_1_1_L=p_2_1_L,p_1_1_H=p_2_1_H,p_1_2_L=p_2_2_L,p_1_2_H=p_2_2_H,p_1_3_L=p_2_3_L,p_1_3_H=p_2_3_H,p_1_4_L=p_2_4_L,p_1_4_H=p_2_4_H,p_1_5_L=p_2_5_L,p_1_5_H=p_2_5_H,
g1_L=g2_L,
g1_H=g2_H,
c1=c2,
c1s=c2s,
c1_sth=c2_sth,
c2_sth=c1_sth,
c1_skip=c2_skip,
c1_sth_init = c2_sth_init] endmodule

module Client3=Client1[p_1_1_L=p_3_1_L,p_1_1_H=p_3_1_H,p_1_2_L=p_3_2_L,p_1_2_H=p_3_2_H,p_1_3_L=p_3_3_L,p_1_3_H=p_3_3_H,p_1_4_L=p_3_4_L,p_1_4_H=p_3_4_H,p_1_5_L=p_3_5_L,p_1_5_H=p_3_5_H,
g1_L=g3_L,
g1_H=g3_H,
c1=c3,
c1s=c3s,
c1_sth=c3_sth,
c3_sth=c1_sth,
c1_skip=c3_skip,
c1_sth_init = c3_sth_init] endmodule

module Client4=Client1[p_1_1_L=p_4_1_L,p_1_1_H=p_4_1_H,p_1_2_L=p_4_2_L,p_1_2_H=p_4_2_H,p_1_3_L=p_4_3_L,p_1_3_H=p_4_3_H,p_1_4_L=p_4_4_L,p_1_4_H=p_4_4_H,p_1_5_L=p_4_5_L,p_1_5_H=p_4_5_H,
g1_L=g4_L,
g1_H=g4_H,
c1=c4,
c1s=c4s,
c1_sth=c4_sth,
c4_sth=c1_sth,
c1_skip=c4_skip,
c1_sth_init = c4_sth_init] endmodule

module Client5=Client1[p_1_1_L=p_5_1_L,p_1_1_H=p_5_1_H,p_1_2_L=p_5_2_L,p_1_2_H=p_5_2_H,p_1_3_L=p_5_3_L,p_1_3_H=p_5_3_H,p_1_4_L=p_5_4_L,p_1_4_H=p_5_4_H,p_1_5_L=p_5_5_L,p_1_5_H=p_5_5_H,
g1_L=g5_L,
g1_H=g5_H,
c1=c5,
c1s=c5s,
c1_sth=c5_sth,
c5_sth=c1_sth,
c1_skip=c5_skip,
c1_sth_init = c5_sth_init] endmodule

const int SERVER1 = 1;
const int SERVER2 = 2;
const int SERVER3 = 3;
const int SERVER4 = 4;
const int SERVER5 = 5;

const bool s1_init = true;
const bool s2_init = false;
const bool s3_init = false;
const bool s4_init = false;
const bool s5_init = false;

module Server1

	s1_sth : bool init s1_init;
	[update] !s1_sth & connected_client_has_sth -> (s1_sth'=true);
	[update] s1_sth | (!s1_sth & !connected_client_has_sth) -> true;
	[END] true -> true;

endmodule

formula connected_client_has_sth = ((c1s=SERVER1 & c1_sth) | (c2s=SERVER1 & c2_sth) | (c3s=SERVER1 & c3_sth) | (c4s=SERVER1 & c4_sth) | (c5s=SERVER1 & c5_sth));


module Server2=Server1[s1_sth=s2_sth,s2_sth=s1_sth,SERVER1=SERVER2,s1_init=s2_init] endmodule
module Server3=Server1[s1_sth=s3_sth,s3_sth=s1_sth,SERVER1=SERVER3,s1_init=s3_init] endmodule
module Server4=Server1[s1_sth=s4_sth,s4_sth=s1_sth,SERVER1=SERVER4,s1_init=s4_init] endmodule
module Server5=Server1[s1_sth=s5_sth,s5_sth=s1_sth,SERVER1=SERVER5,s1_init=s5_init] endmodule

