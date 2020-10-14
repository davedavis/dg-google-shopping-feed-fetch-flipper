""" Main function that checks the time and updates the Google shopping feed fetch schedule alternating
    twice per day. """

import sys
import datetime
from shopping.content import common


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

                # Switch needs to happen at 10:15 Europe/Dublin time. So here, we need to set the time
                # comparison to 08:15 as the docker container is on UTC.
                # ToDo: Check after daylight savings come in for bugs.
                now_time = datetime.datetime.now().time()
                morning_run = datetime.time(22, 15)
                evening_run = datetime.time(9, 15)
                if now_time >= morning_run or now_time <= evening_run:
                    country_datafeed["fetchSchedule"]["hour"] = 10
                else:
                    country_datafeed["fetchSchedule"]["hour"] = 23

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
