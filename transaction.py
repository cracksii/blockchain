from base import Base
from utxo import UTXO
import crypto
from config import BLOCK_REWARD


class BaseTransaction(Base):
    def __init__(self, utxos, receiver_public_keys, data):
        assert isinstance(receiver_public_keys, list)
        assert isinstance(data, list)
        assert len(receiver_public_keys) == len(data)
        assert len(receiver_public_keys) > 0

        if utxos:
            assert isinstance(utxos, list)
            assert len(utxos) > 0
            for i in utxos:
                assert isinstance(i, UTXO)
                assert i.public_key == utxos[0].public_key
            self.utxos = utxos

        self.receiver_public_keys = receiver_public_keys
        self.data = data

    def get_dict(self):
        base = {
            "receiver_public_keys": self.receiver_public_keys,
            "data": self.data
        }

        try:
            base["utxos"] = [_.get_dict() for _ in self.utxos]
        finally:
            return base


class Transaction(BaseTransaction):
    def __init__(self, utxos, receiver_public_keys, data, signature):
        super().__init__(utxos, receiver_public_keys, data)
        self.signature = signature
        assert self.is_valid()

    def get_dict(self):
        return {
            "receiver_public_keys": self.receiver_public_keys,
            "data": self.data,
            "utxos": [_.get_dict() for _ in self.utxos],
            "signature": self.signature
        }

    def is_valid(self):
        tx = BaseTransaction(self.utxos, self.receiver_public_keys, self.data)
        signature_valid = crypto.verify(self.utxos[0].public_key, self.signature, tx.get_hash())
        spent = 0
        for val in self.data:
            spent += val

        balance = 0
        for utxo in self.utxos:
            balance += utxo.data
        transaction_valid = balance == spent
        return signature_valid and transaction_valid


class UnsignedTransaction(BaseTransaction):
    def __init__(self, utxos, receiver_public_keys, data):
        super().__init__(utxos, receiver_public_keys, data)

    def get_signature(self, private_key, password):
        return crypto.sign(private_key, password, self.get_hash())

    def sign(self, private_key, password):
        return Transaction(self.utxos, self.receiver_public_keys, self.data, self.get_signature(private_key, password))


class CoinbaseTransaction(BaseTransaction):
    def __init__(self, receiver):
        super().__init__(None, [receiver], [BLOCK_REWARD])
