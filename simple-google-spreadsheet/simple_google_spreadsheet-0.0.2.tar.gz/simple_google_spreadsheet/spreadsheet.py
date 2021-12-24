import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def convert1toA(num):
    col = ""
    while num > 0:
        num, remainder = divmod(num - 1, 26)
        col = chr(65 + remainder) + col
    return col

class TokenFileTypeException(Exception):
    pass

class CredentialsFileTypeException(Exception):
    pass

class CredentialsFileNotFoundException(Exception):
    pass

class InvalidSheet(Exception):
    pass

class SpreadSheet():

    def __init__(self, spreadsheet_id: str, credentials_filename: str, token_filename: str):

        self._spreadsheet_id = spreadsheet_id
        
        if not credentials_filename.endswith('.json'):
            raise CredentialsFileTypeException('Credentials file type must be .json')
        
        if not os.path.exists(credentials_filename):
            raise CredentialsFileNotFoundException('Credentials file not found')

        self._credentials_filename = credentials_filename

        if not token_filename.endswith('.json'):
            raise TokenFileTypeException('Token file type must be .json')
        
        self._token_filename = token_filename

        self._scopes = [
            'https://www.googleapis.com/auth/spreadsheets'
        ]

    def _service(self):

        creds = None
        if os.path.exists(self._token_filename):
            creds = Credentials.from_authorized_user_file(self._token_filename, self._scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self._credentials_filename, self._scopes)
                creds = flow.run_local_server(port=0)
            with open(self._token_filename, 'w') as token:
                token.write(creds.to_json())

        return build('sheets', 'v4', credentials=creds).spreadsheets()

    def clear_values(self, sheet: str, range: str = None) -> None:

        if not range:        
            for fsheet in self._service().get(spreadsheetId=self._spreadsheet_id).execute()['sheets']:
                if fsheet['properties']['title'] == sheet:
                    end_col = convert1toA(fsheet['properties']['gridProperties']['columnCount'])
                    end_lin = fsheet['properties']['gridProperties']['rowCount']
                    range = f'A1:{end_col}{end_lin}'
                    break

        if not range:
            raise InvalidSheet('Invalid sheet properties')

        self._service().values().clear(
            spreadsheetId=self._spreadsheet_id,
            range=f'{sheet}!{range}'
        ).execute()

    def get_values(self, sheet: str, range: str = None, cast_boolean: list = [], cast_float: list = []) -> list:

        if not range:        
            for fsheet in self._service().get(spreadsheetId=self._spreadsheet_id).execute()['sheets']:
                if fsheet['properties']['title'] == sheet:
                    end_col = convert1toA(fsheet['properties']['gridProperties']['columnCount'])
                    end_lin = fsheet['properties']['gridProperties']['rowCount']
                    range = f'A1:{end_col}{end_lin}'
                    break

        if not range:
            raise InvalidSheet('Invalid sheet properties')

        values = self._service().values().get(
            spreadsheetId=self._spreadsheet_id,
            range=f'{sheet}!{range}'
        ).execute().get('values',[])

        num = 1
        cols = []
        data = []
        for line in values:
            if num == 1:
                cols = line
            else:
                row = {}
                line_cols = len(line)
                for n,col in enumerate(cols):
                    cel = line[n] if n < line_cols and line[n] != '' else None
                    if col in cast_boolean:
                        cel = True if cel == 'TRUE' or cel == '1' else False
                    elif col in cast_float and cel is not None:
                        cel = float(cel.replace('.','').replace(',','.'))
                    row[col] = cel
                data.append(row)
            num += 1

        return data

    def set_values(self, data: list, sheet: str, range: str = 'A1') -> None:

        cols = []
        for row in data:
            for col in row.keys():
                if col not in cols:
                    cols.append(col)
        values = [cols]
        for row in data:
            line = []
            for col in cols:
                line.append(row[col] if col in row else None)
            values.append(line)

        self._service().values().update(
            spreadsheetId=self._spreadsheet_id,
            range=f'{sheet}!{range}',
            valueInputOption='USER_ENTERED',
            body={'values':values}
        ).execute()
