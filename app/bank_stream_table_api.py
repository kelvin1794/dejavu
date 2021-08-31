import os
import shutil

from pyflink.common.typeinfo import Types
from pyflink.common.serialization import Encoder
from pyflink.table import StreamTableEnvironment
from pyflink.table import expressions as expr
from pyflink.table.expressions import col
from pyflink.table.window import Tumble
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors import StreamingFileSink
from pyflink.datastream.execution_mode import RuntimeExecutionMode

env = StreamExecutionEnvironment.get_execution_environment()
env.set_parallelism(1)
env.set_runtime_mode(RuntimeExecutionMode.BATCH)

t_env = StreamTableEnvironment.create(stream_execution_environment=env)

input_path = "/opt/app/data/source.csv"
output_path = "/tmp/output"

if os.path.exists(output_path):
    if os.path.isfile(output_path):
        os.remove(output_path)
    else:
        shutil.rmtree(output_path)

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

source = t_env.from_path("bank_source")

result = (
    source.select("account_no, date, amount")
    .window(Tumble.over(expr.lit(30).days).on("date").alias("w"))
    .group_by("w, account_no")
    .select(
        col("w").start.alias("window_start"),
        col("w").end.alias("window_end"),
        col("w").rowtime.alias("window_time"),
        col("account_no"),
        source.amount.sum.alias("total"),
    )
    .filter(col("total") > 10 ** 7)
)

ds = t_env.to_append_stream(
    result,
    Types.ROW(
        [
            Types.SQL_TIMESTAMP(),  # window_start
            Types.SQL_TIMESTAMP(),  # window_end
            Types.SQL_TIMESTAMP(),  # window_time
            Types.STRING(),  # account_no
            Types.DOUBLE(),  # total
        ]
    ),
)

ds.add_sink(
    StreamingFileSink.for_row_format(
        output_path, Encoder.simple_string_encoder()
    ).build()
)

env.execute("bank_stream_table_api")
