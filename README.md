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
Open source AI Agent evaluation framework for web tasks with Playwright. Also has a banana theme because why not? 🍌
Repo provides the code to statically host sites, the evaluations to test against, and a simple pytest wrapper for actually running the evaluations. Focus currently is on measuring timing and functional correctness.

### Bananalyzer
Why make our own evals Repo? Don't want to be coupled to existing non-web-specific evals. We also do not care for fuzzy matching answers. It is for direct answers only based on evaluating HTML content, current web page, and retrieved data.

Issues is that web pages are slow and difficult to test. Curates a collection of sites that and evals for our current use cases. Today we focus on tasks involving multi-step page navigation and single page data retrieval.
Care only about structured output through information directly from the websites. 

### How does it work?
Banalyzer is a CLI tool that runs a set of evaluations against a set of websites. It will run each evaluation multiple times and output the results to a JSON file. The results can then be used to train an AI agent.
The package is separated into two parts, a web server that serves websites
We currently support the following types of websites: 
- Local static sites:
- Remote static sites: 
- Remote dynamic sites: Typical consumer facing websites today. 

Note we use Async playwright

### Generalizable domain
Support for all website types. Issue with the web is that standard practices are so loose that there are an abundance of different underlying ways to represent a single individual website
Open-domain. By allowing agents to interact with the
web, we open up the world’s supply of websites as a rich
source of learning environments and application domains.
Since agents directly work with the UI, we can use existing
web infrastructure without designing specialized APIs.

# Getting Started
Section outlines how to get started with using the hosted package in a local project

### Installation
- `pip install ___`
- Implement the ____ interface and make a banalyzer.py test file
- Run `bananalyze ./tests/banalyzer.py`. By default it will run with the following arguments:
```
--headless --count 3 --live
```

### Arguments
- `--headless` - Run Playwright headless mode
- `--count` - Number of times to run each test
- `--numproccesses` - Number of processes to run in parallel
- `--debug` - Run in debug mode
- `--proxy` - Run with proxy
- `--website` - Only run tests for a specific website
- `--group` - Only run tests for a specific group
- `--id` - Only run tests for a specific test
- `--live` Will run tests that require access to live websites

# Contributing


# Dataset
Want to make an open state/observation space
### Model
```
{
    "id": "string",
    "commit-sha": "string",
    
}
```
### Categories
- Website
- Category
- Subcategory


### Extending available websites
TODO

### Extending available evals
TODO

# Roadmap
- [ ] Webserver serving static MHTML files
- [ ] Webserver serving dynamic sites
- [ ] Agent interface required for running the tool
- [ ] Pytest wrapper to enable CLI testing
- [ ] 25 Data retrieval evals
- [ ] Translate WebArena evals
- [ ] Translate Mind2Web evals
- [ ] Better visualization/separation of categories and outputs
- [ ] Multi-step navigation evals
- [ ] E2E tests requiring both navigation and data retrieval
- [ ] Tests requiring pop-up closing
- [ ] Lag emulation
- [ ] Tests requiring sign-in
- [ ] Tests requiring captcha solving

# Acknowledgements
### Web arena

### Mind to web

### Web shop

### Bananas
At some point we decided on a monkey theme.
