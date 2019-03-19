from dateutil.parser import parse


def parse_two_dates(date1, date2):
    return parse(date1), parse(date2)
