import hashlib, json, time
from tinydb import TinyDB, Query, JSONStorage
from tinydb.middlewares import CachingMiddleware
blockchain = TinyDB('blockchain.json', storage=JSONStorage, indent=4, sort_keys=True)
current_transactions = [
    {
        'sender': 0,
        'recipient': "unknown",
        'amount': 0,
        'fee': 0,
        'timestamp': time.time()
    }
]


def add_transaction(sender, recipient, amount, fee):
    global current_transactions
    current_transactions.append({
        'sender': sender,
        'recipient': recipient,
        'amount': amount,
        'fee': fee,
        'timestamp': time.time()
    })
    subsidy = 50
    fees = sum(t.get('fee') for t in current_transactions[1:])
    current_transactions[0] = {
        'sender': "0",
        'recipient': "unknown",
        'amount': subsidy + fees,
        'fee': 0,
        'timestamp': time.time()
    }

def create_block_object(proof=0, last_block_id=None, id_type="automatic"):
    global current_transactions
    Block = Query()
    block = blockchain.all()
    if last_block_id:
        if id_type == "automatic":
            #filter based on automatically generated id
            last_block = blockchain.get(doc_id=last_block_id)
        elif id_type == "manual":
            #using manual id field
            last_block = blockchain.search(Block.id == 0)
    last_block = block[-1]
    block_dict = {'id': len(block),
             'timestamp': time.time(), 
             'transactions': current_transactions, 
             'proof': proof,
             'previous_hash': hashlib.sha256(json.dumps(last_block, sort_keys=True).encode()).hexdigest()
            }
    return block_dict
def add_block_to_blockchain(block):
    global current_transactions
    encoded_block = json.dumps(block, sort_keys=True).encode()
    if check_proof_validity(encoded_block):
        blockchain.insert(block)
    current_transactions = [
        {
        'sender': "0",
        'recipient': "unknown",
        'amount': 0,
        'fee': 0,
        'timestamp': time.time()
        }
    ]
    return
def check_proof_validity(encoded_block):
    hash = hashlib.sha256(encoded_block).hexdigest()
    return hash[:4] == "0000"
def mine(block, user):
    block['transactions'][0]['recipient'] = user
    nonce = 0
    while True:
        block['proof'] = nonce
        encoded_block = json.dumps(block, sort_keys=True).encode()
        if check_proof_validity(encoded_block):
            break
        nonce += 1
    return nonce
username = "user"
block = create_block_object()
proof = mine(block, username)
block["proof"] = proof
add_block_to_blockchain(block)
