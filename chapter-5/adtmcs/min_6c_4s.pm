dtmc

formula c1_connected_server_has_sth = (c1s=1 & s1_sth)|(c1s=2 & s2_sth)|(c1s=3 & s3_sth)|(c1s=4 & s4_sth);
formula c2_connected_server_has_sth = (c2s=1 & s1_sth)|(c2s=2 & s2_sth)|(c2s=3 & s3_sth)|(c2s=4 & s4_sth);
formula c3_connected_server_has_sth = (c3s=1 & s1_sth)|(c3s=2 & s2_sth)|(c3s=3 & s3_sth)|(c3s=4 & s4_sth);
formula c4_connected_server_has_sth = (c4s=1 & s1_sth)|(c4s=2 & s2_sth)|(c4s=3 & s3_sth)|(c4s=4 & s4_sth);
formula c5_connected_server_has_sth = (c5s=1 & s1_sth)|(c5s=2 & s2_sth)|(c5s=3 & s3_sth)|(c5s=4 & s4_sth);
formula c6_connected_server_has_sth = (c6s=1 & s1_sth)|(c6s=2 & s2_sth)|(c6s=3 & s3_sth)|(c6s=4 & s4_sth);
formula updated_client_gossips = (c1_sth & !c1_skip)|(c2_sth & !c2_skip)|(c3_sth & !c3_skip)|(c4_sth & !c4_skip)|(c5_sth & !c5_skip)|(c6_sth & !c6_skip);
formula nonupdated_client_gossips = (!c1_sth & !c1_skip)|(!c2_sth & !c2_skip)|(!c3_sth & !c3_skip)|(!c4_sth & !c4_skip)|(!c5_sth & !c5_skip)|(!c6_sth & !c6_skip);
formula s1_connected_client_has_sth = (c1s=1 & c1_sth)|(c2s=1 & c2_sth)|(c3s=1 & c3_sth)|(c4s=1 & c4_sth)|(c5s=1 & c5_sth)|(c6s=1 & c6_sth);
formula s2_connected_client_has_sth = (c1s=2 & c1_sth)|(c2s=2 & c2_sth)|(c3s=2 & c3_sth)|(c4s=2 & c4_sth)|(c5s=2 & c5_sth)|(c6s=2 & c6_sth);
formula s3_connected_client_has_sth = (c1s=3 & c1_sth)|(c2s=3 & c2_sth)|(c3s=3 & c3_sth)|(c4s=3 & c4_sth)|(c5s=3 & c5_sth)|(c6s=3 & c6_sth);
formula s4_connected_client_has_sth = (c1s=4 & c1_sth)|(c2s=4 & c2_sth)|(c3s=4 & c3_sth)|(c4s=4 & c4_sth)|(c5s=4 & c5_sth)|(c6s=4 & c6_sth);

formula abs_c1_sth = ((c1=2 & ( (!c1_sth & c1_connected_server_has_sth) | c1_sth )) | (c1!=2 & c1_sth)?1:0);
formula abs_c2_sth = ((c2=2 & ( (!c2_sth & c2_connected_server_has_sth) | c2_sth )) | (c2!=2 & c2_sth)?1:0);
formula abs_c3_sth = ((c3=2 & ( (!c3_sth & c3_connected_server_has_sth) | c3_sth )) | (c3!=2 & c3_sth)?1:0);
formula abs_c4_sth = ((c4=2 & ( (!c4_sth & c4_connected_server_has_sth) | c4_sth )) | (c4!=2 & c4_sth)?1:0);
formula abs_c5_sth = ((c5=2 & ( (!c5_sth & c5_connected_server_has_sth) | c5_sth )) | (c5!=2 & c5_sth)?1:0);
formula abs_c6_sth = ((c6=2 & ( (!c6_sth & c6_connected_server_has_sth) | c6_sth )) | (c6!=2 & c6_sth)?1:0);

formula abs_s1_sth = 0 + ( ( c1!=2 & s1_sth ) | ( c1=2 & (!s1_sth & s1_connected_client_has_sth) | s1_sth )?1:0);
formula abs_s2_sth = 0 + ( ( c1!=2 & s2_sth ) | ( c1=2 & (!s2_sth & s2_connected_client_has_sth) | s2_sth )?1:0);
formula abs_s3_sth = 0 + ( ( c1!=2 & s3_sth ) | ( c1=2 & (!s3_sth & s3_connected_client_has_sth) | s3_sth )?1:0);
formula abs_s4_sth = 0 + ( ( c1!=2 & s4_sth ) | ( c1=2 & (!s4_sth & s4_connected_client_has_sth) | s4_sth )?1:0);

