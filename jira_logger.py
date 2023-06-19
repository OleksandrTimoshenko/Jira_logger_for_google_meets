import os
import webbrowser
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv
from get_date import get_and_validate_date

# Jira API credentials
load_dotenv("./creds/.env")
JIRA_URL = os.getenv("JIRA_URL")
JIRA_TOKEN = os.getenv("JIRA_TOKEN")


def log_time(ticket_key, started_time, time_spent, comment):

    # Construct the API URL for logging work
    api_url = f'{JIRA_URL}/rest/api/2/issue/{ticket_key}/worklog'

    # Set the authentication headers
    headers = {
        'Authorization': f'Bearer {JIRA_TOKEN}',
        'Content-Type': 'application/json'
    }

    # Worklog data
    worklog_data = {
        "started": f"{started_time}T12:00:00.000+0000",
        # Time spent in Jira work log format (e.g., 2h, 1d)
        'timeSpent': time_spent,
        'comment': comment,  # Comment for the work log
        # error(
        #   'properties': [
        #       {
        #           'key': '_BillingKey_',
        #           'value': 'test'  # Replace 'SelectedOption' with the desired value
        #       }
        #   ]
    }

    # Send the POST request to log work
    response = requests.post(api_url, headers=headers, json=worklog_data, timeout=10)

    # Check the response status code
    if response.status_code == 201:
        print(
            f"Work logged successfully - {time_spent} to {ticket_key} with comment {comment}")
    else:
        print(f"Failed to log work. Status code: {response.status_code}")

def open_tempo(endpoint):
    url = urljoin(JIRA_URL, endpoint)

    response = requests.get(url, timeout=10)

    # Open the URL in the browser if the request was successful
    if response.status_code == 200:
        webbrowser.open(url)
    else:
        print(f"Error: {response.status_code}")

if __name__ == '__main__':
    log_date = get_and_validate_date()
    log_time("XXXXXXX-NNN", log_date, "0h 15m", "Testing stuff")
    open_tempo("/secure/Tempo.jspa#/my-work/week")
