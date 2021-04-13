# Data Migration

## Export & Import into common data formats. <a id="DataMigration-Export&amp;Importintocommondataformats."></a>

Pros and cons:  
![\(plus\)](../../.gitbook/assets/add.png) Data can be inserted in some other than ClickHouse DBMS.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Needs additional sync for data consistency.  
![\(minus\)](../../.gitbook/assets/forbidden.png) High CPU and network usage.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Decoding&Encoding in common data formats slower than ClickHouse native formats.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Some of common data formats have incomplete support.

## remote/remoteSecure or cluster/Distributed table <a id="DataMigration-remote/remoteSecureorcluster/Distributedtable"></a>

Pros and cons:  
![\(plus\)](../../.gitbook/assets/add.png) Simple to run.  
![\(plus\)](../../.gitbook/assets/add.png) It’s possible to change schema and distribution of data between shards.  
![\(plus\)](../../.gitbook/assets/add.png) Needs only access to ClickHouse TCP port.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Needs additional sync for data consistency.  
![\(minus\)](../../.gitbook/assets/forbidden.png) High CPU and network usage.

Related settings:

```text
connect_timeout_with_failover_ms
connect_timeout_with_failover_secure_ms

max_insert_threads
min_insert_block_size_rows
min_insert_block_size_bytes
```

Suitable:

* Small amount of data. \(with some scripting would work even for big clusters\).
* Re-sharding and schema changing.

## clickhouse-copier <a id="DataMigration-clickhouse-copier"></a>

Pros and cons:

![\(plus\)](../../.gitbook/assets/add.png) Possible to change schema.  
![\(plus\)](../../.gitbook/assets/add.png) Needs only access to ClickHouse TCP port.  
![\(plus\)](../../.gitbook/assets/add.png) It’s possible to change schema and distribution of data between shards.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Doesn’t work well if data being ingested in source cluster.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Hard to setup.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Requires zookeeper.  
![\(minus\)](../../.gitbook/assets/forbidden.png) High CPU and network usage.

Notes:  
Internally it works like smart `INSERT INTO cluster(…) SELECT * FROM ...`  with some consistency checks.  
[clickhouse-copier](altinity-kb-clickhouse-copier/)

## rsync/manual parts moving <a id="DataMigration-rsync/manualpartsmoving"></a>

Pros and cons:  
![\(plus\)](../../.gitbook/assets/add.png) Low CPU and network usage.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Table schema should be the same.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Parts need’s to be properly registered in zookeeper.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Needs additional sync for data consistency.  
  
Notes:  
With some additional care and scripting it’s possible to do cheap re-sharding on parts level.

## Replication protocol <a id="DataMigration-Replicationprotocol"></a>

Pros and cons:  
![\(plus\)](../../.gitbook/assets/add.png) Simple to setup  
![\(plus\)](../../.gitbook/assets/add.png) No need for additional sync for data consistency.  
![\(plus\)](../../.gitbook/assets/add.png) Low CPU and network usage.  
![\(minus\)](../../.gitbook/assets/forbidden.png) Needs to reach both zookeeper client \(2181\) and ClickHouse replication ports: \(`interserver_http_port` or `interserver_https_port`\)  
![\(minus\)](../../.gitbook/assets/forbidden.png) In case of cluster migration, zookeeper need’s to be migrated too.  
[Zookeeper cluster migration](../altinity-kb-zookeeper/altinity-kb-zookeeper-cluster-migration.md)

## How to register parts in zookeeper: <a id="DataMigration-Howtoregisterpartsinzookeeper:"></a>

* Move them to `clickhouse/data/database/replicated_mt_table/detached` directory and run `ALTER TABLE replicated_mt_table ATTACH PARTITION ID ''` query for each partition.
* Move them to regular MergeTree table with same schema and run `ALTER TABLE replicated_mt_table ATTACH PARTITION ID '' FROM regular_mt_table` query for each partition.

Automation of that approach:  
[https://github.com/Altinity/clickhouse-zookeeper-recovery](https://github.com/Altinity/clickhouse-zookeeper-recovery)

## Github issues: <a id="DataMigration-Githubissues:"></a>

[https://github.com/ClickHouse/ClickHouse/issues/10943](https://github.com/ClickHouse/ClickHouse/issues/10943)  
[https://github.com/ClickHouse/ClickHouse/issues/20219](https://github.com/ClickHouse/ClickHouse/issues/20219)  
[https://github.com/ClickHouse/ClickHouse/pull/17871](https://github.com/ClickHouse/ClickHouse/pull/17871)

## Other links: <a id="DataMigration-Otherlinks:"></a>

[https://habr.com/ru/company/avito/blog/500678/](https://habr.com/ru/company/avito/blog/500678/)

