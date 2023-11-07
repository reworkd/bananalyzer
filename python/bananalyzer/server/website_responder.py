from abc import ABC, abstractmethod
from pathlib import Path

from bananalyzer.data.examples import get_examples_path
from bananalyzer.data.schemas import Example


class WebsiteResponder(ABC):
    """
    Abstract class dealing with returning a website response
    """

    @abstractmethod
    def get_url(self, example: Example) -> str:
        """
        Get the website response
        """
        raise NotImplementedError("get_url not implemented")


class MHTMLWebsiteResponder(WebsiteResponder):
    """
    Return local MHTML files as the response. MHTML is a format that embeds all resources in a single file.
    Ideally this would be hosted by a webserver but browsers like chrome don't support MHTML
    """

    def __init__(self, data_path: Path):
        super().__init__()
        self.data_path = data_path

    def get_url(self, example: Example) -> str:
        mhtml_path = self.data_path / example.id / "index.mhtml"
        return f"file://{mhtml_path.as_posix()}"


class HostedWebsiteResponder(WebsiteResponder):
    """
    Some stable environments are already hosted on a stable server (WebArena) so we can just return the URL directly.
    """

    def get_url(self, example: Example) -> str:
        return example.url


def get_website_responder(example: Example) -> WebsiteResponder:
    if example.source == "mhtml":
        return MHTMLWebsiteResponder(get_examples_path())
    elif example.source == "hosted":
        return HostedWebsiteResponder()
    else:
        raise ValueError(f"Unknown example source {example.source}")
