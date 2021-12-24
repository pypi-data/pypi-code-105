"""
This function will convert a text string to a PDF document.

TODO:  add more content
"""


class Converter:
    """A simple converter for converting PDFs to text"""

    def convert_to_text(self, path: str) -> None:
        """
        Convert the given PDF to text file and save

        Parameters:
        path (str): The path to a PDF file

        Returns:
        None
        """

        print(f"{path} pdf2text")


if __name__ == "__main__":
    conv = Converter()
    conv.convert_to_text("hello")
