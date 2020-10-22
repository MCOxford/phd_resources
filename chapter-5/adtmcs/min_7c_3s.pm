dtmc

formula c1_connected_server_has_sth = (c1s=1 & s1_sth)|(c1s=2 & s2_sth)|(c1s=3 & s3_sth);
formula c2_connected_server_has_sth = (c2s=1 & s1_sth)|(c2s=2 & s2_sth)|(c2s=3 & s3_sth);
formula c3_connected_server_has_sth = (c3s=1 & s1_sth)|(c3s=2 & s2_sth)|(c3s=3 & s3_sth);
formula c4_connected_server_has_sth = (c4s=1 & s1_sth)|(c4s=2 & s2_sth)|(c4s=3 & s3_sth);
formula c5_connected_server_has_sth = (c5s=1 & s1_sth)|(c5s=2 & s2_sth)|(c5s=3 & s3_sth);
formula c6_connected_server_has_sth = (c6s=1 & s1_sth)|(c6s=2 & s2_sth)|(c6s=3 & s3_sth);
formula c7_connected_server_has_sth = (c7s=1 & s1_sth)|(c7s=2 & s2_sth)|(c7s=3 & s3_sth);
formula updated_client_gossips = (c1_sth & !c1_skip)|(c2_sth & !c2_skip)|(c3_sth & !c3_skip)|(c4_sth & !c4_skip)|(c5_sth & !c5_skip)|(c6_sth & !c6_skip)|(c7_sth & !c7_skip);
formula nonupdated_client_gossips = (!c1_sth & !c1_skip)|(!c2_sth & !c2_skip)|(!c3_sth & !c3_skip)|(!c4_sth & !c4_skip)|(!c5_sth & !c5_skip)|(!c6_sth & !c6_skip)|(!c7_sth & !c7_skip);
formula s1_connected_client_has_sth = (c1s=1 & c1_sth)|(c2s=1 & c2_sth)|(c3s=1 & c3_sth)|(c4s=1 & c4_sth)|(c5s=1 & c5_sth)|(c6s=1 & c6_sth)|(c7s=1 & c7_sth);
formula s2_connected_client_has_sth = (c1s=2 & c1_sth)|(c2s=2 & c2_sth)|(c3s=2 & c3_sth)|(c4s=2 & c4_sth)|(c5s=2 & c5_sth)|(c6s=2 & c6_sth)|(c7s=2 & c7_sth);
formula s3_connected_client_has_sth = (c1s=3 & c1_sth)|(c2s=3 & c2_sth)|(c3s=3 & c3_sth)|(c4s=3 & c4_sth)|(c5s=3 & c5_sth)|(c6s=3 & c6_sth)|(c7s=3 & c7_sth);

formula abs_c1_sth = ((c1=2 & ( (!c1_sth & c1_connected_server_has_sth) | c1_sth )) | (c1!=2 & c1_sth)?1:0);
formula abs_c2_sth = ((c2=2 & ( (!c2_sth & c2_connected_server_has_sth) | c2_sth )) | (c2!=2 & c2_sth)?1:0);
formula abs_c3_sth = ((c3=2 & ( (!c3_sth & c3_connected_server_has_sth) | c3_sth )) | (c3!=2 & c3_sth)?1:0);
formula abs_c4_sth = ((c4=2 & ( (!c4_sth & c4_connected_server_has_sth) | c4_sth )) | (c4!=2 & c4_sth)?1:0);
formula abs_c5_sth = ((c5=2 & ( (!c5_sth & c5_connected_server_has_sth) | c5_sth )) | (c5!=2 & c5_sth)?1:0);
formula abs_c6_sth = ((c6=2 & ( (!c6_sth & c6_connected_server_has_sth) | c6_sth )) | (c6!=2 & c6_sth)?1:0);
formula abs_c7_sth = ((c7=2 & ( (!c7_sth & c7_connected_server_has_sth) | c7_sth )) | (c7!=2 & c7_sth)?1:0);

formula abs_s1_sth = 0 + ( ( c1!=2 & s1_sth ) | ( c1=2 & (!s1_sth & s1_connected_client_has_sth) | s1_sth )?1:0);
formula abs_s2_sth = 0 + ( ( c1!=2 & s2_sth ) | ( c1=2 & (!s2_sth & s2_connected_client_has_sth) | s2_sth )?1:0);
formula abs_s3_sth = 0 + ( ( c1!=2 & s3_sth ) | ( c1=2 & (!s3_sth & s3_connected_client_has_sth) | s3_sth )?1:0);

