from transaction import Transaction

mempool = None


def get_mempool():
    global mempool
    if not mempool:
        mempool = Mempool()
    return mempool


class Mempool:
    def __init__(self):
        self.tx = []

    def insert_transaction(self, tx):
        assert isinstance(tx, Transaction)
        assert tx.is_valid()
        self.tx.append(tx)

    def clear(self):
        self.tx = []
