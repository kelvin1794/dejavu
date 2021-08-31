CREATE TABLE bank_source (
    account_no STRING,
    `date` TIMESTAMP(3),
    transaction_details STRING,
    value_date TIMESTAMP,
    transaction_type STRING,
    amount DOUBLE,
    balance DOUBLE,
    WATERMARK FOR `date` AS `date` - INTERVAL '5' SECOND
) WITH (
    'connector' = 'filesystem',
    'format' = 'csv',
    'path' = '/opt/app/data/source.csv'
);

SELECT
    window_start,
    window_end,
    account_no,
    SUM(amount) AS total
FROM
    TABLE(
        TUMBLE(
            TABLE bank_source,
            DESCRIPTOR(`date`),
            INTERVAL '30' DAYS
        )
    )
GROUP BY
    window_start,
    window_end,
    account_no
HAVING
    SUM(amount) > 10000000;
