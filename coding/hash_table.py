# Hash Table:
# Methods:
    # Insert / Update (key, value). __setitem__(self, key, value): calculte hash -> linear_probing -> save
    # Search (key) # __getitem__(self, key)
    # Delete (key) # __delitem__(self, key)
    #               # __len__(self)
                    # __resize(self)

    # List of keys, values
    # Table is power of 2
    # For keys we have 3 states: None (empty), "DELETE", or Filled

class HashTable:
    def __init__(self, load_factor_thr = 0.5):

        self.DELETE = object()
        self.EMPTY = None

        self.capacity = 8
        self.size = 0
        self.keys = [self.EMPTY]*self.capacity
        self.values = [self.EMPTY]*self.capacity
        self.load_factor_thr = load_factor_thr


    def __len__(self):
        return self.size
    
    def _probing(self, key):
        hash_value = hash(key)
        index = hash_value & (self.capacity - 1)
        probing_idx = 0
        first_delete_idx = -1
        while probing_idx < self.capacity and self.keys[index] != self.EMPTY and self.keys[index] != key:
            if self.keys[index] == self.DELETE and first_delete_idx == -1:
                first_delete_idx = index
            probing_idx += 1
            index = (hash_value + probing_idx ** 2) & (self.capacity - 1)
        
        if probing_idx == self.capacity and first_delete_idx == -1:
            self.__resize__()
            return self._probing(key)
        
        return index, first_delete_idx

    def __setitem__(self, key, value):
        # check if load_factor is greater than acceptable threshold
        if self.size / self.capacity > self.load_factor_thr:
            self.__resize__()
        # calculate hash -> find index -> try quadratic probing
        index, first_delete_idx = self._probing(key)
        # if we found the key
        if self.keys[index] == key:
            self.values[index] = value
        # if we found empty cell
        elif first_delete_idx != -1:
            # we there is a DELETE cell
            self.keys[first_delete_idx] = key
            self.values[first_delete_idx] = value
            self.size += 1
        else:
            self.keys[index] = key
            self.values[index] = value
            self.size += 1

    def __getitem__(self, key):
        index, _ = self._probing(key)
        # check if the cell empty
        if self.keys[index] == self.EMPTY or self.keys[index] == self.DELETE:
            raise KeyError
        return self.values[index]
    
    def __delitem__(self, key):
        index, _ = self._probing(key)
        if self.keys[index] == key:
            self.keys[index] = self.DELETE
            self.size -= 1
        
    def __resize__(self):
        old_keys = self.keys
        old_values = self.values
        self.capacity *= 2
        self.keys = [self.EMPTY]*self.capacity
        self.values = [self.EMPTY]*self.capacity
        self.size = 0
        for key, value in zip(old_keys, old_values):
            if key != self.EMPTY and key != self.DELETE:
                self.__setitem__(key, value)




