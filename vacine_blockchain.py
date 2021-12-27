import hashlib
import time
import json


class VaccinationBlock:
    def __init__(self, index, previous_block_hash, transactions, timestamp, nonce=0):
        self.index = index
        self.previous_block_hash = previous_block_hash
        self.transactions = transactions
        self.timestamp = timestamp
        self.nonce = nonce
        self.block_hash = self.get_block_hash()

    def get_block_hash(self):
        '''The hash is calculated with the data of all block attributes.'''
        block_data = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()


class VaccinationBlockchain:
    '''The bigger the number, the harder it is to pass in the proof-of-work method.'''
    MINING_DIFFICULTY = 2

    def __init__(self):
        self.chain = []
        self.unconfirmed_transactions = []
        self.create_initial_block()

    @property
    def blockchhain_integrity(self):
        ''' Testing if the hash sequence makes sense.'''
        for index in range((len(self.chain) - 1), 1, -1):
            if self.chain[index].previous_block_hash != self.chain[index - 1].block_hash:
                return False
        
        return True

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def create_initial_block(self):
        initial_block = VaccinationBlock(0, 'First Block', [], time.time())
        self.chain.append(initial_block)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.get_last_block()

        new_block = VaccinationBlock(
            last_block.index + 1,
            last_block.block_hash,
            self.unconfirmed_transactions,
            time.time()
        )

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def get_last_block(self):
        return self.chain[-1]
    
    def proof_of_work(self, block):
        '''While the number of 0s at the beggining of the hash isn't equals to the number of 0s set by the constant
        MINING_DIFFICULTY, it keeps changing the "nounce" attibute in the block in order to computer a new hash and find
        the wanted number of 0s.'''
        block.nonce = 0
        computed_hash = block.get_block_hash()
        while not computed_hash.startswith('0' * VaccinationBlockchain.MINING_DIFFICULTY):
            block.nonce += 1
            computed_hash = block.get_block_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.get_last_block().block_hash
        if previous_hash != block.previous_block_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * VaccinationBlockchain.MINING_DIFFICULTY) and 
                block_hash == block.get_block_hash())


def insert_test_data(blockchain):
    info1 = {
        'name': 'Mateus Denucci',
        'cpf': '46943393030',
        'is_vaccinated': True
    }

    info2 = {
        'name': 'Random Person',
        'cpf': '46943393030',
        'is_vaccinated': False
    }

    info3 = {
        'name': 'Random Person 2',
        'cpf': '46943396030',
        'is_vaccinated': False
    }

    blockchain.add_new_transaction([info1, info2])
    blockchain.mine()
    blockchain.add_new_transaction([info3])
    blockchain.mine()

def main():
    blockchain = VaccinationBlockchain()
    insert_test_data(blockchain)

    for vaccination_block in blockchain.chain:
        print(vaccination_block.transactions)

    print(blockchain.blockchhain_integrity)


if __name__ == '__main__':
    main()