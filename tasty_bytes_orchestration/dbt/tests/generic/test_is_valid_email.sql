{% test is_valid_email(model, column_name) %}

    select *
    from {{ model }}
    where not {{ column_name }} regexp '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'

{% endtest %}