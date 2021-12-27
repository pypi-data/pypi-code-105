"""Module for BPOs."""

from datetime import datetime
from typing import List, Optional
import bs4
from dateutil.parser import parse as _parsedate

try:
    import aiohttp
except ModuleNotFoundError:
    aiohttp = None
try:
    import requests
except ModuleNotFoundError:
    requests = None
BPO_BASE = "https://bugs.python.org/"
__version__ = "0.0.4a"


class error(Exception):
    """Base exception for bpolib related exception raising"""


class NotFound(error):
    """Raised when a message or issue could not be found.

    This is subclassed by MessageNotFound and IssueNotFound.
    """

    def __init__(self, id: int):
        self.id = id

    def __int__(self):
        return self.id


class MessageNotFound(NotFound):
    """Raised when a message could not be found."""


class IssueNotFound(NotFound):
    """Raised when an issue could not be found."""


class Base:
    """Serves as a base for BPO objects."""

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


class Message(Base):
    """An object to represent a message."""

    url: str
    message_number: int
    author: str
    recipients: List[str]
    date: datetime
    spambayes_score: Optional[float]
    marked_as_misclassified: bool
    message_id: str
    in_reply_to: str
    content: str

    def __repr__(self):
        return f"<msg#{self.message_number}, url='{self.url}'>"

    def __str__(self):
        return self.content

    def __int__(self):
        return self.message_number

    def __len__(self):
        return len(str(self))


class Issue(Base):
    """An object to represent an issue."""

    url: str
    title: str
    bpo_number: int
    type: Optional[str]
    stage: Optional[str]
    components: List[str]
    versions: List[str]
    status: str
    resolution: Optional[str]
    dependencies: List[str]
    superseder: Optional[str]
    assigned_to: Optional[str]
    nosy_list: List[str]
    priority: str
    keywords: List[str]
    messages: List[Message]
    message_count: int
    last_edited_at: datetime
    created_at: datetime
    author: str
    last_editor: str

    attrs = (
        "url",
        "title",
        "bpo_number",
        "type",
        "stage",
        "components",
        "versions",
        "status",
        "resolution",
        "dependencies",
        "superseder",
        "assigned_to",
        "nosy_list",
        "priority",
        "keywords",
        "messages",
        "message_count",
        "last_edited_at",
        "created_at",
        "author",
        "last_editor",
    )

    def __int__(self):
        return self.bpo_number

    def __repr__(self):
        return f"<BPO {self.bpo_number}, url='{self.url}'>"

    def __str__(self):
        return f"bpo-{self.bpo_number}"

    @property
    def messages(self):
        if self._messages is None:
            raise ValueError(
                "message cache has not yet been fetched, fetch with Issue.get_messages() or Issue.fetch_messages()"
            )
        return self._messages

    @property
    def message_count(self):
        self.messages  # this will just raise exception that we want
        return self._message_count

    def get_messages(self) -> List[Message]:
        """Get all the messages for this issue. This requires the requests module.
        This sets the message and message_count attributes.

        Returns
        -------
        List[Message]
            All the Message objects.
        """
        soup = self._soup
        message_numbers = map(
            lambda x: int(x.a.text[3:]), soup.find(class_="messages").find_all("tr")[1::2]
        )
        messages = list(map(get_message, message_numbers))
        self._messages = messages
        self._message_count = len(messages)
        return messages

    async def fetch_messages(self) -> List[Message]:
        """Get all the messages asynchronously for this issue. This requires the aiohttp module.
        This sets the message and message_count attributes.

        Returns
        -------
        List[Message]
            All the Message objects.
        """
        soup = self._soup
        message_numbers = map(
            lambda x: int(x.a.text[3:]), soup.find(class_="messages").find_all("tr")[1::2]
        )
        messages = [await m for m in map(fetch_message, message_numbers)]
        self._messages = messages
        self._message_count = len(messages)
        return messages


def _create_list(text):
    r = text.strip().split(", ")
    return r if r != [""] else []


def _create_message_request(msg_no):
    return _create_synchronous_request("message", format_message_url(msg_no))


def _create_issue_request(issue_no):
    return _create_synchronous_request("issue", format_issue_url(issue_no))


def _create_async_message_request(msg_no):
    return _create_asynchronous_request("message", format_message_url(msg_no))


def _create_async_issue_request(issue_no):
    return _create_asynchronous_request("issue", format_issue_url(issue_no), issue_no)


def _create_synchronous_request(instance, endpoint) -> str:
    request = requests.get(endpoint)
    _check_request(instance, request)
    return request.text


async def _create_asynchronous_request(instance, endpoint, object_id) -> str:
    async with aiohttp.request("GET", endpoint) as request:
        _check_request(instance, request, object_id)
        return await request.text()


def _check_request(instance, request, object_id):
    if requests and isinstance(request, requests.Response):
        attr = "status_code"
    elif aiohttp and isinstance(request, aiohttp.ClientResponse):
        attr = "status"
    else:
        # this should never happen
        raise TypeError("receieved unrecognised request response object (%r)" % requests)
    if getattr(request, attr) != 200:
        if instance == "issue":
            exc_type = IssueNotFound
        elif instance == "message":
            exc_type = MessageNotFound
        else:
            raise ValueError("unknown instance '%s'" % instance)
        raise exc_type(object_id)


