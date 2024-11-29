---
description: clickhouse-backup restore to different table and/or DB 
---

# Question: How can a backup from a particular database or table be restored to a different database or table? 

I have two databases, one is `analytics`, and it has a table called `trips` that I'd like to restore to the the `prod` database 

### Solution

This can be accomplished using the two options

* Database re-mapping: `--restore-database-mapping old:new`
* Table re-mapping: `--restore-table-mapping old:new` 

These can be used together or exclusively, depening on what one wants

Below, the following demonstrates how both are used in conjunction with another to achieve the stated goal of the question

### Demonstration 

#### Confirm the backup to be made and create it

First, confirm/identify a table you might want to backup, in this case in a database called `analytics`:

```yaml

$ clickhouse-backup tables --tables=analytics.*
analytics.trips  118.58MiB  default  full

$ clickhouse-client -d analytics
ClickHouse client version 24.9.2.42 (official build).
Connecting to database analytics at 127.0.0.1:9000 as user default.
Connected to ClickHouse server version 24.9.2.

infra :) select count(*) from trips;

SELECT count(*)
FROM trips

Query id: fb4a5d18-5a82-490c-9309-8cbe4e0f0de7

   ┌─count()─┐
1. │ 3000317 │ -- 3.00 million
   └─────────┘

1 row in set. Elapsed: 0.005 sec. 

```


As seen above, `analytics.trips` is the one of interest. 

Create a local backup:

```bash
$ clickhouse-backup create --table analytics.trips
```

list backups to confirm it was created. 

```bash
$ clickhouse-backup list
2024-11-29T17-04-22   118.59MiB   29/11/2024 17:04:22   local      regular
```

Also, it'll be found on the filesystem in `/var/lib/clickhouse/backup`, time-stamped directory:

```bash

infra:/var/lib/clickhouse/backup$ ls -l 2024-11-29T17-04-22/
total 16
drwxr-x--- 2 clickhouse clickhouse 4096 Nov 29 17:04 access
drwxr-x--- 3 clickhouse clickhouse 4096 Nov 29 17:04 metadata
-rw-r----- 1 clickhouse clickhouse  582 Nov 29 17:04 metadata.json
drwxr-x--- 3 clickhouse clickhouse 4096 Nov 29 17:04 shadow

```

Now, restore


```bash
clickhouse-backup restore --table analytics.trips --restore-database-mapping analytics:prod --restore-table-mapping trips:newtrips  2024-11-29T17-04-22/

```

#### Confirm the restoration!

```
$ clickhouse-backup tables --table prod.*
prod.newtrips  118.58MiB  default  full
```

Check integrity of the data:

```
clickhouse-client -d prod 
ClickHouse client version 24.9.2.42 (official build).
Connecting to database prod at 127.0.0.1:9000 as user default.
Connected to ClickHouse server version 24.9.2.

infra :) select count(*) from newtrips;

SELECT count(*)
FROM newtrips

Query id: e324f435-e751-4de1-9379-e87c43101f19

   ┌─count()─┐
1. │ 3000317 │ -- 3.00 million
   └─────────┘

1 row in set. Elapsed: 0.004 sec. 

```
