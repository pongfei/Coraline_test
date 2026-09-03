
DROP TABLE IF EXISTS cat_reg;

-- query
CREATE TABLE cat_reg AS
SELECT "Category",
       ROUND(SUM(CASE WHEN "Region" = 'East' THEN "TotalPrice" ELSE 0 END)::numeric, 0) AS "East",
       ROUND(SUM(CASE WHEN "Region" = 'West' THEN "TotalPrice" ELSE 0 END)::numeric, 0) AS "West",
       ROUND(SUM("TotalPrice")::numeric, 0) AS "Grand Total"
FROM public."food sales"
GROUP BY "Category";

-- insert
INSERT INTO cat_reg
SELECT
    'Grand Total',
    SUM("East"),
    SUM("West"),
    SUM("Grand Total")
FROM cat_reg;