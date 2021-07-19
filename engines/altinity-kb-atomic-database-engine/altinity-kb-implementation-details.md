# Implementation details

All tables in DatabaseAtomic have persistent UUID and store data in `/clickhouse_path/store/xxx/xxxyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy/`

where `xxxyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy` is UUID of the table.  
RENAMEs are performed without changing UUID and moving table data.

Tables in Atomic databases can be accessed by UUID through DatabaseCatalog.  
On `DROP TABLE`, no data is removed, DatabaseAtomic just marks table as dropped by moving metadata to `/clickhouse_path/metadata_dropped/` and notifies DatabaseCatalog.

Running queries still may use dropped table. Table will be actually removed when it's not in use.  
Allows to execute RENAME and DROP without IStorage-level RWLocks

More info: [https://github.com/ClickHouse/ClickHouse/issues/6787](https://github.com/ClickHouse/ClickHouse/issues/6787)

## References <a id="Implementationdetails-References"></a>

{% embed url="https://github.com/ClickHouse/ClickHouse/issues/6787" caption="" %}

© 2021 Altinity Inc. All rights reserved.

