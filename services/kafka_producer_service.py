from kafka import KafkaProducer
from kafka_utils import config as kafka_config

def send(kafka_producer: KafkaProducer, request_id:str, kafka_request:dict) -> None:
    kafka_producer \
        .send(kafka_config.REQUEST_TOPIC, key=request_id, value=kafka_request) \
        .get(timeout=5)