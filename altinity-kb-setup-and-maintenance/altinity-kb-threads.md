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

© 2021 Altinity Inc. All rights reserved.

