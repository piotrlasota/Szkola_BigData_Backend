from kafka import KafkaConsumer
from kafka_utils import config as kafka_config

import time

def wait_for_response(request_id: str, model: str) -> dict:
    """
    Czeka na odpowiedź na RESPONSE_TOPIC dla danego request_id.
    """
    consumer:KafkaConsumer = kafka_config.create_consumer()
    timeout_sec = kafka_config.RESPONSE_TIMEOUT_SEC
    deadline = time.time() + timeout_sec
    try:
        while time.time() < deadline:
            for msg in consumer:
                if msg.key == request_id:
                    data = msg.value
                    if data.get("request_id") == request_id and data.get("model") == model:
                        return data
            time.sleep(0.05)
    finally:
        consumer.close()

    raise TimeoutError(f"No response from Kafka within {timeout_sec}s for request_id={request_id}")