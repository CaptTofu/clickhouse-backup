---
description: >-
  INSERT INTO destination SELECT * FROM
  remote('ch-server',database,source,user,password)
---

# remote\(...\) table function

Suitable for moving up to hundreds of gigabytes of data.

Clickhouse tries to form blocks of data in memory and while one of limit: `min_insert_block_size_rows` or `min_insert_block_size_bytes` being hit, clickhouse dump this block on disk. If clickhouse tries to execute insert in parallel \(`max_insert_threads > 1`\), it would form multiple blocks at one time.  
So maximum memory usage can be calculated like this: `max_insert_threads * first(min_insert_block_size_rows OR min_insert_block_size_bytes)`

Default values:

```sql
┌─name────────────────────────┬─value─────┐
│ min_insert_block_size_rows  │ 1048545   │
│ min_insert_block_size_bytes │ 268427520 │
│ max_insert_threads          │ 0         │ <- Values 0 or 1 means that INSERT SELECT is not run in parallel.
└─────────────────────────────┴───────────┘
```

Depends on your table width \(average row size\) and amount of memory which are safe to occupy by INSERT SELECT query, you need to tune settings accordingly.

Possible issues:

```sql
SELECT count()
FROM remote('server.from.remote.dc:9440', 'default.table', 'admin', 'password')
Received exception from server (version 20.8.11):
Code: 519. DB::Exception: Received from localhost:9000. DB::Exception: All attempts to get table structure failed. Log:
Code: 279, e.displayText() = DB::NetException: All connection tries failed. Log:
Code: 209, e.displayText() = DB::NetException: Timeout: connect timed out: 192.0.2.1:9440 (server.from.remote.dc:9440) (version 20.8.11.17 (official build))
Code: 209, e.displayText() = DB::NetException: Timeout: connect timed out: 192.0.2.1:9440 (server.from.remote.dc:9440) (version 20.8.11.17 (official build))
Code: 209, e.displayText() = DB::NetException: Timeout: connect timed out: 192.0.2.1:9440 (server.from.remote.dc:9440) (version 20.8.11.17 (official build))
```

1. Using remote\(...\) table function with secure TCP port \(default values is 9440\). There is remoteSecure\(\) function for that.  
2. High \(&gt;50ms\) ping between servers, values for `connect_timeout_with_failover_ms,`  `connect_timeout_with_failover_secure_ms` need's to be adjusted accordingly.  

Default values:

```sql
┌─name────────────────────────────────────┬─value─┐
│ connect_timeout_with_failover_ms        │ 50    │
│ connect_timeout_with_failover_secure_ms │ 100   │
└─────────────────────────────────────────┴───────┘
```

© 2021 Altinity Inc. All rights reserved.

