JOIN_KOMMUNEPLAN = """
WITH
kommuneplan as (
SELECT 
    *
FROM `eiendomsplattform.kartdata.kommuneplaner_parsed` 
),

adresser AS (
SELECT 
    *
FROM `eiendomsplattform.kartdata.matrikkler_parsed`  )

SELECT 
    adresser.lokalId, 
    FID, 
    gml_id, 
    oppdaterin, 
    link, 
    kommunenum, 
    planidenti, 
    plantype, 
    planstatus, 
    planbestem, 
    lovreferan, 
    ikrafttred, 
    plannavn, 
    forsteDig, 
    vedtakEnde, 
    kunngjori, 
    informasjo, 
    lovrefer_1, 
    prosesshis
FROM adresser
LEFT JOIN kommuneplan ON ST_WITHIN(centroid, geom)
"""