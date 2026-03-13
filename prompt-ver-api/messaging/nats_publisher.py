import nats

from utils.exceptions import NATSPublishException, NATSRequestException
from utils.json_utils import deserialize, serialize


class NATSPublisher:
    def __init__(self, nc: nats.aio.client.Client) -> None:
        self.nc = nc

    async def publish(self, subject: str, payload: dict) -> None:
        try:
            await self.nc.publish(subject, serialize(payload))
        except Exception as e:
            raise NATSPublishException(str(e)) from e

    async def request(self, subject: str, payload: dict, timeout: float = 5.0) -> dict:
        try:
            msg = await self.nc.request(subject, serialize(payload), timeout=timeout)
            return deserialize(msg.data)
        except Exception as e:
            raise NATSRequestException(str(e)) from e
