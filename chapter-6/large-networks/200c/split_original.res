P=? [ F<=T1*402 "detect" ]:
T1	Result
1	0.0195
2	0.248
3	0.7535
4	0.918
5	0.964
6	0.978
7	0.989
8	0.995
9	0.9985
10	0.999
11	0.9995
12	1.0
13	1.0
14	1.0
15	1.0
16	1.0
17	1.0
18	1.0
19	1.0
20	1.0

R{"client_proportion_old"}=? [ I=T2*402 ]:
Result
0.6059624999999997

R{"client_proportion_real"}=? [ I=T2*402 ]:
Result
0.2917849999999999

R{"client_proportion_fake"}=? [ I=T2*402 ]:
Result
0.10005749999999893

R{"log_connections_STHOnly"}=? [ C<=T2*402 ]:
Result
88.264

R{"log_connections_STHAndProof"}=? [ C<=T2*402 ]:
Result
10.0215
