---
description: Clickhouse table sampling example
---

# Sampling example

The most important idea about sampling that the primary index must have low cardinality -- in this case sampling will work.

And sampling requires values which occupy all range of sampled column type. I cannot use `transaction_id` directly because I am not sure that min value of `transaction_id` = 0 and max value = MAX\_UINT64. So I used `cityHash64(transaction_id)`. Otherwise the results of sampled queries will be skewed. Because CH simply requests `where sample_col >= 0 and sample_col <= MAX_UINT64/2` in case of `sample 0.5`.

### Sampling-freandly table

```sql
CREATE TABLE table_one
( timestamp UInt64,
  transaction_id UInt64,
  banner_id UInt16,
  value UInt32
)
ENGINE = MergeTree()
PARTITION BY toYYYYMMDD(toDateTime(timestamp))
ORDER BY (banner_id, 
          toStartOfHour(toDateTime(timestamp)),  
          cityHash64(transaction_id))
SAMPLE BY cityHash64(transaction_id)
SETTINGS index_granularity = 8192

insert into table_one 
select 1602809234+intDiv(number,100000), 
       number, 
       number%991, 
       toUInt32(rand())
from numbers(10000000000);
```

I had to reduced the granularity of the `timestamp` column to one hour `toStartOfHour(toDateTime(timestamp))` otherwise sampling will not work.

#### Test that sampling is working:

```sql
-- Q1. No where filters. 
-- The query is 10 times faster with SAMPLE 0.01
select banner_id, sum(value), count(value), max(value)
from table_one 
group by banner_id format Null;

0 rows in set. Elapsed: 11.490 sec. 
     Processed 10.00 billion rows, 60.00 GB (870.30 million rows/s., 5.22 GB/s.)

select banner_id, sum(value), count(value), max(value)
from table_one SAMPLE 0.01
group by banner_id format Null;

0 rows in set. Elapsed: 1.316 sec. 
     Processed 452.67 million rows, 6.34 GB (343.85 million rows/s., 4.81 GB/s.)


-- Q2. Filter by the first column in index (banner_id = 42)
-- The query is 20 times faster with SAMPLE 0.01
-- reads 20 times less rows: 10.30 million rows VS Processed 696.32 thousand rows
select banner_id, sum(value), count(value), max(value)
from table_one 
WHERE banner_id = 42
group by banner_id format Null;

0 rows in set. Elapsed: 0.020 sec. 
     Processed 10.30 million rows, 61.78 MB (514.37 million rows/s., 3.09 GB/s.)

select banner_id, sum(value), count(value), max(value)
from table_one SAMPLE 0.01
WHERE banner_id = 42
group by banner_id format Null;

0 rows in set. Elapsed: 0.008 sec. 
     Processed 696.32 thousand rows, 9.75 MB (92.49 million rows/s., 1.29 GB/s.)


-- Q3. No filters
-- The query is 10 times faster with SAMPLE 0.01
-- reads 20 times less rows.
select banner_id, 
       toStartOfHour(toDateTime(timestamp)) hr, 
       sum(value), count(value), max(value)
from table_one 
group by banner_id, hr format Null;
0 rows in set. Elapsed: 36.660 sec. 
     Processed 10.00 billion rows, 140.00 GB (272.77 million rows/s., 3.82 GB/s.)

select banner_id, 
       toStartOfHour(toDateTime(timestamp)) hr, 
       sum(value), count(value), max(value)
from table_one SAMPLE 0.01
group by banner_id, hr format Null;
0 rows in set. Elapsed: 3.741 sec. 
     Processed 452.67 million rows, 9.96 GB (121.00 million rows/s., 2.66 GB/s.)



-- Q4. Filter by not indexed column
-- The query is 6 times faster with SAMPLE 0.01
-- reads 20 times less rows.
select count()
from table_one 
where value = 666 format Null;
1 rows in set. Elapsed: 6.056 sec. 
     Processed 10.00 billion rows, 40.00 GB (1.65 billion rows/s., 6.61 GB/s.)

select count()
from table_one  SAMPLE 0.01
where value = 666 format Null;
1 rows in set. Elapsed: 1.214 sec. 
     Processed 452.67 million rows, 5.43 GB (372.88 million rows/s., 4.47 GB/s.)
     
```

