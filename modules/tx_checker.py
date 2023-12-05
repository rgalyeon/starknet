import asyncio

from loguru import logger
from tabulate import tabulate

from . import Starknet
from utils.password_handler import get_wallet_data


async def get_nonce(account: Starknet):
    try:
        nonce = await account.account.get_nonce()

        return nonce
    except:
        await get_nonce(account)


async def check_tx(type_account: str):
    tasks = []

    logger.info("Start transaction checker")

    accounts = [data['private_key'] for _, data in get_wallet_data().items()]

    for _id, pk in enumerate(accounts, start=1):
        account = Starknet(_id, pk, type_account)

        tasks.append(asyncio.create_task(get_nonce(account), name=hex(account.address)))

    await asyncio.gather(*tasks)

    table = [[k, i.get_name(), i.result()] for k, i in enumerate(tasks, start=1)]

    headers = ["#", "Address", "Nonce"]

    print(tabulate(table, headers, tablefmt="github"))
