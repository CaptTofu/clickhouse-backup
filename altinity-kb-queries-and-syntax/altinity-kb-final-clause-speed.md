# FINAL clause speed

SELECT \* FROM table FINAL

* Before 20.5 - always executed in a single thread and slow.
* Since 20.5   - final can be parallel, see [https://github.com/ClickHouse/ClickHouse/pull/10463](https://github.com/ClickHouse/ClickHouse/pull/10463)
* Since 20.10 - you can use `do_not_merge_across_partitions_select_final` setting.

See [https://github.com/ClickHouse/ClickHouse/pull/15938](https://github.com/ClickHouse/ClickHouse/pull/15938) and [https://github.com/ClickHouse/ClickHouse/issues/11722](https://github.com/ClickHouse/ClickHouse/issues/11722)

So it can work in the following way:

1. daily partitioning
2. after day end + some time interval during which you can get some updates - for example at 3am / 6am you do OPTIMIZE TABLE xxx PARTITION ' prev day ' FINAL
3. in that case using that FINAL with `do_not_merge_across_partitions_select_final` will be cheap.

© 2021 Altinity Inc. All rights reserved.

