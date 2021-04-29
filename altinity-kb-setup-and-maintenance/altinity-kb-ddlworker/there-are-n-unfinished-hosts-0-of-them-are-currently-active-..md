# There are N unfinished hosts \(0 of them are currently active\).

Sometimes your Distributed DDL queries are being stuck, and not executing on all or subset of nodes, there is a lot of possible reasons for that kind of behavior, so it's would take some time and effort to investigation.

#### Possible reasons:

#### Clickhouse node can't recognize itself.

```sql
SELECT * FROM system.clusters; -- check is_local column, it should have 1 for itself
```

```bash
getent hosts clickhouse.local.net # or other name which should be local
hostname --fqdn

cat /etc/hosts
cat /etc/hostname
```

{% page-ref page="./" %}

#### Debian / Ubuntu

There is an issue in Debian based images, when hostname being mapped to 127.0.1.1 address which doesn't literally match network interface and clickhouse fails to detect this address as local.

{% embed url="https://github.com/ClickHouse/ClickHouse/issues/23504" %}

#### Previous task is being executed and taking some time.

It's usually some heavy operations like merges, mutations, alter columns, so it make sense to check those tables:

```sql
SHOW PROCESSLIST;
SELECT * FROM system.merges;
SELECT * FROM system.mutations;
```

In that case, you can just wait completion of previous task.

#### Previous task is stuck because of some error.

In that case, the first step is understand which exact task is stuck and why. There is some queries which can help with that.

```sql
-- list of all distributed ddl queries, path can be different in your installation
SELECT * FROM system.zookeeper WHERE path = '/clickhouse/task_queue/ddl/';

-- information about specific task.
SELECT * FROM system.zookeeper WHERE path = '/clickhouse/task_queue/ddl/query-0000001000/';
SELECT * FROM system.zookeeper WHERE path = '/clickhouse/task_queue/ddl/' AND name = 'query-0000001000';

-- How many nodes executed this task
SELECT name, numChildren as success_nodes FROM system.zookeeper WHERE path = '/clickhouse/task_queue/ddl/query-0000001000/' AND name = 'finished';

┌─name─────┬─success_nodes─┐
│ finished │             0 │
└──────────┴───────────────┘

-- Latest successfull executed tasks from query_log.
SELECT query FROM system.query_log WHERE query LIKE '%ddl_entry%' AND type = 2 ORDER BY event_time DESC LIMIT 5;

-- Information about task execution from logs.
grep -C 40 "ddl\_entry" /var/log/clickhouse-server/clickhouse-server*.log
```

#### Issues that can prevent the task execution:

Obsolete replicas left in zookeeper.

```sql
SELECT database, table, zookeeper_path, replica_path zookeeper FROM system.replicas WHERE total_replicas != active_replicas;

SELECT * FROM system.zookeeper WHERE path = '/clickhouse/cluster/tables/01/database/table/replicas';

SYSTEM DROP REPLICA 'replica_name';

SYSTEM STOP REPLICATION QUEUES;
SYSTEM START REPLICATION QUEUES;
```

[https://clickhouse.tech/docs/en/sql-reference/statements/system/\#query\_language-system-drop-replica](https://clickhouse.tech/docs/en/sql-reference/statements/system/#query_language-system-drop-replica)

