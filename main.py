import asyncio
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Union
from itertools import count

import loguru
import questionary
from questionary import Choice

from config import RECIPIENTS
from utils.helpers import remove_wallet
from utils.sleeping import sleep
from utils.password_handler import get_private_keys
from utils.logs_handler import filter_out_utils
from modules_settings import *
from settings import (
    TYPE_WALLET,
    RANDOM_WALLET,
    SLEEP_FROM,
    SLEEP_TO,
    QUANTITY_THREADS,
    THREAD_SLEEP_FROM,
    THREAD_SLEEP_TO, REMOVE_WALLET
)


def get_module():
    counter = count(1)
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice(f"{next(counter)}) Encrypt starknet wallets", encrypt_privates),
            Choice(f"{next(counter)}) Make withdraw from OKX", withdraw_okx),
            Choice(f"{next(counter)}) Make deposit to Starknet", deposit_starknet),
            Choice(f"{next(counter)}) Make withdraw from Starknet", withdraw_starknet),
            Choice(f"{next(counter)}) Deploy argent account", deploy_argent),
            Choice(f"{next(counter)}) Upgrade argent account", upgrade_argent),
            Choice(f"{next(counter)}) Bridge on Orbiter", bridge_orbiter),
            Choice(f"{next(counter)}) Make swap on JediSwap", swap_jediswap),
            Choice(f"{next(counter)}) Make swap on MySwap", swap_myswap),
            Choice(f"{next(counter)}) Make swap on 10kSwap", swap_starkswap),
            Choice(f"{next(counter)}) Make swap on SithSwap", swap_sithswap),
            Choice(f"{next(counter)}) Make swap on Avnu", swap_avnu),
            Choice(f"{next(counter)}) Make swap on Protoss", swap_protoss),
            Choice(f"{next(counter)}) Deposit ZkLend", deposit_zklend),
            Choice(f"{next(counter)}) Deposit Nostra", deposit_nostra),
            Choice(f"{next(counter)}) Withdraw ZkLend", withdraw_zklend),
            Choice(f"{next(counter)}) Withdraw Nostra", withdraw_nostra),
            Choice(f"{next(counter)}) Enable collateral ZkLend", enable_collateral_zklend),
            Choice(f"{next(counter)}) Disable collateral ZkLend", disable_collateral_zklend),
            Choice(f"{next(counter)}) Mint Starknet ID", mint_starknet_id),
            Choice(f"{next(counter)}) Dmail send mail", send_mail_dmail),
            Choice(f"{next(counter)}) Mint StarkStars NFT", mint_starkstars),
            Choice(f"{next(counter)}) Mint NFT on Pyramid", create_collection_pyramid),
            Choice(f"{next(counter)}) Mint Gol token", mint_gol),
            Choice(f"{next(counter)}) Mint Starkverse NFT", mint_starkverse),
            Choice(f"{next(counter)}) Unframed", cancel_order_unframed),
            Choice(f"{next(counter)}) Flex", cancel_order_flex),
            Choice(f"{next(counter)}) Approve almanac NFT", approve_almanac),
            Choice(f"{next(counter)}) Approve ninth token", approve_ninth),
            Choice(f"{next(counter)}) Deploy token", deploy_token),
            Choice(f"{next(counter)}) Deploy and mint NFT", deploy_nft),
            Choice(f"{next(counter)}) Transfer", make_transfer),
            Choice(f"{next(counter)}) Swap tokens to ETH", swap_tokens),
            Choice(f"{next(counter)}) Use Multiswap", swap_multiswap),
            Choice(f"{next(counter)}) Use custom routes ", custom_routes),
            Choice(f"{next(counter)}) Use automatic routes ", automatic_routes),
            Choice(f"{next(counter)}) Check transaction count", "tx_checker"),
            Choice(f"{next(counter)}) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("\n❤️ Author – https://t.me/sybilwave")
        print("❤️ Fork Author – https://t.me/rgalyeon\n")
        sys.exit()
    return result


def get_wallets(use_recipients: bool = False):
    ACCOUNTS = get_private_keys()
    if use_recipients:
        account_with_recipients = dict(zip(ACCOUNTS, RECIPIENTS))

        wallets = [
            {
                "id": _id,
                "key": key,
                "recipient": account_with_recipients[key],
            } for _id, key in enumerate(account_with_recipients, start=1)
        ]
    else:
        wallets = [
            {
                "id": _id,
                "key": key,
            } for _id, key in enumerate(ACCOUNTS, start=1)
        ]

    return wallets


async def run_module(module, account_id, key, recipient: Union[str, None] = None):
    try:
        if recipient:
            await module(account_id, key, TYPE_WALLET, recipient)
        else:
            await module(account_id, key, TYPE_WALLET)
    except Exception as e:
        loguru.logger.error(e)

    if REMOVE_WALLET:
        remove_wallet(key, recipient)

    await sleep(SLEEP_FROM, SLEEP_TO)


def _async_run_module(module, account_id, key, recipient):
    asyncio.run(run_module(module, account_id, key, recipient))


def main(module):
    if module == encrypt_privates:
        return encrypt_privates(force=True)
    if module in [deposit_starknet, withdraw_starknet, bridge_orbiter, make_transfer]:
        wallets = get_wallets(True)
    else:
        wallets = get_wallets()

    if RANDOM_WALLET:
        random.shuffle(wallets)

    with ThreadPoolExecutor(max_workers=QUANTITY_THREADS) as executor:
        for _, account in enumerate(wallets, start=1):
            executor.submit(
                _async_run_module,
                module,
                account.get("id"),
                account.get("key"),
                account.get("recipient", None)
            )
            time.sleep(random.randint(THREAD_SLEEP_FROM, THREAD_SLEEP_TO))


if __name__ == '__main__':
    print("❤️ Author – https://t.me/sybilwave")
    print("❤️ Fork Author – https://t.me/rgalyeon\n")

    loguru.logger.add('logs.txt', filter=filter_out_utils)
    module = get_module()
    if module == "tx_checker":
        get_tx_count(TYPE_WALLET)
    else:
        main(module)

    print("\n❤️ Author – https://t.me/sybilwave")
    print("❤️ Fork Author – https://t.me/rgalyeon\n")
