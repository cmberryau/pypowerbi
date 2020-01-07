# -*- coding: future_fstrings -*-
import requests
import json
from pypowerbi.utils import convert_datetime_fields

import datetime

from requests.exceptions import HTTPError


class ActivityLog:

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

        self.activities_events_snippet = "activityevents"
        self.group_part = "admin"   # This is always admin. Not really a group, but follows the format of other code

    def get_activity_log(self, dt, filter=None):
        dt_str = dt.strftime("%Y-%m-%d")
        st_dt_str = f"{dt_str}T00:00:00"
        et_dt_str = f"{dt_str}T23:59:59"

        # https://api.powerbi.com/v1.0/myorg/admin/activityevents?startDateTime='{st_dt_str}'&endDateTime='{et_dt_str}'

        # form the url
        filter_snippet = f"startDateTime='{st_dt_str}'&endDateTime='{et_dt_str}'"
        url = f'{self.base_url}/{self.group_part}/{self.activities_events_snippet}?{filter_snippet}'

        if filter is not None:
            url += f"$filter={filter}"

        # form the headers
        headers = self.client.auth_header

        # get the response
        response = requests.get(url, headers=headers)

        # 200 is the only successful code, raise an exception on any other response code
        if response.status_code != 200:
            raise HTTPError(response, f'Get Datasets request returned http error: {response.json()}')

        response_obj = response.json()

        event_entities = response_obj["activityEventEntities"]
        continuation_uri = response_obj["continuationUri"]
        continuation_token = response_obj["continuationToken"]

        activity_events = event_entities

        # Even if nothing is returned, it takes around 24 tries until no continuation token is returned.
        # This is how Microsoft says the API is to be used.
        cont_count = 1
        while continuation_token is not None:

            response = requests.get(continuation_uri, headers=headers)
            response_obj = response.json()

            event_entities = response_obj["activityEventEntities"]
            continuation_uri = response_obj["continuationUri"]
            continuation_token = response_obj["continuationToken"]

            activity_events.extend(event_entities)
            cont_count += 1

        #print(f"Took {cont_count} tries to exhaust continuation token for {len(activity_events)} events.")

        # Convert Datetime Strings to Python datetimes
        _date_fmt_str = '%Y-%m-%dT%H:%M:%S'
        for event in activity_events:
            event["CreationTime"] = datetime.datetime.strptime(event["CreationTime"], _date_fmt_str)
            # Change the Timezone to UTC
            event["CreationTime"] = event["CreationTime"].replace(tzinfo=datetime.timezone.utc)

        return activity_events
