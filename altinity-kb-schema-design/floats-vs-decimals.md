# Floats vs Decimals

Float arithmetics is not accurate: [https://floating-point-gui.de/](https://floating-point-gui.de/)

In case you need accurate calculations you should use Decimal datatypes.

### Operations on floats are not associative

```text
select toFloat64(100000000000000000.1) + toFloat64(7.5) - toFloat64(100000000000000000.1) as res;
# 0
select toFloat64(100000000000000000.1) - toFloat64(100000000000000000.1) + toFloat64(7.5) as res;
# 7.5

# no problem with Decimals:

select toDecimal64(100000000000000000.1,1) + toDecimal64(7.5,1) - toDecimal64(100000000000000000.1,1) as res;
# 7.5
select toDecimal64(100000000000000000.1,1) - toDecimal64(100000000000000000.1,1) + toDecimal64(7.5,1) as res;
# 7.5
```

{% hint style="warning" %}
Because clickhouse uses MPP order of execution of a single query can vary on each run, and you can get slightly different results from the float column every time you run the query. 

Usually, this deviation is small, but it can be significant when some kind of arithmetic operation is performed on very large and very small numbers at the same time.
{% endhint %}

### Some decimal numbers has no accurate float representation

```text
select sum(toFloat64(0.45)) from numbers(10000);
# 4499.999999999948 

select toFloat32(0.6)*6;
# 3.6000001430511475

# no problem with Decimal

select sum(toDecimal64(0.45,2)) from numbers(10000);
# 4500.00  

select toDecimal32(0.6,1)*6;
# 3.6
```

### Direct comparisons of floats may be impossible

The same number can have several floating-point representations and because of that you should not compare Floats directly 

```text
select toFloat32(0.1)*10 = toFloat32(0.01)*100;
# 0

SELECT
    sumIf(0.1, number < 10) AS a,
    sumIf(0.01, number < 100) AS b,
    a = b AS a_eq_b
FROM numbers(100)

Row 1:
──────
a:      0.9999999999999999
b:      1.0000000000000007
a_eq_b: 0
```

See also

[https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/](https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/)  
[https://stackoverflow.com/questions/4915462/how-should-i-do-floating-point-comparison](https://stackoverflow.com/questions/4915462/how-should-i-do-floating-point-comparison)  
https://stackoverflow.com/questions/2100490/floating-point-inaccuracy-examples  
[https://stackoverflow.com/questions/10371857/is-floating-point-addition-and-multiplication-associative](https://stackoverflow.com/questions/10371857/is-floating-point-addition-and-multiplication-associative)

### 

### 

