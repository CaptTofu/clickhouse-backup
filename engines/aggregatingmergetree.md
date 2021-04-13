# AggregatingMergeTree

Q. What happens with columns which are nor the part of ORDER BY key, nor have the AggregateFunction type?

A. it picks the first value met, \(similar to `any`\)

```text
CREATE TABLE agg_test
(
    `a` String,
    `b` UInt8,
    `c` SimpleAggregateFunction(max, UInt8)
)
ENGINE = AggregatingMergeTree
ORDER BY a;

insert into agg_test values ('a', 1, 1);
insert into agg_test values ('a', 2, 2);

SELECT * FROM agg_test FINAL;

┌─a─┬─b─┬─c─┐
│ a │ 1 │ 2 │
└───┴───┴───┘

insert into agg_test values ('a', 3, 3);
select * from agg_test;
┌─a─┬─b─┬─c─┐
│ a │ 1 │ 2 │
└───┴───┴───┘
┌─a─┬─b─┬─c─┐
│ a │ 3 │ 3 │
└───┴───┴───┘

OPTIMIZE TABLE agg_test FINAL;
select * from agg_test;
┌─a─┬─b─┬─c─┐
│ a │ 1 │ 3 │
└───┴───┴───┘
```

© 2021 Altinity Inc. All rights reserved.