def run_all_tests():
    print("Running HashTable tests...")

    # helper class to force hash collisions
    class BadHash:
        def __init__(self, value):
            self.value = value
        def __hash__(self):
            return 1
        def __eq__(self, other):
            return isinstance(other, BadHash) and self.value == other.value

        

    # -------------------------
    # 1. Basic insert + get
    # -------------------------
    ht = HashTable()
    ht["a"] = 1
    assert ht["a"] == 1
    ht["a"] = 2
    assert ht["a"] == 2

    # -------------------------
    # 2. Bulk inserts
    # -------------------------
    ht = HashTable()
    for i in range(100):
        ht[i] = i * 10
    for i in range(100):
        assert ht[i] == i * 10

    # -------------------------
    # 3. Missing key
    # -------------------------
    ht = HashTable()
    try:
        ht["missing"]
        assert False, "Expected KeyError"
    except KeyError:
        pass

    # -------------------------
    # 4. Delete basic
    # -------------------------
    ht = HashTable()
    ht["x"] = 42
    del ht["x"]
    try:
        ht["x"]
        assert False
    except KeyError:
        pass

    # -------------------------
    # 5. Reinsert after delete
    # -------------------------
    ht = HashTable()
    ht["x"] = 1
    del ht["x"]
    ht["x"] = 5
    assert ht["x"] == 5

    # -------------------------
    # 6. Search past tombstone
    # -------------------------
    ht = HashTable()
    for i in range(3):
        ht[i] = i
    del ht[0]
    assert ht[1] == 1
    assert ht[2] == 2

    # -------------------------
    # 7. Only tombstones except one key
    # -------------------------
    ht = HashTable()
    keys = [f"k{i}" for i in range(20)]
    for k in keys:
        ht[k] = k
    for k in keys[:-1]:
        del ht[k]

    assert ht[keys[-1]] == keys[-1]

    try:
        ht["zzz"]
        assert False
    except KeyError:
        pass

    # -------------------------
    # 8. Insert after many tombstones
    # -------------------------
    ht = HashTable()
    for i in range(20):
        ht[i] = i
    for i in range(20):
        del ht[i]

    ht["x"] = 99
    assert ht["x"] == 99

    # -------------------------
    # 9. Resize correctness
    # -------------------------
    ht = HashTable(load_factor_thr=0.5)
    for i in range(500):
        ht[i] = i * 3
    for i in range(500):
        assert ht[i] == i * 3

    # -------------------------
    # 10. Resize with tombstones
    # -------------------------
    ht = HashTable(load_factor_thr=0.5)
    for i in range(50):
        ht[i] = i
    for i in range(25):
        del ht[i]

    for i in range(50, 200):
        ht[i] = i

    for i in range(25, 200):
        assert ht[i] == i

    # -------------------------
    # 11. Forced collisions
    # -------------------------
    ht = HashTable()
    objs = [BadHash(i) for i in range(20)]
    for o in objs:
        ht[o] = o.value

    print(len(ht))
    for o in objs:
        assert ht[o] == o.value

    # -------------------------
    # 12. Collision + delete + reinsert
    # -------------------------
    ht = HashTable()
    keys = [BadHash(i) for i in range(10)]
    for k in keys:
        ht[k] = k.value
    del ht[keys[0]]
    del ht[keys[1]]
    ht[keys[0]] = 999
    ht[keys[1]] = 888
    assert ht[keys[0]] == 999
    assert ht[keys[1]] == 888

    # -------------------------
    # 13. Random stress test
    # -------------------------
    import random
    d = {}
    ht = HashTable()
    for _ in range(2000):
        op = random.choice(["insert", "delete", "lookup"])
        key = random.randint(0, 500)

        if op == "insert":
            val = random.randint(0, 1_000_000)
            d[key] = val
            ht[key] = val

        elif op == "delete":
            if key in d:
                del d[key]
                del ht[key]

        elif op == "lookup":
            if key in d:
                assert ht[key] == d[key]
            else:
                try:
                    ht[key]
                    assert False
                except KeyError:
                    pass

    # -------------------------
    # 14. Edge cases
    # -------------------------
    ht = HashTable()
    ht[None] = "none"
    ht[""] = "empty"
    ht[True] = "true"
    ht[False] = "false"
    assert ht[None] == "none"
    assert ht[""] == "empty"
    assert ht[True] == "true"
    assert ht[False] == "false"

    # -------------------------
    # 15. Overwrite
    # -------------------------
    ht = HashTable()
    ht["A"] = 10
    ht["A"] = 99
    assert ht["A"] == 99

    # -------------------------
    # 16. Reinsertion after resize
    # -------------------------
    ht = HashTable(load_factor_thr=0.5)
    for i in range(100):
        ht[i] = i
    for i in range(50):
        del ht[i]
    for i in range(100, 200):
        ht[i] = i
    for i in range(50, 200):
        assert ht[i] == i

    print("ALL TESTS PASSED ✔️")


if __name__ == "__main__":
    run_all_tests()