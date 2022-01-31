import time
from threading import Thread
from base import Base
from block import Block
from genesis import genesis_coinbase
from transaction import Transaction, CoinbaseTransaction
import hashing
from utxo import UTXO
from config import MINING_TARGET
from mempool import get_mempool

blockchain = None


def get_blockchain():
    global blockchain
    if not blockchain:
        blockchain = Blockchain()
    return blockchain


class Blockchain(Base):
    def __init__(self):
        self.blocks = [Block("fGORvCrl9EyT950GofQeugK1YXmUjiX8cxHfCUL+tWI=", [genesis_coinbase()], 0)]
        self.hps = 0
        Thread(target=self.info).start()

    def insert_block(self, block):
        assert isinstance(block, Block)
        for tx in block.transactions:
            if isinstance(tx, Transaction):
                if not tx.is_valid():
                    print("tx is not valid")
                    return False
                for utxo in tx.utxos:
                    if not self.is_valid_utxo(utxo):
                        print("utxo is not valid")
                        return
            elif isinstance(tx, CoinbaseTransaction):
                if block.transactions.index(tx) != 0:
                    print("multiple coinbase-transactions are not allowed")
                    return False
            else:
                print(type(tx))
                return False
        if not self.check_against_target(block.get_hash()):
            print("target is not matched")
            return False
        self.blocks.append(block)
        get_mempool().clear()
        return True

    def check_against_target(self, hash_string):
        self.hps += 1
        hex = hashing.string_to_hex(hash_string)
        for i in range(MINING_TARGET):
            if not hex[i] == "0":
                return False
        return True

    def info(self):
        while True:
            time.sleep(0.99)
            print(self.hps)
            self.hps = 0

    def is_valid_utxo(self, utxo):
        valid = False
        for block in self.blocks:
            for tx in block.transactions:
                if tx.get_hash() == utxo.tx_hash:
                    counter = 0
                    for public_key in tx.receiver_public_keys:
                        if public_key in utxo.public_key:
                            if utxo.data == tx.data[counter]:
                                valid = True
                        counter += 1
        if not valid:
            return False

        for block in self.blocks:
            for tx in block.transactions:
                if isinstance(tx, Transaction):
                    for tx_utxo in tx.utxos:
                        if tx_utxo.get_hash() == utxo.get_hash():
                            return False
        return True

    def get_utxos(self, public_key):
        utxos = []
        for block in self.blocks:
            for tx in block.transactions:
                counter = 0
                for pk in tx.receiver_public_keys:
                    if pk in public_key:
                        utxo = UTXO(tx.get_hash(), public_key, tx.data[counter])
                        utxos.append(utxo)
                    counter += 1
        return utxos

    def get_latest_block(self):
        return self.blocks[-1]

    def get_dict(self):
        return {
            "blocks": [_.get_dict() for _ in self.blocks]
        }
