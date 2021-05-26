# Backups



ClickHouse is currently at the design stage of creating some universal backup solution. Some custom backup strategies are:

1. Each shard is backed up separately.
2. FREEZE the table/partition. For more information, see [Alter Freeze Partition](https://clickhouse.tech/docs/en/sql-reference/statements/alter/partition/#alter_freeze-partition).
   1. This creates hard links in shadow subdirectory.
3. rsync that directory to a backup location, then remove that subfolder from shadow.
   1. Cloud users are recommended to use [Rclone](https://rclone.org/).
4. Always add the full contents of the metadata subfolder that contains the current DB schema and clickhouse configs to your backup.
5. For a second replica, it’s enough to copy metadata and configuration. This implementation follows a similar approach by [clickhouse-backup](https://github.com/AlexAkulov/clickhouse-backup). We have not used this tool on production systems, and can make no recommendations for or against it. As of this time clickhouse-backup is not a complete backup solution, but it does simply some parts of the backup process.
6. Don’t try to compress backups; the data is already compressed in ClickHouse.

