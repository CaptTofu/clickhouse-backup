# Implementation details

All tables in DatabaseAtomic have persistent UUID and store data in `/clickhouse_path/store/xxx/xxxyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy/`

where `xxxyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy` is UUID of the table.  
RENAMEs are performed without changing UUID and moving table data.

Tables in Atomic databases can be accessed by UUID through DatabaseCatalog.  
On `DROP TABLE`, no data is removed, DatabaseAtomic just marks table as dropped by moving metadata to `/clickhouse_path/metadata_dropped/` and notifies DatabaseCatalog.

Running queries still may use dropped table. Table will be actually removed when it's not in use.  
Allows to execute RENAME and DROP without IStorage-level RWLocks

The idea is to store table data in unique directories that don't contain the table name and link to them via symlinks. These directories will be refcounted and may live after table DROP if the table is in use.

## Step 1 <a id="Implementationdetails-Step1"></a>

Allow special clause UUID in ATTACH TABLE statement that may contain randomly generated UUID for table.

Create `DatabaseAtomic` that is intended to replace `DatabaseOrdinary` as the default database engine.

* On table creation it will:
  * generate UUID for table;
  * store table metadata as ATTACH query in usual `/metadata/database/table.sql` file;
  * ATTACH query will contain UUID clause;
  * ATTACH query will contain some placeholder instead of table name. Example: `ATTACH TABLE table`;
  * create a directory for table data at `/store/xxx/xxxyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy/`;
  * `store` is a new directory inside ClickHouse path; `xxx` - is the first three letters of uuid.
  * this directory does not contain table name neither database name;
  * create symlink `/data/database/table` that resembles the structure of DatabaseOrdinary;
  * set up refcount in memory that is hold by database object.
* On table drop it will:
  * remove symlink `/data/database/table`;
  * remove table metadata \(`.sql` file\);
  * decrement refrount that was held by database; Refcounts for table are stored only in memory.
* On table rename it will:
  * rename symlink and metadata file;
  * change table name in it's object in memory; table name is accessed and changed under short lock with a simple mutex.
* On database load at startup:
  * the table name is determined by the name of the `.sql` file.

Additional considerations:

* the table data may be deleted lazily and deletion can be postponed to some time similar to deletion of data parts in StorageMergeTree;
* the table data may be left as "garbage" after incorrect server restart; probably it's better to avoid implementing garbage collection at all \(or at least avoid to do it automatically\);
* if there is a safety limit on maximum table size to drop, it should limit both the DROP query itself and background deletion;
* provide a way to naturally use UUIDs as "replica path" for ReplicatedMergeTree tables; the user should not worry about replica path;
* need to show UUIDs in system.tables;
* easy possible enhancement is to allow specify different path for "store" for a table;
* tables for different databases are stored together in "store" - this allows simple moving between databases with RENAME \(if the databases have the same engine and tables have the same stores\);
* symlinks are actually unneeded but will be created for easy introspection/debugging.

## Step 2 <a id="Implementationdetails-Step2"></a>

We want the same for databases to allow `RENAME DATABASE`. But we cannot create a different engine - we need just to adopt existing catalog:

* allow `database.sql` files to contain UUID clause and a placeholder instead of database name: `CREATE DATABASE database ENGINE = 'Atomic' UUID = 'yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy'`;
* make `metadata` directory a symlink to `/store/xxx/xxxyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy/metadata`;
* make `data` directory a symlink to `/store/xxx/xxxyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy/data`; \(note that if the database is DatabaseAtomic, its data directory will also contain symlinks\)

Databases will be created in this way under feature flag \(initially disabled by default\).  
Default database engine \(`Ordinary`, `Atomic`\) is also controlled by a setting.

## References <a id="Implementationdetails-References"></a>

{% embed url="https://github.com/ClickHouse/ClickHouse/issues/6787" %}

© 2021 Altinity Inc. All rights reserved.
