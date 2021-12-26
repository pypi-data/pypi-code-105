from ..objects.post import Post
from ..objects.coordinates import Coordinates
from ..objects.pictures import Pictures
from ..objects.picture import Picture
from ..objects.picturesize import PictureSize
from ..objects.postlist import PostList
from ..objects.user import User
from ..objects.page import Page
from ..objects.rocket.room import Room
from ..objects.comment import Comment
from ..objects.rocket.message import Message
from ..objects.rocket.anonfields import AnonFields
from ..objects.rocket.rocketuser import RocketUser
from ..objects.rocket.channel import Channel
from ..objects.rocket.suggestedchannel import SuggestedChannel
from ...lib.rocket.notification import Notification
from ...lib.rocket.notificationpayload import NotificationPayload
from ...lib.rocket.notificationsender import NotificationSender
from ...lib.rocket.notificationmessage import NotificationMessage
from typing import Optional

def composePictures(obj: dict) -> Pictures:
    type: str = obj["type"]
    id: str = obj["id"]
    picturesJson: str = obj["data"]
    extraSmall: Optional[Picture]
    small: Optional[Picture]
    medium: Optional[Picture]
    large: Optional[Picture]
    extraLarge: Optional[Picture]
    original: Optional[Picture]
    try:
        extraSmallJson: dict = picturesJson["extraSmall"]
        sizeJson: dict = extraSmallJson["size"]
        size: PictureSize = PictureSize(sizeJson["width"], sizeJson["height"])
        extraSmall = Picture(
            extraSmallJson["url"],
            size
        )
    except KeyError:
        extraSmall = None
    try:
        smallJson: dict = picturesJson["small"]
        sizeJson: dict = smallJson["size"]
        size: PictureSize = PictureSize(sizeJson["width"], sizeJson["height"])
        small = Picture(
            smallJson["url"],
            size
        )
    except KeyError:
        small = None
    try:
        mediumJson: dict = picturesJson["medium"]
        sizeJson: dict = mediumJson["size"]
        size: PictureSize = PictureSize(sizeJson["width"], sizeJson["height"])
        medium = Picture(
            mediumJson["url"],
            size
        )
    except KeyError:
        medium = None
    try:
        largeJson: dict = picturesJson["large"]
        sizeJson: dict = largeJson["size"]
        size: PictureSize = PictureSize(sizeJson["width"], sizeJson["height"])
        large = Picture(
            largeJson["url"],
            size
        )
    except KeyError:
        large = None
    try:
        extraLargeJson: dict = picturesJson["extraLarge"]
        sizeJson: dict = extraLargeJson["size"]
        size: PictureSize = PictureSize(sizeJson["width"], sizeJson["height"])
        extraLarge = Picture(
            extraLargeJson["url"],
            size
        )
    except KeyError:
        extraLarge = None
    try:
        originalJson: dict = picturesJson["original"]
        sizeJson: dict = originalJson["size"]
        size: PictureSize = PictureSize(sizeJson["width"], sizeJson["height"])
        original = Picture(
            originalJson["url"],
            size
        )
    except KeyError:
        original = None
    return Pictures(type, id, extraSmall, small, medium, large, extraLarge, original)

def composeUser(obj: dict) -> User:
    photoJson: dict = obj["photo"]
    bannerJson: dict = obj["banner"]
    photo: Optional[Pictures] = None
    banner: Optional[Pictures] = None
    if photoJson != None:
        photo = composePictures(photoJson)
    if bannerJson != None:
        banner = composePictures(bannerJson)
    return User(obj["id"], obj["name"], photo, banner)

def composePage(obj: dict) -> Page:
    photoJson: dict = obj["photo"]
    bannerJson: dict = obj["banner"]
    photo: Optional[Pictures] = None
    banner: Optional[Pictures] = None
    if photoJson != None:
        photo = composePictures(photoJson)
    if bannerJson != None:
        banner = composePictures(bannerJson)
    return Page(
        obj["id"],
        obj["type"],
        obj["status"],
        obj["ownedBy"],
        obj["title"],
        obj["description"],
        photo,
        banner
    )

