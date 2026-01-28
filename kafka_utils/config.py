from kafka import KafkaProducer, KafkaConsumer
import json

KAFKA_BOOTSTRAP = "localhost:9092"
REQUEST_TOPIC = "concrete.model.request"
RESPONSE_TOPIC = "concrete.model.response"
RESPONSE_TIMEOUT_SEC = 10


def create_producer() -> KafkaProducer:
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP,
        key_serializer=lambda k: k.encode("utf-8"),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all",
        retries=3,
    )
    return producer

def create_consumer() -> KafkaConsumer:
    consumer = KafkaConsumer(
        RESPONSE_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP,
        auto_offset_reset="latest",   # start od "teraz", nie od historii
        enable_auto_commit=False,
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        consumer_timeout_ms=250,       # żeby pętla mogła sprawdzać timeout
    )
    return consumer