"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
import json
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

class Googbot:
	def __init__(self):
		# Setup the Sheets API
		self.store = file.Storage('credentials.json')
		self.creds = self.store.get()
		if not self.creds or self.creds.invalid:
		    raise Exception(f'Credentials file not found...')
		self.service = build('sheets', 'v4', http=self.creds.authorize(Http()))

		# Call the Sheets API
		with open('sheet_address.json', 'r') as f:
			sheet_address = json.load(f)
		self.SPREADSHEET_ID = sheet_address['sheet_id']
		self.RANGE_NAME = sheet_address['list_name'] + '!{}'
		
	def get_data_from_sheet(self, my_sheet_range) -> list:
		result = self.service.spreadsheets().values().get(
			spreadsheetId=self.SPREADSHEET_ID,
			range=self.RANGE_NAME.format(my_sheet_range)).execute()
		values = result.get('values', [])
		if not values:
		    print('No data found.')
		return values