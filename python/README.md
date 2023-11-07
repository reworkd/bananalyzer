![Banner](public/banner.png)
<p align="center">
  <em>🍌 Open source AI Agent evaluations for web tasks 🍌</em>
</p>
<p align="center">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
</p>

<p align="center">
<a href="https://agentgpt.reworkd.ai">🔗 Main site</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://twitter.com/reworkdai">🐦 Twitter</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://discord.gg/gcmNyAAFfV">📢 Discord</a>
</p>

----
# Banana-lyzer
### Introduction
Banana-lyzer is an open source AI Agent evaluation framework and dataset for **web tasks** with Playwright.
We've created our own evals repo because:
- Websites change overtime, are affected by latency, and may have anti bot protections. We need a system that can reliably save and deploy historic/static snapshots of websites.  
- Standard web practices are loose and there is an abundance of different underlying ways to represent a single individual website. For an agent to best generalize, we require building a diverse dataset of websites across industries and use-cases.
- We have specific evaluation criteria and agent use cases focusing on structured and direct information retrieval across websites.  
- There exists valuable web task datasets and evaluations that we'd like to unify in a single repo ([Mind2Web](https://osu-nlp-group.github.io/Mind2Web/), [WebArena](https://webarena.dev/), etc).

### How does it work?
Banana-lyzer is a CLI tool that runs a set of evaluations against a set of websites. It will run each evaluation multiple times and output the results to a JSON file. The results can then be used to train an AI agent.
The package is separated into two parts, a web server that serves websites
We currently support the following types of websites: 
- Local static sites:
- Remote static sites: 
- Remote dynamic sites: Typical consumer facing websites today. 

Note that this repo is very much a work in progress,

# Getting Started
### Local testing installation
- `pip install ___`
- Implement the `agent_runner.py` interface and make a banalyzer.py test file
- Run `bananalyze ./tests/banalyzer.py` to run the test suite again

### Arguments
- `-h` or `--headless`: Run Playwright headless mode

### Adding evaluations
To add a snaps

# Roadmap
##### Launch
- [x] Functions to serve local MHTML sites
- [x] Agent interface required for running the tool
- [ ] Pytest wrapper to enable CLI testing with additional arguments
- [ ] Document a majority of the repo

##### Features
- [ ] Ability to save 
- [ ] Translate WebArena evals
- [ ] Translate Mind2Web evals
- [ ] Lag and bot detection emulation
- [ ] Updated test visualization with separation of categories and outputs


##### Dataset updates
- [ ] 15 additional data retrieval evals
- [ ] 15 click evals
- [ ] 15 navigation evals
- [ ] Tests requiring multi-step navigation
- [ ] Tests requiring both navigation and data retrieval
- [ ] Tests requiring pop-up closing
- [ ] Tests requiring sign-in
- [ ] Tests requiring captcha solving





# Citations
```
bibtex
@misc{reworkd2023bananalyzer,
  title        = {Bananalyzer},
  author       = {Asim Shrestha and Adam Watkins and Rohan Pandey and Srijan Subedi},
  year         = {2023},
  howpublished = {GitHub},
  url          = {https://github.com/reworkd/bananalyzer}
}
```
