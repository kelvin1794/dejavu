import os
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import (
    StreamTableEnvironment,
    CsvTableSink,
    DataTypes,
    EnvironmentSettings,
)
from pyflink.table.descriptors import Schema, Rowtime, Json, Kafka, Elasticsearch
from pyflink.table.window import Tumble

s_env = StreamExecutionEnvironment.get_execution_environment()
s_env.set_parallelism(1)
s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
st_env = StreamTableEnvironment.create(
    s_env,
    environment_settings=EnvironmentSettings.new_instance()
    .in_streaming_mode()
    .use_blink_planner()
    .build(),
)
st_env.execute_sql(
    """
    CREATE TABLE transaction_source (
        transaction_id STRING,
        account_number STRING,
        transaction_reference STRING,
        transaction_datetime TIMESTAMP(3),
        amount DOUBLE,
        WATERMARK FOR `transaction_datetime` AS `transaction_datetime` - INTERVAL '5' SECOND
    ) WITH (
        'connector'='kafka',
        'topic'='transactions',
        'properties.zookeeper.connect' = 'zookeeper:2181',  
        'properties.bootstrap.servers' = 'kafka:9092',
        'format'='json',
        'scan.startup.mode' = 'latest-offset'
    )
    """
)

output_path = "/tmp/output/output_file.csv"
if os.path.exists(output_path):
    os.remove(output_path)
st_env.register_table_sink(
    "sink_into_csv",
    CsvTableSink(
        [
            "window_end",
            "account_number",
            "amount",
        ],
        [
            DataTypes.TIMESTAMP(3),
            DataTypes.STRING(),
            DataTypes.DOUBLE(),
        ],
        output_path,
    ),
)

st_env.execute_sql(
    """
    CREATE TABLE transaction_sink (
        window_end TIMESTAMP(3),
        account_number STRING,
        total_amount DOUBLE
    ) WITH (
        'connector'='kafka',
        'topic'='temp_result',
        'properties.zookeeper.connect' = 'zookeeper:2181',  
        'properties.bootstrap.servers' = 'kafka:9092',
        'format'='json',
        'scan.startup.mode' = 'latest-offset'
    )
    """
)

# fmt: off
st_env.from_path("transaction_source") \
    .window(Tumble.over("20.seconds").on("transaction_datetime").alias("w")) \
    .group_by("account_number, w") \
    .select(
        """
        w.end as window_end,
        account_number,
        SUM(amount) AS total_amount
        """) \
    .insert_into("transaction_sink")
# fmt: on

st_env.execute("app")
