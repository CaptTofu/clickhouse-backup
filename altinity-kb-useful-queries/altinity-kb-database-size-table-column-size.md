# Database Size - Table - Column size

## Table size <a id="DatabaseSize-Table-Columnsize-Tablesize"></a>

```sql
SELECT
    database,
    table,
    formatReadableSize(sum(bytes) AS size) AS compressed,
    formatReadableSize(sum(data_uncompressed_bytes)) AS uncompressed,
    sum(rows) AS rows,
    count() AS part_count
FROM system.parts
WHERE (active = 1) AND (table LIKE '%') AND (database LIKE '%')
GROUP BY
    database,
    table
ORDER BY size DESC;


┌─database─┬─table───────┬─compressed─┬─uncompressed─┬──────rows─┬─part_count─┐
│ default  │ test        │ 1.94 GiB   │ 6.34 GiB     │ 210000000 │          6 │
│ default  │ dated_value │ 280.00 B   │ 34.00 B      │         2 │          1 │
└──────────┴─────────────┴────────────┴──────────────┴───────────┴────────────┘
```

## Column size <a id="DatabaseSize-Table-Columnsize-Columnsize"></a>

```sql
SELECT
    database,
    table,
    column,
    formatReadableSize(sum(column_data_compressed_bytes) AS size) AS compressed,
    formatReadableSize(sum(column_data_uncompressed_bytes)) AS uncompressed
FROM system.parts_columns
WHERE (active = 1) AND (table LIKE 'query_log')
GROUP BY
    database,
    table,
    column
ORDER BY size DESC

Query id: 468f5d9c-f3e8-49b3-8cd4-69ef4fc68897

┌─database─┬─table─────┬─column──────────────────────────────┬─compressed─┬─uncompressed─┐
│ system   │ query_log │ query_id                            │ 37.38 MiB  │ 67.95 MiB    │
│ system   │ query_log │ ProfileEvents.Values                │ 25.29 MiB  │ 173.31 MiB   │
│ system   │ query_log │ thread_ids                          │ 8.96 MiB   │ 32.20 MiB    │
│ system   │ query_log │ ProfileEvents.Names                 │ 7.80 MiB   │ 431.57 MiB   │
│ system   │ query_log │ event_time_microseconds             │ 7.67 MiB   │ 14.69 MiB    │
│ system   │ query_log │ query_start_time_microseconds       │ 6.60 MiB   │ 14.69 MiB    │
```

© 2021 Altinity Inc. All rights reserved.

