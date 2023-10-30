![asd](./misc/banner.png)
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

# Bananalyzer
Open source AI Agent evaluation framework for web tasks with Playwright. Also has a banana theme because why not? 🍌
Repo provides the code to statically host sites, the evaluations to test against, and a simple pytest wrapper for actually running the evaluations. Focus currently is on measuring timing and functional correctness.

Why make our own evals Repo? Don't want to be coupled to existing non-web-specific evals. We also do not care for fuzzy matching answers. It is for direct answers only based on evaluating HTML content, current web page, and retrieved data.

Issues is that web pages are slow and difficult to test. Curates a collection of sites that and evals for our current use cases. Today we focus on tasks involving multi-step page navigation and single page data retrieval.  



# Arguments
- `--headless` - Run Playwright headless mode
- `--count` - Number of times to run each test
- `--numproccesses` - Number of processes to run in parallel
- `--debug` - Run in debug mode
- `--proxy` - Run with proxy
- `--website` - Only run tests for a specific website
- `--group` - Only run tests for a specific group
- `--id` - Only run tests for a specific test
- `--live` Will run tests that require access to live websites

# Getting Started
- `pip install ___`
- Implement the ____ interface and make a banalyzer.py test file
- Run `bananalyze ./tests/banalyzer.py`. By default it will run with the following arguments:
```
--headless --count 3 --live
```

# Adding evaluations to existing sites
TODO

# Adding new websites
TODO

# Plans
- [ ] Navigation evals
- [ ] Data retrieval evals
- [ ] Interface to implement for testing
- [ ] Pytest wrapper
- [ ] Lag emulation
- [ ] E2E tests requiring both navigation and data retrieval
- [ ] Tests requiring sign-in
- [ ] Tests requiring captcha solving
- [ ] Tests requiring pop-up closing

# Acknowledgements
- Web Arena
- Web Shop
- Bananas
