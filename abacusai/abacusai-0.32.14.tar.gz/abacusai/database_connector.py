from .return_class import AbstractApiClass


class DatabaseConnector(AbstractApiClass):
    """
        A connector to an external service
    """

    def __init__(self, client, databaseConnectorId=None, service=None, name=None, status=None, auth=None, createdAt=None):
        super().__init__(client, databaseConnectorId)
        self.database_connector_id = databaseConnectorId
        self.service = service
        self.name = name
        self.status = status
        self.auth = auth
        self.created_at = createdAt

    def __repr__(self):
        return f"DatabaseConnector(database_connector_id={repr(self.database_connector_id)},\n  service={repr(self.service)},\n  name={repr(self.name)},\n  status={repr(self.status)},\n  auth={repr(self.auth)},\n  created_at={repr(self.created_at)})"

    def to_dict(self):
        return {'database_connector_id': self.database_connector_id, 'service': self.service, 'name': self.name, 'status': self.status, 'auth': self.auth, 'created_at': self.created_at}

    def list_objects(self):
        """Lists querable objects in the database connector."""
        return self.client.list_database_connector_objects(self.database_connector_id)

    def get_object_schema(self, object_name=None):
        """Get the schema of an object in an database connector."""
        return self.client.get_database_connector_object_schema(self.database_connector_id, object_name)

    def rename(self, name):
        """Renames a Database Connector"""
        return self.client.rename_database_connector(self.database_connector_id, name)

    def verify(self):
        """Checks to see if Abacus.AI can access the database."""
        return self.client.verify_database_connector(self.database_connector_id)

    def delete(self):
        """Delete a database connector."""
        return self.client.delete_database_connector(self.database_connector_id)