formula abs_stage = 0 + (c1=1 & updated_client_gossips & !nonupdated_client_gossips?1:0) +
(c1=1 & !updated_client_gossips & nonupdated_client_gossips?2:0) +
(c1=1 & updated_client_gossips & nonupdated_client_gossips?3:0) +
(c1=1 & !updated_client_gossips & !nonupdated_client_gossips?4:0) +
(c1=2?5:0) +
(c1=3?6:0) +
(c1=4?7:0);

label "abs_t" = abs_c1_sth+abs_c2_sth+abs_c3_sth+abs_c4_sth+abs_c5_sth+abs_c6_sth=6 & abs_stage>=6;

const bool c1_sth_init = false;
const bool c2_sth_init = false;
const bool c3_sth_init = false;
const bool c4_sth_init = false;
const bool c5_sth_init = false;
const bool c6_sth_init = true;

prob g1_L = 0.5772144531450976;
prob g1_H = 0.5972144531450976;
prob g2_L = 0.20753297741444293;
prob g2_H = 0.22753297741444295;
prob g3_L = 0.16611570929300523;
prob g3_H = 0.18611570929300525;
prob g4_L = 0.3582039538384828;
prob g4_H = 0.3782039538384828;
prob g5_L = 0.3875196791946993;
prob g5_H = 0.40751967919469934;
prob g6_L = 0.3268201513066109;
prob g6_H = 0.3468201513066109;

prob p_1_1_L = 0.25585364506494285;
prob p_1_1_H = 0.27585364506494287;
prob p_1_2_L = 0.3314001053794364;
prob p_1_2_H = 0.35140010537943644;
prob p_1_3_L = 0.1712440688819204;
prob p_1_3_H = 0.19124406888192041;
prob p_1_4_L = 0.20150218067370013;
prob p_1_4_H = 0.22150218067370014;

prob p_2_1_L = 0.2573008556294393;
prob p_2_1_H = 0.2773008556294393;
prob p_2_2_L = 0.1751188379903581;
prob p_2_2_H = 0.19511883799035812;
prob p_2_3_L = 0.18988084997914745;
prob p_2_3_H = 0.20988084997914747;
prob p_2_4_L = 0.33769945640105514;
prob p_2_4_H = 0.35769945640105516;

prob p_3_1_L = 0.25361325559392345;
prob p_3_1_H = 0.27361325559392347;
prob p_3_2_L = 0.11449016258721227;
prob p_3_2_H = 0.13449016258721228;
prob p_3_3_L = 0.2351263260589315;
prob p_3_3_H = 0.2551263260589315;
prob p_3_4_L = 0.3567702557599328;
prob p_3_4_H = 0.37677025575993284;

prob p_4_1_L = 0.26376710733104286;
prob p_4_1_H = 0.2837671073310429;
prob p_4_2_L = 0.29905110363898085;
prob p_4_2_H = 0.31905110363898087;
prob p_4_3_L = 0.17058144103444514;
prob p_4_3_H = 0.19058144103444516;
prob p_4_4_L = 0.226600347995531;
prob p_4_4_H = 0.24660034799553102;

prob p_5_1_L = 0.3104336715665374;
prob p_5_1_H = 0.3304336715665374;
prob p_5_2_L = 0.24843761923120417;
prob p_5_2_H = 0.2684376192312042;
prob p_5_3_L = 0.1667861222941384;
prob p_5_3_H = 0.1867861222941384;
prob p_5_4_L = 0.23434258690812;
prob p_5_4_H = 0.25434258690812;

prob p_6_1_L = 0.3185756882888661;
prob p_6_1_H = 0.33857568828886614;
prob p_6_2_L = 0.20907064703693157;
prob p_6_2_H = 0.22907064703693159;
prob p_6_3_L = 0.2780790409507488;
prob p_6_3_H = 0.29807904095074883;
prob p_6_4_L = 0.15427462372345332;
prob p_6_4_H = 0.17427462372345334;

