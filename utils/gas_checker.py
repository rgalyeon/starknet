import time
import random

from starknet_py.net.gateway_client import GatewayClient

from web3 import AsyncWeb3
from web3.eth import AsyncEth
from config import RPC, REALTIME_SETTINGS_PATH
from settings import CHECK_GWEI, MAX_GWEI, GAS_SLEEP_FROM, GAS_SLEEP_TO, RANDOMIZE_GWEI, MAX_GWEI_RANGE, REALTIME_GWEI
from loguru import logger
import json

from utils.sleeping import sleep


def get_max_gwei_user_settings():
    max_gwei = MAX_GWEI
    if RANDOMIZE_GWEI:
        left_bound, right_bound = MAX_GWEI_RANGE
        max_gwei = random.uniform(left_bound, right_bound)
    if REALTIME_GWEI:
        try:
            with open(REALTIME_SETTINGS_PATH, 'r') as f:
                new_max_gwei = json.load(f)['MAX_GWEI']
            if new_max_gwei < 0:
                raise ValueError('Max gwei is not an integer')
            max_gwei = new_max_gwei
        except Exception:
            pass
    return max_gwei


async def get_gas():
    try:
        w3 = AsyncWeb3(
            AsyncWeb3.AsyncHTTPProvider(random.choice(RPC["ethereum"]["rpc"])),
            modules={"eth": (AsyncEth,)},
        )
        gas_price = await w3.eth.gas_price
        gwei = w3.from_wei(gas_price, 'gwei')
        return gwei
    except Exception as error:
        logger.error(error)


async def wait_gas_ethereum():
    logger.info("Get GWEI")
    while True:
        gas = await get_gas()

        max_gwei = get_max_gwei_user_settings()
        if gas > max_gwei:
            logger.info(f'Current GWEI: {gas} > {max_gwei}')
            await sleep(GAS_SLEEP_FROM, GAS_SLEEP_TO)
        else:
            logger.success(f"GWEI is normal | current: {gas} < {max_gwei}")
            break


async def wait_gas_starknet():
    logger.info("Get GWEI")

    client = GatewayClient("mainnet")

    while True:
        block_data = await client.get_block("latest")
        gas = AsyncWeb3.from_wei(block_data.gas_price, "gwei")

        max_gwei = get_max_gwei_user_settings()
        if gas > max_gwei:
            logger.info(f'Current GWEI: {gas} > {max_gwei}')
            await sleep(GAS_SLEEP_FROM, GAS_SLEEP_TO)
        else:
            logger.success(f"GWEI is normal | current: {gas} < {max_gwei}")
            break


def check_gas(network: str):
    def decorator(func):
        async def _wrapper(*args, **kwargs):
            if CHECK_GWEI:
                if network == "ethereum":
                    await wait_gas_ethereum()
                else:
                    await wait_gas_starknet()
            return await func(*args, **kwargs)

        return _wrapper

    return decorator
