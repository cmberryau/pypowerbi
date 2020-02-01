# -*- coding: future_fstrings -*-
import requests

import datetime

from requests.exceptions import HTTPError


class ActivityLogs:

    def __init__(self, client):
        self.client = client
        self.base_url = f'{self.client.api_url}/{self.client.api_version_snippet}/{self.client.api_myorg_snippet}'

        self.activities_events_snippet = "activityevents"
        self.group_part = "admin"   # This is always admin. Not really a group, but follows the
                                    # format of the rest of the library code

    def get_activity_logs(self, st, et=None, filter=None):
        """
        Get's the activity log for the specified date or date range. If et is None, it will get all logs (from midnight
        to 11:59:59 UTC) for the date specified by st. If et is set, it will retrieve logs from st-et. Note that the
        Power BI Activity Service currently supports only retrieving one day of logs at a time.

        "filter" is a string parameter that's sent to the service to filter the types of events returned. For example,
        "Activity eq 'viewreport' and UserId eq 'john@contoso.com'" gets report views for john(contoso.com).
        Right now the service only supports the operators ['eq', 'and'].

        NOTE: It appears that only data from December 15th, 2019 and on can be retrieved by the API as of the writing
        of this code. This isn't an official limitation I've found in the documentation, but seems to be the case.

        NOTE: This API allows at most 200 Requests per hour.

        For a good overview of the service, see https://powerbi.microsoft.com/en-us/blog/the-power-bi-activity-log-makes-it-easy-to-download-activity-data-for-custom-usage-reporting/

        :param st: The date to retrieve usage for (python datetime).
        :param et: The date to retrieve usage for (python datetime).
        :param filter: A string that defines a filter for retrieving the information. See the Power BI REST API
                       Documentation for details.
        :return:
        """
        # TODO: It would be nice if the available parameters for the "filter" function were defined somewhere in code.

        if et is None:
            dt_str = st.strftime("%Y-%m-%d")
            st_dt_str = f"{dt_str}T00:00:00"
            et_dt_str = f"{dt_str}T23:59:59"
        else:
            st_dt_str = st.strftime("%Y-%m-%dT:%H%M%S")
            et_dt_str = et.strftime("%Y-%m-%dT:%H%M%S")

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
        # (This is how Microsoft says the API is to be used.)
        # It seems to send the first set of actual data around 12-15 calls in. This doesn't seem to change even if you
        # slow down the API calls (in total number of calls required or when the first set of actual data is returned).

        cont_count = 1
        while continuation_token is not None:

            response = requests.get(continuation_uri, headers=headers)
            response_obj = response.json()

            event_entities = response_obj["activityEventEntities"]
            continuation_uri = response_obj["continuationUri"]
            continuation_token = response_obj["continuationToken"]

            activity_events.extend(event_entities)
            # print(f"{cont_count}: {len(event_entities)}")
            cont_count += 1

        # print(f"Took {cont_count} tries to exhaust continuation token for {len(activity_events)} events.")

        # Convert Datetime Strings to Python datetimes
        _date_fmt_str = '%Y-%m-%dT%H:%M:%S'
        for event in activity_events:
            event["CreationTime"] = datetime.datetime.strptime(event["CreationTime"], _date_fmt_str)
            # Change the Timezone to UTC
            event["CreationTime"] = event["CreationTime"].replace(tzinfo=datetime.timezone.utc)

        return activity_events
