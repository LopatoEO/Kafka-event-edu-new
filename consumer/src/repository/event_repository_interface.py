from abc import ABC, abstractmethod


class IEventRepository(ABC):

    @abstractmethod
    def insert_events(self, events: list[dict]) -> None:
        pass
