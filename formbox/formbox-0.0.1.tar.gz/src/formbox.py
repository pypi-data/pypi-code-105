#!/usr/bin/env python
# Format mbox as HTML/XML
# Copyright (C) 2021  Nguyễn Gia Phong
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from argparse import ArgumentParser
from email.header import decode_header
from email.utils import parsedate_to_datetime
from functools import partial
from itertools import starmap
from mailbox import mbox
from pathlib import Path
from urllib.parse import quote

from bleach import clean, linkify
from markdown import markdown

sanitise = partial(clean, tags=('a', 'code', 'em', 'strong', 'sub', 'sup',
                                'blockquote', 'p', 'pre', 'ul', 'ol', 'li'),
                   protocols=('ftp', 'gemini', 'gopher', 'http', 'https',
                              'irc', 'ircs', 'mailto', 'matrix', 'xmpp'))


def extract(archive, parent):
    for message_id, message in archive.copy().items():
        # TODO: handle multipart
        if message['In-Reply-To'] != parent: continue
        archive.pop(message_id)
        yield message, extract(archive, message_id)


def decode(header):
    for string, charset in decode_header(header):
        encoding = 'utf-8' if charset is None else charset
        yield string.decode(encoding)


def render(template, forest, parent):
    for self, children in forest:
        message_id = self['Message-Id']
        date = parsedate_to_datetime(self['Date']).date().isoformat()
        author, address = decode(self['From'])
        body = sanitise(linkify(markdown(self.get_payload(),
                                         output_format='html5')))
        rendered_children = render(template, children, message_id)
        yield template.format(message_id=quote(message_id),
                              date=date, author=author, body=body,
                              children='\n'.join(rendered_children))


parser = ArgumentParser()
parser.add_argument('mbox')
parser.add_argument('id')
parser.add_argument('template', type=Path)
args = parser.parse_args()

archive = {m['Message-Id']: m for m in mbox(args.mbox)}
template = args.template.read_text()
print(*render(template, extract(archive, args.id), args.id), sep='', end='')
