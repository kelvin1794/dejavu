from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
from pyflink.datastream.execution_mode import RuntimeExecutionMode

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
env.set_runtime_mode(RuntimeExecutionMode.BATCH)

t_env = StreamTableEnvironment.create(stream_execution_environment=env)

input_path = "/opt/app/data/source.csv"

t_env.execute_sql(
    """
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
        'path' = '{}'
    )
""".format(
        input_path
    )
)

t_env.execute_sql(
    """
    SELECT window_start, window_end, account_no, SUM(amount) AS total
    FROM TABLE(
        TUMBLE(TABLE bank_source, DESCRIPTOR(`date`), INTERVAL '30' DAYS)
    )
    GROUP BY window_start, window_end, account_no
    HAVING SUM(amount) > 10000000
"""
).print()
