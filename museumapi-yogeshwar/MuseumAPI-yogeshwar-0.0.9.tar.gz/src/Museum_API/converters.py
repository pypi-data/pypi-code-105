import csv
import logging
import pandas as pd
import pdfkit
import os


def flatten(obj, keys):
    """
     It will flatten the dictionary object specified in the argument
     :param obj: object to be flattened
     :param keys: list of keys which are not flattened by default
     :return: reference of flattened object
    """
    for key in keys:
        values = obj[key]
        if values:
            for value in values:
                for k, v in value.items():
                    obj[k] = v
            del obj[key]
    return obj


class Converter:
    """
    converter class to convert a list of dictionary objects to various formats
    """
    @staticmethod
    def convert_to_csv(object_list, field_names, path):
        """
        converts list of dictionary objects to csv
         param object_list: list containing dictionary objects
         param field_names: list of field names
         param path: output path of generated csv
        """
        if object_list is None:
            raise TypeError("object_list cannot be none")
        if not isinstance(object_list, list) or not isinstance(object_list[0], dict):
            raise TypeError("list of dictionaries is expected as input for object_list parameter")
        if path is None:
            raise TypeError("path cannot be none")
        if field_names is None:
            raise TypeError("field_names cannot be none")
        try:
            with open(path, 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=field_names)
                writer.writeheader()
                for obj in object_list:
                    d = {key: value for key, value in obj.items() if key in field_names}
                    writer.writerow(d)
        except PermissionError as pe:
            logging.error("Permission error occurred in convert_to_csv func : " + str(pe))
        except FileNotFoundError as fe:
            logging.error("FileNotFound error occurred in convert_to_csv func : " + str(fe))

    @staticmethod
    def convert_to_pdf(object_list, path):
        """
        converts list of dictionary objects to pdf
         : param object_list: list containing dictionary objects
         : param path: output path of generated pdf
        """
        if object_list is None:
            raise TypeError("object_list cannot be none")
        if not isinstance(object_list, list) or not isinstance(object_list[0], dict):
            raise TypeError("list of dictionaries is expected as input for object_list parameter")
        if path is None:
            raise TypeError("path cannot be none")
        try:
            df = pd.DataFrame(data=object_list)
            temp_html_filename = "temp.html"
            df.to_html(temp_html_filename)
            pdfkit.from_file(temp_html_filename, output_path=path,
                             options={"page-height": "1500", "page-width": "660"})
            os.remove(temp_html_filename)
        except PermissionError as pe:
            logging.error("Permission error occurred in convert_to_pdf func : " + str(pe))
        except FileNotFoundError as fe:
            logging.error("FileNotFound error occurred in convert_to_pdf func : " + str(fe))

    @staticmethod
    def convert_to_html(object_list, path):
        """
        converts list of dictionary objects to html
          : param object_list: list containing dictionary objects
         : param path: output path of generated html
        """
        if object_list is None:
            raise TypeError("object_list cannot be none")
        if not isinstance(object_list, list) or not isinstance(object_list[0], dict):
            raise TypeError("list of dictionaries is expected as input for object_list parameter")
        if path is None:
            raise TypeError("path cannot be none")
        try:
            df = pd.DataFrame(data=object_list)
            df.to_html(path)
        except PermissionError as pe:
            logging.error("Permission error occurred in convert_to_html func : " + str(pe))
        except FileNotFoundError as fe:
            logging.error("FileNotFound error occurred in convert_to_html func : " + str(fe))

    @staticmethod
    def convert_to_xml(object_list, path):
        """
        converts list of dictionary objects to xml
          : param object_list: list containing dictionary objects
         : param path: output path of generated xml
        """
        if object_list is None:
            raise TypeError("object_list cannot be none")
        if not isinstance(object_list, list) or not isinstance(object_list[0], dict):
            raise TypeError("list of dictionaries is expected as input for object_list parameter")
        if path is None:
            raise TypeError("path cannot be none")
        try:
            df = pd.DataFrame(data=object_list)
            df.to_xml(path)
        except PermissionError as pe:
            logging.error("Permission error occurred in convert_to_xml func : " + str(pe))
        except FileNotFoundError as fe:
            logging.error("FileNotFound error occurred in convert_to_xml func : " + str(fe))

    @staticmethod
    def convert_to_excel(object_list, path):
        """
        converts list of dictionary objects to excel
          : param object_list: list containing dictionary objects
         : param path: output path of generated excel
        """
        if object_list is None:
            raise TypeError("object_list cannot be none")
        if not isinstance(object_list, list) or not isinstance(object_list[0], dict):
            raise TypeError("list of dictionaries is expected as input for object_list parameter")
        if path is None:
            raise TypeError("path cannot be none")
        try:
            df = pd.DataFrame(data=object_list)
            df.to_excel(path)
        except PermissionError as pe:
            logging.error("Permission error occurred in convert_to_excel func : " + str(pe))
        except FileNotFoundError as fe:
            logging.error("FileNotFound error occurred in convert_to_excel func : " + str(fe))
