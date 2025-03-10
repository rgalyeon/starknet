import time

from loguru import logger

from config import SITHSWAP_CONTRACT, SITHSWAP_ABI, STARKNET_TOKENS
from utils.gas_checker import check_gas
from utils.helpers import retry
from . import Starknet


class SithSwap(Starknet):
    def __init__(self, _id: int, private_key: str, type_account: str) -> None:
        super().__init__(_id=_id, private_key=private_key, type_account=type_account)

        self.contract = self.get_contract(SITHSWAP_CONTRACT, SITHSWAP_ABI)

    async def get_min_amount_out(self, amount: int, slippage: float, path: list):
        min_amount_out_data = await self.contract.functions["getAmountOut"].prepare(
            amount,
            path[0],
            path[1]
        ).call()

        min_amount_out = min_amount_out_data.amount
        stable = min_amount_out_data.stable

        return int(min_amount_out - (min_amount_out / 100 * slippage)), stable

    @retry
    @check_gas("starknet")
    async def swap(
            self,
            from_token: str,
            to_token: str,
            min_amount: float,
            max_amount: float,
            decimal: int,
            slippage: float,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            from_token,
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(
            f"[{self._id}][{self.address_str}] Swap on SithSwap - {from_token} -> {to_token} | {amount} {from_token}"
        )

        path = [STARKNET_TOKENS[from_token], STARKNET_TOKENS[to_token]]

        deadline = int(time.time()) + 1000000

        min_amount_out, stable = await self.get_min_amount_out(amount_wei, slippage, path)

        route = [{"from_address": path[0], "to_address": path[1], "stable": stable}]

        approve_contract = self.get_contract(STARKNET_TOKENS[from_token])

        approve_call = approve_contract.functions["approve"].prepare(
            SITHSWAP_CONTRACT,
            amount_wei
        )

        swap_call = self.contract.functions["swapExactTokensForTokens"].prepare(
            amount_wei,
            min_amount_out,
            route,
            self.address,
            deadline
        )

        transaction = await self.sign_transaction([approve_call, swap_call])

        transaction_response = await self.send_transaction(transaction)

        await self.wait_until_tx_finished(transaction_response.transaction_hash)
