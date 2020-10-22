P=? [ F<=T1*202 "detect" ]:
T1	Result
1	0.0185
2	0.163
3	0.6505
4	0.9055
5	0.9635
6	0.984
7	0.9895
8	0.9955
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

R{"client_proportion_old"}=? [ I=T2*202 ]:
Result
0.5964949999999997

R{"client_proportion_real"}=? [ I=T2*202 ]:
Result
0.26266999999999985

R{"client_proportion_fake"}=? [ I=T2*202 ]:
Result
0.14351999999999895

R{"log_connections_STHOnly"}=? [ C<=T2*202 ]:
Result
46.5415

R{"log_connections_STHAndProof"}=? [ C<=T2*202 ]:
Result
7.9845
