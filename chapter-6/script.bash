#!/bin/bash

symm_h1=0;
symm_h2=7;

symm_s1=1;
symm_s2=6;

mem=30;

vh="model-checking/normal";
vs="model-checking/splitworld";

prism ${vh}/normal.prism ${vh}/normal.props -const T=1:1:20 -cuddmaxmem ${mem}g -symm ${symm_h1} ${symm_h2};
echo "normal.prism done";
prism ${vh}/normal_ext.prism ${vh}/normal_ext.props -const T=1:1:20 -cuddmaxmem ${mem}g -symm ${symm_h1} ${symm_h2};
echo "normal_ext.prism done";

for i in 5 50 100 200
do
	s="large-networks/${i}c";
	prism ${s}/normal_original.prism ${s}/normal_original.props -const T1=1:1:20 -sim -simpathlen 20000 -simsamples 2000;
	prism ${s}/normal_new.prism ${s}/normal_new.props -const T1=1:1:20 -sim -simpathlen 20000 -simsamples 2000;
	echo "normal sim ${i} done";
done

prism ${vs}/splitworld.prism ${vs}/splitworld.props -s -const T=1:1:20 -cuddmaxmem ${mem}g -symm ${symm_s1} ${symm_s2};
echo "split.prism done";
# Do each property separately for splitworld_ext - this takes a long time!
for i in 1 2 3 4 5 6
do
	prism ${vs}/splitworld_ext.prism ${vs}/splitworld_ext.props -m -prop ${i} -const T=1:1:20 -cuddmaxmem ${mem}g -symm ${symm_s1} ${symm_s2};
	echo "prop${i} done";
done
echo "split_ext.prism done";

for i in 5 50 100 200
do
	s="large-networks/${i}c";
	prism ${s}/split_original.prism ${s}/split_original.props -const T1=1:1:20 -sim -simpathlen 20000 -simsamples 2000;
	prism ${s}/split_new.prism ${s}/split_new.props -const T1=1:1:20 -sim -simpathlen 20000 -simsamples 2000;
	echo "split sim ${i} done";
done