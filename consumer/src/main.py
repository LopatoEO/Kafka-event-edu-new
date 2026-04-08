
from dishka import make_container
from src.dispatcher.dispatcher import EventDispatcher
from src.depencies.clickhouse_provider import ClickHouseClientProvider, RepositoryProvider, BatchWriterProvider
from src.depencies.kafka_provider import KafkaConsumerServiceProvider, KafkaProducerServiceProvider, KafkaConsumerProvider, KafkaProducerProvider
from src.kafka_init import create_topics
from src.batch_writer.batch_writer import BatchWriter
from src.broker.consumer import KafkaConsumer
from src.broker.producer import KafkaProducer



dispatcher = EventDispatcher(field="event")


@dispatcher.handler("created")
def handle_created(event):
    dispatcher.batch_writer.add(event)

@dispatcher.handler("updated")
def handle_updated(event):
    dispatcher.batch_writer.add(event)

@dispatcher.handler("deleted")
def handle_deleted(event):
    dispatcher.batch_writer.add(event)

def main():
    container = make_container(KafkaConsumerProvider(),
                               KafkaConsumerServiceProvider(),
                               KafkaProducerProvider(),
                               KafkaProducerServiceProvider(),
                               ClickHouseClientProvider(),
                               RepositoryProvider(),
                               BatchWriterProvider())
    dispatcher.register_depencies(batch_writer=container.get(BatchWriter),
                                 consumer=container.get(KafkaConsumer),
                                 producer=container.get(KafkaProducer))
    dispatcher.run()

if __name__ == "__main__":
    create_topics()
    main()