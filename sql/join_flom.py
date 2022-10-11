JOIN_FLOM = """
EXPORT DATA
  OPTIONS (
    uri = '{output_location}', --'gs://bucket/folder/matrikkel_flom.csv',
    format = 'CSV',
    overwrite = true,
    header = true,
    field_delimiter = ';')
AS (

WITH 
adresser AS (
SELECT 
    * EXCEPT(Nord,
    __st),
    CAST(NULL AS STRING) AS flag,
    ST_CENTROID(SAFE.ST_GEOGPOINT(SAFE_CAST (__st AS FLOAT64), SAFE_CAST (Nord AS FLOAT64))) AS centroid
FROM
    `eiendomsplattform.kartdata.matrikkler` ),

flom10_simplified AS (
SELECT
    ST_UNION_AGG(geom) AS geom
FROM (
    SELECT
    ST_SIMPLIFY(ST_GEOGFROMTEXT(WKT),2) AS geom
    FROM
    `eiendomsplattform.kartdata.flomsone_10aar_raw` ) ),

flom20_simplified AS (
SELECT
    ST_UNION_AGG(geom) AS geom
FROM (
    SELECT
    ST_SIMPLIFY(SAFE.st_geogfromtext(WKT),2) AS geom
    FROM
    `eiendomsplattform.kartdata.flomsone_20aar_raw` ) ),
flom50_simplified AS (
SELECT
    ST_UNION_AGG(geom) AS geom
FROM (
    SELECT
    ST_SIMPLIFY(SAFE.st_geogfromtext(WKT),2) AS geom
    FROM
    `eiendomsplattform.kartdata.flomsone_50aar_raw` ) ),

flom10 AS (
SELECT
    adresser.* EXCEPT(flag),
    COALESCE(flag,
    CASE
        WHEN f10s.geom IS NOT NULL THEN "Flom10"
    ELSE
    NULL
    END
    ) AS FlomFare
FROM
    adresser
LEFT JOIN
    flom10_simplified f10s
ON
    ST_DWITHIN(centroid, f10s.geom, 0) ),

flom20 AS (
SELECT
    flom10.* EXCEPT(FlomFare),
    COALESCE(FlomFare,
    CASE
        WHEN f20s.geom IS NOT NULL THEN "Flom20"
    ELSE
    NULL
    END
    ) AS FlomFare
FROM
    flom10
LEFT JOIN
    flom20_simplified f20s
ON
    ST_DWITHIN(centroid, f20s.geom, 0) ),

flom50 AS (
SELECT
    flom20.* EXCEPT(FlomFare),
    COALESCE(FlomFare,
    CASE
        WHEN f50s.geom IS NOT NULL THEN "Flom50"
    ELSE
    NULL
    END
    ) AS FlomFare
FROM
    flom20
LEFT JOIN
    flom50_simplified f50s
ON
    ST_DWITHIN(centroid, f50s.geom, 0) )

SELECT
    distinct * --using distinct to force BQ to push into one file 
FROM
flom50
ORDER BY
FlomFare DESC  
);
"""