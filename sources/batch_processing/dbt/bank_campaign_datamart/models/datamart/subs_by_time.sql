{{
  config(
    materialized = 'view'
  )
}}

SELECT date,
  day_of_week,
  sum(case subscribe when true then 1
         else 0
         end) as subs,
  sum(case subscribe when true then 0
        else 1
        end) as not_subs
FROM {{ ref('partition_cluster_time') }}
group by 1,2
order by 1,2