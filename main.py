from wallet import Wallet
from blockchain import get_blockchain
from miner import Miner


def mine(pk, tid):
    Miner(pk, tid)


if __name__ == '__main__':
    # print(hashing.hash("Ayo, razer mouse and iPhone 11 look very smooth together. Nvm pikachu is even cooler."))
    w = Wallet()
    w.send_money([w.public_key], [50])
    print(get_blockchain().get_json())
    mine(w.public_key, 1)
