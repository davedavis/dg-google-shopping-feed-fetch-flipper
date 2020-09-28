""" Main function that checks the time and updates the Google shopping feed fetch schedule alternating
    twice per day. """

from __future__ import print_function
import sys
from datetime import datetime, time
from shopping.content import common


def is_time_between(begin_time, end_time):
    """Helper function that checks if the current time (the time the script is being run)
    is between a range of hours so we can switch the feed fetch time to the
    correct side of the day."""
    check_time = datetime.utcnow().time()
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


# Main method, gets the list of feed IDs and makes the change depending on the current time.
def main(argv):
    # Authenticate and construct service.
    service, config, _ = common.init(argv, __doc__)
    merchant_id = config["merchantId"]

    request = service.datafeeds().list(merchantId=merchant_id, maxResults=100)

    while request is not None:
        result = request.execute()
        datafeeds = result.get("resources")

        for datafeed in datafeeds:
            # Check to make sure there's actually a fetch schedule and exclude countries where we don't want this run.
            if (
                "fetchSchedule" in datafeed.keys()
                and datafeed["targets"][0]["country"]
                and datafeed["id"] != "108311856"
                and datafeed["id"] != "108512856" != ("CA" or "US" or "AU" or "NZ")
            ):
                # Change the fetch schedule and normalize the fetch timezone to Dublin.
                country_datafeed = (
                    service.datafeeds()
                    .get(merchantId=merchant_id, datafeedId=datafeed["id"])
                    .execute()
                )

                # Changing the scheduled fetch time to appropriate Dublin time, depending on what time it is on server.
                if is_time_between(time(10, 0), time(23, 00)):
                    country_datafeed["fetchSchedule"]["hour"] = 23
                else:
                    country_datafeed["fetchSchedule"]["hour"] = 10

                country_datafeed["fetchSchedule"]["timeZone"] = "Europe/Dublin"
                request = service.datafeeds().update(
                    merchantId=merchant_id,
                    datafeedId=datafeed["id"],
                    body=country_datafeed,
                )

                result = request.execute()
                print(
                    "Datafeed with ID %s and fetchSchedule %s was updated."
                    % (result["id"], str(result["fetchSchedule"]))
                )

        request = service.datafeeds().list_next(request, result)


if __name__ == "__main__":
    main(sys.argv)
