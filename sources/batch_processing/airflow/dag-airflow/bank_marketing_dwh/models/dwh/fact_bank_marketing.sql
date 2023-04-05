{{
  config(
    materialized = 'table',
    unique_key = 'client_id'
  )
}}

SELECT
    client_id,
    date,
    day_of_week,
    age,
    job_id,
    marital_id,
    education_id,
    credit_id,
    housing as housing_loan,
    loan as personal_loan,
    contact_id,
    duration,
    campaign,
    poutcome,
    emp_var_rate,
    cons_price_idx,
    cons_conf_idx,
    euribor3m,
    nr_employed,
    y as subscribe
FROM
    {{ ref('stg_bank_marketing') }} as stg
    LEFT JOIN {{ ref('dim_contact') }} as ctc ON stg.contact = ctc.contact_type
    LEFT JOIN {{ ref('dim_credit') }} as cr ON stg.credit = cr.credit_type
    LEFT JOIN {{ ref('dim_education') }} as edu ON stg.education = edu.education_type
    LEFT JOIN {{ ref('dim_job') }} as job ON stg.job = job.job_type
    LEFT JOIN {{ ref('dim_marital') }} as mrt ON stg.marital = mrt.marital_type
ORDER BY 1