### Not Sampling-freandly table

```sql
CREATE TABLE table_one
( timestamp UInt64,
  transaction_id UInt64,
  banner_id UInt16,
  value UInt32
)
ENGINE = MergeTree()
PARTITION BY toYYYYMMDD(toDateTime(timestamp))
ORDER BY (banner_id, 
          timestamp, 
          cityHash64(transaction_id))
SAMPLE BY cityHash64(transaction_id)
SETTINGS index_granularity = 8192

insert into table_one 
select 1602809234+intDiv(number,100000), 
       number, 
       number%991, 
       toUInt32(rand())
from numbers(10000000000);
```

All is the same BUT granularity of `timestamp` column is not reduced.

#### Test that sampling is not working:

```sql
-- Q1. No where filters. 
-- The query is 2 times SLOWER!!! with SAMPLE 0.01
-- Because it needs to read excessive column with sampling data!
select banner_id, sum(value), count(value), max(value)
from table_one 
group by banner_id format Null;
0 rows in set. Elapsed: 11.196 sec. 
     Processed 10.00 billion rows, 60.00 GB (893.15 million rows/s., 5.36 GB/s.)

select banner_id, sum(value), count(value), max(value)
from table_one SAMPLE 0.01
group by banner_id format Null;
0 rows in set. Elapsed: 24.378 sec. 
     Processed 10.00 billion rows, 140.00 GB (410.21 million rows/s., 5.74 GB/s.)


-- Q2. Filter by the first column in index (banner_id = 42)
-- The query is SLOWER with SAMPLE 0.01
select banner_id, sum(value), count(value), max(value)
from table_one 
WHERE banner_id = 42
group by banner_id format Null;
0 rows in set. Elapsed: 0.022 sec. 
     Processed 10.27 million rows, 61.64 MB (459.28 million rows/s., 2.76 GB/s.)

select banner_id, sum(value), count(value), max(value)
from table_one SAMPLE 0.01
WHERE banner_id = 42
group by banner_id format Null;
0 rows in set. Elapsed: 0.037 sec. 
     Processed 10.27 million rows, 143.82 MB (275.16 million rows/s., 3.85 GB/s.)


-- Q3. No filters
-- The query is SLOWER with SAMPLE 0.01
select banner_id, 
       toStartOfHour(toDateTime(timestamp)) hr, 
       sum(value), count(value), max(value)
from table_one 
group by banner_id, hr format Null;
0 rows in set. Elapsed: 21.663 sec. 
     Processed 10.00 billion rows, 140.00 GB (461.62 million rows/s., 6.46 GB/s.)


select banner_id, 
       toStartOfHour(toDateTime(timestamp)) hr, sum(value), 
       count(value), max(value)
from table_one SAMPLE 0.01
group by banner_id, hr format Null;
0 rows in set. Elapsed: 26.697 sec. 
     Processed 10.00 billion rows, 220.00 GB (374.57 million rows/s., 8.24 GB/s.)


-- Q4. Filter by not indexed column
-- The query is SLOWER with SAMPLE 0.01
select count()
from table_one 
where value = 666 format Null;
0 rows in set. Elapsed: 7.679 sec. 
     Processed 10.00 billion rows, 40.00 GB (1.30 billion rows/s., 5.21 GB/s.)

select count()
from table_one  SAMPLE 0.01
where value = 666 format Null;
0 rows in set. Elapsed: 21.668 sec. 
     Processed 10.00 billion rows, 120.00 GB (461.51 million rows/s., 5.54 GB/s.)

```

