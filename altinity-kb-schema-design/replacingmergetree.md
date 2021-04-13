# ReplacingMergeTree

### Last state

```sql
CREATE TABLE repl_tbl
(
    `key` UInt32,
    `val_1` UInt32,
    `val_2` String,
    `val_3` String,
    `val_4` String,
    `val_5` UUID,
    `ts` DateTime
)
ENGINE = ReplacingMergeTree(ts)
ORDER BY key

SYSTEM STOP MERGES repl_tbl;

INSERT INTO repl_tbl SELECT number as key, rand() as val_1, randomStringUTF8(10) as val_2, randomStringUTF8(5) as val_3, randomStringUTF8(4) as val_4, generateUUIDv4() as val_5, now() as ts FROM numbers(10000000);
INSERT INTO repl_tbl SELECT number as key, rand() as val_1, randomStringUTF8(10) as val_2, randomStringUTF8(5) as val_3, randomStringUTF8(4) as val_4, generateUUIDv4() as val_5, now() as ts FROM numbers(10000000);
INSERT INTO repl_tbl SELECT number as key, rand() as val_1, randomStringUTF8(10) as val_2, randomStringUTF8(5) as val_3, randomStringUTF8(4) as val_4, generateUUIDv4() as val_5, now() as ts FROM numbers(10000000);
INSERT INTO repl_tbl SELECT number as key, rand() as val_1, randomStringUTF8(10) as val_2, randomStringUTF8(5) as val_3, randomStringUTF8(4) as val_4, generateUUIDv4() as val_5, now() as ts FROM numbers(10000000);

SELECT count() FROM repl_tbl

┌──count()─┐
│ 50000000 │
└──────────┘
```

#### Single key

```sql
SELECT key, argMax(val_1, ts) as val_1, argMax(val_2, ts) as val_2, argMax(val_3, ts) as val_3, argMax(val_4, ts) as val_4, argMax(val_5, ts) as val_5, max(ts) FROM repl_tbl WHERE key = 10 GROUP BY key;
1 rows in set. Elapsed: 0.017 sec. Processed 40.96 thousand rows, 5.24 MB (2.44 million rows/s., 312.31 MB/s.)

SELECT * FROM repl_tbl WHERE key = 10 ORDER BY ts DESC LIMIT 1 BY key ;
1 rows in set. Elapsed: 0.017 sec. Processed 40.96 thousand rows, 5.24 MB (2.39 million rows/s., 305.41 MB/s.)

SELECT * FROM repl_tbl WHERE key = 10 AND ts = (SELECT max(ts) FROM repl_tbl WHERE key = 10);
1 rows in set. Elapsed: 0.019 sec. Processed 40.96 thousand rows, 1.18 MB (2.20 million rows/s., 63.47 MB/s.)

SELECT * FROM repl_tbl FINAL WHERE key = 10;
1 rows in set. Elapsed: 0.021 sec. Processed 40.96 thousand rows, 5.24 MB (1.93 million rows/s., 247.63 MB/s.)
```

#### Multiple keys

```sql
SELECT key, argMax(val_1, ts) as val_1, argMax(val_2, ts) as val_2, argMax(val_3, ts) as val_3, argMax(val_4, ts) as val_4, argMax(val_5, ts) as val_5, max(ts) FROM repl_tbl WHERE key IN (SELECT toUInt32(number)　FROM numbers(1000000)　WHERE number % 100) GROUP BY key FORMAT Null;
Peak memory usage (for query): 2.31 GiB.
0 rows in set. Elapsed: 3.264 sec. Processed 5.04 million rows, 645.01 MB (1.54 million rows/s., 197.60 MB/s.)

-- set optimize_aggregation_in_order=1;
Peak memory usage (for query): 1.11 GiB.
0 rows in set. Elapsed: 1.772 sec. Processed 2.74 million rows, 350.30 MB (1.54 million rows/s., 197.73 MB/s.)

SELECT * FROM repl_tbl WHERE key IN (SELECT toUInt32(number)　FROM numbers(1000000)　WHERE number % 100) ORDER BY ts DESC LIMIT 1 BY key FORMAT Null;
Peak memory usage (for query): 1.08 GiB.
0 rows in set. Elapsed: 2.429 sec. Processed 5.04 million rows, 645.01 MB (2.07 million rows/s., 265.58 MB/s.)

SELECT * FROM repl_tbl WHERE (key, ts) IN (SELECT key, max(ts) FROM repl_tbl WHERE key IN (SELECT toUInt32(number)　FROM numbers(1000000)　WHERE number % 100) GROUP BY key) FORMAT Null;
Peak memory usage (for query): 432.57 MiB.
0 rows in set. Elapsed: 0.939 sec. Processed 5.04 million rows, 160.33 MB (5.36 million rows/s., 170.69 MB/s.)

-- set optimize_aggregation_in_order=1;
Peak memory usage (for query): 202.88 MiB.
0 rows in set. Elapsed: 0.824 sec. Processed 5.04 million rows, 160.33 MB (6.11 million rows/s., 194.58 MB/s.)
```



