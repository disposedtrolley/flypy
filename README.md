# FlyPy

A library for querying airfares via the Google QPX API. Data are presented as Python objects containing a subset of properties returned in the raw JSON response.

## Example

**FlyPy** is extremely easy to use. Here, I'm searching for a one-way nonstop flight from Melbourne (`MEL`) to Shanghai (`PVG`) for a single adult:

```{python}
from query import Query
from query_response import QueryResponse
from helper import convert_str_to_date_tz_naive

# Instantiate a new Query object.
query = Query()
# Add the origin airport to the query.
query.add_origin("MEL")
# Add the intended departure date.
query.add_dept_date(convert_str_to_date_tz_naive("2017-07-09"))
# Add a single adult passenger.
query.add_pax(1)
# Restrict the maximum stops to 0 (nonstop).
query.add_max_stops(0)

# Send the query to QPX, and store the QueryResponse object.
response = query.send()
```

The query returns a `QueryResponse` object which we've referenced in the `response` variable. We can use this to display some details of the trip:

```{python}
trips = response.get_trips()
    for trip in trips:
        print(trip)
        for journey in trip.journeys:
            print(journey)
            for leg in journey.legs:
                print(leg)
```

## Nomenclature

