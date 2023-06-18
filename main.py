import os
from dotenv import load_dotenv
from google_calendar import get_meets
from jira_logger import log_time, open_tempo
from get_date import get_and_validate_date

load_dotenv("./creds/.env")
MY_EMAIL = os.getenv('MY_EMAIL')

# Create your own function based on the names of your meets and Jira tickets
def get_jira_ticket(key):
    if "ZERMP" in key or "Zermatt MP" in key:
        return "ZERMP-288"
    elif "Zermatt App" in key:
        return "ZERAPP-257"
    elif key == "1 to 1 Oleksandr / Artem" or key == "CI-Team weekly":
        return "CITEAM-359"
    else:
        return ""


def work_with_data(meet):
    data = {}

    for key, value in meet.items():
        hours = value.seconds // 3600
        minutes = (value.seconds // 60) % 60
        formatted_data = f"{hours}h {minutes}m"
        jira_ticket = get_jira_ticket(key)
        if jira_ticket != "":
            data[jira_ticket] = [key, formatted_data]
        else:
            print(f"We coudn`t find the Jira ticket for {key} meeting")
    return data


if __name__ == '__main__':
    tempo_endpoint = "/secure/Tempo.jspa#/my-work/week"
    date = get_and_validate_date()
    meets = get_meets(date)
    if meets[MY_EMAIL]:
        for meet in meets[MY_EMAIL]:
            jira_log_data = work_with_data(meet)
            if jira_log_data != {}:
                for key, value in jira_log_data.items():
                    log_time(key, date, value[1], value[0])
        print("Please add the 'Billing key' to each new event manually.")
        open_tempo(tempo_endpoint)

    else:
        print(f"Can not find meetings for email {MY_EMAIL} for date {date}")
