class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

# implements a doubly linked list
class DLL:
    def __init__(self):
        self.head = None
    
    def insert_back(self, data):
        if self.head is None:
            self.head = Node(data)
            return
        curr = self.head
        while curr.next is not None:
            curr = curr.next
        curr.next = Node(data)
        curr.next.prev = curr

# main
dll = DLL()
dll.insert_back(3)
dll.insert_back(4)
dll.insert_back(5)
print(dll.head.next.data)
print(dll.head.next.prev.data)
print(dll.head.next.prev.next.data)