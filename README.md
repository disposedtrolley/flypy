<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [FlyPy](#flypy)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Nomenclature](#nomenclature)
    - [Making a Query](#making-a-query)
    - [QueryResponse](#queryresponse)
    - [Trip](#trip)
    - [Journey](#journey)
    - [Leg](#leg)
    - [Layover](#layover)
  - [Acknowledgements](#acknowledgements)
  - [Licence](#licence)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# FlyPy

A library for querying airfares via the Google QPX API. Instead of returning JSON, the results are parsed into Python objects containing a subset of properties returned in the raw response.

Let's find a one-way nonstop flight from Melbourne (`MEL`) to Shanghai (`PVG`) for a single adult, departing on the 9th of July 2017:

```{python}
from flypy import *

# Instantiate a new Query object.
query = Query()
# Add the origin airport to the query.
query.add_origin("MEL")
# Add the destination airport to the query.
query.add_dest("PVG")
# Add the intended departure date.
query.add_dept_date("2017-07-09")
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
#     [Journey] MEL to PVG.
#         [Leg] MU738 from MEL to PVG. DUR: 645. AC: 332. DEPT: 2017-07-09 11:00:00+10:00. ARR: 2017-07-09 19:45:00+08:00.
# [Trip] JOURNEYS: 1. COST: AUD795.14.
#     [Journey] MEL to PVG.
#         [Leg] QF341 from MEL to PVG. DUR: 645. AC: 332. DEPT: 2017-07-09 11:00:00+10:00. ARR: 2017-07-09 19:45:00+08:00.
```

## Installation

1. Clone the repo.
3. Extract and `cd` into the cloned repo.
4. Run `pip install -r requirements.txt` in your shell to install any required
libraries.
5. Place the `flypy` folder inside your project.
6. Input your API key in the `api_key.py` file in the `flypy` folder. Follow the directions [here](https://developers.google.com/qpx-express/v1/prereqs) to obtain one if you don't have one already.
7. Import `flypy` inside your code - `from flypy import *`

## Usage

### Nomenclature

`Query` objects are used to specify the details of the airfares we want. A successful query returns a `QueryResponse` object which includes an array of trip options found by QPX. A trip option is a `Trip` object representing an airfare which meets all of the query criteria.

`Trip`s have `Journey`s; a single `Journey` for one-way airfares, and two for return airfares. Each `Journey` comprises of `Leg`s and `Layover`s. `Leg`s are always present and represent a flight. `Layover`s are present when multiple flights are required within a `Journey` and a connection time occurs at an airport.

### Making a Query

A blank query can be created by instantiating an object of the `Query` class. `query = Query` sets up a query which will return an unlimited number of results. An integer can be passed into the constructor to limit the number of results, e.g. `query = Query(1)` will return a single result.

Search parameters can be added to the query using the `query.add*` methods.

A basic `Query` has four mandatory search parameters:

+   `origin`: the [IATA](https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_A) code of the originating airport
    *   e.g. `query.add_origin("MEL")`
+   `dest`: the [IATA](https://en.wikipedia.org/wiki/List_of_airports_by_IATA_code:_A) code of the destination airport
    *   e.g. `query.add_dest("PVG")`
+   `dept_date`: the intended departure date from the originating airport
    *   e.g. `query.add_dept_date("2017-07-09")`
+   `pax`: the number of passengers of each type travelling
    *   e.g. `query.add_pax(1)    # adds an adult passenger`

The query will not run unless all mandatory parameters are supplied.

The following optional parameters can be supplied to further customise the search:

+   `query.add_return_date(...)`
+   `query.add_airline(...)    # restricts results to a particular airline`
+   `query.add_max_stops(...)    # maximum allowed layovers`

More documentation for these methods are available inline in the Query class.

Once the desired parameters are added, it's time to send the query! `response = query.send()` will fire off the query and return a `QueryResponse` object, which we'll describe in the next section.

### QueryResponse

A `QueryResponse` object contains the raw JSON response from QPX, and the various trip objects generated by the library. We'll mostly be concerned with the trip objects.

`response.get_trips()` returns an array of `Trip` objects for each result returned by the query.

### Trip

A `Trip` has a total cost - the total airfare in the currency of the originating country, and an array of `Journey` objects, which represent each portion of the trip. A one-way fare includes a single `Journey`, a return airfare includes two.

+   `get_cost()` - returns the cost of the trip in the originating country's currency
+   `get_journeys()` - returns an array of Journey objects

`Trip`s can be printed to show a high level overview.

### Journey

A `Journey` has `Leg`s, and `Layover`s. The latter is only present when connections occur at airports.

+   `get_legs()` - returns an array of Leg objects
+   `get_layovers()` - returns an array of Layover objects

`Journey`s can be printed to show a high level overview.

### Leg

A `Leg` has the following methods:

+   `get_origin()` - returns a dictionary of the originating airport's details
+   `get_dest()` - returns a dictionary of the destination airport's details
+   `get_dept_time()` - returns the departure time and date with timezone
+   `get_arr_time()` - returns the arrival time and date with timezon
+   `get_flight()` - returns the flight number and carrier name
+   `get_aircraft()` - returns the aircraft code and name
+   `get_duration()` - returns the duration of the flight in minutes

`Leg`s can be printed to show a high level overview.

### Layover

A `Layover` has the following methods:

+   `get_layover_airport()` - returns a dictionary of the layover airport's details
+   `get_layover_dur()` - returns the duration of the layover in minutes
+   `get_layover_start()` - returns the starting time of the layover (e.g. when the flight arrives)
+   `get_layover_end()` - returns the ending time of the layover (e.g. when the departing flight leaves)

`Layover`s can be printed to show a high level overview.

## Acknowledgements

+   Airlines JSON data sourced from https://github.com/BesrourMS/Airlines
+   Airports data sourced from http://ourairports.com/data/ and converted to JSON format.

## Licence

The project is licensed under the MIT license.