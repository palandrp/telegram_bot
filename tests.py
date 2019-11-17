# -*- coding: utf-8 -*-
from datetime import datetime
from pprint import pprint
from business import ShiftSheet


def tests():
    business = ShiftSheet()

    dt = datetime.now()
    month = dt.strftime('%B')
    day = dt.strftime('%d')
    pprint(business.show_day_shifts(month, day, 'CHEL'))


tests()