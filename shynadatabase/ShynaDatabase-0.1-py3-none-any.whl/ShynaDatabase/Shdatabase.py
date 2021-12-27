from ShynaCreatecredentials import Shcreatecredentials
import mysql.connector


class ShynaDatabase:
    cc_d = Shcreatecredentials.CreateCredentials()
    database_user = 'pythoqdx_Shyna'
    default_database = 'pythoqdx_Shyna'
    host = ''
    passwd = ''

    def set_host(self, cred_filename_host, key_file_host):
        self.cc_d.cred_filename = cred_filename_host
        self.cc_d.key_file = key_file_host
        return self.cc_d.read_credentials()

    def set_password(self, cred_filename_pass, key_file_pass):
        self.cc_d.cred_filename = cred_filename_pass
        self.cc_d.key_file = key_file_pass
        return self.cc_d.read_credentials()

    def check_connectivity(self):
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            if my_db.is_connected():
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False
        finally:
            if my_db.is_connected():
                my_db.close()

    def create_insert_update_or_delete(self, query):
        """ Insert value in database with no return."""
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(query)
            my_db.commit()
        except Exception as e:
            print(e)
        finally:
            my_db.close()

    def select_from_table(self, query):
        """Select all row using the given query and return the result in dictionary format."""
        result = []
        my_db = mysql.connector.connect(host=self.host,
                                        user=self.database_user,
                                        passwd=self.passwd,
                                        database=self.default_database
                                        )
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(query)
            cursor = my_cursor.fetchall()
            if len(cursor) > 0:
                for row in cursor:
                    result.append(row)
            else:
                result.append('Empty')
        except Exception as e:
            print("Exception is: \n", e)
            result = "Exception"
        finally:
            my_db.close()
            return result
