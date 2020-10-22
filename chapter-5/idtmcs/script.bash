#!/bin/bash

# Requires the development version of PRISM to perform model checking on IDTMCs
# Git repo can be cloned from: https://github.com/MCOxford/prism.git (checkout "abs_test" branch)

javmem='10g';
prism normal_idtmc.prism normal_idtmc.props -const T=1:1:20 -cuddmaxmem 20g -javamaxmem ${javmem};
prism normal_ext_idtmc.prism normal_idtmc.props -const T=1:1:20 -cuddmaxmem 20g -javamaxmem ${javmem};
prism splitworld_idtmc.prism splitworld_idtmc.props -const T=1:1:20 -cuddmaxmem 20g -javamaxmem ${javmem};
prism splitworld_ext_idtmc.prism splitworld_idtmc.props -const T=1:1:20 -cuddmaxmem 20g -javamaxmem ${javmem};