import asyncio  
import time
from dataclasses import dataclass, field
from typing import Literal, Union, List
from aiohttp import ClientSession
import os
from dotenv import load_dotenv


@dataclass
class Event:
    name: str
    value: Union[int, float]
    timestamp: float  # unix timestamp in seconds
    agg_func: Literal["sum", "avg", "min", "max"] = "sum"


@dataclass
class Metric:
    name: str
    value: Union[int, float]
    timestamp: float = field(
        default_factory=lambda: time.time()
    )  # unix timestamp in seconds


class VaBus:
    def __init__(self, url: str):
        self.url = url
        self._session = ClientSession(base_url=url)

    async def __aenter__(self) -> "VaBus":
        """
        Initialize connection to bus
        """
        await self._session.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Close connection to bus
        """
        await self._session.__aexit__(exc_type, exc_val, exc_tb)

    async def get_event(self) -> Event: # Получает события из шины данных VaBus
        await asyncio.sleep(0.1)
        pass

    async def send_metric(self, metric: Metric): # Отправляет метрику в шину данных VaBus
        await asyncio.sleep(0.1)
        pass


    # additional functions

    async def aggregate_events(self, event: List[Event]) -> Event: # Агрегирует данные из листа событий
        pass

    async def send_to_postgres(self, event: Event) -> Metric: # Отправляет агрегированные данные в БД Postgres 
        pass


# Модуль - main.py

async def main():
    load_dotenv()
    url = "https://vabus.sibur.digital:8080"
    async with VaBus(url) as bus:
        start_time = time.time()
        end_time = float(os.getenv("END_TIME")) 
        events = []
        while True:
            if time.time()-start_time < end_time:
                event = asyncio.create_task(bus.get_event())
                ev = await event
                events.append(ev)
            else:
                agg_task = asyncio.create_task(aggregate_events(events))
                aggregated_event = await agg_task
                events = []
                send_task = asyncio.create_task(send_to_postgres(aggregated_event))
                metric = await send_task
                start_time = time.time()
                send_m_task = asyncio.create_task(send_metric(metric))
                
                await asyncio.gather(send_m_task, event_task)

asyncio.run(main())



        












