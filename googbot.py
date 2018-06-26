"""
Shows basic usage of the Sheets API. Prints values from a Google Spreadsheet.
"""
import json
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

API_NAME = 'sheets'
API_VERSION = 'v4'
API_CREDANTIALS = 'credentials.json'
SHEET_ADDRES = 'sheet_address.json'

class Googbot:
	def __init__(self):
		# Setup the Sheets API
		try:
			self.store = file.Storage(API_CREDANTIALS)
		except Exception:
			raise Exception('Credentials file not found...')
		self.creds = self.store.get()
		if not self.creds or self.creds.invalid:
		    raise Exception('Credentials not found...')
		self.service = build(API_NAME, API_VERSION, http=self.creds.authorize(Http()))

		# Call the Sheets API
		#try:
		with open(SHEET_ADDRES, 'r') as f:
			sheet_address = json.load(f)
		#except JSONDecodeError as e:
		#	print(e)
		#except FileNotFoundError:
		#	print(e)
		#else Exception as e:
		#	print(e)
		self.SPREADSHEET_ID = sheet_address['sheet_id']
		self.RANGE_NAME = sheet_address['list_name'] + '!{}'
		
	def post_data_from_sheet(self, my_sheet_range) -> list:
		result = self.service.spreadsheets().values().get(
			spreadsheetId=self.SPREADSHEET_ID,
			range=self.RANGE_NAME.format(my_sheet_range)).execute()
		values = result.get('values', [])
		if not values:
		    print('No data found.')
		return values