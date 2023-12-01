import random

from loguru import logger
from utils.sleeping import sleep
from . import Starknet
from typing import List


class Routes(Starknet):
    def __init__(self, _id: int, private_key: str, type_account: str) -> None:
        super().__init__(_id=_id, private_key=private_key, type_account=type_account)

        self.private_key = private_key
        self.type_account = type_account

    def process_module(self, module):
        if isinstance(module, list):
            return self.process_module(random.choice(module))
        elif isinstance(module, tuple):
            return [self.process_module(module[0]) for _ in range(random.randint(module[1], module[2]))]
        else:
            return module

    def run_modules(self, use_modules) -> List:
        modules_to_run = []
        for module in use_modules:
            result = self.process_module(module)
            if isinstance(result, list):
                modules_to_run.extend(result)
            else:
                modules_to_run.append(result)
        return modules_to_run

    def generate_module_sequence(self, cheap_modules, expensive_modules, num_transactions, cheap_ratio=1.0):
        """
        Генерирует случайную последовательность модулей.

        :param num_transactions: количество транзакций
        :param cheap_ratio: доля дешевых транзакций от общего числа (от 0 до 1)
        :param cheap_modules
        :param expensive_modules
        """
        sequence = []
        for _ in range(num_transactions):
            if random.random() < cheap_ratio:
                module = random.choice(cheap_modules + [None])
            else:
                module = random.choice(expensive_modules + [None])

            # Случайно решаем, добавлять ли вложенность или повторения
            if random.random() < 0.2:  # 20% шанс добавить вложенность
                module = [module, self.generate_nested_module(cheap_modules)]
            elif random.random() < 0.1:  # 10% шанс добавить повторения
                module = (module, 1, random.randint(1, 2))

            sequence.append(module)
        return sequence

    def generate_nested_module(self, cheap_modules):
        """ Генерирует вложенный модуль. """
        if random.random() < 0.5:
            return random.choice(cheap_modules + [None])
        else:
            return [random.choice(cheap_modules + [None]), self.generate_nested_module(cheap_modules)]

    async def start(self, use_modules: list, sleep_from: int, sleep_to: int, random_module: bool):
        logger.info(f"[{self._id}][{self.address_str}] Start using routes")

        run_modules = self.run_modules(use_modules)

        if random_module:
            random.shuffle(run_modules)

        for module in run_modules:
            if module is None:
                logger.info(f"[{self._id}][{self.address_str}] Skip module")
                continue

            await module(self._id, self.private_key, self.type_account)

            await sleep(sleep_from, sleep_to)

    async def start_automatic(self, transaction_count, cheap_ratio,
                              sleep_from, sleep_to,
                              cheap_modules, expensive_modules):
        logger.info(f"[{self._id}][{self.address_str}] Start using automatic routes")

        use_modules = self.generate_module_sequence(cheap_modules, expensive_modules, transaction_count, cheap_ratio)

        run_modules = self.run_modules(use_modules)

        for module in run_modules:
            if module is None:
                logger.info(f"[{self._id}][{self.address_str}] Skip module")
                continue

            await module(self._id, self.private_key, self.type_account)

            await sleep(sleep_from, sleep_to)
