dtmc

formula c1_connected_server_has_sth = (c1s=1 & s1_sth)|(c1s=2 & s2_sth)|(c1s=3 & s3_sth)|(c1s=4 & s4_sth)|(c1s=5 & s5_sth)|(c1s=6 & s6_sth);
formula c2_connected_server_has_sth = (c2s=1 & s1_sth)|(c2s=2 & s2_sth)|(c2s=3 & s3_sth)|(c2s=4 & s4_sth)|(c2s=5 & s5_sth)|(c2s=6 & s6_sth);
formula c3_connected_server_has_sth = (c3s=1 & s1_sth)|(c3s=2 & s2_sth)|(c3s=3 & s3_sth)|(c3s=4 & s4_sth)|(c3s=5 & s5_sth)|(c3s=6 & s6_sth);
formula c4_connected_server_has_sth = (c4s=1 & s1_sth)|(c4s=2 & s2_sth)|(c4s=3 & s3_sth)|(c4s=4 & s4_sth)|(c4s=5 & s5_sth)|(c4s=6 & s6_sth);
formula updated_client_gossips = (c1_sth & !c1_skip)|(c2_sth & !c2_skip)|(c3_sth & !c3_skip)|(c4_sth & !c4_skip);
formula nonupdated_client_gossips = (!c1_sth & !c1_skip)|(!c2_sth & !c2_skip)|(!c3_sth & !c3_skip)|(!c4_sth & !c4_skip);
formula s1_connected_client_has_sth = (c1s=1 & c1_sth)|(c2s=1 & c2_sth)|(c3s=1 & c3_sth)|(c4s=1 & c4_sth);
formula s2_connected_client_has_sth = (c1s=2 & c1_sth)|(c2s=2 & c2_sth)|(c3s=2 & c3_sth)|(c4s=2 & c4_sth);
formula s3_connected_client_has_sth = (c1s=3 & c1_sth)|(c2s=3 & c2_sth)|(c3s=3 & c3_sth)|(c4s=3 & c4_sth);
formula s4_connected_client_has_sth = (c1s=4 & c1_sth)|(c2s=4 & c2_sth)|(c3s=4 & c3_sth)|(c4s=4 & c4_sth);
formula s5_connected_client_has_sth = (c1s=5 & c1_sth)|(c2s=5 & c2_sth)|(c3s=5 & c3_sth)|(c4s=5 & c4_sth);
formula s6_connected_client_has_sth = (c1s=6 & c1_sth)|(c2s=6 & c2_sth)|(c3s=6 & c3_sth)|(c4s=6 & c4_sth);

formula abs_c1_sth = ((c1=2 & ( (!c1_sth & c1_connected_server_has_sth) | c1_sth )) | (c1!=2 & c1_sth)?1:0);
formula abs_c2_sth = ((c2=2 & ( (!c2_sth & c2_connected_server_has_sth) | c2_sth )) | (c2!=2 & c2_sth)?1:0);
formula abs_c3_sth = ((c3=2 & ( (!c3_sth & c3_connected_server_has_sth) | c3_sth )) | (c3!=2 & c3_sth)?1:0);
formula abs_c4_sth = ((c4=2 & ( (!c4_sth & c4_connected_server_has_sth) | c4_sth )) | (c4!=2 & c4_sth)?1:0);

formula abs_s1_sth = 0 + ( ( c1!=2 & s1_sth ) | ( c1=2 & (!s1_sth & s1_connected_client_has_sth) | s1_sth )?1:0);
formula abs_s2_sth = 0 + ( ( c1!=2 & s2_sth ) | ( c1=2 & (!s2_sth & s2_connected_client_has_sth) | s2_sth )?1:0);
formula abs_s3_sth = 0 + ( ( c1!=2 & s3_sth ) | ( c1=2 & (!s3_sth & s3_connected_client_has_sth) | s3_sth )?1:0);
formula abs_s4_sth = 0 + ( ( c1!=2 & s4_sth ) | ( c1=2 & (!s4_sth & s4_connected_client_has_sth) | s4_sth )?1:0);
formula abs_s5_sth = 0 + ( ( c1!=2 & s5_sth ) | ( c1=2 & (!s5_sth & s5_connected_client_has_sth) | s5_sth )?1:0);
formula abs_s6_sth = 0 + ( ( c1!=2 & s6_sth ) | ( c1=2 & (!s6_sth & s6_connected_client_has_sth) | s6_sth )?1:0);

