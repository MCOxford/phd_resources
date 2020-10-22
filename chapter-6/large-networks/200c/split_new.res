P=? [ F<=T1*404 "detect" ]:
T1	Result
1	0.1105
2	0.566
3	0.8595
4	0.9445
5	0.97
6	0.9885
7	0.9935
8	0.9965
9	0.9985
10	0.9995
11	0.9995
12	0.9995
13	0.9995
14	0.9995
15	1.0
16	1.0
17	1.0
18	1.0
19	1.0
20	1.0

R{"client_proportion_old"}=? [ I=T2*404 ]:
Result
0.5354849999999995

R{"client_proportion_real"}=? [ I=T2*404 ]:
Result
0.40163999999999894

R{"client_proportion_fake"}=? [ I=T2*404 ]:
Result
0.052707499999999095

R{"log_connections_STHOnly"}=? [ C<=T2*404 ]:
Result
99.799

R{"log_connections_STHAndProof"}=? [ C<=T2*404 ]:
Result
8.4665
