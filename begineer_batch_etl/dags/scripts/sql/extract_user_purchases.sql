COPY (
    SELECT *
    FROM {{ params.table_name }}
) TO '{{ params.user_purchases_file }}' WITH (FORMAT CSV, DELIMITER ',', HEADER);