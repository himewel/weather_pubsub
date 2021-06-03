import json
import logging

import requests

from pubsub import KafkaPublisher


def get_data():
    start_date = "2020-01-01"
    end_date = "2021-06-02"
    station_id = "A826"
    response = requests.get(
        f"https://apitempo.inmet.gov.br/estacao/{start_date}/{end_date}/{station_id}"
    )

    data = json.loads(response.text)
    send_list = []
    for row in data:
        send = {
            "temperature": float(row["TEM_INS"] or 0),
            "humidity": float(row["UMD_INS"] or 0),
            "pressure": float(row["PRE_INS"] or 0),
        }
        send_list.append(send)
    return send_list


if __name__ == "__main__":
    logging.basicConfig(
        format="[%(levelname)s] %(name)s - %(message)s",
        level=logging.INFO,
    )

    logging.info("Downloading new data")
    data_list = get_data()

    kafka_publisher = KafkaPublisher()
    kafka_publisher.create_topic()
    kafka_publisher.publish(data_list=data_list)
