{{
  config(
    materialized = 'view'
  )
}}

SELECT education_type,
  job_type,
  marital_type,
  sum(case subscribe when true then 1
         else 0
         end) as subs,
  sum(case subscribe when true then 0
        else 1
        end) as not_subs
FROM {{ ref('stg_fact_bank_marketing') }}
group by 1,2,3
order by 4 desc, 5 desc