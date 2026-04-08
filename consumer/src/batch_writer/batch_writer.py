from src.repository.event_repository import EventRepository
from src.settings import settings

class BatchWriter:
    
    def __init__(self, repository: EventRepository):  
        self.repository = repository
        self.batch_size = settings.BATCH_SIZE
        self.batch = []
        self.initialized = True

    def add(self, item):    
        self.batch.append(item)
    
    def commit(self):
        if len(self.batch) >= self.batch_size:
            self.repository.insert_events(self.batch)
            self.flush()
            return True
        return False

    def flush(self):
        if not self.batch:
            return
        self.repository.insert_events(self.batch)
        self.batch.clear()