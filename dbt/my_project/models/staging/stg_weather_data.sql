{{
    config(
        materialized='table',
        unique_key='id',
    )
}}
WITH source AS (
    SELECT 
        *
    FROM 
        {{ source('dev', 'raw_weather_data') }}
), deduped AS (
    SELECT
        *,
        ROW_NUMBER() OVER(PARTITION BY time ORDER BY inserted_at) AS rnk
    FROM
        source
)
SELECT
    id,
    city,
    latitude,
    longitude,
    temperature_cel AS temperature_in_celcius,
    ROUND((temperature_cel * 1.8)::NUMERIC + 32, 2) AS temperature_in_fahrenheit,
    wind_speed AS wind_speed_in_kmph,
    (wind_speed * 0.621371) AS wind_speed_in_mph,
    humidity,
    weather_description,
    time AS weather_time_local,
    inserted_at AT TIME ZONE 'UTC' AT TIME ZONE utc_offset AS inserted_at_local
FROM
    deduped
WHERE
    rnk = 1
