from googbot import Googbot


class ShiftSheet:
	def __init__(self):
		self.MONTHS = ['yanuar','februar','march','april','may','juny',
			'july','august','september','october','november','december']
		self.ATTENDANT_NUMBERS_FIELD = 'A18:B23'
		self.CHEL_SHIFT_TIME_FIELD = 'E18:E23'
		self.MSK_SHIFT_TIME_FIELD = 'F18:F23'

		#Sheet's fields offsets
		self.OFFSET_START_FROM = 16
		self.WORK_FIELD_START_OFFSET = 2
		self.WORK_FIELD_END_OFFSET = 8
		self.DATE_FIELD_OFFSET = 1
		self.NEXT_BLOCK_OFFSET = 9

		#Date offset
		self.MONTH_OFFSET = 5

		self.FIELD_TEMTLATE = 'G{}:AK{}' #'G18:AK23' WORK_FIELD
		self.MONTH_NAME_TEMPLATE = 'A{}:A{}'

		self.googbot = Googbot()

	def __month_on_sheet(self, actual_month) -> int:
		month_on_sheet = self.MONTHS.index(actual_month)-self.MONTH_OFFSET
		if month_on_sheet < 0:
			month_on_sheet += 12
		return month_on_sheet

	def __block_number(self) -> int:
		return self.__month_on_sheet()*self.NEXT_BLOCK_OFFSET

	def __month_offset(self, actual_month) -> int:
		return (
			self.OFFSET_START_FROM+ \
			self.__month_on_sheet(actual_month)* \
			self.NEXT_BLOCK_OFFSET)

	def post_month_name(self, actual_month) -> list:
		month_coordinates = self.__month_offset(actual_month)
		field = self.MONTH_NAME_TEMPLATE.format(month_coordinates,month_coordinates)
		return self.googbot.post_data_from_sheet(field)

	def post_date_field(self, actual_month) -> list:
		date_coordinates = self.DATE_FIELD_OFFSET+self.__month_offset(actual_month)
		field = self.FIELD_TEMTLATE.format(date_coordinates,date_coordinates)
		return self.googbot.post_data_from_sheet(field)

	def post_work_field(self, actual_month) -> list:
		work_field_coordinate_1 = (
			self.WORK_FIELD_START_OFFSET+self.__month_offset(actual_month))
		work_field_coordinate_2 = (
			self.WORK_FIELD_END_OFFSET+self.__month_offset(actual_month))
		field = self.FIELD_TEMTLATE.format(
			work_field_coordinate_1,work_field_coordinate_2)
		return self.googbot.post_data_from_sheet(field)


ss = ShiftSheet()
print(ss.post_month_name('yanuar'))
print(ss.post_date_field('yanuar'))
print(ss.post_work_field('yanuar'))