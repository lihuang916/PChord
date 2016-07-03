# A Distributed Hash Table implementation


class Node:
    def __init__(self, ID, nxt = None, prev = None):
        self.ID = ID
        self.data = dict()
        self.next = nxt
        self.prev = prev

class DHT:
    # Size is the total number of IDs available in the DHT
    # Typically, this number is powers of 2
    def __init__(self, size):
        self._size = size    
        self._startNode = Node(0)
        self._startNode.next = self._startNode
        self._startNode.prev = self._startNode


    # Hash function used to get the ID
    def getHashId(self, key):
        return key % self._size

    # Get distance between to IDs
    def distance(self, n1, n2):
        if n1 == n2:
            return 0
        if n1 < n2:
            return n2 - n1
        return self._size - n1 + n2

    # Get number of nodes in the system
    def getNumNodes(self):
        if self._startNode == None:
            return 0
        node = self._startNode
        n = 1
        while node.next != self._startNode:
            n = n + 1
            node = node.next
        return n
    
    # Find the node responsible for the key
    def findNode(self, start, key):
        hashId = self.getHashId(key)
        curr = start
        while self.distance(curr.ID, hashId) > \
              self.distance(curr.next.ID, hashId):
            curr = curr.next
        if hashId == curr.ID:
            return curr
        return curr.next

    # Look up a key in the DHT
    def lookup(self, start, key):
        nodeForKey = self.findNode(start, key)
        print("The key is in node: ", nodeForKey.ID)
        return nodeForKey.data[key]

    # Store a key-value pair in the DHT
    def store(self, start, key, value):
        nodeForKey = self.findNode(start, key)
        nodeForKey.data[key] = value

    # When new node joins the system
    def join(self, newNode):
        # Find the node before which the new node should be inserted
        origNode = self.findNode(self._startNode, newNode.ID)

        print(origNode.ID, "  ", newNode.ID)
        # If there is a node with the same id, decline the join request for now
        if origNode.ID == newNode.ID:
            print("There is already a node with the same id!")
            return
        
        # Copy the key-value pairs that will belong to the new node after
        # the node is inserted in the system
        for key in origNode.data:
            hashId = self.getHashId(key)
            if self.distance(hashId, newNode.ID) < self.distance(hashId, origNode.ID):
                newNode.data[key] = origNode.data[key]

        # Update the prev and next pointers
        prevNode = origNode.prev
        newNode.next = origNode
        newNode.prev = prevNode
        origNode.prev = newNode
        prevNode.next = newNode

        # Delete keys that have been moved to new node
        for key in list(origNode.data.keys()):
            hashId = self.getHashId(key)
            if self.distance(hashId, newNode.ID) < self.distance(hashId, origNode.ID):
                del origNode.data[key]
                
    
    def leave(self, node):
        # Copy all its key-value pairs to its successor in the system
        for k, v in node.data.items():
            node.next.data[k] = v
        # If this node is the only node in the system.
        if node.next == node:
            self._startNode = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            # If this deleted node was an entry point to the system, we
            # need to choose another entry point. Simply choose its successor
            if self._startNode == node:
                self._startNode = node.next

    # TODO: avoid duplicate nodes. 
        

            

def main():
    pass

d = DHT(128)
d.store(d._startNode, 50, "hello")
d.lookup(d._startNode, 50)
d.join(Node(60))
print(d.lookup(d._startNode, 50))
d.join(Node(40))
print(d.lookup(d._startNode, 50))      
d.join(Node(55))
print(d.lookup(d._startNode, 50))      
d.join(Node(50))
print(d.lookup(d._startNode, 50))
    
if __name__ == "__main__":
    main()
