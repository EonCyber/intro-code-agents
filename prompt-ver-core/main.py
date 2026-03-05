import asyncio
from signal import SIGINT, SIGTERM

import nats
import structlog
from rich.console import Console
from rich.panel import Panel

from src.adapters.messaging.nats_event_publisher import NatsEventPublisher
from src.adapters.messaging.nats_handler import NatsMessageHandler
from src.infra.config import load_settings
from src.infra.database import build_engine, build_session_factory, create_tables
from src.infra.logging import configure_logging

console = Console()
log = structlog.get_logger(__name__)


async def main() -> None:
    settings = load_settings()
    configure_logging(settings.log_level)
    console.print(Panel("[bold green]prompt-ver-core starting[/bold green]"))

    engine = build_engine(settings.db_url)
    await create_tables(engine)
    session_factory = build_session_factory(engine)

    nc = await nats.connect(settings.nats_url)

    publisher = NatsEventPublisher(nc)
    handler = NatsMessageHandler(session_factory, publisher)
    subs = await handler.subscribe_all(nc)

    log.info("app.ready", nats_url=settings.nats_url, db_url=settings.db_url)

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    loop.add_signal_handler(SIGINT, stop_event.set)
    loop.add_signal_handler(SIGTERM, stop_event.set)
    await stop_event.wait()

    log.info("app.stopping")
    for sub in subs:
        await sub.unsubscribe()
    await nc.drain()
    await engine.dispose()
    log.info("app.stopped")


if __name__ == "__main__":
    asyncio.run(main())
