import subprocess
import mwparserfromhell
import xml.sax
import os
import gc
import re
import json
from datetime import datetime
from .cleanup import MonetaryCleanup

partition_dir = None

money_cleaner = MonetaryCleanup()


def humanize_date(match):
    formatted = datetime.strptime(match, '%Y/%m/%d')
    return formatted.strftime("%d %B, %Y")


def normalize_date(date: str) -> str:
    '''
    Given a date string, return a formatted version of the
    date in yyyy/mm/dd format
        Parameters:
            date : str - Date in yyyy/mm/dd format or yyyy/m/d format

        Returns:
            str - date in yyyy/mm/dd  format
    '''
    y, m, d = date
    if len(m) == 1:
        m = '0' + m
    if len(d) == 1:
        d = '0' + d
    date = f'{y}/{m}/{d}'
    return date


def str_to_list(string: str) -> list:
    '''
    Convert a comma-separated string to an array of strings
    '''
    if type(string) is not str:
        return string
    return [strng.strip() for strng in string.split(',')]


def normalize_str(value: str) -> str:
    '''
    Apply different kinds of normalization and cleanup strategies on a string
        Parameters:
            value: str      String to apply normalization/cleaning on

        Returns:
            str             Normalized string
    '''
    if type(value) is not str:
        return value

    value = value.strip()
    # remove links marked with [[ and ]] (Media Wiki template)
    if value.startswith('[[') or value.endswith(']]'):
        value = value.strip('[[').strip(']]')

    # remove any space at string start or end
    value = value.strip()
    # remove any , at string start or end
    if value.startswith(',') or value.endswith(','):
        value = value.strip(',')

    # remove line break tags
    value = value.replace('< br / >', ', ')\
                 .replace('< br/ >', ', ')\
                 .replace('< br >', ', ')
    # remove references marked with < ref > abcdefgh < /ref >
    value = re.sub(
        r'< ref ([a-zA-Z0-9\s]+=\s?\\?\"?.*?\\?\"?\s?)?\/?\s?>(.*< \/ref >)?',
        '',
        value
    )
    # remove comments
    value = re.sub(r'<\s?!--.*?--\s?>', '', value)
    # remove extra whitespace and remove new line feed
    value = value.replace(' , ', ',').replace('\n', '')
    # remove incomplete comment tags at start or end
    value = value.strip('< !--').strip('-- >')
    # remove small tags as their content can be directly interpreted
    value = re.sub(r'<\s?small\s?>', '', value)
    value = re.sub(r'<\s?/\s?small', '', value)
    # remove & nbsp; from  value
    value = value.replace('& nbsp;', '')
    # remove extra spaces
    value = value.replace(' , ', ',').replace(' ( ', '(').replace(' ) ', ')')
    return value


