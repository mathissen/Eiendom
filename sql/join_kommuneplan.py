JOIN_KOMMUNEPLAN = """
WITH
kommuneplan as (
SELECT 
    * EXCEPT(Shape__Are, Shape__Len)
FROM `eiendomsplattform.kartdata.kommuneplaner_parsed` 
),

adresser AS (
SELECT 
    *
FROM `eiendomsplattform.kartdata.matrikkler_parsed`  )

SELECT 
    adresser.lokalId, 
    kommuneplan.*
FROM adresser
JOIN kommuneplan ON ST_WITHIN(centroid, geom)
"""