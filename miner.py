from transaction import Transaction, CoinbaseTransaction
import random
from mempool import get_mempool
from blockchain import get_blockchain
from block import Block
from config import MAX_MINING_APPEND
import time


class Miner:
    def __init__(self, miner_public_key, id):
        self.public_key = miner_public_key
        self.blockchain = get_blockchain()
        self.tid = id
        print(f"Started mining for pk {self.public_key}")
        while True:
            self.mine()

    def mine(self):
        latest_block = self.blockchain.get_latest_block()
        assert isinstance(latest_block, Block)
        previous_hash = latest_block.get_hash()
        txs = get_mempool().tx
        for i in txs:
            assert isinstance(i, Transaction) or isinstance(i, CoinbaseTransaction)
            if isinstance(i, Transaction):
                if not i.is_valid():
                    txs.remove(i)

        coinbase = CoinbaseTransaction(self.public_key)
        txs.insert(0, coinbase)
        while True:
            if self.blockchain.get_latest_block() != latest_block:
                break
            block = Block(previous_hash, txs, random.randint(0, MAX_MINING_APPEND))
            valid = self.blockchain.check_against_target(block.get_hash())
            if valid:
                if self.blockchain.insert_block(block):
                    print(f"Miner {self.tid} found new block")
                    print(self.blockchain.get_json())
                    break
