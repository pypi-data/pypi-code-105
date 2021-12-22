import xmltodict
import json
import csv
from dict2xml import dict2xml
from io import StringIO
#import pandas as pd


def transform_to_dict(data, content_format):
    data = str(data)

    if content_format == 'json':
        parsed = json_to_dict(data)

    elif content_format == 'xml':
        parsed = xml_to_dict(data)

    elif content_format == 'csv':
        parsed = csv_to_dict(data)

    elif content_format == 'tsv':
        parsed = csv_to_dict(data, delimiter='\t')

    else:
        print("unknown input format")
        return None

    return parsed


def transform_to(data, output_format):

    if output_format == 'json':
        data = dict_to_json(data)

    elif output_format == 'xml':
        data = dict_to_xml(data)

    elif output_format == 'csv':
        data = dict_to_csv(data)
        print("skip csv output", data)
        # data = str(data)
    elif output_format == 'tsv':
        data = dict_to_csv(data, delimiter='\t')

    else:
        print("unknown output format")
        return None

    return data


def json_to_dict(json_data):
    return json.loads(json_data)


def xml_to_dict(xml_data):
    return xmltodict.parse(xml_data, dict_constructor=dict)


def csv_to_dict(csv_data, delimiter=','):  # could use pandas instead
    csv_data = StringIO(csv_data)
    csv_reader = csv.DictReader(csv_data, delimiter=delimiter)
    parsed = [row for row in csv_reader]

    return parsed[0]#{"items": parsed}

    if len(parsed) == 1:
        return {"items": parsed}
    # return parsed[0]  else parsed
    # alt. with pandas
    a = pd.read_csv(StringIO(csv_data))
    b = a.to_dict(orient='list')
    return b

def dict_to_csv(dict_data, delimiter=','):    
    csv_data = StringIO()
    try:
        writer = csv.DictWriter(csv_data, fieldnames=dict_data.keys(), delimiter=delimiter)
        writer.writeheader()
        writer.writerow(dict_data)
    except IOError:
        print("I/O error")
    except Exception as e:
        print("WHAT", e)
    
    return csv_data.getvalue()


def dict_to_json(dict_data):
    return json.dumps(dict_data)


def iterate_depth_of_dict(data):
    prev_value = None
    while True:
        prev_value = data
        data = get_first_value(data)

        if isinstance(data, str):
            return prev_value

        if isinstance(data, list):
            return data


def dict_to_csv2(dict_data):
    if isinstance(dict_data, dict):
        dict_data = iterate_depth_of_dict(dict_data)

    # normalized = pd.json_normalize(dict_data)
    # out = normalized.to_csv(index_label=False, index=False)
    # return out


def dict_to_xml(dict_data):
    wrap = None
    if isinstance(dict_data, dict):
        return dict2xml(dict_data, indent='  ', wrap="root")

    if isinstance(dict_data, list):  # if it's a list of dictionaries
        return NotImplementedError
        result = None

        xml_objects = []
        for _dict in dict_data:
            xml_objects.append(dict2xml(dict_data, wrap='item', indent='  '))

        result = '<?xml version="1.0" ?>\n<root>\n' + \
            "\t".join(xml_objects) + '\n</root>'
        return result


def get_first_value(dict: dict):
    return next(iter(dict.items()))[1]