def format_issue_url(issue_number: int) -> str:
    """Format an issue URL from an issue number.
    This function does not also check if the URL exists.

    Parameters
    ----------
    issue_number: int
        The issue number for the issue.

    Returns
    -------
    str
        The issue's curated URL.
    """
    return BPO_BASE + f"issue{issue_number}"


def format_message_url(message_number: int) -> str:
    """Format an message URL from a message number.
    This function does not also check if the URL exists.

    Parameters
    ----------
    message_number: int
        The message number for the message.

    Returns
    -------
    str
        The message's curated URL.
    """
    return BPO_BASE + f"msg{message_number}"


def _parse_message_soup(soup: bs4.BeautifulSoup):
    td_all = tuple(map(lambda x: x.td.text, soup.find(class_="form").find_all("tr")))
    message_number = int(soup.title.text[9:15])
    ATTRS = {
        "url": format_message_url(message_number),
        "message_number": message_number,
        "author": td_all[0],
        "recipients": _create_list(td_all[1]),
        "date": _parsedate(td_all[2].replace(".", " ")),
        "spambayes_score": float(td_all[3]) if td_all[3] else None,
        "marked_as_misclassified": True if td_all[4] == "Yes" else False,
        "message_id": td_all[5] or None,
        "in_reply_to": td_all[6] or None,
        "content": soup.find(class_="messages").pre.text,
    }

    return Message(**ATTRS)


def _parse_issue_soup(soup: bs4.BeautifulSoup):
    content_body = soup.find(id="content-body")
    info_text = content_body.p.text
    lc = info_text.rfind(", last changed")
    td_all = tuple(map(lambda x: x.text, content_body.find_all("td")))
    bpo_number = int(soup.find(id="breadcrumb").text.strip()[5:])
    ATTRS = {
        "url": format_issue_url(bpo_number),
        "title": content_body.input.get("value"),
        "bpo_number": bpo_number,
        "type": td_all[1] or None,
        "stage": td_all[2] or None,
        "components": _create_list(td_all[3]),
        "versions": _create_list(td_all[4]),
        "status": td_all[5],  # this will always have a value
        "resolution": td_all[6] or None,
        "dependencies": _create_list(td_all[7]),
        "superseder": td_all[8].strip() or None,
        "assigned_to": td_all[9].strip() or None,
        "nosy_list": _create_list(td_all[10]),
        "priority": td_all[11],  # this will always have a value
        "keywords": _create_list(td_all[12]),
        "_soup": soup,
    }
    last_edited_at = _parsedate(dt := info_text[lc + 14 : lc + 14 + 16])
    created_at = _parsedate(info_text[11:27])
    author = info_text[31 : info_text.index(", last changed")]
    last_editor = (
        info_text[info_text.rfind(dt) + len(dt) + 5 :][
            slice(None, -1) if ATTRS["status"] != "closed" else slice(None, -27)
        ],
    )

    ATTRS["_messages"] = None  # private for property
    ATTRS["_message_count"] = None  # private for property
    ATTRS["last_edited_at"] = last_edited_at
    ATTRS["created_at"] = created_at
    ATTRS["author"] = author
    ATTRS["last_editor"] = last_editor

    return Issue(**ATTRS)


def get_issue(issue_number: int) -> Issue:
    """Fetch an issue from an issue number. This requires the requests module.

    Parameters
    ----------
    issue_number: int
        The issue number for the issue.

    Returns
    -------
    `Issue`
        The Issue object packed with attributes.
    """
    if requests is None:
        raise ImportError("the requests module is required for get_issue()")
    soup = bs4.BeautifulSoup(_create_issue_request(issue_number), "html.parser")
    return _parse_issue_soup(soup)


async def fetch_issue(issue_number: int) -> Issue:
    """Fetch an issue asynchronously from an issue number. This requires the aiohttp module.

    Parameters
    ----------
    issue_number: int
        The issue number for the issue.

    Returns
    -------
    `Issue`
        The Issue object packed with attributes.
    """
    if aiohttp is None:
        raise ImportError("the aiohttp module is required for fetch_issue()")
    text = await _create_async_issue_request(issue_number)
    soup = bs4.BeautifulSoup(text, "html.parser")
    return _parse_issue_soup(soup)


def get_message(message_number: int) -> Message:
    """Get a message from a message number. This requires the requests module.

    Parameters
    ----------
    message_number: int
        The message number for the message.

    Returns
    -------
    `Message`
        The Message object packed with attributes.
    """
    if requests is None:
        raise ImportError("the requests module is required for get_message()")
    soup = bs4.BeautifulSoup(_create_message_request(message_number), "html.parser")
    return _parse_message_soup(soup)


async def fetch_message(message_number: int) -> Issue:
    """Fetch a message asynchronously from a message number. This requires the aiohttp module.

    Parameters
    ----------
    message_number: int
        The message number for the message.

    Returns
    -------
    `Message`
        The Message object packed with attributes.
    """
    if aiohttp is None:
        raise ImportError("the aiohttp module is required for fetch_message()")
    text = await _create_async_message_request(message_number)
    soup = bs4.BeautifulSoup(text, "html.parser")
    return _parse_message_soup(soup)
