from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from datetime import datetime

def test_logic():
    date_str = "2023-12-31T23:59:59"
    dt = parse(date_str)
    expected = datetime(2023, 12, 31, 23, 59, 59)
    if dt != expected:
        print(f"Parsing failed: {dt} != {expected}")
        exit(1)

    start_date = datetime(2024, 1, 31)
    end_date = start_date + relativedelta(months=+1)
    if end_date.day != 29:
        print(f"Relativedelta failed: {end_date.day} != 29")
        exit(1)

    print("dateutil functional test: PASSED")

if __name__ == "__main__":
    test_logic()