import json
from kafka import KafkaProducer
from core.config import settings

def load_data(file_path: str):
    """
    Load data from a JSON file.

    Args:
        file_path (str): Path to the data file.

    Returns:
        list: Loaded data.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def preprocess_data(data: list):
    """
    Preprocess the loaded data.

    Args:
        data (list): Raw data.

    Returns:
        list: Preprocessed data.
    """
    # Implement your preprocessing steps here
    preprocessed = [event for event in data if event.get('important_field')]
    return preprocessed

def send_to_kafka(data: list):
    """
    Send preprocessed data to Kafka.

    Args:
        data (list): Preprocessed data.
    """
    producer = KafkaProducer(
        bootstrap_servers=settings.KAFKA_SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    for event in data:
        producer.send(settings.KAFKA_TOPIC, value=event)
    producer.flush()

def main():
    """
    Main function to orchestrate data loading, preprocessing, and sending to Kafka.
    """
    file_path = "path/to/your/data/file.json"
    raw_data = load_data(file_path)
    processed_data = preprocess_data(raw_data)
    send_to_kafka(processed_data)

if __name__ == "__main__":
    main()
