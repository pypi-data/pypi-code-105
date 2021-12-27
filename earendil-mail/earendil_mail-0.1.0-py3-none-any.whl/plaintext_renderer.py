"""Functionality for converting Markdown-formatted text into human-readable form."""

import re

__unescaped_emphasis = re.compile(r"(?<!\\)(?:\\{2})*(\*|#)")
__hyperlink = re.compile(r"\[(.+)\]\((.+)\)")


def __convert_markdown_line(line: str) -> str:
    # Remove leading and trailing whitespace.
    line = line.strip()

    # Remove hashtags representing headings.
    heading_count = 0
    for i in range(7):
        if i < len(line) and line[i] == "#":
            heading_count += 1
        else:
            break
    if heading_count < 7:
        line = line[heading_count:]
        line = line.strip()

    # Remove unescaped asterisks used for emphasis.
    line = re.sub(__unescaped_emphasis, lambda match: match.group(0)[:-1], line)

    # Convert hyperlinks into URLs in parentheses.
    line = re.sub(__hyperlink, lambda match: f"{match.group(1)} ({match.group(2)})", line)

    return line


def markdown_to_plaintext(text: str) -> str:
    """Converts the given Markdown string to plaintext.

    Args:
        text: Possibly multi-line string of Markdown-formatted text.

    Returns:
        Plaintext version of text, with extra formatting stripped out.
    """
    lines = text.split("\n")

    # Remove consecutive lines of whitespace.
    trimmed_lines = [line for i, line in enumerate(lines) if i == 0 or line != lines[i - 1] or line != ""]

    new_lines = []
    for line in trimmed_lines:
        new_lines.append(__convert_markdown_line(line))

    return "\n".join(new_lines)
