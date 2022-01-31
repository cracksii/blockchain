import json
import os
import crypto
from blockchain import get_blockchain
from utxo import UTXO
from transaction import UnsignedTransaction, Transaction
from config import KEY_FILE_NAME
from mempool import get_mempool


class Wallet:
    def __init__(self):
        if os.path.isfile("private_key.json"):
            self.private_key, self.password = self.load_from_file()
        else:
            self.password = crypto.generate_password()
            self.private_key = crypto.generate_private_pem_string(self.password)
            self.save_to_file()
        self.public_key = crypto.generate_public_pem_string(self.private_key, self.password)

    def send_money(self, receiver_public_keys, data):
        total = sum(data)
        tx = self.create_transaction(self.get_utxos(total), receiver_public_keys, data)
        self.insert_to_mempool(tx)

    def get_utxos(self, total):
        blockchain = get_blockchain()
        utxos = blockchain.get_utxos(self.public_key)
        assert isinstance(utxos, list)
        valid_utxos = []
        for i in utxos:
            assert isinstance(i, UTXO)
            if blockchain.is_valid_utxo(i):
                valid_utxos.append(i)

        needed_utxos = []
        amount = 0
        for i in valid_utxos:
            needed_utxos.append(i)
            amount += i.data
            if amount >= total:
                break
        return needed_utxos

    def create_transaction(self, utxos, receiver_public_keys, data):
        unsigned = UnsignedTransaction(utxos, receiver_public_keys, data)
        return unsigned.sign(self.private_key, self.password)

    @staticmethod
    def insert_to_mempool(tx):
        get_mempool().insert_transaction(tx)

    def save_to_file(self):
        data = {
            "private_key": self.private_key,
            "password": self.password
        }

        with open(KEY_FILE_NAME, "w") as f:
            json.dump(data, f)

    @staticmethod
    def load_from_file():
        with open(KEY_FILE_NAME, "r") as f:
            data = json.load(f)
            return data["private_key"], data["password"]