formula abs_stage = 0 + (c1=1 & updated_client_gossips & !nonupdated_client_gossips?1:0) +
(c1=1 & !updated_client_gossips & nonupdated_client_gossips?2:0) +
(c1=1 & updated_client_gossips & nonupdated_client_gossips?3:0) +
(c1=1 & !updated_client_gossips & !nonupdated_client_gossips?4:0) +
(c1=2?5:0) +
(c1=3?6:0) +
(c1=4?7:0);

label "abs_t" = abs_c1_sth+abs_c2_sth+abs_c3_sth+abs_c4_sth+abs_c5_sth+abs_c6_sth+abs_c7_sth=7 & abs_stage>=6;

const bool c1_sth_init = false;
const bool c2_sth_init = false;
const bool c3_sth_init = false;
const bool c4_sth_init = false;
const bool c5_sth_init = false;
const bool c6_sth_init = false;
const bool c7_sth_init = true;

prob g1_L = 0.48429133220791887;
prob g1_H = 0.5042913322079189;
prob g2_L = 0.24653545156189655;
prob g2_H = 0.26653545156189656;
prob g3_L = 0.5600475413867184;
prob g3_H = 0.5800475413867184;
prob g4_L = 0.21779465345909652;
prob g4_H = 0.23779465345909653;
prob g5_L = 0.6945839774977214;
prob g5_H = 0.7145839774977214;
prob g6_L = 0.7893698570006279;
prob g6_H = 0.8093698570006279;
prob g7_L = 0.14534451377113844;
prob g7_H = 0.16534451377113846;

prob p_1_1_L = 0.3193045293439933;
prob p_1_1_H = 0.3393045293439933;
prob p_1_2_L = 0.3353553913144708;
prob p_1_2_H = 0.3553553913144708;
prob p_1_3_L = 0.3153400793415359;
prob p_1_3_H = 0.3353400793415359;

prob p_2_1_L = 0.28705853988387015;
prob p_2_1_H = 0.30705853988387016;
prob p_2_2_L = 0.33503256466246273;
prob p_2_2_H = 0.35503256466246275;
prob p_2_3_L = 0.3479088954536672;
prob p_2_3_H = 0.36790889545366723;

prob p_3_1_L = 0.2623289433550919;
prob p_3_1_H = 0.2823289433550919;
prob p_3_2_L = 0.3553328612010934;
prob p_3_2_H = 0.37533286120109344;
prob p_3_3_L = 0.3523381954438146;
prob p_3_3_H = 0.37233819544381463;

prob p_4_1_L = 0.32445761686055025;
prob p_4_1_H = 0.34445761686055026;
prob p_4_2_L = 0.3348545020880246;
prob p_4_2_H = 0.3548545020880246;
prob p_4_3_L = 0.31068788105142514;
prob p_4_3_H = 0.33068788105142516;

prob p_5_1_L = 0.307602001821291;
prob p_5_1_H = 0.327602001821291;
prob p_5_2_L = 0.35830246610738575;
prob p_5_2_H = 0.37830246610738577;
prob p_5_3_L = 0.30409553207132317;
prob p_5_3_H = 0.3240955320713232;

prob p_6_1_L = 0.3079154128327484;
prob p_6_1_H = 0.32791541283274844;
prob p_6_2_L = 0.24993744821334374;
prob p_6_2_H = 0.26993744821334376;
prob p_6_3_L = 0.4121471389539079;
prob p_6_3_H = 0.43214713895390794;

prob p_7_1_L = 0.26307600291750916;
prob p_7_1_H = 0.2830760029175092;
prob p_7_2_L = 0.3271997973904043;
prob p_7_2_H = 0.3471997973904043;
prob p_7_3_L = 0.3797241996920865;
prob p_7_3_H = 0.3997241996920865;

