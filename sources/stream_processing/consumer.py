from confluent_kafka.avro import AvroConsumer
from google.cloud import bigquery
import os 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/Credentials/google_credentials.json"

dataset_name = 'stream'
table_name = 'bank_marketing'

client = bigquery.Client()
client.create_dataset(dataset_name, exists_ok=True)
dataset = client.dataset(dataset_name)

schema = [
    bigquery.SchemaField('client_id', 'NUMERIC'),
    bigquery.SchemaField('age', 'NUMERIC'),
    bigquery.SchemaField('job', 'STRING'),
    bigquery.SchemaField('marital', 'STRING'),
    bigquery.SchemaField('education', 'STRING'),
    bigquery.SchemaField('credit', 'STRING'),
    bigquery.SchemaField('housing', 'STRING'),
    bigquery.SchemaField('loan', 'STRING'),
    bigquery.SchemaField('contact', 'STRING'),
    bigquery.SchemaField('day_of_week', 'STRING'),
    bigquery.SchemaField('duration', 'NUMERIC'),
    bigquery.SchemaField('campaign', 'NUMERIC'),
    bigquery.SchemaField('pdays', 'NUMERIC'),
    bigquery.SchemaField('previous', 'NUMERIC'),
    bigquery.SchemaField('poutcome', 'STRING'),
    bigquery.SchemaField('emp_var_rate', 'FLOAT64'),
    bigquery.SchemaField('cons_price_idx', 'FLOAT64'),
    bigquery.SchemaField('cons_conf_idx', 'FLOAT64'),
    bigquery.SchemaField('euribor3m', 'FLOAT64'),
    bigquery.SchemaField('nr_employed', 'FLOAT64'),
    bigquery.SchemaField('y', 'STRING'),
    bigquery.SchemaField('date', 'STRING')
]

table_ref = bigquery.TableReference(dataset, table_name)
table = bigquery.Table(table_ref, schema=schema)
client.create_table(table, exists_ok=True)

def read_messages():
    consumer_config = {"bootstrap.servers": "localhost:9092",
                       "schema.registry.url": "http://localhost:8081",
                       "group.id": "practice.bitcoin.avro.consumer.2",
                       "auto.offset.reset": "earliest"}

    consumer = AvroConsumer(consumer_config)
    consumer.subscribe(["bank_marketing"])

    while(True):
        try:
            message = consumer.poll(5)
        except Exception as e:
            print(f"Exception while trying to poll messages - {e}")
        else:
            if message is not None:
                print(f"Successfully poll a record from "
                      f"Kafka topic: {message.topic()}, partition: {message.partition()}, offset: {message.offset()}\n"
                      f"message key: {message.key()} || message value: {message.value()}")
                consumer.commit()
                # INSERT STREAM TO BIGQUERY
                client.insert_rows(table, [message.value()])
            else:
                print("No new messages at this point. Try again later.")

    consumer.close()


if __name__ == "__main__":
    read_messages()

