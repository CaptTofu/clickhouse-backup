# Roaring bitmaps for calculating retention

```text

CREATE TABLE test_roaring_bitmap
ENGINE = MergeTree
ORDER BY h AS
SELECT
    intDiv(number, 10) AS h,
    groupArray(number + (rand() % 30)) AS vals,
    groupBitmapState(number + (rand() % 30)) AS vals_bitmap
FROM numbers(100)
GROUP BY h

Ok.

0 rows in set. Elapsed: 0.017 sec. 


SELECT *
FROM test_roaring_bitmap

┌─h─┬─vals────────────────────────────────────┬─vals_bitmap───────┐
│ 0 │ [23,26,31,16,25,26,18,23,11,23]         │ �
                                                                   │
│ 1 │ [36,25,19,21,30,23,44,39,19,27]         │ 	$,'
│ 2 │ [37,41,44,49,41,51,33,48,56,47]         │ 	%),13!08/ │
│ 3 │ [52,47,46,42,40,40,52,61,47,61]         │ 4/.*(=            │
│ 4 │ [53,62,44,54,63,47,70,53,52,56]         │ 	5>,6?/F48 │
│ 5 │ [73,73,81,80,74,60,66,57,64,71]         │ 	IQPJ<B9@G │
│ 6 │ [87,73,74,73,85,88,87,85,87,70]         │ WIJUXF            │
│ 7 │ [93,71,88,98,95,100,77,84,94,96]        │ 
]GXb_dMT^`        │
│ 8 │ [89,110,110,101,99,111,87,114,93,90]    │ 	YnecoWr]Z │
│ 9 │ [113,98,108,103,118,109,107,126,98,109] │qblgvmk~          │
└───┴─────────────────────────────────────────┴───────────────────┘

10 rows in set. Elapsed: 0.005 sec. 



SELECT
    groupBitmapAnd(vals_bitmap),
    bitmapToArray(groupBitmapAndState(vals_bitmap))
FROM test_roaring_bitmap
WHERE h IN (0, 1)

┌─groupBitmapAnd(vals_bitmap)─┬─bitmapToArray(groupBitmapAndState(vals_bitmap))─┐
│                           2 │ [23,25]                                         │
└─────────────────────────────┴─────────────────────────────────────────────────┘

1 rows in set. Elapsed: 0.006 sec. 

```

See also [https://cdmana.com/2021/01/20210109005922716t.html](https://cdmana.com/2021/01/20210109005922716t.html)

