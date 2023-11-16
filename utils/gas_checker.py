import time
import random

from starknet_py.net.gateway_client import GatewayClient

from web3 import AsyncWeb3
from web3.eth import AsyncEth
from config import RPC
from settings import CHECK_GWEI, MAX_GWEI, GAS_SLEEP_FROM, GAS_SLEEP_TO
from loguru import logger

from utils.sleeping import sleep


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

        if gas > MAX_GWEI:
            logger.info(f'Current GWEI: {gas} > {MAX_GWEI}')
            await sleep(GAS_SLEEP_FROM, GAS_SLEEP_TO)
        else:
            logger.success(f"GWEI is normal | current: {gas} < {MAX_GWEI}")
            break


async def wait_gas_starknet():
    logger.info("Get GWEI")

    client = GatewayClient("mainnet")

    while True:
        block_data = await client.get_block("latest")
        gas = AsyncWeb3.from_wei(block_data.gas_price, "gwei")

        if gas > MAX_GWEI:
            logger.info(f'Current GWEI: {gas} > {MAX_GWEI}')
            await sleep(GAS_SLEEP_FROM, GAS_SLEEP_TO)
        else:
            logger.success(f"GWEI is normal | current: {gas} < {MAX_GWEI}")
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
