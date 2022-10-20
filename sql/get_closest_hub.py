GET_CLOSEST_HUB = """
WITH knutepunkter as (
SELECT *, ST_GEOGPOINT(CAST(Adresse_Longitude AS Float64), CAST(Adresse_Latitude AS Float64)) as centroid FROM `eiendomsplattform.kartdata.knutepunkter ` 
),
adresser AS (
SELECT 
    *
FROM
    `eiendomsplattform.kartdata.matrikkler_parsed` 
    WHERE centroid is not null),

add_distance as (
SELECT 
lokalId,
Bygningsnr, 
ST_DISTANCE(k.centroid, a.centroid) as distance
FROM knutepunkter k, adresser a

),
add_rows as (
SELECT 
* EXCEPT(distance),
distance as distance,
row_number() over (partition by lokalId ORDER BY distance asc) rn
FROM add_distance 
)

SELECT * EXCEPT(rn) FROM add_rows
WHERE rn = 1
ORDER BY distance

"""