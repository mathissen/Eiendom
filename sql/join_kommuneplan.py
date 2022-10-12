JOIN_KOMMUNEPLAN = """
WITH
kommuneplan as (
SELECT 
    * EXCEPT(WKT), 
    SAFE.st_geogfromtext(WKT) as geom FROM `eiendomsplattform.kartdata.kommuneplaner` 
),
adresser AS (
SELECT 
    * EXCEPT(Nord,
    __st),
    ST_CENTROID(SAFE.ST_GEOGPOINT(SAFE_CAST (__st AS FLOAT64), SAFE_CAST (Nord AS FLOAT64))) AS centroid
FROM
    `eiendomsplattform.kartdata.matrikkler` )

SELECT 
    adresser.lokalId, 
    kommuneplan.*
FROM adresser
LEFT JOIN kommuneplan ON ST_WITHIN(centroid, geom)
"""