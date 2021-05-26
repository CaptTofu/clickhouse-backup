# Cluster Configuration Process

Use ansible/puppet/salt or other systems to control the servers’ configurations.

1. Configure ClickHouse access to Zookeeper by adding the file zookeeper.xml in /etc/clickhouse-server/config.d/ folder. This file must be placed on all ClickHouse servers.

```markup
<yandex>
    <zookeeper>
        <node>
            <host>zookeeper1</host>
            <port>2181</port>
        </node>
        <node>
            <host>zookeeper2</host>
            <port>2181</port>
        </node> 
        <node>
            <host>zookeeper3</host>
            <port>2181</port>
        </node>
    </zookeeper>
</yandex>
```

1. On each server put the file macros.xml in `/etc/clickhouse-server/config.d/` folder.

&lt;yandex&gt;

    &lt;!--

        That macros are defined per server,

        and they can be used in DDL, to make the DB schema cluster/server neutral

    --&gt;

    &lt;macros&gt;

        &lt;cluster&gt;prod\_cluster&lt;/cluster&gt;

        &lt;shard&gt;01&lt;/shard&gt;

        &lt;replica&gt;clickhouse-sh1r1&lt;/replica&gt; &lt;!-- better - use the same as hostname  --&gt;

    &lt;/macros&gt;

&lt;/yandex&gt;

1. On each server place the file cluster.xml in /etc/clickhouse-server/config.d/ folder.

&lt;yandex&gt;

    &lt;remote\_servers&gt;

        &lt;prod\_cluster&gt; &lt;!-- you need to give a some name for a cluster --&gt;

            &lt;shard&gt;

                &lt;internal\_replication&gt;true&lt;/internal\_replication&gt;

                &lt;replica&gt;

                    &lt;host&gt;clickhouse-sh1r1&lt;/host&gt;

                    &lt;port&gt;9000&lt;/port&gt;

                &lt;/replica&gt;

                &lt;replica&gt;

                    &lt;host&gt;clickhouse-sh1r2&lt;/host&gt;

                    &lt;port&gt;9000&lt;/port&gt;

                &lt;/replica&gt;

            &lt;/shard&gt;

            &lt;shard&gt;

                &lt;internal\_replication&gt;true&lt;/internal\_replication&gt;

                &lt;replica&gt;

                    &lt;host&gt;clickhouse-sh2r1&lt;/host&gt;

                    &lt;port&gt;9000&lt;/port&gt;

                &lt;/replica&gt;

                &lt;replica&gt;

                    &lt;host&gt;clickhouse-sh2r2&lt;/host&gt;

                    &lt;port&gt;9000&lt;/port&gt;

                &lt;/replica&gt;

            &lt;/shard&gt;

            &lt;shard&gt;

                &lt;internal\_replication&gt;true&lt;/internal\_replication&gt;

                &lt;replica&gt;

                    &lt;host&gt;clickhouse-sh3r1&lt;/host&gt;

                    &lt;port&gt;9000&lt;/port&gt;

                &lt;/replica&gt;

                &lt;replica&gt;

                    &lt;host&gt;clickhouse-sh3r2&lt;/host&gt;

                    &lt;port&gt;9000&lt;/port&gt;

                &lt;/replica&gt;

            &lt;/shard&gt;

        &lt;/prod\_cluster&gt;

    &lt;/remote\_servers&gt;

&lt;/yandex&gt;

1. A good practice is to create 2 additional cluster configurations similar to prod\_cluster above with the following distinction: but listing all nodes nodes of single shard \(all are replicas\) and as nodes of 6 different shards \(no replicas\)
   1. prod\_cluster\_replicated: All nodes are listed as replicas in a single shard.
   2. prod\_cluster\_sharded: All nodes are listed as separate shards with no replicas.

Once this is complete, other queries that span nodes can be performed. For example:

CREATE TABLE test\_table ON CLUSTER '{cluster}' \(id UInt8\)  Engine=ReplicatedMergeTree\('/clickhouse/tables/{database}/{shard}/{table}', '{replica}'\) ORDER BY \(id\);