def composePostList(array: list, cursor: str) -> PostList[Post]:
    pList: PostList = PostList(cursor)
    for item in array:
        coordinatesJson: dict = item["coordinates"]
        coordinates: Coordinates = None
        if coordinatesJson != None:
            coordinates = Coordinates(
                coordinatesJson["latitude"],
                coordinatesJson["longitude"],
                coordinatesJson["zoom"]
            )
        photo: Pictures = None
        content: str = None
        isCreatedByPage: bool = item["isCreatedByPage"]
        authorJson: dict = item["author"]
        pageJson: dict = item["page"]
        author: User = None
        page: Page = None
        if authorJson != None:
            author = composeUser(authorJson)
        if pageJson != None:
            page = composePage(pageJson)
        contents = item["contents"]
        for c in contents:
            if c["type"] == "TEXT":
                content = c["data"]["value"]
            elif c["type"] == "IMAGE":
                photo = composePictures(c)
        post: Post = Post(
            item["id"],
            isCreatedByPage,
            item["status"],
            item["type"],
            coordinates,
            item["isCommentable"],
            item["hasAdultContent"],
            item["isAuthorHidden"],
            photo,
            content,
            author,
            page
        )
        pList.append(post)
    return pList

def composeRoom(obj: dict) -> Room:
    return Room(
        obj["_id"],
        obj["msgs"],
        obj["ts"],
        obj["_updatedAt"],
        obj["usernames"]
        )

def composeComment(obj: dict) -> Comment:
    contents: list = obj["contents"]
    content: str
    for c in contents:
        if c ["type"] == "TEXT":
            content = c["data"]["value"]
    return Comment(
        obj["id"],
        content,
        obj["authorId"],
        obj["createdAt"],
        obj["updatedAt"],
        obj["isAuthorHidden"],
        obj["replyToCommentId"],
        obj["replyToAuthorId"]
    )

def composeMessage(obj: dict) -> Message:
    user: dict = obj["u"]
    customFields: dict = user["customFields"]
    anonFields = AnonFields(
        customFields["anonym_id"],
        customFields["photoUrl"],
        customFields["registeredAt"]
    )
    author = RocketUser(
        user["_id"],
        user["username"],
        user["name"],
        anonFields
    )
    return Message(
        obj["_id"],
        obj["msg"],
        obj["alias"],
        obj["rid"],
        obj["ts"],
        obj["_updatedAt"],
        author
    )

def composeChannel(obj: dict) -> Channel:
    description: str
    try: description = obj["description"]
    except KeyError: description = None
    return Channel(
        obj["_id"],
        obj["name"],
        obj["fname"],
        obj["msgs"],
        obj["usersCount"],
        obj["ts"],
        obj["_updatedAt"],
        obj["country"],
        description
    )

def composeSuggestedChannelList(array: list) -> list[SuggestedChannel]:
    cList: list[SuggestedChannel] = list()
    for channel in array:
        description: str
        try: description = channel["description"]
        except KeyError: description = None
        cList.append(SuggestedChannel(
            channel["_id"],
            channel["lm"],
            channel["fname"],
            channel["msgs"],
            description
        ))
    return cList

def composeNotification(obj: dict) -> Notification:
    field = obj["fields"]["args"][0]
    payloadJson = field["payload"]
    senderJson = payloadJson["sender"]
    messageJson = payloadJson["message"]
    message = NotificationMessage(
        messageJson["msg"]
    )
    sender = NotificationSender(
        senderJson["_id"],
        senderJson["username"],
        senderJson["name"]
    )
    payload = NotificationPayload(
        payloadJson["_id"],
        payloadJson["rid"],
        sender,
        payloadJson["type"],
        message
    )
    return Notification(
        obj["msg"],
        obj["collection"],
        obj["id"],
        field["title"],
        field["text"],
        payload
    )