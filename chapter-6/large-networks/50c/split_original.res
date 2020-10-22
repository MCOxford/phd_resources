P=? [ F<=T1*102 "detect" ]:
T1	Result
1	0.016
2	0.1065
3	0.452
4	0.8205
5	0.945
6	0.976
7	0.9905
8	0.9965
9	0.9995
10	0.9995
11	0.9995
12	0.9995
13	1.0
14	1.0
15	1.0
16	1.0
17	1.0
18	1.0
19	1.0
20	1.0

R{"client_proportion_old"}=? [ I=T2*102 ]:
Result
0.5531400000000013

R{"client_proportion_real"}=? [ I=T2*102 ]:
Result
0.22257000000000104

R{"client_proportion_fake"}=? [ I=T2*102 ]:
Result
0.20818999999999965

R{"log_connections_STHOnly"}=? [ C<=T2*102 ]:
Result
27.5575

R{"log_connections_STHAndProof"}=? [ C<=T2*102 ]:
Result
6.252
