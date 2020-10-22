#!/bin/bash

prism normal/normal.prism normal/normal.props -const T=1:1:20 -cuddmaxmem 20g -symm 1 6;
prism normal/normal_sim.prism normal/normal_sim.props -const T=1:1:20 -sim -simpathlen 20000 -simsamples 2000;

prism normal/normal_ext.prism normal/normal.props -const T=1:1:20 -cuddmaxmem 20g -symm 1 6;
prism normal/normal_ext_sim.prism normal/normal_ext_sim.props -const T=1:1:20 -sim -simpathlen 20000 -simsamples 2000;

prism splitworld/splitworld.prism splitworld/splitworld.props -const T=1:1:20 -cuddmaxmem 20g -symm 1 6;
prism splitworld/splitworld_sim.prism splitworld/splitworld_sim.props -const T=1:1:20 -sim -simpathlen 20000 -simsamples 2000;

prism splitworld/splitworld_ext.prism splitworld/splitworld.props -const T=1:1:20 -cuddmaxmem 20g -symm 1 6;
prism splitworld/splitworld_ext_sim.prism splitworld/splitworld_ext_sim.props -const T=1:1:20 -sim -simpathlen 20000 -simsamples 2000;