That will create a table on all servers in the cluster. You can insert data into this table and it will be replicated automatically to the other shards.To store the data or read the data from all shards at the same time, create a Distributed table that links to the replicatedMergeTree table.

#### **Hardening ClickHouse Security**

**See** [**https://docs.altinity.com/operationsguide/security/clickhouse-hardening-guide/**](https://docs.altinity.com/operationsguide/security/clickhouse-hardening-guide/)

### Additional Settings

See https://kb.altinity.com/altinity-kb-setup-and-maintenance/altinity-kb-settings-to-adjust

#### Users

Disable or add password for the default users default and readonly if your server is accessible from non-trusted networks.

If you add password to the default user, you will need to adjust cluster configuration, since the other servers need to know the default user’s should know the default user’s to connect to each other.

If you’re inside a trusted network, you can leave default user set to nothing to allow the ClickHouse nodes to communicate with each other.

#### Engines & ClickHouse building blocks

For general explanations of roles of different engines - check the post [Distributed vs Shard vs Replicated ahhh, help me!!!](https://github.com/yandex/ClickHouse/issues/2161).

#### Zookeeper Paths

Use conventions  for zookeeper paths.  For example, use:

  
ReplicatedMergeTree\('/clickhouse/{cluster}/tables/{shard}/table\_name', '{replica}'\) 

for: 

SELECT \* FROM system.zookeeper WHERE path='/ ...';

#### Configuration Best Practices

<table>
  <thead>
    <tr>
      <th style="text-align:left">
        <p>Attribution</p>
        <p>Modified by a post <a href="https://github.com/ClickHouse/ClickHouse/issues/3607#issuecomment-440235298">on GitHub by Mikhail Filimonov</a>.</p>
      </th>
    </tr>
  </thead>
  <tbody></tbody>
</table>

The following are recommended Best Practices when it comes to setting up a ClickHouse Cluster with Zookeeper:

1. Don’t edit/overwrite default configuration files. Sometimes a newer version of ClickHouse introduces some new settings or changes the defaults in config.xml and users.xml.
   1. Set configurations via the extra files in conf.d directory. For example, to overwrite the interface save the file conf.d/listen.xml, with the following:

&lt;?xml version="1.0"?&gt;

&lt;yandex&gt;

    &lt;listen\_host replace="replace"&gt;::&lt;/listen\_host&gt;

&lt;/yandex&gt;  


1. The same is true for users. For example, change the default profile by putting the file in users.d/profile\_default.xml:

&lt;?xml version="1.0"?&gt;

&lt;yandex&gt;

    &lt;profiles&gt;

        &lt;default replace="replace"&gt;

            &lt;max\_memory\_usage&gt;15000000000&lt;/max\_memory\_usage&gt;

            &lt;max\_bytes\_before\_external\_group\_by&gt;12000000000&lt;/max\_bytes\_before\_external\_group\_by&gt;

            &lt;max\_bytes\_before\_external\_sort&gt;12000000000&lt;/max\_bytes\_before\_external\_sort&gt;

            &lt;distributed\_aggregation\_memory\_efficient&gt;1&lt;/distributed\_aggregation\_memory\_efficient&gt;

            &lt;use\_uncompressed\_cache&gt;0&lt;/use\_uncompressed\_cache&gt;

            &lt;load\_balancing&gt;random&lt;/load\_balancing&gt;

            &lt;log\_queries&gt;1&lt;/log\_queries&gt;

            &lt;max\_execution\_time&gt;600&lt;/max\_execution\_time&gt;

        &lt;/default&gt;

    &lt;/profiles&gt;

&lt;/yandex&gt;

1. Or you can create a user by putting a file users.d/user\_xxx.xml:

&lt;?xml version="1.0"?&gt;

&lt;yandex&gt;

    &lt;users&gt;

        &lt;xxx&gt;

            &lt;!-- PASSWORD=$\(base64 &lt; /dev/urandom \| head -c8\); echo "$PASSWORD"; echo -n "$PASSWORD" \| sha256sum \| tr -d '-' --&gt;

            &lt;password\_sha256\_hex&gt;...&lt;/password\_sha256\_hex&gt;

            &lt;networks incl="networks" /&gt;

            &lt;profile&gt;readonly&lt;/profile&gt;

            &lt;quota&gt;default&lt;/quota&gt;

            &lt;allow\_databases incl="allowed\_databases" /&gt;

        &lt;/xxx&gt;

    &lt;/users&gt;

&lt;/yandex&gt;

1. Some parts of configuration will contain repeated elements \(like allowed ips for all the users\). To avoid repeating that - use substitutions file. By default its /etc/metrika.xml, but you can change it for example to /etc/clickhouse-server/substitutions.xml with the &lt;include\_from&gt; section of the main config. Put the repeated parts into substitutions file, like this:

&lt;?xml version="1.0"?&gt;

&lt;yandex&gt;

    &lt;networks&gt;

        &lt;ip&gt;::1&lt;/ip&gt;

        &lt;ip&gt;127.0.0.1&lt;/ip&gt;

        &lt;ip&gt;10.42.0.0/16&lt;/ip&gt;

        &lt;ip&gt;192.168.0.0/24&lt;/ip&gt;

    &lt;/networks&gt;

&lt;clickhouse\_remote\_servers&gt;

&lt;!-- cluster definition --&gt;

    &lt;/clickhouse\_remote\_servers&gt;

    &lt;zookeeper-servers&gt;

        &lt;node&gt;

            &lt;host&gt;zookeeper1&lt;/host&gt;

            &lt;port&gt;2181&lt;/port&gt;

        &lt;/node&gt;

        &lt;node&gt;

            &lt;host&gt;zookeeper2&lt;/host&gt;

            &lt;port&gt;2181&lt;/port&gt;

        &lt;/node&gt;

        &lt;node&gt;

            &lt;host&gt;zookeeper3&lt;/host&gt;

            &lt;port&gt;2181&lt;/port&gt;

        &lt;/node&gt;

    &lt;/zookeeper-servers&gt;

    &lt;clickhouse\_compression&gt;&lt;/clickhouse\_compression&gt;

&lt;/yandex&gt;  


These files can be common for all the servers inside the cluster or can be individualized per server. If you choose to use one substitutions file per cluster, not per node, you will also need to generate the file with macros, if macros are used.

This way you have full flexibility; you’re not limited to the settings described in the template. You can change any settings per server or data center just by assigning files with some settings to that server or server group. It becomes easy to navigate, edit, and assign files.

### Other Configuration Recommendations

Other configurations that should be evaluated:

* &lt;listen&gt; in config.xml: Determines which IP addresses and ports the ClickHouse servers listen for incoming communications.
* &lt;max\_memory\_..&gt; and &lt;max\_bytes\_before\_external\_...&gt; in users.xml. These are part of the profile &lt;default&gt;.
* &lt;max\_execution\_time&gt;
* &lt;log\_queries&gt;

The following extra debug logs should be considered:

* part\_log
* text\_log

### Understanding The Configuration

ClickHouse configuration stores most of its information in two files:

* config.xml: Stores [Server configuration parameters](https://clickhouse.yandex/docs/en/operations/server_settings/). They are server wide, some are hierarchical , and most of them can’t be changed in runtime. Only 3 sections will be applied w/o restart:
  * macros
  * remote\_servers
  * logging level
* users.xml: Configure users, and user level / session level [settings](https://clickhouse.yandex/docs/en/operations/settings/settings/).
  * Each user can change these during their session by:
    * Using parameter in http query
    * By using parameter for clickhouse-client
    * Sending query like set allow\_experimental\_data\_skipping\_indices=1.
  * Those settings and their current values are visible in system.settings. You can make some settings global by editing default profile in users.xml, which does not need restart.
  * You can forbid users to change their settings by using readonly=2 for that user, or using [setting constraints](https://clickhouse.yandex/docs/en/operations/settings/constraints_on_settings/).
  * Changes in users.xml are applied w/o restart.

For both config.xml and users.xml, it’s preferable to put adjustments in the config.d and users.d subfolders instead of editing config.xml and users.xml directly.

You can check if the config file was reread by checking /var/lib/clickhouse/preprocessed\_configs/ folder.  


