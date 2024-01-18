import pytest
from pytest_mock import MockFixture

from bananalyzer.data.schemas import Example
from bananalyzer.runner.website_responder import (
    HostedWebsiteResponder,
    MHTMLWebsiteResponder,
    get_website_responder,
)


def test_get_website_responder_with_mhtml_source(mocker: MockFixture) -> None:
    example: Example = mocker.Mock()
    example.source = "mhtml"

    responder = get_website_responder(example)

    assert isinstance(responder, MHTMLWebsiteResponder)


def test_get_website_responder_with_hosted_source(mocker: MockFixture) -> None:
    example: Example = mocker.Mock()
    example.source = "hosted"

    responder = get_website_responder(example)

    assert isinstance(responder, HostedWebsiteResponder)


def test_get_website_responder_with_unknown_source(mocker: MockFixture) -> None:
    example: Example = mocker.Mock()
    example.source = "unknown"

    with pytest.raises(ValueError):
        get_website_responder(example)
