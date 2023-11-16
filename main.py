import asyncio
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Union

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
    result = questionary.select(
        "Select a method to get started",
        choices=[
            Choice("0) Encrypt starknet wallets", encrypt_privates),
            Choice("1) Make deposit from OKX", withdraw_okx),
            Choice("2) Make deposit to Starknet", deposit_starknet),
            Choice("3) Make withdraw from Starknet", withdraw_starknet),
            Choice("4) Deploy argent account", deploy_argent),
            Choice("5) Upgrade argent account", upgrade_argent),
            Choice("6) Bridge on Orbiter", bridge_orbiter),
            Choice("7) Make swap on JediSwap", swap_jediswap),
            Choice("8) Make swap on MySwap", swap_myswap),
            Choice("9) Make swap on 10kSwap", swap_starkswap),
            Choice("10) Make swap on SithSwap", swap_sithswap),
            Choice("11) Make swap on Avnu", swap_avnu),
            Choice("12) Make swap on Protoss", swap_protoss),
            Choice("13) Deposit ZkLend", deposit_zklend),
            Choice("14) Deposit Nostra", deposit_nostra),
            Choice("15) Withdraw ZkLend", withdraw_zklend),
            Choice("16) Withdraw Nostra", withdraw_nostra),
            Choice("17) Enable collateral ZkLend", enable_collateral_zklend),
            Choice("18) Disable collateral ZkLend", disable_collateral_zklend),
            Choice("19) Mint Starknet ID", mint_starknet_id),
            Choice("20) Dmail send mail", send_mail_dmail),
            Choice("21) Mint StarkStars NFT", mint_starkstars),
            Choice("22) Mint NFT on Pyramid", create_collection_pyramid),
            Choice("23) Unframed", cancel_order_unframed),
            Choice("24) Flex", cancel_order_flex),
            Choice("25) Deploy token", deploy_token),
            Choice("26) Deploy and mint NFT", deploy_nft),
            Choice("27) Transfer", make_transfer),
            Choice("28) Swap tokens to ETH", swap_tokens),
            Choice("29) Use Multiswap", swap_multiswap),
            Choice("30) Use custom routes ", custom_routes),
            Choice("31) Check transaction count", "tx_checker"),
            Choice("32) Exit", "exit"),
        ],
        qmark="⚙️ ",
        pointer="✅ "
    ).ask()
    if result == "exit":
        print("\n❤️ Author – https://t.me/sybilwave\n")
        print("\n❤️ Fork Author – https://t.me/rgalyeon\n")
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
    if recipient:
        await module(account_id, key, TYPE_WALLET, recipient)
    else:
        await module(account_id, key, TYPE_WALLET)

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
    print("❤️ Author – https://t.me/sybilwave\n")
    print("\n❤️ Fork Author – https://t.me/rgalyeon\n")

    loguru.logger.add('logs.txt', filter=filter_out_utils)
    module = get_module()
    if module == "tx_checker":
        get_tx_count(TYPE_WALLET)
    else:
        main(module)

    print("\n❤️ Author – https://t.me/sybilwave\n")
    print("\n❤️ Fork Author – https://t.me/rgalyeon\n")
