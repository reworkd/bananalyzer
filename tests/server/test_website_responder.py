import pytest
from typing import Any

from bananalyzer.data.schemas import Example
from bananalyzer.server import get_website_responder
from bananalyzer.server.website_responder import (
    HostedWebsiteResponder,
    MHTMLWebsiteResponder,
)


def test_get_website_responder_with_mhtml_source(mocker: Any) -> None:
    example: Example = mocker.Mock()
    example.source = "mhtml"

    responder = get_website_responder(example)

    assert isinstance(responder, MHTMLWebsiteResponder)


def test_get_website_responder_with_hosted_source(mocker: Any) -> None:
    example: Example = mocker.Mock()
    example.source = "hosted"

    responder = get_website_responder(example)

    assert isinstance(responder, HostedWebsiteResponder)


def test_get_website_responder_with_unknown_source(mocker: Any) -> None:
    example: Example = mocker.Mock()
    example.source = "unknown"

    with pytest.raises(ValueError):
        get_website_responder(example)
