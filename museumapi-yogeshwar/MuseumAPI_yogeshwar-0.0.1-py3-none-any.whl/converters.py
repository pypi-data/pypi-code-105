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
    def __init__(self, objectlist):
        self.objectlist = objectlist

    def convert_to_csv(self, fnames):
        """
        converts list of dictionary objects to csv

         :param fnames: list of field names
        """
        try:
            with open("mymuseum.csv", 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fnames)
                writer.writeheader()
                for obj in self.objectlist:
                    d = {key: value for key, value in obj.items() if key in fnames}
                    writer.writerow(d)
        except PermissionError as pe:
            logging.error('Error occured in convert_to_csv func : ' + str(pe))

    def convert_to_pdf(self):
        """
        converts list of dictionary objects to pdf
        """
        try:
            df = pd.DataFrame(data=self.objectlist)
            temp_html_filename = 'temp.html'
            df.to_html(temp_html_filename)
            pdfkit.from_file(temp_html_filename, output_path="mymuseum.pdf",
                             options={'page-height': '1500', 'page-width': '660'})
            os.remove(temp_html_filename)
        except PermissionError as pe:
            logging.error('Error occured in convert_to_pdf func : ' + str(pe))

    def convert_to_html(self):
        """
        converts list of dictionary objects to html
        """
        try:
            df = pd.DataFrame(data=self.objectlist)
            df.to_html("myhtml.html")
        except PermissionError as pe:
            logging.error('Error occured in convert_to_html func : ' + str(pe))

    def convert_to_xml(self):
        """
        converts list of dictionary objects to xml
        """
        try:
            df = pd.DataFrame(data=self.objectlist)
            df.to_xml("myxml.xml")
        except PermissionError as pe:
            logging.error('Error occured in convert_to_xml func : ' + str(pe))

    def convert_to_excel(self):
        """
        converts list of dictionary objects to excel
        """
        try:
            df = pd.DataFrame(data=self.objectlist)
            df.to_excel("myexcel.xlsx")
        except PermissionError as pe:
            logging.error('Error occured in convert_to_excel func : ' + str(pe))
