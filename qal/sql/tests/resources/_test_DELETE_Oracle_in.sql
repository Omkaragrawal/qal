DELETE "Test"
FROM  "Test" T1 JOIN (SELECT 'CSV11' AS "Column1",'CSV12' AS "Column2" FROM DUAL
UNION
SELECT 'CSV21','CSV22' FROM DUAL) AS T2 ON ((T2."Column1" = T1."Column1"))
