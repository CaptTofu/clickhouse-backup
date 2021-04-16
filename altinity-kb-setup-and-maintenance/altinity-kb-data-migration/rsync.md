# rsync

### Short Instruction

1. Do [FREEZE TABLE](https://clickhouse.tech/docs/en/sql-reference/statements/alter/partition/#alter_freeze-partition) on needed table, partition. It would produce consistent snapshot of table data.
2. Run rsync command.

   ```bash
   rsync -ravlW --bwlimit=100000 /var/lib/clickhouse/data/shadow/N/database/table 
       root@remote_host:/var/lib/clickhouse/data/database/table/detached
   ```

   `--bwlimit` is transfer limit in KBytes per second. 

3. Run[ ATTACH PARTITION](https://clickhouse.tech/docs/en/sql-reference/statements/alter/partition/#alter_attach-partition) for each partition from `./detached` directory.

### How to register parts in zookeeper:

* Move them to `clickhouse/data/database/replicated_mt_table/detached` directory and run `ALTER TABLE replicated_mt_table ATTACH PARTITION ID ''` query for each partition.
* Move them to regular MergeTree table with same schema and run `ALTER TABLE replicated_mt_table ATTACH PARTITION ID '' FROM regular_mt_table` query for each partition.

Automation of that approach:  
[https://github.com/Altinity/clickhouse-zookeeper-recovery](https://github.com/Altinity/clickhouse-zookeeper-recovery)

This script can be reused for register parts in ZooKeeper, because situation when you just moved your parts to ReplicatedMergeTree table directory and don't have them in ZooKeeper is identical with loss data in ZooKeeper.

© 2021 Altinity Inc. All rights reserved.