module Client1

	c1 : [0..4] init 0;
	c1s : [0..4] init 0;
	c1_sth : bool init c1_sth_init;
	c1_skip : bool init false;
	[connect] c1=0 -> [g1_L, g1_H] : (c1'=1) + [1-g1_H, 1-g1_L] : (c1'=1) & (c1_skip'=true);
	[choose] c1_skip=false & c1=1 -> [p_1_1_L, p_1_1_H] : (c1'=2)&(c1s'=1) +
					 [p_1_2_L, p_1_2_H] : (c1'=2)&(c1s'=2) +
					 [p_1_3_L, p_1_3_H] : (c1'=2)&(c1s'=3) +
					 [p_1_4_L, p_1_4_H] : (c1'=2)&(c1s'=4);
	[choose] c1_skip=true & c1=1-> (c1'=2);
	[update] !c1_skip & c1=2 & connected_server_has_sth  -> (c1'=3) & (c1_sth'=true);
	[update] c1=2 & ((!c1_skip & !connected_server_has_sth) | c1_skip) -> (c1'=3);
	[round_complete] c1=3 & !clients_all_updated -> (c1'=0) & (c1s'=0) & (c1_skip'=false);
	[round_complete] c1=3 & clients_all_updated -> (c1'=4);
	[END] c1=4 -> true;

endmodule

formula connected_server_has_sth = ((c1s=1 & s1_sth) | (c1s=2 & s2_sth) | (c1s=3 & s3_sth) | (c1s=4 & s4_sth));
formula clients_all_updated = c1_sth&c2_sth&c3_sth&c4_sth&c5_sth&c6_sth;
label "clients_all_updated" = c1_sth&c2_sth&c3_sth&c4_sth&c5_sth&c6_sth;


module Client2=Client1[p_1_1_L=p_2_1_L,p_1_1_H=p_2_1_H,p_1_2_L=p_2_2_L,p_1_2_H=p_2_2_H,p_1_3_L=p_2_3_L,p_1_3_H=p_2_3_H,p_1_4_L=p_2_4_L,p_1_4_H=p_2_4_H,
g1_L=g2_L,
g1_H=g2_H,
c1=c2,
c1s=c2s,
c1_sth=c2_sth,
c2_sth=c1_sth,
c1_skip=c2_skip,
c1_sth_init = c2_sth_init] endmodule

module Client3=Client1[p_1_1_L=p_3_1_L,p_1_1_H=p_3_1_H,p_1_2_L=p_3_2_L,p_1_2_H=p_3_2_H,p_1_3_L=p_3_3_L,p_1_3_H=p_3_3_H,p_1_4_L=p_3_4_L,p_1_4_H=p_3_4_H,
g1_L=g3_L,
g1_H=g3_H,
c1=c3,
c1s=c3s,
c1_sth=c3_sth,
c3_sth=c1_sth,
c1_skip=c3_skip,
c1_sth_init = c3_sth_init] endmodule

module Client4=Client1[p_1_1_L=p_4_1_L,p_1_1_H=p_4_1_H,p_1_2_L=p_4_2_L,p_1_2_H=p_4_2_H,p_1_3_L=p_4_3_L,p_1_3_H=p_4_3_H,p_1_4_L=p_4_4_L,p_1_4_H=p_4_4_H,
g1_L=g4_L,
g1_H=g4_H,
c1=c4,
c1s=c4s,
c1_sth=c4_sth,
c4_sth=c1_sth,
c1_skip=c4_skip,
c1_sth_init = c4_sth_init] endmodule

module Client5=Client1[p_1_1_L=p_5_1_L,p_1_1_H=p_5_1_H,p_1_2_L=p_5_2_L,p_1_2_H=p_5_2_H,p_1_3_L=p_5_3_L,p_1_3_H=p_5_3_H,p_1_4_L=p_5_4_L,p_1_4_H=p_5_4_H,
g1_L=g5_L,
g1_H=g5_H,
c1=c5,
c1s=c5s,
c1_sth=c5_sth,
c5_sth=c1_sth,
c1_skip=c5_skip,
c1_sth_init = c5_sth_init] endmodule

module Client6=Client1[p_1_1_L=p_6_1_L,p_1_1_H=p_6_1_H,p_1_2_L=p_6_2_L,p_1_2_H=p_6_2_H,p_1_3_L=p_6_3_L,p_1_3_H=p_6_3_H,p_1_4_L=p_6_4_L,p_1_4_H=p_6_4_H,
g1_L=g6_L,
g1_H=g6_H,
c1=c6,
c1s=c6s,
c1_sth=c6_sth,
c6_sth=c1_sth,
c1_skip=c6_skip,
c1_sth_init = c6_sth_init] endmodule

const int SERVER1 = 1;
const int SERVER2 = 2;
const int SERVER3 = 3;
const int SERVER4 = 4;

const bool s1_init = true;
const bool s2_init = false;
const bool s3_init = false;
const bool s4_init = false;

module Server1

	s1_sth : bool init s1_init;
	[update] !s1_sth & connected_client_has_sth -> (s1_sth'=true);
	[update] s1_sth | (!s1_sth & !connected_client_has_sth) -> true;
	[END] true -> true;

endmodule

formula connected_client_has_sth = ((c1s=SERVER1 & c1_sth) | (c2s=SERVER1 & c2_sth) | (c3s=SERVER1 & c3_sth) | (c4s=SERVER1 & c4_sth) | (c5s=SERVER1 & c5_sth) | (c6s=SERVER1 & c6_sth));


module Server2=Server1[s1_sth=s2_sth,s2_sth=s1_sth,SERVER1=SERVER2,s1_init=s2_init] endmodule
module Server3=Server1[s1_sth=s3_sth,s3_sth=s1_sth,SERVER1=SERVER3,s1_init=s3_init] endmodule
module Server4=Server1[s1_sth=s4_sth,s4_sth=s1_sth,SERVER1=SERVER4,s1_init=s4_init] endmodule