formula abs_stage = 0 + (c1=1 & updated_client_gossips & !nonupdated_client_gossips?1:0) +
(c1=1 & !updated_client_gossips & nonupdated_client_gossips?2:0) +
(c1=1 & updated_client_gossips & nonupdated_client_gossips?3:0) +
(c1=1 & !updated_client_gossips & !nonupdated_client_gossips?4:0) +
(c1=2?5:0) +
(c1=3?6:0) +
(c1=4?7:0);

label "abs_t" = abs_c1_sth+abs_c2_sth+abs_c3_sth+abs_c4_sth=4 & abs_stage>=6;

const bool c1_sth_init = false;
const bool c2_sth_init = false;
const bool c3_sth_init = false;
const bool c4_sth_init = true;

prob g1_L = 0.2876788109081787;
prob g1_H = 0.3076788109081787;
prob g2_L = 0.765029295087822;
prob g2_H = 0.785029295087822;
prob g3_L = 0.5821679829751512;
prob g3_H = 0.6021679829751512;
prob g4_L = 0.6410260862748469;
prob g4_H = 0.6610260862748469;

prob p_1_1_L = 0.19917178299063518;
prob p_1_1_H = 0.2191717829906352;
prob p_1_2_L = 0.1037308509791929;
prob p_1_2_H = 0.1237308509791929;
prob p_1_3_L = 0.15080884482156656;
prob p_1_3_H = 0.17080884482156658;
prob p_1_4_L = 0.1064901924685903;
prob p_1_4_H = 0.1264901924685903;
prob p_1_5_L = 0.2014285891068043;
prob p_1_5_H = 0.22142858910680432;
prob p_1_6_L = 0.17836973963321054;
prob p_1_6_H = 0.19836973963321056;

prob p_2_1_L = 0.09700409758153493;
prob p_2_1_H = 0.11700409758153492;
prob p_2_2_L = 0.19776871583864786;
prob p_2_2_H = 0.21776871583864787;
prob p_2_3_L = 0.15009598535949756;
prob p_2_3_H = 0.17009598535949758;
prob p_2_4_L = 0.13463620440333096;
prob p_2_4_H = 0.15463620440333098;
prob p_2_5_L = 0.16265755120604788;
prob p_2_5_H = 0.1826575512060479;
prob p_2_6_L = 0.1978374456109408;
prob p_2_6_H = 0.21783744561094082;

prob p_3_1_L = 0.20503714360883182;
prob p_3_1_H = 0.22503714360883184;
prob p_3_2_L = 0.13133442342771795;
prob p_3_2_H = 0.15133442342771797;
prob p_3_3_L = 0.06149524129090283;
prob p_3_3_H = 0.08149524129090283;
prob p_3_4_L = 0.21724586861910541;
prob p_3_4_H = 0.23724586861910543;
prob p_3_5_L = 0.15053150394976228;
prob p_3_5_H = 0.1705315039497623;
prob p_3_6_L = 0.1743558191036796;
prob p_3_6_H = 0.1943558191036796;

prob p_4_1_L = 0.2342065694329987;
prob p_4_1_H = 0.2542065694329987;
prob p_4_2_L = 0.1443499990072954;
prob p_4_2_H = 0.1643499990072954;
prob p_4_3_L = 0.1170406227898683;
prob p_4_3_H = 0.1370406227898683;
prob p_4_4_L = 0.15142727782741935;
prob p_4_4_H = 0.17142727782741937;
prob p_4_5_L = 0.09893713153608356;
prob p_4_5_H = 0.11893713153608355;
prob p_4_6_L = 0.19403839940633463;
prob p_4_6_H = 0.21403839940633465;

