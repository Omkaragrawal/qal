DELETE FROM "Test" T1 USING (SELECT CSV11 AS "Column1",CSV12 AS "Column2"
UNION
SELECT CSV21,CSV22) AS T2 WHERE  ((T2."Column1" = T1."Column1"))
