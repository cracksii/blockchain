from base import Base


class Block(Base):
    def __init__(self, previous_hash, transactions, nonce):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce

    def get_dict(self):
        return {
            "transaction_hashes": [_.get_hash() for _ in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
