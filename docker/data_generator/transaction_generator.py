import time
import datetime
import random
import pandas as pd
from faker import Faker
from kafka import KafkaProducer
from json import dumps
import random
import uuid
from dateutil.relativedelta import relativedelta

fake = Faker()


def generate_id():
    return uuid.uuid4().hex


def generate_account_number(list):
    return str(random.choice(list)).zfill(10)


def generate_ref():
    fake.paragraph(1)


# fmt: off
def generate_datetime():
    return fake.date_time_between(
        start_date="-1m", end_date="now"
    ).strftime(
        "%Y-%m-%d %H:%M:%S.%f"
    )[:-3]
# fmt: on


def generate_amount():
    return round(random.randint(1, 10 ** 3) * random.random(), 2)


def generate_record(account_id_list):
    return {
        "transaction_id": generate_id(),
        "account_number": generate_account_number(account_id_list),
        "transaction_reference": generate_ref(),
        "transaction_datetime": generate_datetime(),
        "amount": generate_amount(),
    }


account_numbers = random.sample(range(1, 1000000), 10)
end_datetime = datetime.datetime.now() + relativedelta(years=100)
current_datetime = datetime.datetime.now()

start_time = time.time()
while current_datetime <= end_datetime:
    producer = KafkaProducer(
        bootstrap_servers=["kafka:9092"],
        value_serializer=lambda x: dumps(x).encode("utf-8"),
    )

    trans = pd.DataFrame(
        [generate_record(account_numbers) for _ in range(1000)]
    ).to_dict(orient="records")
    for transaction in trans:
        future = producer.send("transactions", value=transaction)
        result = future.get(timeout=5)
    print("--- {} seconds ---".format(time.time() - start_time))
    time.sleep(5)
    current_datetime = datetime.datetime.combine(
        datetime.date.today(), datetime.datetime.now().time()
    )
