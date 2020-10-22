P=? [ F<=T1*204 "detect" ]:
T1	Result
1	0.1275
2	0.535
3	0.834
4	0.93
5	0.9655
6	0.983
7	0.99
8	0.995
9	0.998
10	0.999
11	0.9995
12	0.9995
13	0.9995
14	0.9995
15	0.9995
16	1.0
17	1.0
18	1.0
19	1.0
20	1.0

R{"client_proportion_old"}=? [ I=T2*204 ]:
Result
0.5345149999999992

R{"client_proportion_real"}=? [ I=T2*204 ]:
Result
0.4111149999999994

R{"client_proportion_fake"}=? [ I=T2*204 ]:
Result
0.06158000000000135

R{"log_connections_STHOnly"}=? [ C<=T2*204 ]:
Result
52.296

R{"log_connections_STHAndProof"}=? [ C<=T2*204 ]:
Result
5.1745
