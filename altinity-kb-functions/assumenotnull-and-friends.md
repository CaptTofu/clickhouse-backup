# assumeNotNull and friends

`assumeNotNull` result is implementation specific:

```sql
WITH CAST(NULL, 'Nullable(UInt8)') AS column
SELECT
    column,
    assumeNotNull(column + 999) AS x


┌─column─┬─x─┐
│   ᴺᵁᴸᴸ │ 0 │
└────────┴───┘

WITH CAST(NULL, 'Nullable(UInt8)') AS column
SELECT
    column,
    assumeNotNull(materialize(column) + 999) AS x

┌─column─┬───x─┐
│   ᴺᵁᴸᴸ │ 999 │
└────────┴─────┘
```

If it's possible to have Null values, it's better to use `ifNull` function instead.

```sql
SELECT count()
FROM numbers_mt(1000000000)
WHERE NOT ignore(ifNull(toNullable(number), 0))

┌────count()─┐
│ 1000000000 │
└────────────┘

1 rows in set. Elapsed: 0.705 sec. Processed 1.00 billion rows, 8.00 GB (1.42 billion rows/s., 11.35 GB/s.)

SELECT count()
FROM numbers_mt(1000000000)
WHERE NOT ignore(coalesce(toNullable(number), 0))

┌────count()─┐
│ 1000000000 │
└────────────┘

1 rows in set. Elapsed: 2.383 sec. Processed 1.00 billion rows, 8.00 GB (419.56 million rows/s., 3.36 GB/s.)

SELECT count()
FROM numbers_mt(1000000000)
WHERE NOT ignore(assumeNotNull(toNullable(number)))

┌────count()─┐
│ 1000000000 │
└────────────┘

1 rows in set. Elapsed: 0.051 sec. Processed 1.00 billion rows, 8.00 GB (19.62 billion rows/s., 156.98 GB/s.)
```

