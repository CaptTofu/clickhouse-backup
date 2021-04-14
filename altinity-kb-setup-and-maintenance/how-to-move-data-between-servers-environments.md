# How to move data between servers / environments

### 

### INSERT ... SELECT FROM remote\(...\) \(or FROM cluster\(...\)\)

The easiest way, the best for relatively small tables. Just run 

```text
INSERT ... SELECT FROM remote(...) 
```

on the receiver side. 

```

```

#### 



```text
SET
```

### 

### clickhouse-copier

see [https://clickhouse.tech/docs/en/operations/utilities/clickhouse-copier/](https://clickhouse.tech/docs/en/operations/utilities/clickhouse-copier/)

### Manual parts manipulations

#### 

It's actually the same as using clickhouse backup \(but executed manually\), bit better control, but more complex.





