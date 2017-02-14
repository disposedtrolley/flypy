# FlyPy

A library for querying airfares via the Google QPX API. Instead of returning JSON, the results are parsed into Python objects containing a subset of properties returned in the raw response.

## Example

Let's find a one-way nonstop flight from Melbourne (`MEL`) to Shanghai (`PVG`) for a single adult, departing on the 9th of July 2017:

```{python}
from query import Query
from query_response import QueryResponse
from helper import convert_str_to_date_tz_naive

# Instantiate a new Query object.
query = Query()
# Add the origin airport to the query.
query.add_origin("MEL")
# Add the destination airport to the query.
query.add_dest("PVG")
# Add the intended departure date.
query.add_dept_date(convert_str_to_date_tz_naive("2017-07-09"))
# Add a single adult passenger.
query.add_pax(1)
# Restrict the maximum stops to 0 (nonstop).
query.add_max_stops(0)

# Send the query to QPX, and store the QueryResponse object.
response = query.send()
```

`query.send()` returns a `QueryResponse` object which stores the raw response and the created objects. We can use this to display some details of the trip:

```{python}
trips = response.get_trips()
    for trip in trips:
        print(trip)
        for journey in trip.journeys:
            print(journey)
            for leg in journey.legs:
                print(leg)

# [Trip] JOURNEYS: 1. COST: AUD689.25.
# [Journey] MEL to MEL.
# [Leg] MU738 from MEL to PVG. DUR: 645. AC: 332. DEPT: 2017-07-09 11:00:00+10:00. ARR: 2017-07-09 19:45:00+08:00.
# [Trip] JOURNEYS: 1. COST: AUD795.14.
# [Journey] MEL to MEL.
# [Leg] QF341 from MEL to PVG. DUR: 645. AC: 332. DEPT: 2017-07-09 11:00:00+10:00. ARR: 2017-07-09 19:45:00+08:00.
```

## Installation

1. Clone the repo.
3. Extract and `cd` into the cloned repo.
4. Run `pip install -r requirements.txt` in your shell to install any required
libraries.
5. Place the `flypy` folder inside your project.
6. Import `flypy` inside your code - `from flypy import *`

## Nomenclature

`Query` objects are used to specify the details of the airfares we want. A successful query returns a `QueryResponse` object which includes an array of trip options found by QPX. A trip option is a `Trip` object representing an airfare which meets all of the query criteria.

`Trip`s have `Journey`s; a single `Journey` for one-way airfares, and two for return airfares. Each `Journey` comprises of `Leg`s and `Layover`s. `Leg`s are always present and represent a flight. `Layover`s are present when multiple flights are required within a `Journey` and a connection time occurs at an airport.

## Making a Query



## Licence

The project is licensed under the MIT license.