# Local Differential Priacy

## :warning: NOTE: This repo is deprecated and contains old (and mostly undocumented code) - Please see https://github.com/Samuel-Maddock/pure-LDP for an updated library that contains a large number of LPD implementations including Apple's CMS/HCMS and Google's RAPPOR for private frequency estimation :warning:

An implementation of various local differential privacy (LDP) techniques mainly focusing on algorithms outlined by Apple. 

The project aims to provide implementations of the most recent and practical algorithms for LDP. All algorithms will be implemented in Python 3. The project also serves as a way to compare and analyse these techniques in both performance and implementation by providing various simulations and benchmarks.

The repo aims to implement the following:
* Apple's LDP: [Paper](https://machinelearning.apple.com/docs/learning-with-privacy-at-scale/appledifferentialprivacysystem.pdf)
* Googles' RAPPOR: [Paper](http://arxiv.org/abs/1407.6981), [Repo](https://www.github.com/google/rappor)
* Extensions to Google's RAPPOR for heavy-hitters: [Paper](https://arxiv.org/abs/1503.01214)
* Implement two further LDP algorithms outlined in ["Practical Locally Private Heavy Hitters"](https://arxiv.org/abs/1707.04982)

A good introduction and brief survey of recent LDP algorithms is presented [here](https://arxiv.org/abs/1907.11908).

:warning: While most of the code is done, much of the code is undocumented :warning:

# TODO
- [ ] Misc: Documentation !!!
- [ ] Google: Implement the RAPPOR extension

# Resources
1) [Algorithmic Foundations of Differential Privacy](https://www.cis.upenn.edu/~aaroth/Papers/privacybook.pdf)
2) [Local Differential Privacy: a tutorial](https://arxiv.org/abs/1907.11908)
2) [Learning with Privacy at Scale by Apple](https://machinelearning.apple.com/docs/learning-with-privacy-at-scale/appledifferentialprivacysystem.pdf)
3) [RAPPOR repo](https://www.github.com/google/rappor)
4) [RAPPOR paper](http://arxiv.org/abs/1407.6981)
5) [Extensions to RAPPOR for heavy-hitters](https://arxiv.org/abs/1503.01214)
6) [BNST Paper: Practical Locally Private Heavy Hitters](https://arxiv.org/abs/1707.04982)
