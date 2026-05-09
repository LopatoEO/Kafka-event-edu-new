from consumer.src.repository.event_repository_interface import IEventRepository


class BatchWriter:
    def __init__(self, repository: IEventRepository, batch_size: int) -> None:
        self._repository = repository
        self.batch_size = batch_size
        self.batch = []
        self.initialized = True

    def add(self, item) -> None:
        self.batch.append(item)

    def commit(self) -> bool:
        if len(self.batch) >= self.batch_size:
            self._repository.insert_events(self.batch)
            self.flush()
            return True
        return False

    def flush(self) -> None:
        if not self.batch:
            return
        self._repository.insert_events(self.batch)
        self.batch.clear()