def process_article(title, text, timestamp, template='Infobox film'):
    """Process a wikipedia article looking for template"""

    # Create a parsing object
    wikicode = mwparserfromhell.parse(text)

    # Search through templates for the template
    matches = wikicode.filter_templates(matches=template)

    # Filter out errant matches
    matches = [x for x in matches
               if x.name.strip_code().strip().lower() == template.lower()]

    if len(matches) >= 1:
        # template_name = matches[0].name.strip_code().strip()
        properties = {}
        # Extract information from infobox
        for param in matches[0].params:
            # based on
            exp_match = re.search(r'{{based on.*''(.*)''.*}}',
                                  str(param.value), flags=re.I)
            if exp_match:
                source_name, creator_name, val = None, None, None
                based_on_phrases = re.search(r"''(.*?)''.*(?=\|)\|(.*)}}",
                                             str(param.value), flags=re.I)
                if based_on_phrases:
                    source_name = based_on_phrases.group(1)
                    creator_name = based_on_phrases.group(2).split('|')
                    source_name = normalize_str(source_name)
                    names = []
                    for name in creator_name:
                        names.append(normalize_str(name))

                if source_name and names:
                    val = '{0} by {1}'.format(source_name, ', '.join(names))

                properties[param.name.strip_code().strip()] = val or ''

            # Releases
            exp_match = re.search(r'{{film date\s?\|(df=.*?\|)?(.*?)}}',
                                  normalize_str(str(param.value)), flags=re.I)
            if exp_match:
                film_date = exp_match.group(2)
                date = ''
                releases = re.findall(r'\d{4}\|\d{1,2}\|\d{1,2}', film_date)
                properties[param.name.strip_code().strip()] = []
                y, m, d, loc = '', '', '', ''
                if len(releases) > 1:
                    # regex to match 2002|09|12|
                    # [[Toronto International Film Festival|Toronto]]
                    # |2002|09|12|Toronto International Film Festival|Toronto
                    release_dates = re.findall(
                        r'(\d{4})\|(\d{1,2})\|(\d{1,2})',
                        film_date
                    )
                    locs = re.findall(r'(?<!\d)[a-zA-Z\s\\|<>\/&]+(?!\d)',
                                      film_date)

                    for release_date, loc in list(zip(release_dates, locs)):
                        date = normalize_date(release_date)
                        properties[param.name.strip_code().strip()].append({
                            'date': date,
                            'location': normalize_str(loc)
                        })

                else:
                    try:
                        release_date = re.findall(
                            r'(\d{4})\|(\d{1,2})\|(\d{1,2})|(\d{4})',
                            film_date
                        )[0]
                    except Exception:
                        print('An error occured')
                        continue
                    loc = re.findall(r'(?<!\d)[a-zA-Z\s\\|<>\/&]+(?!\d)',
                                     film_date)
                    if len([k for k in release_date if k]) == 1:
                        y = release_date[3]
                        if len(loc) == 0:
                            loc = ''
                    elif len(release_date) > 3:
                        y, m, d, loc = release_date
                    else:
                        y, m, d = release_date

                    if len(m) == 1:
                        m = '0' + m
                    if len(d) == 1:
                        d = '0' + d
                    date = '{0}/{1}/{2}'.format(y, m, d)
                    if date.endswith('//'):
                        date = date[:-2]
                    properties[param.name.strip_code().strip()].append({
                            'date': date,
                            'location': normalize_str(loc)
                        })

            # Screenplay/Story/Dialogue

            exp_match = re.findall(
                r'([\w\s\]]+?)\((?=screenplay|story|dialogue)(\w+)\)',
                str(param.value),
                flags=re.I
            )
            exp_match_2 = re.search(
                r'Screenplay:\s,\s+([\w\s]+)|Dialogues?:\s,\s+([\w\s]+)',
                str(param.value),
                flags=re.I
            )
            if exp_match or exp_match_2:
                # has story or screenplay  or dialogue in the value
                exp_match = re.findall(
                    r'([\w\s\]]+?)\((?=screenplay|story|dialogue)(\w+)\)',
                    str(param.value),
                    flags=re.I
                )
                if len(exp_match) > 0:
                    for match in exp_match:
                        person, label = match
                        properties[normalize_str(label)] =\
                            normalize_str(person)

                else:
                    exp_match = re.search(
                        r'Screenplay:\s,\s+([\w\s]+)|Dialogues?:\s,\s+([\w\s]+)',
                        str(param.value),
                        flags=re.I
                    )
                    if exp_match:
                        screenplay = exp_match.group(1)
                        dialogue = exp_match.group(2)
                        if screenplay:
                            properties['screenplay'] =\
                                normalize_str(screenplay)
                        if dialogue:
                            properties['dialogue'] = normalize_str(dialogue)

            # Gross collection / Budget

            key = normalize_str(param.name.strip_code().strip())
            if key == 'gross' or key == 'budget':
                try:
                    value = value.replace(',', '')
                    if '-' in value:
                        print(
                            f'name: {properties["name"]} , original: {value}'
                        )
                    value = money_cleaner.remove_equivalent_amt(value)
                    value = money_cleaner.large_num_names(value)
                    value = money_cleaner.extract_series_collection(value)
                    value = money_cleaner.extract_estimated_amount(value)
                    value = money_cleaner.money(value)
                    
                    properties[key] = value
                except Exception as e:
                    print(e)

            # default config
            else:
                if param.value.strip_code().strip():
                    value: str = param.value.strip_code().strip()
                    value = normalize_str(value)
                    key = normalize_str(param.name.strip_code().strip())
                    if '.' in key:
                        key = key.replace('.', '')
                    if ',' in value and (key != 'name'
                                         or key != 'gross'
                                         or key != 'budget'):
                        properties[key] = str_to_list(value)

                    else:
                        properties[key] = value
        # Infobox params sometimes dont contain 'name'
        if not properties.get('name', None):
            properties['name'] = title
        return {title: properties}


class WikiXmlHandler(xml.sax.handler.ContentHandler):
    """Parse through XML data using SAX"""
    def __init__(self):
        xml.sax.handler.ContentHandler.__init__(self)
        self._buffer = None
        self._values = {}
        self._current_tag = None
        self._films = {}
        self._article_count = 0
        self._non_matches = []

    def characters(self, content):
        """Characters between opening and closing tags"""
        if self._current_tag:
            self._buffer.append(content)

    def startElement(self, name, attrs):
        """Opening tag of element"""
        if name in ('title', 'text', 'timestamp'):
            self._current_tag = name
            self._buffer = []

    def endElement(self, name):
        """Closing tag of element"""
        if name == self._current_tag:
            self._values[name] = ' '.join(self._buffer)

        if name == 'page':
            self._article_count += 1
            # Search through the page to see if the page is a book
            film = process_article(**self._values, template='Infobox film')
            # Append to the list of books
            if film:
                self._films.update(film)


processed = 0


def find_films(data_path, partition_dir, limit=None, save=True):
    """Find all the film articles from a compressed wikipedia XML dump.
       `limit` is an optional argument to only return a set number of films.
        If save, films are saved to partition directory based on file name"""

    # Object for handling xml
    handler = WikiXmlHandler()
    global processed

    # Parsing object
    parser = xml.sax.make_parser()
    parser.setContentHandler(handler)

    # Iterate through compressed file
    print(f'Working with {data_path}')
    try:
        # Split operations for brevity
        # Works exactly the same
        lines = subprocess.Popen(['bzcat'],
                                 stdin=open(data_path),
                                 stdout=subprocess.PIPE).stdout
        for i, line in enumerate(lines):
            parser.feed(line)
            # Optional limit
            # if limit is not None and len(handler._films) >= limit:
            #     return handler._films

        if save:
            processed += 1
            # Create file name based on partition name
            p_str = os.path.splitext(data_path.split('/')[-1])[0]
            out_dir = os.path.join(partition_dir, f'{p_str}.json')

            # Create extraction directory if not exist
            if not os.path.isdir(partition_dir):
                os.mkdir(partition_dir)
            # Open the file
            with open(out_dir, 'w') as fout:
                # Write as json
                fout.write(json.dumps(handler._films) + '\n')

            print(f'{processed} files processed- {p_str}.json')
    except StopIteration:
        return
    except xml.sax.SAXParseException:
        print(f'Encountered Parse exception in {data_path}')
        return

    # Memory management
    del handler
    del parser
    gc.collect()
    return None
