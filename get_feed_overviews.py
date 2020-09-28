"""Gets all datafeeds on the specified account."""

from __future__ import print_function
import sys
import pprint
from shopping.content import common
from datetime import datetime, time

# Set up prettyprint object for debugging returned objects
pp = pprint.PrettyPrinter(indent=4)


# Main method, gets the list of feed IDs.
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

                print(
                    datafeed["targets"][0]["country"],
                    datafeed["id"],
                    datafeed["fetchSchedule"]["hour"],
                    datafeed["fetchSchedule"]["timeZone"],
                    datafeed["name"],
                    sep="\t",
                )

        request = service.datafeeds().list_next(request, result)


if __name__ == "__main__":
    main(sys.argv)
