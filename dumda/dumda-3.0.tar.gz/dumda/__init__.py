from . import cities
from . import names
from . import phones
from . import emails
from . import text


class Person(object):
    def __init__(self, country: str = "United States", sex: str = None):
        self.name = names.get_full_name(sex)
        self.location = cities.get_random_city(country)
        self.email = emails.generate_email(self.name)
        self.phone = phones.generate_number()

    def json(self):
        """
        returns a Json Object of the generated
        Person object as an alternative to manually working
        with the Python object
        :return: JSON Object
        """
        import json
        response = json.dumps({
            'full_name': self.name,
            'location': self.location,
            'email': self.email,
            'phone': self.phone
        })

        return json.loads(response)
