from ..repository.event_repository import EventRepository

class BatchWriter:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(BatchWriter, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, repository: EventRepository, commit_func=None):  
        if not hasattr(self, 'initialized'):
            self.repository = repository
            self.batch_size = 10
            self.batch = []
            self.commit_func = commit_func
            self.initialized = True

    async def add(self, item):    
        self.batch.append(item)
        if len(self.batch) >= self.batch_size:
            await self.repository.insert_events(self.batch)
            if self.commit_func:
                await self.commit_func()
            await self.flush()

    async def flush(self):
        if not self.batch:
            return
        await self.repository.insert_events(self.batch)
        if self.commit_func:
            await self.commit_func()
        self.batch.clear()