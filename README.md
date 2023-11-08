![Banner](https://github.com/reworkd/bananalyzer/blob/main/public/banner.png?raw=true)
<p align="center">
  <em>🍌 Open source AI Agent evaluations for web tasks 🍌</em>
</p>
<p align="center">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" />
</p>

<p align="center">
<a href="https://reworkd.ai/">🔗 Main site</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://twitter.com/reworkdai">🐦 Twitter</a>
<span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
<a href="https://discord.gg/gcmNyAAFfV">📢 Discord</a>
</p>

----

# Banana-lyzer
### Introduction
Banana-lyzer is an open source AI Agent evaluation framework and dataset for **web tasks** with Playwright (And has a banana theme because why not).
We've created our own evals repo because:
- Websites change overtime, are affected by latency, and may have anti bot protections.
- We need a system that can reliably save and deploy historic/static snapshots of websites.  
- Standard web practices are loose and there is an abundance of different underlying ways to represent a single individual website. For an agent to best generalize, we require building a diverse dataset of websites across industries and use-cases.
- We have specific evaluation criteria and agent use cases focusing on structured and direct information retrieval across websites.  
- There exists valuable web task datasets and evaluations that we'd like to unify in a single repo ([Mind2Web](https://osu-nlp-group.github.io/Mind2Web/), [WebArena](https://webarena.dev/), etc).

https://github.com/reworkd/bananalyzer/assets/50181239/4587615c-a5b4-472d-bca9-334594130af1

### How does it work?
⚠️ Note that this repo is a work in progress. ⚠️

Banana-lyzer is a CLI tool that runs a set of evaluations against a set of example websites.
The examples are defined in [examples.py](https://github.com/reworkd/bananalyzer/blob/main/bananalyzer/data/examples.py) using a schema similar to [Mind2Web](https://osu-nlp-group.github.io/Mind2Web/) and [WebArena](https://webarena.dev/). The examples store metadata like the agent goal and the expected agent output in addition to snapshots of urls via mhtml to ensure the page is not changed over time. Note all examples today expect structured JSON output using data directly extracted from the page. 

The CLI tool will sequentially run examples against a user defined agent by dynamically constructing a pytest test suite and executing it.
As a user, you simply create a file that implements the `AgentRunner` interface and defines an instance of your AgentRunner in a variable called "agent".
AgentRunner exposes the example, and a playwright browser context to use.  

In the future we will support more complex evaluation methods and examples that require multiple steps to complete. The plan is to translate existing datasets like Mind2Web and WebArena into this format.

# Getting Started
### Local testing installation
- `pip install --dev bananalyzer`
- Implement the `agent_runner.py` interface and make a banalyzer.py test file (The name doesn't matter). Below is an example file
```
import asyncio
from playwright.async_api import BrowserContext
from bananalyzer.data.schemas import Example
from bananalyzer.runner.agent_runner import AgentResult, AgentRunner


class NullAgentRunner(AgentRunner):
    """
    A test agent class that just returns an empty string
    """

    async def run(
        self,
        context: BrowserContext,
        example: Example,
    ) -> AgentResult:
        page = await context.new_page()
        await page.goto(example.get_static_url())   # example.url has the real url, example.get_static_url() returns the local mhtml file url
        await asyncio.sleep(0.5)
        return example.evals[0].expected    # Just return expected output directly so that tests pass
```
- Run `bananalyze ./tests/banalyzer.py` to run the test suite

#### Arguments
- `-h` or `--headless`: Run with Playwright headless mode

### Contributing
#### Running the server
The project has a basic FastAPI server to expose example data. You can run it with the following command:
```
cd server
poetry run uvicorn server:app --reload   
```
Then travel to `http://127.0.0.1:8000/api/docs` in your browser to see the API docs.

#### Adding examples
All current examples have been manually added through running the `fetch.ipynb` notebook at the root of this project.
This notebook will load a site with Playwright and use the chrome developer API to save the page as an MHTML file.

# Roadmap
##### Launch
- [x] Functions to serve local MHTML sites
- [x] Agent interface required for running the tool
- [x] Pytest wrapper to enable CLI testing with additional arguments
- [x] Document a majority of the repo

##### Features
- [ ] Ability to add multiple site pages to examples
- [ ] Ability to add in-page actions to examples
- [ ] Translate WebArena evals
- [ ] Translate Mind2Web evals
- [ ] Lag and bot detection emulation
- [ ] Updated test visualization with separation of categories and outputs


##### Dataset updates
- [ ] 15 additional data retrieval examples
- [ ] 15 click examples
- [ ] 15 navigation examples
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
