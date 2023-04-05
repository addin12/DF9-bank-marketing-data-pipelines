{{
  config(
    materialized='ephemeral'
  )
}}

SELECT 
    client_id,
    date,
    day_of_week,
    age,
    job_type,
    marital_type,
    education_type,
    credit_type,
    housing_loan,
    personal_loan,
    contact_id,
    duration,
    campaign,
    poutcome,
    emp_var_rate,
    cons_price_idx,
    cons_conf_idx,
    euribor3m,
    nr_employed,
    subscribe

FROM {{ source('bank_marketing_dwh','fact_bank_marketing')}} as fact
LEFT JOIN {{ source('bank_marketing_dwh','dim_credit')}} as cr on fact.credit_id = cr.credit_id
LEFT JOIN {{ source('bank_marketing_dwh','dim_job')}} as job on fact.job_id = job.job_id
LEFT JOIN {{ source('bank_marketing_dwh','dim_education')}} as edu on fact.education_id = edu.education_id
LEFT JOIN {{ source('bank_marketing_dwh','dim_marital')}} as mrt on fact.marital_id = mrt.marital_id


