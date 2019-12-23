# Local Differential Priacy

An implementation of various local differential privacy (LDP) techniques mainly focusing on algorithms outlined by Apple. 

The project aims to provide implementations of the most recent and practical algorithms for LDP. All algorithms will be implemented in Python 3. The project also serves as a way to compare and analyse these techniques in both performance and implementation by providing various simulations and benchmarks.

The repo aims to implement the following:
* Apple's LDP: [Paper](https://machinelearning.apple.com/docs/learning-with-privacy-at-scale/appledifferentialprivacysystem.pdf)
* Googles's RAPPOR: [Paper](http://arxiv.org/abs/1407.6981), [Repo](https://www.github.com/google/rappor)
* Extensions to Google's RAPPOR for heavy-hitters: [Paper](https://arxiv.org/abs/1503.01214)
* Implement two further LDP algorithms outlined in ["Practical Locally Private Heavy Hitters"](https://arxiv.org/abs/1707.04982)

A good introduction and brief survey of recent LDP algorithms is presented [here](https://arxiv.org/abs/1907.11908).

:warning: This repo currently is very much WIP and much of the code is undocumented :warning:

# TODO
- [x] Apple: Implement Count-Mean-Sketch (CMS) and Hadamard Count-Mean-Sketch
- [x] Apple: Implement the Sequence Fragment Puzzle (SFP) Algorithm
- [x] Apple: Basic simulations for CMS, HCMS, SFP 
- [x] Google: Port over RAPPOR client-side from the RAPPOR repo (based on code [here](https://github.com/google/rappor/blob/master/client/python/rappor.py))
- [x] Google: Implement RAPPOR's server-side algorithm (based on code [here](https://github.com/google/rappor/tree/master/analysis/R))
- [ ] Google: Implement the RAPPOR extension
- [ ] Google: Simulations for RAPPOR + extensions
- [x] BNST: Implement TreeHistogram (based on code [here](https://bitbucket.org/abhradt/locallyprivatehistogram/src/master/))
- [x] BNST: Implement the Simple Bitstogram Protocol (ExplicitHist + SuccinctHist)
- [x] BNST: Implement the Full Bitstogram Protocol without error correcting codes
- [ ] BNST: Add error correcting codes to the Bitstogram algorithm
- [ ] BNST: Simulations for TreeHistogram and Bitstogram
- [ ] Misc: Documentation !!!
- [ ] Misc: Modularisation to support combining algorithms
- [ ] Misc: More concrete simulations/applications
- [ ] Misc: Finishing the README
# Resources
1) [Algorithmic Foundations of Differential Privacy](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)
2) [Local Differential Privacy: a tutorial](https://arxiv.org/abs/1907.11908)
2) [Learning with Privacy at Scale by Apple](https://machinelearning.apple.com/docs/learning-with-privacy-at-scale/appledifferentialprivacysystem.pdf)
3) [RAPPOR repo](https://www.github.com/google/rappor)
4) [RAPPOR paper](http://arxiv.org/abs/1407.6981)
5) [Extensions to RAPPOR for heavy-hitters](https://arxiv.org/abs/1503.01214)
6) [BNST Paper: Practical Locally Private Heavy Hitters](https://arxiv.org/abs/1707.04982)