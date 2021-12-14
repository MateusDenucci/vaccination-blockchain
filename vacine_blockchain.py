import hashlib
import time
import json


class VaccinationBlock:
    def __init__(self, index, previous_block_hash, record_list, timestamp):
        self.index = index
        self.previous_block_hash = previous_block_hash
        self.record_list = record_list
        self.timestamp = timestamp
        self.block_hash = self.get_block_hash()

    def get_block_hash(self):
        block_data = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_data.encode()).hexdigest()


class VaccinationBlockchain:
    def __init__(self):
        self.chain = []
        self.create_initial_block()
    
    def create_initial_block(self):
        initial_block = VaccinationBlock(0, 'First Block', [], time.time())
        self.chain.append(initial_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, record_list):
        last_block = self.get_last_block()

        vaccination_block = VaccinationBlock(
            last_block.index + 1,
            last_block.block_hash,
            record_list,
            time.time()
        )

        self.chain.append(vaccination_block)
    
    @property
    def blockchhain_integrity(self):
        for index in range((len(self.chain) - 1), 1, -1):
            if self.chain[index].previous_block_hash != self.chain[index - 1].block_hash:
                return False
        
        return True


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

    blockchain.add_block([info1, info2])
    blockchain.add_block([info3])

def main():
    blockchain = VaccinationBlockchain()
    insert_test_data(blockchain)

    for vaccination_block in blockchain.chain:
        print(vaccination_block.record_list)

    print(blockchain.blockchhain_integrity)


if __name__ == '__main__':
    main()