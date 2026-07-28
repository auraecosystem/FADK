import hashlib 
import time

class Block: 
def init(self, index, timestamp, data, previous_hash): 
self.index = index 
self.timestamp = timestamp 
self.data = data 
self.previous_hash = previous_hash 
self.nonce = 0 
self.hash = self.compute_hash()
def compute_hash(self):
    block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def mine_block(self, difficulty):
    print("Mining block with difficulty =", difficulty)
    start_time = time.time()

    prefix_str = "0" * difficulty
    while not self.hash.startswith(prefix_str):
        self.nonce += 1
        self.hash = self.compute_hash()

    end_time = time.time()
    print("\nBlock mined successfully!")
    print("Nonce:", self.nonce)
    print("Hash:", self.hash)
    print("Time taken:", round(end_time - start_time, 4), "seconds")

Run the block mining
if name == "main": 
difficulty = 4 
block = Block(1, time.time(), "Transaction A -> B", "0") 
block.mine_block(difficulty)

import hashlib 
import time

class Block: 
def init(self, index, timestamp, data, previous_hash): 
self.index = index 
self.timestamp = timestamp 
self.data = data 
self.previous_hash = previous_hash 
self.nonce = 0 
self.hash = self.compute_hash()

def compute_hash(self):
    block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
    return hashlib.sha256(block_string.encode()).hexdigest()

Create Genesis Block
genesis_block = Block(0, time.time(), "Genesis Block", "0") 
print(f"Block 0: {genesis_block.hash}")

Create Block 1
block1 = Block(1, time.time(), "Transaction A -> B", genesis_block.hash) 
print(f"Block 1: {block1.hash}")

Create Block 2
block2 = Block(2, time.time(), "Transaction B -> C", block1.hash) 
print(f"Block 2: {block2.hash}")

Store blocks in a chain
blockchain = [genesis_block, block1, block2,block3,block4]

print("\n--- Blockchain ---") 
for block in blockchain: 
print(f"Index: {block.index}, Hash: {block.hash}, PrevHash: {block.previous_hash}")

Challenge: Tamper with Block 1
print("\n--- Tampering Block 1 ---") 
block1.data = "Transaction A -> HACKED" 
block1.hash = block1.compute_hash()

Check integrity
print(f"Tampered Block 1 Hash: {block1.hash}") 
print(f"Block 2 PrevHash (unchanged): {block2.previous_hash}")

Is blockchain still valid?
print("\n--- Integrity Check ---") 
if block2.previous_hash != block1.hash: 
print(" Blockchain is INVALID due to tampering in Block 1!") 
else: 
print(" Blockchain is still valid.")

import hashlib 
import time

class Block: 
def init(self, index, timestamp, data, previous_hash): 
self.index = index 
self.timestamp = timestamp 
self.data = data 
self.previous_hash = previous_hash 
self.nonce = 0 
self.hash = self.compute_hash()

def compute_hash(self):
    block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
    return hashlib.sha256(block_string.encode()).hexdigest()

def mine_block(self, difficulty):
    print("Mining block with difficulty =", difficulty)
    start_time = time.time()

    prefix_str = "0" * difficulty
    while not self.hash.startswith(prefix_str):
        self.nonce += 1
        self.hash = self.compute_hash()

    end_time = time.time()
    print("\nBlock mined successfully!")
    print("Nonce:", self.nonce)
    print("Hash:", self.hash)
    print("Time taken:", round(end_time - start_time, 4), "seconds")

Run the block mining
if name == "main": 
difficulty = 4 
block = Block(1, time.time(), "Transaction A -> B", "0") 
block.mine_block(difficulty)
