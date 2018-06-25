from googbot import Googbot


ATTENDANT_NUMBERS = 'A18:B23'
CHEL_SHIFT_TIME = 'E18:E23'
MSK_SHIFT_TIME = 'F18:F23'

OFFSET = 4
MONTHS = ['jiny','july','august','september','october','november',
		  'december','yanuar','februar','march','april','may']
MONTH_OFFSET = 4
DAY_OF_MONTH = 'G17:AK17'
WORK_FILD = 'G18:AK23'

attendant_numbers = Googbot().get_data_from_sheet(ATTENDANT_NUMBERS)
day_of_month = Googbot().get_data_from_sheet(DAY_OF_MONTH)
work_fild = Googbot().get_data_from_sheet(WORK_FILD)
print(attendant_numbers)
print(day_of_month)
print(work_fild)