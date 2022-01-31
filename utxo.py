from base import Base


class UTXO(Base):
    def __init__(self, tx_hash, public_key, data):
        self.tx_hash = tx_hash
        self.public_key = public_key
        self.data = data

    def get_dict(self):
        return {
            "tx_hash": self.tx_hash,
            "public_key": self.public_key,
            "data": self.data
        }
