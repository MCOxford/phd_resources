#!/bin/bash

# Requires the development version of PRISM to perform model checking on IDTMCs
# Git repo can be cloned from: https://github.com/MCOxford/prism.git (checkout "abs_test" branch)

# IDTMC model checking (requires development version of PRISM)
prism min_7c_3s.pm prop1.props -const T=1:1:20 -exportresults min_7c_3s.res -javamaxmem 12g -ex;
prism min_6c_4s.pm prop1.props -const T=1:1:20 -exportresults min_6c_4s.res -javamaxmem 12g -ex;
prism min_5c_5s.pm prop1.props -const T=1:1:20 -exportresults min_5c_5s.res -javamaxmem 12g -ex;
prism min_4c_6s.pm prop1.props -const T=1:1:20 -exportresults min_4c_6s.res -javamaxmem 12g -ex;

# ADTMC model checking (run in prism/prism)
PRISM_MAINCLASS=prism.AbstractionTest bin/prism ../adtmc-examples/min_7c_3s.pm -Xmx 12g;
PRISM_MAINCLASS=prism.AbstractionTest bin/prism ../adtmc-examples/min_6c_4s.pm -Xmx 12g;
PRISM_MAINCLASS=prism.AbstractionTest bin/prism ../adtmc-examples/min_5c_5s.pm -Xmx 12g;
PRISM_MAINCLASS=prism.AbstractionTest bin/prism ../adtmc-examples/min_4c_6s.pm -Xmx 12g;