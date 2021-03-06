# PhD Project Resources
This repository contains all the files, code an results used for the PhD thesis "Quantitative Verification of Gossip Protocols for Certificate Transparency".

## Summary of contents

* chapter-4 - PRISM models and results for chapter 4 (Modelling the Gossip Protocols).
* chapter-5 - PRISM models and results for chapter 5 (Tackling Uncertainty and Scalability using IDTMCs). To run PRISM for the models in this folder, you will need a forked version of PRISM which can be found [here](https://github.com/MCOxford/prism). At the moment, building IDTMCs can only be done using the explicit engine (```-ex``` option).
* chapter-6 - PRISM models and results for chapter 6 (Model Parameter Optimisation).
* python - [Python3](https://www.python.org/) source code: 
	* create-prism-models - Automatically create ```.prism``` files by providing the necessary model parameters and client data.
	* optimise-model - Use libraries designed for hyperparameter optimisation ([hyperopt](https://github.com/hyperopt/hyperopt), [benderopt](https://github.com/Dreem-Organization/benderopt)) to find suggested model parameters to produce 'bad' scenarios for gossip protocol properties. The libraries apply the tree-structured Parzen estimator approach (see [Bergstra et al](https://www.lri.fr/~kegl/research/PDFs/BeBaBeKe11.pdf)). Package requirements can be found in ```requirements.txt```.
	* prism-simulations - Randomly chooses client data from imported files to construct models and uses PRISM's statistical model checking capabilities to return approximated results. Contains both the artificial client data and results used for each chapter (for example, Chapter 4 data is given by ch4_data.py). Requires the ```PRISMModel``` class (found in ```create-prism-models/prism_model.py```) but the code should be able to import this automatically provided that you do not move the ```create-prism-models/``` directory.

## Related Work

Some of this work is also used in:
* M. Oxford, D. Parker and M. Ryan; _Quantitative Verification of Certificate Transparency Gossip Protocols_; In: _The Sixth International Workshop on Security and Privacy in the Cloud (SPC'20)_; July 2020; IEEE ([link](https://www.prismmodelchecker.org/papers/spc20.pdf)).

The gossip protocols we analyse take inspiration from:
* [RFC6962](https://tools.ietf.org/html/rfc6962) (this is expected to be superseded by [RFC6962-bis](https://datatracker.ietf.org/doc/draft-ietf-trans-rfc6962-bis/))
* B. Laurie; _Certificate Transparency_; In: _Communications of the ACM_; Volume 57, Issue 10; September 2014; p. 10 ([link](https://dl.acm.org/doi/fullHtml/10.1145/2659897))
* L. Chuat, P. Szalachowski, A. Perrig, B. Laurie, E. Messeri; _Efficient Gossip Protocols for Verifying the Consistency of Certificate Logs_; In: _The 18th Communications and Networking Simulation
Symposium (CNS’15)_; April 2015; IEEE ([link](https://arxiv.org/pdf/1511.01514.pdf))

Model checking was performed using the symbolic probabilistic model checker PRISM ([website](http://www.prismmodelchecker.org/), [github](https://github.com/prismmodelchecker/prism)).

Code for abstracting IDMTC (as well as DTMC) models can be found [here](https://github.com/MCOxford/prism/blob/abs_test/prism/src/prism/AbstractionTest.java).

## Acknowledgements

Many thanks to my doctoral supervisors [Prof. Dave Parker](www.cs.bham.ac.uk/~parkerdx) and [Prof. Mark Ryan](www.cs.bham.ac.uk/~mdr) for always giving me constructive feedback on my work and making time for me whenever I needed it. I also want to thank [Dr Eike Ritter](https://www.cs.bham.ac.uk/~exr/) for his input, viva examiners [Dr David Galindo](https://www.birmingham.ac.uk/staff/profiles/computer-science/galindo-david.aspx) and [Prof. Alice Miller](https://www.gla.ac.uk/schools/computing/staff/alicemiller/) for their recommendations and [Robert Hendley](https://www.cs.bham.ac.uk/~rjh/) for acting as chair.

Some of the verfication results we found was made possible thanks to the [University of Birmingham's BlueBEAR HPC service](http://www.birmingham.ac.uk/bear), which provides a High Performance Computing service to the University's research community.