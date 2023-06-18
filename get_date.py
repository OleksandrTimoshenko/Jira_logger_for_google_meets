import argparse
from datetime import datetime, timedelta
from sys import exit

# TODO: add the ability to transmit multiple dates, or a period of time

def validate_date(date_string):
    try:
        date = datetime.strptime(date_string, "%Y-%m-%d")
        if date.strftime("%Y-%m-%d") == date_string:
            return True
        else:
            return False
    except ValueError:
        return False


def get_and_validate_date():
    parser = argparse.ArgumentParser(
        description='Jog staff from Google calendar to Jira!!!!')
    parser.add_argument(
        "-date",
        default="today",
        help="set date for logging (YYYY-MM-DD)")
    args = parser.parse_args()
    if args.date == "today":
        day = datetime.now().strftime("%Y-%m-%d")
    elif args.date == "yesterday":
        day = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    elif validate_date(args.date):
        day = args.date
    else:
        print(f"Wrong date format: {args.date}, should be YYYY-MM-DD")
        exit()
    return day


if __name__ == '__main__':
    print(get_and_validate_date())
