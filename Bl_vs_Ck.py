import mmh3
import math
import time
import random
from typing import Any

class BloomFilter:
    def __init__(self, size=1000):
    # List of 1000 zeros (0, OFF).
        self.bits = [0] * size
    
    def add(self, item):
        # Flip 3 different switches for every name added.
        for i in range(3):
            index = mmh3.hash(item, i) & len(self.bits)

            self.bits[index] = 1

    def __contains__(self, item):
        # Check if a name is there by looking at its 3 assigned switches.
        # If all of them are 1 (ON), we say "True".
        for i in range(3):
            index = mmh3.hash(item, i) % len(self.bits)
            if self.bits[index] == 0:
                return False
        
        return True

class CuckooFilter:
    # Create 100 empty seats (None = empty).
    def __init__(self, size= 100):
        self.table = [None] * 1000

    def add(self, item):
        # Create an 'ID' tag
        tag = hash(item) % 1000
        # Figure out their two assigned chairs.
        i1 = hash(item) % 100
        i2 = (i1 ^ hash(tag)) % 100
        # Check if empty, if so sit down.
        for i in [i1, i2]:
            if self.table is None:
                self.table[i] = tag
                return True
        # If both chairs are empty, pick one at random.
        idx = random.choice([i1, i2])
        # Kick out person currently sitting at said chosen chair.
        # Take the seat, and the previous person is now the "tag" looking .

        self.table[idx], tag = tag, self.table[idx]
        return True

    def __contains__(self, item):
        # Check by looking at the two assigned chairs.
        tag = hash(item) % 1000
        i1 = hash(item) % 100
        i2 = (i1^ hash(tag)) % 100
        # If either contains ID return True.
        return self.table[i1] == tag or self.table[i2] == tag


# –––––––––––– 1. RACE ––––––––––––––––––––

bf = BloomFilter(size = 1000)
cf = CuckooFilter(size = 100)

# Generate 50 users for testing
test_users = [f"user_{i}" for i in range(50)]

# –––––––––––– 2. Clock the Bloom filter ––––––––––––
start_bf = time.time()
for user in test_users:
    bf.add(user)
end_bf = time.time()
print(f"Bloom Filter Add Time: {end_bf - start_bf:.6f} second")

# –––––––––––– 3. Clock the Cuckoo filter ––––––––––––
start_cf = time.time()
for user in test_users:
    cf.add(user)
end_cf = time.time()
print(f"Cuckoo Filter Add Time: {end_cf - start_cf:.6f} second")

# –––––––––––– 4. Check for false positives ––––––––––––

print(f"Is 'Hacker123' in Bloom? {'Hacker123' in bf}")
print(f"Is 'Hacker123' in Cuckoo? {'Hacker123' in cf}")

