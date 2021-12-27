from commmons import html_from_url, get_host_url


def scrape(url):
    tree = html_from_url(url)
    host_url = get_host_url(url)

    divs = tree.xpath("//div[contains(@class, 'video-item')]")
    for div in divs:
        if "data-id" in div.attrib:
            dataid = div.attrib["data-id"]
            atags = div.xpath("./a[@class='n']")
            if atags:
                img = div.xpath("./a/picture/img")[0]
                yield {
                    "fileid": "sb" + dataid,
                    "sourceurl": host_url + atags[0].attrib["href"],
                    "filename": img.attrib["alt"],
                    "thumbnailurl": img.attrib["data-src"]
                }