module Client1

	c1 : [0..4] init 0;
	c1s : [0..3] init 0;
	c1_sth : bool init c1_sth_init;
	c1_skip : bool init false;
	[connect] c1=0 -> [g1_L, g1_H] : (c1'=1) + [1-g1_H, 1-g1_L] : (c1'=1) & (c1_skip'=true);
	[choose] c1_skip=false & c1=1 -> [p_1_1_L, p_1_1_H] : (c1'=2)&(c1s'=1) +
					 [p_1_2_L, p_1_2_H] : (c1'=2)&(c1s'=2) +
					 [p_1_3_L, p_1_3_H] : (c1'=2)&(c1s'=3);
	[choose] c1_skip=true & c1=1-> (c1'=2);
	[update] !c1_skip & c1=2 & connected_server_has_sth  -> (c1'=3) & (c1_sth'=true);
	[update] c1=2 & ((!c1_skip & !connected_server_has_sth) | c1_skip) -> (c1'=3);
	[round_complete] c1=3 & !clients_all_updated -> (c1'=0) & (c1s'=0) & (c1_skip'=false);
	[round_complete] c1=3 & clients_all_updated -> (c1'=4);
	[END] c1=4 -> true;

endmodule

formula connected_server_has_sth = ((c1s=1 & s1_sth) | (c1s=2 & s2_sth) | (c1s=3 & s3_sth));
formula clients_all_updated = c1_sth&c2_sth&c3_sth&c4_sth&c5_sth&c6_sth&c7_sth;
label "clients_all_updated" = c1_sth&c2_sth&c3_sth&c4_sth&c5_sth&c6_sth&c7_sth;


module Client2=Client1[p_1_1_L=p_2_1_L,p_1_1_H=p_2_1_H,p_1_2_L=p_2_2_L,p_1_2_H=p_2_2_H,p_1_3_L=p_2_3_L,p_1_3_H=p_2_3_H,
g1_L=g2_L,
g1_H=g2_H,
c1=c2,
c1s=c2s,
c1_sth=c2_sth,
c2_sth=c1_sth,
c1_skip=c2_skip,
c1_sth_init = c2_sth_init] endmodule

module Client3=Client1[p_1_1_L=p_3_1_L,p_1_1_H=p_3_1_H,p_1_2_L=p_3_2_L,p_1_2_H=p_3_2_H,p_1_3_L=p_3_3_L,p_1_3_H=p_3_3_H,
g1_L=g3_L,
g1_H=g3_H,
c1=c3,
c1s=c3s,
c1_sth=c3_sth,
c3_sth=c1_sth,
c1_skip=c3_skip,
c1_sth_init = c3_sth_init] endmodule

module Client4=Client1[p_1_1_L=p_4_1_L,p_1_1_H=p_4_1_H,p_1_2_L=p_4_2_L,p_1_2_H=p_4_2_H,p_1_3_L=p_4_3_L,p_1_3_H=p_4_3_H,
g1_L=g4_L,
g1_H=g4_H,
c1=c4,
c1s=c4s,
c1_sth=c4_sth,
c4_sth=c1_sth,
c1_skip=c4_skip,
c1_sth_init = c4_sth_init] endmodule

module Client5=Client1[p_1_1_L=p_5_1_L,p_1_1_H=p_5_1_H,p_1_2_L=p_5_2_L,p_1_2_H=p_5_2_H,p_1_3_L=p_5_3_L,p_1_3_H=p_5_3_H,
g1_L=g5_L,
g1_H=g5_H,
c1=c5,
c1s=c5s,
c1_sth=c5_sth,
c5_sth=c1_sth,
c1_skip=c5_skip,
c1_sth_init = c5_sth_init] endmodule

module Client6=Client1[p_1_1_L=p_6_1_L,p_1_1_H=p_6_1_H,p_1_2_L=p_6_2_L,p_1_2_H=p_6_2_H,p_1_3_L=p_6_3_L,p_1_3_H=p_6_3_H,
g1_L=g6_L,
g1_H=g6_H,
c1=c6,
c1s=c6s,
c1_sth=c6_sth,
c6_sth=c1_sth,
c1_skip=c6_skip,
c1_sth_init = c6_sth_init] endmodule

module Client7=Client1[p_1_1_L=p_7_1_L,p_1_1_H=p_7_1_H,p_1_2_L=p_7_2_L,p_1_2_H=p_7_2_H,p_1_3_L=p_7_3_L,p_1_3_H=p_7_3_H,
g1_L=g7_L,
g1_H=g7_H,
c1=c7,
c1s=c7s,
c1_sth=c7_sth,
c7_sth=c1_sth,
c1_skip=c7_skip,
c1_sth_init = c7_sth_init] endmodule

const int SERVER1 = 1;
const int SERVER2 = 2;
const int SERVER3 = 3;

const bool s1_init = true;
const bool s2_init = false;
const bool s3_init = false;

module Server1

	s1_sth : bool init s1_init;
	[update] !s1_sth & connected_client_has_sth -> (s1_sth'=true);
	[update] s1_sth | (!s1_sth & !connected_client_has_sth) -> true;
	[END] true -> true;

endmodule

formula connected_client_has_sth = ((c1s=SERVER1 & c1_sth) | (c2s=SERVER1 & c2_sth) | (c3s=SERVER1 & c3_sth) | (c4s=SERVER1 & c4_sth) | (c5s=SERVER1 & c5_sth) | (c6s=SERVER1 & c6_sth) | (c7s=SERVER1 & c7_sth));


module Server2=Server1[s1_sth=s2_sth,s2_sth=s1_sth,SERVER1=SERVER2,s1_init=s2_init] endmodule
module Server3=Server1[s1_sth=s3_sth,s3_sth=s1_sth,SERVER1=SERVER3,s1_init=s3_init] endmodule

