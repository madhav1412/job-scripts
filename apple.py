import concurrent.futures
import math
from collections import deque

import requests

all_job_names = deque()


def get_list_of_jobs(page_number):
    try:
        url = "https://jobs.apple.com/api/v1/search"

        payload = {
            "query": "",
            "filters": {
                "locations": [
                    "postLocation-USA"
                ],
                "teams": [
                    {
                        "team": "teamsAndSubTeams-SFTWR",
                        "subTeam": "subTeam-AF"
                    },
                    {
                        "team": "teamsAndSubTeams-SFTWR",
                        "subTeam": "subTeam-CLD"
                    },
                    {
                        "team": "teamsAndSubTeams-SFTWR",
                        "subTeam": "subTeam-ISTECH"
                    }
                ]
            },
            "page": page_number,
            "locale": "en-us",
            "sort": "",
            "format": {
                "longDate": "MMMM D, YYYY",
                "mediumDate": "MMM D, YYYY"
            }
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, json=payload)
        response_json = response.json()
        all_job_names.extend([job["postingTitle"] for job in response_json["res"]["searchResults"]])
        return math.ceil(response_json["res"]["totalRecords"] / 20)
    except Exception as exc:
        print(exc)


total_number_of_pages = get_list_of_jobs(1)

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(get_list_of_jobs, page) for page in range(1, total_number_of_pages + 1)]
    for future in concurrent.futures.as_completed(futures):
        try:
            jobs_response = future.result()
        except Exception as exc:
            print(exc)
for title in all_job_names:
    print(title)
