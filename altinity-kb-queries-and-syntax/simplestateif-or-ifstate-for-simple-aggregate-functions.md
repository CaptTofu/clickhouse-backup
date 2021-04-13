# -SimpleStateIf or -IfState for simple aggregate functions

## Question

SimpleAggregateFunction is great feature to have. It allows us to reduce memory usage by a lot \(between 3 and 10 times\) and improve query performance, but it's impossible to use it with combinators, like `-If`. Is there a workaround for this use case:

We can change order of combinators, so we would first filter by `-If` condition and take state after filtering.

{% hint style="info" %}
`-If` and `-SimpleStateIf` produce the exact same result, but second have `SimpleAggregateFunction` datatype, which is useful for implicit Materialized View.
{% endhint %}

{% hint style="warning" %}
`-SimpleState` supported since 21.1. See [https://github.com/ClickHouse/ClickHouse/pull/16853/](https://github.com/ClickHouse/ClickHouse/pull/16853/commits/5b1e5679b4a292e33ee5e60c0ba9cefa1e8388bd)
{% endhint %}

```sql
WITH
    minIfState(number, number > 5) AS state_1,
    minSimpleStateIf(number, number > 5) AS state_2
SELECT
    byteSize(state_1),
    toTypeName(state_1),
    byteSize(state_2),
    toTypeName(state_2)
FROM numbers(10)
FORMAT Vertical

-- For UInt64
Row 1:
──────
byteSize(state_1):   24
toTypeName(state_1): AggregateFunction(minIf, UInt64, UInt8)
byteSize(state_2):   8
toTypeName(state_2): SimpleAggregateFunction(min, UInt64)

-- For UInt32
──────
byteSize(state_1):   16
byteSize(state_2):   4

-- For UInt16
──────
byteSize(state_1):   12
byteSize(state_2):   2

-- For UInt8
──────
byteSize(state_1):   10
byteSize(state_2):   1
```

There is one problem with that approach:  
`-SimpleStateIf` Would produce 0 as result in case of no-match, and it can mess up some aggregate functions state.  
It wouldn't affect functions like `max/argMax/sum`, but could affect functions like `min/argMin/any/anyLast`

```sql
SELECT
    minIfMerge(state_1),
    min(state_2)
FROM
(
    SELECT
        minIfState(number, number > 5) AS state_1,
        minSimpleStateIf(number, number > 5) AS state_2
    FROM numbers(5)
    UNION ALL
    SELECT
        minIfState(toUInt64(2), 2),
        minIf(2, 2)
)

┌─minIfMerge(state_1)─┬─min(state_2)─┐
│                   2 │            0 │
└─────────────────────┴──────────────┘
```

## Answer

There is 2 workarounds for that:  
1. Using Nullable datatype.  
2. Set result to some big number in case of no-match, which would be bigger than any possible value, so it would be safe to use. But it would work only for `min/argMin`

```sql
SELECT
    min(state_1),
    min(state_2)
FROM
(
    SELECT
        minSimpleState(if(number > 5, number, 1000)) AS state_1,
        minSimpleStateIf(toNullable(number), number > 5) AS state_2
    FROM numbers(5)
    UNION ALL
    SELECT
        minIf(2, 2),
        minIf(2, 2)
)

┌─min(state_1)─┬─min(state_2)─┐
│            2 │            2 │
└──────────────┴──────────────┘
```

© 2021 Altinity Inc. All rights reserved.