module Client1

	c1 : [0..4] init 0;
	c1s : [0..6] init 0;
	c1_sth : bool init c1_sth_init;
	c1_skip : bool init false;
	[connect] c1=0 -> [g1_L, g1_H] : (c1'=1) + [1-g1_H, 1-g1_L] : (c1'=1) & (c1_skip'=true);
	[choose] c1_skip=false & c1=1 -> [p_1_1_L, p_1_1_H] : (c1'=2)&(c1s'=1) +
					 [p_1_2_L, p_1_2_H] : (c1'=2)&(c1s'=2) +
					 [p_1_3_L, p_1_3_H] : (c1'=2)&(c1s'=3) +
					 [p_1_4_L, p_1_4_H] : (c1'=2)&(c1s'=4) +
					 [p_1_5_L, p_1_5_H] : (c1'=2)&(c1s'=5) +
					 [p_1_6_L, p_1_6_H] : (c1'=2)&(c1s'=6);
	[choose] c1_skip=true & c1=1-> (c1'=2);
	[update] !c1_skip & c1=2 & connected_server_has_sth  -> (c1'=3) & (c1_sth'=true);
	[update] c1=2 & ((!c1_skip & !connected_server_has_sth) | c1_skip) -> (c1'=3);
	[round_complete] c1=3 & !clients_all_updated -> (c1'=0) & (c1s'=0) & (c1_skip'=false);
	[round_complete] c1=3 & clients_all_updated -> (c1'=4);
	[END] c1=4 -> true;

endmodule

formula connected_server_has_sth = ((c1s=1 & s1_sth) | (c1s=2 & s2_sth) | (c1s=3 & s3_sth) | (c1s=4 & s4_sth) | (c1s=5 & s5_sth) | (c1s=6 & s6_sth));
formula clients_all_updated = c1_sth&c2_sth&c3_sth&c4_sth;
label "clients_all_updated" = c1_sth&c2_sth&c3_sth&c4_sth;


module Client2=Client1[p_1_1_L=p_2_1_L,p_1_1_H=p_2_1_H,p_1_2_L=p_2_2_L,p_1_2_H=p_2_2_H,p_1_3_L=p_2_3_L,p_1_3_H=p_2_3_H,p_1_4_L=p_2_4_L,p_1_4_H=p_2_4_H,p_1_5_L=p_2_5_L,p_1_5_H=p_2_5_H,p_1_6_L=p_2_6_L,p_1_6_H=p_2_6_H,
g1_L=g2_L,
g1_H=g2_H,
c1=c2,
c1s=c2s,
c1_sth=c2_sth,
c2_sth=c1_sth,
c1_skip=c2_skip,
c1_sth_init = c2_sth_init] endmodule

module Client3=Client1[p_1_1_L=p_3_1_L,p_1_1_H=p_3_1_H,p_1_2_L=p_3_2_L,p_1_2_H=p_3_2_H,p_1_3_L=p_3_3_L,p_1_3_H=p_3_3_H,p_1_4_L=p_3_4_L,p_1_4_H=p_3_4_H,p_1_5_L=p_3_5_L,p_1_5_H=p_3_5_H,p_1_6_L=p_3_6_L,p_1_6_H=p_3_6_H,
g1_L=g3_L,
g1_H=g3_H,
c1=c3,
c1s=c3s,
c1_sth=c3_sth,
c3_sth=c1_sth,
c1_skip=c3_skip,
c1_sth_init = c3_sth_init] endmodule

module Client4=Client1[p_1_1_L=p_4_1_L,p_1_1_H=p_4_1_H,p_1_2_L=p_4_2_L,p_1_2_H=p_4_2_H,p_1_3_L=p_4_3_L,p_1_3_H=p_4_3_H,p_1_4_L=p_4_4_L,p_1_4_H=p_4_4_H,p_1_5_L=p_4_5_L,p_1_5_H=p_4_5_H,p_1_6_L=p_4_6_L,p_1_6_H=p_4_6_H,
g1_L=g4_L,
g1_H=g4_H,
c1=c4,
c1s=c4s,
c1_sth=c4_sth,
c4_sth=c1_sth,
c1_skip=c4_skip,
c1_sth_init = c4_sth_init] endmodule

const int SERVER1 = 1;
const int SERVER2 = 2;
const int SERVER3 = 3;
const int SERVER4 = 4;
const int SERVER5 = 5;
const int SERVER6 = 6;

const bool s1_init = true;
const bool s2_init = false;
const bool s3_init = false;
const bool s4_init = false;
const bool s5_init = false;
const bool s6_init = false;

module Server1

	s1_sth : bool init s1_init;
	[update] !s1_sth & connected_client_has_sth -> (s1_sth'=true);
	[update] s1_sth | (!s1_sth & !connected_client_has_sth) -> true;
	[END] true -> true;

endmodule

formula connected_client_has_sth = ((c1s=SERVER1 & c1_sth) | (c2s=SERVER1 & c2_sth) | (c3s=SERVER1 & c3_sth) | (c4s=SERVER1 & c4_sth));


module Server2=Server1[s1_sth=s2_sth,s2_sth=s1_sth,SERVER1=SERVER2,s1_init=s2_init] endmodule
module Server3=Server1[s1_sth=s3_sth,s3_sth=s1_sth,SERVER1=SERVER3,s1_init=s3_init] endmodule
module Server4=Server1[s1_sth=s4_sth,s4_sth=s1_sth,SERVER1=SERVER4,s1_init=s4_init] endmodule
module Server5=Server1[s1_sth=s5_sth,s5_sth=s1_sth,SERVER1=SERVER5,s1_init=s5_init] endmodule
module Server6=Server1[s1_sth=s6_sth,s6_sth=s1_sth,SERVER1=SERVER6,s1_init=s6_init] endmodule

