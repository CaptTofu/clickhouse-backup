# Threads

Collect thread names & counts using ps & clickhouse-local

```text
ps H -o 'tid comm' $(pidof -s clickhouse-server) |  tail -n +2 | awk '{ printf("%s\t%s\n", $1, $2) }' | clickhouse-local -S "threadid UInt16, name String" -q "SELECT name, count() FROM table GROUP BY name WITH TOTALS ORDER BY count() DESC FORMAT PrettyCompact"
```

Check threads used by running queries:

```text
select query, length(thread_ids) as threads_count from system.processes order by threads_count;
```

```text
# cat /proc/$(pidof -s clickhouse-server)/status | grep Threads
Threads: 103
# ps hH $(pidof -s clickhouse-server) | wc -l
103
# ps hH -AF | grep clickhouse | wc -l
116
```

Pools

```text
SELECT
    name,
    value
FROM system.settings
WHERE name LIKE '%pool%'

┌─name─────────────────────────────────────────┬─value─┐
│ connection_pool_max_wait_ms                  │ 0     │
│ distributed_connections_pool_size            │ 1024  │
│ background_buffer_flush_schedule_pool_size   │ 16    │
│ background_pool_size                         │ 16    │
│ background_move_pool_size                    │ 8     │
│ background_fetches_pool_size                 │ 8     │
│ background_schedule_pool_size                │ 16    │
│ background_message_broker_schedule_pool_size │ 16    │
│ background_distributed_schedule_pool_size    │ 16    │
│ postgresql_connection_pool_size              │ 16    │
│ postgresql_connection_pool_wait_timeout      │ -1    │
│ odbc_bridge_connection_pool_size             │ 16    │
└──────────────────────────────────────────────┴───────┘
```

```text
SELECT
    metric,
    value
FROM system.metrics
WHERE metric LIKE 'Background%'

Query id: e65544a0-0542-4bd1-bc28-007cdc29d2a3

┌─metric──────────────────────────────────┬─value─┐
│ BackgroundPoolTask                      │     0 │
│ BackgroundFetchesPoolTask               │     0 │
│ BackgroundMovePoolTask                  │     0 │
│ BackgroundSchedulePoolTask              │     0 │
│ BackgroundBufferFlushSchedulePoolTask   │     0 │
│ BackgroundDistributedSchedulePoolTask   │     0 │
│ BackgroundMessageBrokerSchedulePoolTask │     0 │
└─────────────────────────────────────────┴───────┘
```

Stacktraces 

```text
 SET allow_introspection_functions = 1;
 WITH arrayMap(x -> demangle(addressToSymbol(x)), trace) AS all SELECT thread_id, query_id, arrayStringConcat(all, '\n') AS res FROM system.stack_trace　WHERE res ILIKE '%Pool%';
```

© 2021 Altinity Inc. All rights reserved.

