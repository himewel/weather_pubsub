import logging

from pubsub import KafkaSubscriber

if __name__ == '__main__':
    logging.basicConfig(
        format="[%(levelname)s] %(name)s - %(message)s",
        level=logging.INFO,
    )

    subscriber = KafkaSubscriber()
    subscriber.subscribe()
