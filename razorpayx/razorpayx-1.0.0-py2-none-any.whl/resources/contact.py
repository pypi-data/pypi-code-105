from .base import Resource
from ..constants.url import URL


class Contact(Resource):
    def __init__(self, client=None):
        super(Contact, self).__init__(client)
        self.base_url = URL.CONTACTS_URL

    def fetch(self, contact_id, data={}, **kwargs):
        """"
        Fetch Contact for given Id

        Args:
            contact_id : Id for which customer object has to be retrieved

        Returns:
            contact dict for given contact Id
        """
        return super(Contact, self).fetch(contact_id, data, **kwargs)

    def create(self, data={}, **kwargs):
        """"
        Create Contact from given dict

        Returns:
            Contact Dict which was created
        """
        url = self.base_url
        return self.post_url(url, data, **kwargs)

    def edit(self, customer_id, data={}, **kwargs):
        """"
        Edit Customer information from given dict

        Returns:
            Customer Dict which was edited
        """
        url = '{}/{}'.format(self.base_url, customer_id)

        return self.put_url(url, data, **kwargs)
