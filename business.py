# -*- coding: utf-8 -*-
from googbot import Googbot


class ShiftSheet:
    def __init__(self):
        self.MONTHS = [
            'Yanuar', 'Februar', 'March', 'April', 'May', 'June',
            'Jule', 'August', 'September', 'October', 'November', 'December']
        self.X_COORDINATES = [
            'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB',
            'AC', 'AD', 'AE', 'AF', 'AG']

        self.CHEL_SHIFT_TIME_FIELD = 'A15:A20'
        self.MSK_SHIFT_TIME_FIELD = 'B15:E20'
        self.ATTENDANTS = 'A4:B10'

        # Sheet's fields offsets
        self.OFFSET_START_FROM = 13
        self.WORK_FIELD_START_OFFSET = 2
        self.WORK_FIELD_END_OFFSET = 7
        self.DATE_FIELD_OFFSET = 2
        self.NEXT_BLOCK_OFFSET = 9
        self.DAY_OFFSET = 1

        # Date offset
        self.MONTH_OFFSET = 0

        self.FIELD_TEMTLATE = 'G{}:AK{}'
        self.MONTH_NAME_TEMPLATE = 'A{}'

        self.googbot = Googbot()

    def __month_on_sheet(self, actual_month) -> int:
        month_on_sheet = self.MONTHS.index(actual_month) - self.MONTH_OFFSET
        if month_on_sheet < 0:
            month_on_sheet += 12
        return month_on_sheet

    def __month_offset(self, actual_month) -> int:
        return (
                self.OFFSET_START_FROM + \
                self.__month_on_sheet(actual_month) * \
                self.NEXT_BLOCK_OFFSET)

    def __month_field_Y_coordinates(self, actual_month) -> list:
        work_field_coordinate_1 = (
                self.WORK_FIELD_START_OFFSET + self.__month_offset(actual_month))
        work_field_coordinate_2 = (
                self.WORK_FIELD_END_OFFSET + self.__month_offset(actual_month))
        return [work_field_coordinate_1, work_field_coordinate_2]

    def __month_field_X_coordinate(self, actual_day) -> str:
        return self.X_COORDINATES[int(actual_day) - self.DAY_OFFSET]

    def post_month_name(self, actual_month) -> str:
        month_coordinate = self.__month_offset(actual_month)
        field = self.MONTH_NAME_TEMPLATE.format(month_coordinate)
        return self.googbot.post_data_from_sheet(field)[0][0]

    def post_date_field(self, actual_month) -> list:
        date_coordinates = self.DATE_FIELD_OFFSET + self.__month_offset(actual_month)
        field = self.FIELD_TEMTLATE.format(date_coordinates, date_coordinates)
        return self.googbot.post_data_from_sheet(field)[0]

    def post_month_field(self, actual_month) -> list:
        coordinates_Y = self.__month_field_Y_coordinates(actual_month)
        field = self.FIELD_TEMTLATE.format(coordinates_Y[0], coordinates_Y[1])
        return self.googbot.post_data_from_sheet(field)

    def calc_shift_date(self, actual_month, actual_day) -> list:
        return self.post_date_field(actual_month)[int(actual_day) - self.DAY_OFFSET]

    def post_shift_field(self, actual_month, actual_day) -> list:
        coordinates_Y = self.__month_field_Y_coordinates(actual_month)
        coordinate_X = self.__month_field_X_coordinate(actual_day)
        field = f'{coordinate_X}{coordinates_Y[0]}:{coordinate_X}{coordinates_Y[1]}'
        return self.googbot.post_data_from_sheet(field)

    def post_time_intervals(self, location='MSK') -> list:
        """
        This function returns list of strings which presents itself a time interval for the shifts.
        Because of structure of the data it returns every second entrance of time interval in the table.
        :param location:
        :return:
        """
        if location == 'MSK':     # TODO It had hardcoded, it is not good...
            field = self.MSK_SHIFT_TIME_FIELD
        elif location == 'CHEL':
            field = self.CHEL_SHIFT_TIME_FIELD
        else:
            raise Exception('Location not found...')
        temp = self.googbot.post_data_from_sheet(field)
        return [temp[i][0] for i in range(len(temp))]

    def match_names(self) -> dict:
        """
        This function maps the name of attendant and his serial number.
        :return:
        """
        attendant_numbers = self.googbot.post_data_from_sheet(self.ATTENDANTS)
        return {item[1]: item[0] for item in attendant_numbers}

    def show_day_shifts(self, actual_month, actual_day, location) -> str:
        shift_field = self.post_shift_field(actual_month, actual_day)
        time_intervals = self.post_time_intervals(location)
        attendant_numbers = self.match_names()
        for item in shift_field:
            if item:
                item[0] = attendant_numbers[item[0]]
        shift_pairs = {}
        for k, v in zip(time_intervals, shift_field):
            if k in shift_pairs:
                shift_pairs[k] += v
            else:
                shift_pairs[k] = v
        text = ''
        for key in shift_pairs:
            names = ''
            for val in shift_pairs[key]:
                names += '{}\n'.format(val)
            text += '{}:\n{}\n'.format(key, names)
        return text

