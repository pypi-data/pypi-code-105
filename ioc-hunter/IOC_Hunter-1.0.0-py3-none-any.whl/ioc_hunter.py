# -*- coding: utf-8 -*-
import re
import iocextract
import urllib.parse
from .ioc_types import *

# Text that might wrap an IOC, in format <start txt>, <end txt>
# So for example "(10.20.32.123)" -> "10.20.32.123"
WRAPPING_CHARS = [
    ("(", ")"),
    ("<", ">"),
    (";", ";"),
    ("[", "]"),
    ("-", "-"),
    ('"', '"')
]
SPLIT_EXPRESSIONS = []
for pair in WRAPPING_CHARS:
    re_str = r"\{start}([^<>\[\]\(\)]*)\{end}".format(start=pair[0], end=pair[1])
    SPLIT_EXPRESSIONS.append(re.compile(re_str))

# Order of this list determines the detection order, DO NOT CHANGE
# Generally, add new types to the top of this list
IOC_TYPES_SEARCH_ORDER = [
    'ssdeep',
    'sha256',
    'sha1',
    'md5',
    'email',
    'ipv4_public',
    'ipv4_private',
    'ipv6_public',
    'ipv6_private',
    'domain',
    'filename',
    'url',
    'unknown'
]

DEFANGABLE = ['domain', 'ipv4_private', 'ipv4_public', 'url']

IOC_PATTERNS = {
    'ipv4_public': IPv4PublicIOC(),
    'ipv4_private': IPv4PrivateIOC(),
    'ipv6_public': IPv6PublicIOC(),
    'ipv6_private': IPv6PrivateIOC(),

    'url': URLIOC(),
    'email': RegexIOC(r'^[\w%+.-]+@[A-Za-z0-9.-]+\.[a-z]{2,}$'),
    'md5': RegexIOC(r'^[a-fA-F0-9]{32}$'),
    'sha1': RegexIOC(r'^[a-fA-F0-9]{40}$'),
    'sha256': RegexIOC(r'^[a-fA-F0-9]{64}$'),
    'ssdeep': RegexIOC(r'^([1-9]\d*)(?!:\d\d($|:)):([\w+0-9\/]+):([\w+0-9\/]+)$'),
    'filename': FilenameIOC(),
    'domain': DomainIOC(),
    'unknown': AnyIOC()
}


def _unravel(value):
    """
    Pull out any strings that are wrapped by common separators (WRAPPIN_CHARS)
    :param value: The text to pull substrings out of.
    :return: A list of substrings that were found.
    """
    to_return = []
    for expression in SPLIT_EXPRESSIONS:
        match = expression.findall(value)
        if match:
            to_return.extend(match)
        else:
            continue
    return to_return


def _possible_entries(entry):
    """
    Pull out any substrings that are likely a single unit based on common syntax patterns.
    :param entry: The text to pull substrings out of.
    :return: A list of substrings that were found.
    """
    sub_entries = _unravel(entry)

    wrapping_txts = [
        (";", ";"),
        ("href=\"", "\""),
        ("alt=\"", "\""),
        ("<", ">,"),
    ]

    poss = []
    poss.extend(sub_entries)
    poss.append(entry)

    sub_strings = re.split("[<>]", entry)
    poss.extend(sub_strings)

    for start_txt, end_txt in wrapping_txts:
        starts_w = entry.startswith(start_txt)
        ends_w = entry.endswith(end_txt)
        if starts_w:
            poss.append(entry[len(start_txt):])
        if ends_w:
            poss.append(entry[:-len(end_txt)])
        if starts_w and ends_w:
            poss.insert(0, entry[len(start_txt):-len(end_txt)])  # Insert to beginning because of stripping

    return poss


def _defang_results(results):
    """
    Defang any IOC types that we can (see DEFANGABLE)
    :param results: A dictionary with the ioc type as the key and a list of iocs for each value.
    :return: The same as the results input, but any values that could be defanged are.
    """
    new_results = {}
    for key, value in results.items():
        if key in DEFANGABLE:
            new_value = []
            for ioc in value:
                new_value.append(iocextract.defang(ioc))
            new_results[key] = new_value
    results.update(new_results)
    return results


