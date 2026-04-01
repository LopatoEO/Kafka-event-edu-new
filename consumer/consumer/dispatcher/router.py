from . import EventDispatcher
from ..batch_writer import BatchWriter

dispatcher = EventDispatcher(field="event")


@dispatcher.handler("created")
async def handle_created(event, batch_writer=None):
    await batch_writer.add(event)

@dispatcher.handler("updated")
async def handle_updated(event, batch_writer=None):
    await batch_writer.add(event)

@dispatcher.handler("deleted")
async def handle_deleted(event, batch_writer=None):
    await batch_writer.add(event)