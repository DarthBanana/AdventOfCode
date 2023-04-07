class RingNode:
    def __init__(self, value):
        self.data = value
        self.next = self
        self.prev = self
    
    def insert_before(self, node):
        prev_node = self.prev
        prev_node.next = node
        self.prev = node
        node.next = self
        node.prev = prev_node

    def insert_after(self, node):
        next_node = self.next
        next_node.prev = node
        self.next = node
        node.prev = self
        node.next = next_node

    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        self.next = self
        self.prev = self

    def get_n_forward(self, n):
        cur = self
        for i in range(n):
            cur = cur.next
        
        return cur

    def get_n_back(self, n):
        cur = self
        for i in range(n):
            cur = cur.prev
        return cur

    def __str__(self):
        return str(self.data)
    def __repr__(self):
        return self.__str__()
    
    def print_ring(self):
        node = self        
        while True:            
            print(str(node.data), end=",")
            if node == self.prev:
                break
            node = node.next
        print()