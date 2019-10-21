import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint


API_NAME = 'sheets'
API_VERSION = 'v4'
API_CREDANTIALS = 'credentials.json'
SHEET_ADDRES = 'sheet_address.json'


class Googbot:
    '''
    The manual for making connection: https://developers.google.com/docs/api/quickstart/python
    The manual for the given API: https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/get
    '''
    def __init__(self):

        # Call the Sheets API
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        try:
            with open(SHEET_ADDRES, 'r') as f:
                sheet_address = json.load(f)
                self.SPREADSHEET_ID = sheet_address['sheet_id']
                self.RANGE_NAME = sheet_address['list_name'] + '!{}'
        except Exception:
            raise Exception('Address file not found or invalid...')

        self.creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build(API_NAME, API_VERSION, credentials=self.creds)

    def post_data_from_sheet(self, my_sheet_range) -> list:
        request = self.service.spreadsheets().values().get(spreadsheetId=self.SPREADSHEET_ID,
                                                      #range="G4:H5",
                                                      range=self.RANGE_NAME.format(my_sheet_range),
                                                      valueRenderOption='FORMATTED_VALUE',
                                                      dateTimeRenderOption='SERIAL_NUMBER')
        response = request.execute()
        if response.get('values') == None:
            return ['No data found.']
        else:
            return response.get('values')


#pprint(Googbot().post_data_from_sheet()) #DEBUG!