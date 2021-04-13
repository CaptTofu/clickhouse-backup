# Adjusting librdkafka settings

* To set rdkafka options - add to `<kafka>` section in `config.xml` or preferably use a separate file in `config.d/`:
  * [https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md](https://github.com/edenhill/librdkafka/blob/master/CONFIGURATION.md)

Some random example:

```markup
<kafka>
    <max_poll_interval_ms>60000</max_poll_interval_ms>
    <session_timeout_ms>60000</session_timeout_ms>
    <heartbeat_interval_ms>10000</heartbeat_interval_ms>
    <reconnect_backoff_ms>5000</reconnect_backoff_ms>
    <reconnect_backoff_max_ms>60000</reconnect_backoff_max_ms>
    <security_protocol>SSL</security_protocol>
    <ssl_ca_location>/etc/clickhouse-server/ssl/kafka-ca-qa.crt</ssl_ca_location>
    <ssl_certificate_location>/etc/clickhouse-server/ssl/client_clickhouse_client.pem</ssl_certificate_location>
    <ssl_key_location>/etc/clickhouse-server/ssl/client_clickhouse_client.key</ssl_key_location>
    <ssl_key_password>pass</ssl_key_password>
</kafka>
```

## Authentication / connectivity <a id="Adjustinglibrdkafkasettings-Authentication/connectivity"></a>

### Amazon MSK <a id="Adjustinglibrdkafkasettings-AmazonMSK"></a>

```markup
<yandex>
  <kafka>
    <security_protocol>sasl_ssl</security_protocol>
    <sasl_username>root</sasl_username>
    <sasl_password>toor</sasl_password>
  </kafka>
</yandex>
```

[https://leftjoin.ru/all/clickhouse-as-a-consumer-to-amazon-msk/](https://leftjoin.ru/all/clickhouse-as-a-consumer-to-amazon-msk/)

### Inline Kafka certs <a id="Adjustinglibrdkafkasettings-Inlinekafkacerts"></a>

To connect to some Kafka cloud services you may need to use certificates.

If needed they can be converted to pem format and inlined into ClickHouse config.

Example:

```markup
<kafka>
<ssl_key_pem><![CDATA[
  RSA Private-Key: (3072 bit, 2 primes)
    ....
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
]]></ssl_key_pem>
<ssl_certificate_pem><![CDATA[
-----BEGIN CERTIFICATE-----
...
-----END CERTIFICATE-----
]]></ssl_certificate_pem>
</kafka>
```

See also

[https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka](https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka)

12:06

[https://stackoverflow.com/questions/991758/how-to-get-pem-file-from-key-and-crt-files](https://stackoverflow.com/questions/991758/how-to-get-pem-file-from-key-and-crt-files)

### Azure Event Hub <a id="Adjustinglibrdkafkasettings-AzureEventHub"></a>

See [https://github.com/ClickHouse/ClickHouse/issues/12609](https://github.com/ClickHouse/ClickHouse/issues/12609)

### Kerberos <a id="Adjustinglibrdkafkasettings-Kerberos"></a>

[https://clickhouse.tech/docs/en/engines/table-engines/integrations/kafka/\#kafka-kerberos-support](https://clickhouse.tech/docs/en/engines/table-engines/integrations/kafka/#kafka-kerberos-support)

[https://github.com/ClickHouse/ClickHouse/blob/master/tests/integration/test\_storage\_kerberized\_kafka/configs/kafka.xml](https://github.com/ClickHouse/ClickHouse/blob/master/tests/integration/test_storage_kerberized_kafka/configs/kafka.xml)

```markup
  <!-- Kerberos-aware Kafka -->
  <kafka>
    <security_protocol>SASL_PLAINTEXT</security_protocol>
    <sasl_kerberos_keytab>/home/kafkauser/kafkauser.keytab</sasl_kerberos_keytab>
    <sasl_kerberos_principal>kafkauser/kafkahost@EXAMPLE.COM</sasl_kerberos_principal>
  </kafka>
```

© 2021 Altinity Inc. All rights reserved.
