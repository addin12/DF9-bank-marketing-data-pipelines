{{ config(
    materialized = 'view',
    partition_by = {
      "field": "date",
      "data_type": "timestamp",
      "granularity": "month"
    },
    cluster_by = 'day_of_week'
)}}

SELECT
    *
  FROM
    {{ ref('stg_fact_bank_marketing') }}