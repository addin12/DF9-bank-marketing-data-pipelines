{# This macro encode the marital column to numeric #}

{% macro encode_marital(column_name) -%}

    case {{ column_name }}
        when 'married' then 1
        when 'single' then 2
        when 'divorced' then 3
        when 'unknown' then 4
    end

{%- endmacro %}