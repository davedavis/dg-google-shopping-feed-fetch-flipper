""" Main function that checks the time and updates the Google shopping feed fetch schedule alternating
    twice per day. """

import sys
import datetime
from shopping.content import common


# Main method, gets the list of feed IDs and makes the change depending on the current time.
def main(argv):
    # Authenticate and construct service.
    print("It is now: ", datetime.datetime.now().time())
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

                # Switch needs to happen every 2 hours. Hour integer is what's required by the fetchSchedule dict.
                # So this will switch the fetchSchedule to 2 hours after the container is run. There will be
                # accumulation of lag but that doesn't matter much.
                now_time = datetime.datetime.now().time()
                two_hours_from_now = datetime.datetime.now() + datetime.timedelta(hours=2)
                print("Now is: ", now_time.hour)
                print("Two hours from now is: ", two_hours_from_now.hour)

                country_datafeed["fetchSchedule"]["hour"] = two_hours_from_now.hour
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
