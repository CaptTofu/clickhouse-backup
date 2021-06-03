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

### Some decimal number has no accurate float representation

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

The same number can have several floating-point representations, and because of that direct comparisons may be impossible. 

```text
WITH toFloat32(3600) AS f3600
SELECT
    f3600 / 1000 AS a,
    toFloat32(3.6) AS b,
    a = b AS a_equals_b,
    a - b AS diff,
    abs(diff) < 1e-7 AS is_diff_small

Row 1:
──────
a:             3.6
b:             3.6
a_equals_b:    0
diff:          9.536743172944284e-8
is_diff_small: 1
```

[https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/](https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/)  
[https://stackoverflow.com/questions/4915462/how-should-i-do-floating-point-comparison](https://stackoverflow.com/questions/4915462/how-should-i-do-floating-point-comparison)

https://stackoverflow.com/questions/2100490/floating-point-inaccuracy-examples

### 

### 

