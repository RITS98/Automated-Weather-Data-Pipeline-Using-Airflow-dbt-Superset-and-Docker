{{
    config(
        materialized='table'
    )
}}
SELECT
    city,
    latitude,
    longitude,
    DATE(weather_time_local) AS date,
    ROUND(AVG(temperature_in_celcius::NUMERIC), 2) AS avg_temperature_in_celcius,
    ROUND(AVG(temperature_in_fahrenheit::NUMERIC), 2) AS avg_temperature_in_fahrenheit,
    ROUND(AVG(wind_speed_in_kmph::NUMERIC), 2) AS avg_wind_speed_in_kmph,
    ROUND(AVG(wind_speed_in_mph::NUMERIC), 2) AS avg_wind_speed_in_mph,
    ROUND(AVG(humidity::NUMERIC), 2) AS avg_humidity
FROM
    {{ ref('stg_weather_data') }}
GROUP BY
    city,
    latitude,
    longitude,
    date(weather_time_local)
ORDER BY
    city,
    date(weather_time_local)
