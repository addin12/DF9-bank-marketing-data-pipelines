{{ config(materialized='ephemeral') }}

SELECT *
FROM {{ source('bank_marketing_dwh','bank_marketing')}}