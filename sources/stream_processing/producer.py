from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import csv
from time import sleep
import re

def load_avro_schema_from_file():
    key_schema = avro.load("bank_key.avsc")
    value_schema = avro.load("bank_value.avsc")

    return key_schema, value_schema


def send_record():
    key_schema, value_schema = load_avro_schema_from_file()

    producer_config = {
        "bootstrap.servers": "localhost:9092",
        "schema.registry.url": "http://localhost:8081",
        "acks": "1"
    }

    producer = AvroProducer(producer_config, default_key_schema=key_schema, default_value_schema=value_schema)

    file = open('data/bank-marketing.csv')
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        key = {"client_id":  int(row[0])}
        value = {"client_id": int(row[0]), "age": int(row[1]), "job": str(row[2]), "marital": str(row[3]), "education": str(row[4]), "credit": str(row[5]), "housing": str(row[6]),
                 "loan": str(row[7]), "contact": str(row[8]), "day_of_week": str(row[9]), "duration": int(row[10]),
                 "campaign": int(row[11]), "pdays": int(row[12]), "previous": int(row[13]), "poutcome": str(row[14]),
                 "emp_var_rate": float(row[15]), "cons_price_idx": float(row[16]), "cons_conf_idx": float(row[17]), "euribor3m": float(row[18]),
                 "nr_employed": float(row[19]), "y": str(row[20]), "date": str(row[21])}

        try:
            producer.produce(topic='bank_marketing', key=key, value=value)
        except Exception as e:
            print(f"Exception while producing record value - {value}: {e}")
        else:
            print(f"Successfully producing record value - {value}")

        producer.flush()
        sleep(1)

if __name__ == "__main__":
    send_record()