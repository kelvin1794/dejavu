import unittest
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
from pyflink.datastream.execution_mode import RuntimeExecutionMode


class PyFlinkTest(unittest.TestCase):
    @classmethod
    def create_testing_table_environment(cls):
        env = StreamExecutionEnvironment.get_execution_environment()
        env.set_parallelism(1)
        env.set_runtime_mode(RuntimeExecutionMode.BATCH)

        t_env = StreamTableEnvironment.create(stream_execution_environment=env)
        return t_env
