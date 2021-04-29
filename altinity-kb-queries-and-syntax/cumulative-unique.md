# Cumulative unique

```sql
CREATE TABLE events
(
    `ts` DateTime,
    `user_id` UInt32
)
ENGINE = Memory;

INSERT INTO events SELECT
    toDateTime('2021-04-29 10:10:10') + toIntervalHour(7 * number) AS ts,
    toDayOfWeek(ts) + (number % 2) AS user_id
FROM numbers(15);

SELECT
    ts,
    arrayReduce('uniqExactMerge', arrayFilter((x, y) -> (y <= ts), state_arr, ts_arr)) AS uniq
FROM
(
    SELECT
        groupArray(ts) AS ts_arr,
        groupArray(state) AS state_arr
    FROM
    (
        SELECT
            toDate(ts) AS ts,
            uniqExactState(user_id) AS state
        FROM events
        GROUP BY ts
    )
)
ARRAY JOIN ts_arr AS ts

┌─────────ts─┬─uniq─┐
│ 2021-04-29 │    2 │
│ 2021-04-30 │    3 │
│ 2021-05-01 │    4 │
│ 2021-05-02 │    5 │
│ 2021-05-03 │    7 │
└────────────┴──────┘
```

