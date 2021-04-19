# Atomic insert

Insert would be atomic only if those conditions match:

* Insert data only in single partition.
* Numbers of rows is less than `max_insert_block_size`.
* Table doesn't have MV \(there is no atomicity Table &lt;&gt; MV\)
* `input_format_parallel_parsing=0` set for clickhouse versions &gt;= 20.8

[https://github.com/ClickHouse/ClickHouse/issues/9195\#issuecomment-587500824](https://github.com/ClickHouse/ClickHouse/issues/9195#issuecomment-587500824)

