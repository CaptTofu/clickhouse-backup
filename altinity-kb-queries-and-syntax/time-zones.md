# Time zones

Important things to know:  


1. DateTime inside clickhouse is actually UNIX timestamp always, i.e. number of seconds since 1970-01-01 00:00:00 GMT.
2. Conversion from that UNIX timestamp to a human-readable form and reverse can happen on the client \(for native clients\) and on the server \(for HTTP clients, and for some type of queries, like `toString(ts)`\)
3. Depending on the place where that conversion happened rules of different timezones may be applied.
4. You can check server timezone using `SELECT timezone()`
5. clickhouse-client also by default tries to use server timezone \(see also `--use_client_time_zone` flag\)
6. If you want you can store the timezone name inside the data type, in that case, timestamp &lt;-&gt; human-readable time rules of that timezone will be applied.

```text
SELECT
    timezone(),
    toDateTime(now()) AS t,
    toTypeName(t),
    toDateTime(now(), 'UTC') AS t_utc,
    toTypeName(t_utc),
    toUnixTimestamp(t),
    toUnixTimestamp(t_utc)

Row 1:
──────
timezone():                                Europe/Warsaw
t:                                         2021-07-16 12:50:28
toTypeName(toDateTime(now())):             DateTime
t_utc:                                     2021-07-16 10:50:28
toTypeName(toDateTime(now(), 'UTC')):      DateTime('UTC')
toUnixTimestamp(toDateTime(now())):        1626432628
toUnixTimestamp(toDateTime(now(), 'UTC')): 1626432628
```

Since version 20.4 clickhouse uses embedded tzdata \(see [https://github.com/ClickHouse/ClickHouse/pull/10425](https://github.com/ClickHouse/ClickHouse/pull/10425) \) 

You get used tzdata version

```text
SELECT *
FROM system.build_options
WHERE name = 'TZDATA_VERSION'

Query id: 0a9883f0-dadf-4fb1-8b42-8fe93f561430

┌─name───────────┬─value─┐
│ TZDATA_VERSION │ 2020e │
└────────────────┴───────┘
```

and list of available time zones

```text
SELECT *
FROM system.time_zones
WHERE time_zone LIKE '%Anta%'

Query id: 855453d7-eccd-44cb-9631-f63bb02a273c

┌─time_zone─────────────────┐
│ Antarctica/Casey          │
│ Antarctica/Davis          │
│ Antarctica/DumontDUrville │
│ Antarctica/Macquarie      │
│ Antarctica/Mawson         │
│ Antarctica/McMurdo        │
│ Antarctica/Palmer         │
│ Antarctica/Rothera        │
│ Antarctica/South_Pole     │
│ Antarctica/Syowa          │
│ Antarctica/Troll          │
│ Antarctica/Vostok         │
│ Indian/Antananarivo       │
└───────────────────────────┘

13 rows in set. Elapsed: 0.002 sec. 

```