def parse_iocs(text, defang=False, whitelist_regex='', iocs_to_parse=None):
    """
    Extract all IOCs from the given text.
    :param text: A string to parse.
    :param defang: If True, defang any IOCs we can (see DEFANGABLE). If False, return IOCs in their fanged state.
    :param whitelist_regex: Any IOC matching this regex will be ignored
    :param iocs_to_parse: A list of IOC types to look for (see IOC_TYPES_SEARCH_ORDER for options)
    :return: A dictionary with the ioc type as the key and a list of iocs for each value.
    """
    if iocs_to_parse is not None:
        if len(iocs_to_parse) == 1 and iocs_to_parse[0] == 'all':
            iocs_to_parse = IOC_TYPES_SEARCH_ORDER
        for ioc in iocs_to_parse:
            if ioc not in IOC_TYPES_SEARCH_ORDER:
                raise ValueError(f"{ioc} is not a valid IOC type. Valid IOCs are: {', '.join(IOC_TYPES_SEARCH_ORDER)}")
    else:
        iocs_to_parse = IOC_TYPES_SEARCH_ORDER

    result = {}
    for key in iocs_to_parse:
        result[key] = []

    # emails will often enforce strict line limits, so IOCs can be split in half by a newline.
    # remove all linebreaks to avoid this issue.
    text2 = re.sub("[\n\r]+", "", text)
    text3 = urllib.parse.unquote(text2)
    text_chunks = set()
    for text_input in [text, text2, text3]:
        split_text = re.split(r"(\n| )", text_input)
        split_text = map(lambda x: x.strip("\r\t\n "), split_text)
        split_text = filter(lambda x: len(x) > 2, split_text)  # Strip out single chars
        text_chunks.update(split_text)

    # iocextract can find iocs that have been defanged.  They are refanged and added to the correct type.
    # Patched: iocextract has bug in yara regex for long strings causing exponential back string matches.
    # This chain call is the same as extract_iocs except yara is removed.  We tried doing a timeout on
    # the call that searched for yara, but the timeout wrapper wasn't windows compatible.

    if "url" in iocs_to_parse:
        text_chunks.update(iocextract.extract_urls(text, refang=True, strip=False))
    if {"ipv4_public", "ipv4_private", "ipv6_public", "ipv6_private"}.intersection(iocs_to_parse):
        text_chunks.update(iocextract.extract_ips(text, refang=True))
    if "email" in iocs_to_parse:
        text_chunks.update(iocextract.extract_emails(text, refang=True))
    if {'sha512', 'sha256', 'sha1', 'md5'}.intersection(set(iocs_to_parse)):
        text_chunks.update(iocextract.extract_hashes(text))

    for ioc in text_chunks:
        typ = type_ioc(ioc, iocs_to_parse)
        if typ != "unknown":
            result[typ].append(ioc)
        for test in _possible_entries(ioc):
            typ = type_ioc(test, iocs_to_parse)
            if typ != "unknown":
                result[typ].append(test)

    if 'domain' in iocs_to_parse:
        # Append domains from URLs to the domains result
        cleaned_urls = [re.sub("https?(://)?", "", urllib.parse.unquote(u)) for u in result["url"]]  # Strip schema
        cleaned_urls = [re.sub("[/?].*", "", u) for u in cleaned_urls]  # Strip excess /'s

        domain_validator = DomainIOC()
        for cleaned_url in cleaned_urls:
            if domain_validator.run(cleaned_url, check_tld=False):
                result["domain"].append(cleaned_url)

    # remove duplicates
    for k, v in result.items():
        result[k] = list(set(v))

    # Clear results based on whitelist
    if whitelist_regex:
        for ioc_typ in iocs_to_parse:
            ioc_list = []
            for ioc in result[ioc_typ]:
                if re.findall(whitelist_regex, ioc):
                    pass  # Found match, don't add to list
                else:
                    ioc_list.append(ioc)
            result[ioc_typ] = ioc_list
    if defang:
        result = _defang_results(result)
    return result


def is_ip(value):
    """
    Determine whether the given value is an IP address.
    :param value: A string.
    :return: True if value is an IP address, False if not.
    """
    versions = ["4", "6"]
    p_levels = ["public", "private"]
    for v in versions:
        for p_level in p_levels:
            if IOC_PATTERNS["ipv{}_{}".format(v, p_level)].run(value):
                return True
    return False


def type_ioc(ioc, types_to_find=None):
    """
    Determine what type of IOC a string is.
    :param ioc: The IOC to classify.
    :param types_to_find: A list of types you want to look for.
    :return: The type of the IOC as a string, (see IOC_TYPES_SEARCH_ORDER for options)
    """
    iocs = types_to_find if types_to_find is not None else IOC_TYPES_SEARCH_ORDER
    for pat_name in IOC_TYPES_SEARCH_ORDER:
        # The order that the types are checked in matters, so we need to iterate over IOC_TYPES
        if pat_name in iocs:
            if IOC_PATTERNS[pat_name].run(ioc):
                return pat_name
    return "unknown"
