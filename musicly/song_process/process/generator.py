from datetime import datetime
import radar


def date_generoter():
    initial_date = datetime.strptime("1/1/2000", "%m/%d/%Y")
    final_date = datetime.strptime("1/1/2020", "%m/%d/%Y")
    random_date = radar.random_date(initial_date, final_date)
    return random_date