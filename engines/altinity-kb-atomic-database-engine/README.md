# Atomic Database Engine

Supports

* non-blocking drop table / rename table
* tables delete \(&detach\) async \(wait for selects finish but invisible for new selects\)
* atomic drop table \(all files / folders removed\)
* atomic table swap \(table swap by "EXCHANGE TABLES t1 AND t2;"\)
* rename dictionary / rename database
* unique automatic UUID paths in FS and ZK for Replicated

### FAQ <a id="FAQ"></a>

**Q. Data is not removed immediately**

A. Use`DROP TABLE t SYNC;`

Or use parameter \(user level\) database\_atomic\_wait\_for\_drop\_and\_detach\_synchronously`:`

```sql
SET database_atomic_wait_for_drop_and_detach_synchronously = 1;
```

Also, you can decrease the delay used by Atomic for real table drop \(it’s 8 minutes by default\)

```bash
cat /etc/clickhouse-server/config.d/database_atomic_delay_before_drop_table.xml 
<yandex>
    <database_atomic_delay_before_drop_table_sec>1</database_atomic_delay_before_drop_table_sec>
</yandex>
```

**Q. I cannot reuse zookeeper path after dropping the table.**

A. This happens because real table deletion occurs with a controlled delay. See the previous question to remove the table immediately.

With engine=Atomic it’s possible \(and is a good practice if you do it correctly\) to include UUID into zookeeper path, i.e. :

```sql
CREATE ... 
ON CLUSTER ... 
ENGINE=ReplicatedMergeTree('/clickhouse/tables/{uuid}/{shard}/', '{replica}')
```

See also: [https://github.com/ClickHouse/ClickHouse/issues/12135\#issuecomment-653932557](https://github.com/ClickHouse/ClickHouse/issues/12135#issuecomment-653932557)

It’s very important that the table will have the same UUID cluster-wide.

When the table is created using _ON CLUSTER_ - all tables will get the same UUID automatically.  
When it needs to be done manually \(for example - you need to add one more replica\), pick CREATE TABLE statement with UUID from one of the existing replicas.

```sql
set show_table_uuid_in_table_create_qquery_if_not_nil=1　;
SHOW CREATE TABLE xxx; /* or SELECT create_table_query FROM system.tables WHERE ... */
```

### Using Ordinary by default instead of Atomic <a id="Using-Ordinary-by-default-instead-of-Atomic-[hardBreak]"></a>

```bash
# cat /etc/clickhouse-server/users.d/disable_atomic_database.xml 
<?xml version="1.0"?>
<yandex>
    <profiles>
        <default>
            <default_database_engine>Ordinary</default_database_engine>
        </default>
    </profiles>
</yandex>
```

### Presentation <a id="Presentation"></a>

[https://youtu.be/1LVJ\_WcLgF8?t=2744](https://youtu.be/1LVJ_WcLgF8?t=2744)

{% embed url="https://github.com/ClickHouse/clickhouse-presentations/blob/master/meetup46/database\_engines.pdf" %}

© 2021 Altinity Inc. All rights reserved.

