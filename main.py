from googbot import Googbot


class ShiftSheet:
	def __init__(self):
		self.MONTHS = [
			'yanuar','februar','march','april','may','juny',
			'july','august','september','october','november','december']
		self.X_COORDINATES = [
			'G','H','I','J','K','L','M','N','O','P','Q',
			'R','S','T','U','V','W','X','Y','Z','AA','AB',
			'AC','AD','AE','AF','AG','AH','AI','AJ','AK']
		self.ATTENDANT_NUMBERS_FIELD = 'A18:B23'
		self.CHEL_SHIFT_TIME_FIELD = 'E18:E23'
		self.MSK_SHIFT_TIME_FIELD = 'F18:F23'

		#Sheet's fields offsets
		self.OFFSET_START_FROM = 16
		self.WORK_FIELD_START_OFFSET = 2
		self.WORK_FIELD_END_OFFSET = 8
		self.DATE_FIELD_OFFSET = 1
		self.NEXT_BLOCK_OFFSET = 9
		self.DAY_OFFSET = 1

		#Date offset
		self.MONTH_OFFSET = 5

		self.FIELD_TEMTLATE = 'G{}:AK{}'
		self.MONTH_NAME_TEMPLATE = 'A{}'

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

	def __month_field_Y_coordinates(self, actual_month) -> list:
		work_field_coordinate_1 = (
			self.WORK_FIELD_START_OFFSET+self.__month_offset(actual_month))
		work_field_coordinate_2 = (
			self.WORK_FIELD_END_OFFSET+self.__month_offset(actual_month))
		return [work_field_coordinate_1,work_field_coordinate_2]

	def __X_coordinate(self, actual_day) -> str:
		return self.X_COORDINATES[int(actual_day)-self.DAY_OFFSET]

	def post_month_name(self, actual_month) -> str:
		month_coordinate = self.__month_offset(actual_month)
		field = self.MONTH_NAME_TEMPLATE.format(month_coordinate)
		return self.googbot.post_data_from_sheet(field)[0][0]

	def post_date_field(self, actual_month) -> list:
		date_coordinates = self.DATE_FIELD_OFFSET+self.__month_offset(actual_month)
		field = self.FIELD_TEMTLATE.format(date_coordinates,date_coordinates)
		return self.googbot.post_data_from_sheet(field)[0]

	def post_month_field(self, actual_month) -> list:
		coordinates_Y = self.__month_field_Y_coordinates(actual_month)
		field = self.FIELD_TEMTLATE.format(coordinates_Y[0],coordinates_Y[1])
		return self.googbot.post_data_from_sheet(field)

	def calc_shift_date(self, actual_month, actual_day) -> list:
		return self.post_date_field(actual_month)[int(actual_day)-self.DAY_OFFSET]

	def post_shift_field(self, actual_month, actual_day) -> list:
		coordinates_Y = self.__month_field_Y_coordinates(actual_month)
		coordinate_X = self.__X_coordinate(actual_day)
		field = f'{coordinate_X}{coordinates_Y[0]}:{coordinate_X}{coordinates_Y[1]}'
		return self.googbot.post_data_from_sheet(field)

	def post_time_intervals(self, location='MSK') -> list:
		if (location == 'MSK'): field = self.MSK_SHIFT_TIME_FIELD
		elif (location == 'CHEL'): field = self.CHEL_SHIFT_TIME_FIELD
		else: raise Exception('Location not found...')
		temp = self.googbot.post_data_from_sheet(field)
		return [temp[i][0] for i in range(len(temp))]

	def calc_shift_pairs(self, actual_month, actual_day, location) -> dict:
		shift_field = self.post_shift_field(actual_month, actual_day)
		time_intervals = self.post_time_intervals(location)
		shift_pairs = {}
		for k, v in zip(time_intervals,shift_field):
			if k in shift_pairs:
				shift_pairs[k] += v
			else:
				shift_pairs[k] = v
		return shift_pairs # dict(zip(time_intervals,shift_field))



ss = ShiftSheet()
month = ss.post_month_name('july')
date_list = ss.post_date_field('july')
shift_list = ss.post_month_field('july')
actual_shift = ss.post_shift_field('july','01')
date = ss.calc_shift_date('july','01')
time_intervals = ss.post_time_intervals('CHEL')
shift_pairs = ss.calc_shift_pairs('july','01','CHEL')

print(f'Название месяца: {month}')
print(f'Список дат: {date_list}')
print(f'Список смен построчно: {shift_list}')
print(f'Список смен в определённую дату: {actual_shift}')
print(f'Название даты: {date}')
print(f'Список временных интервалов: {time_intervals}')
print(f'Время смены и дежурный: {shift_pairs}')