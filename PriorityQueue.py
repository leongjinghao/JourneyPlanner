class PriorityQueue:
    # binary heap implementation for priority queue
    heap = []

    # constructor for priority queue class
    def __init__(self, start):
        # insert dummy node on the first index, to facilitate subsequent math operations
        self.insert(None, None)
        # insert the starting vertix on construction, value default to 0
        self.insert(start, 0)

    # return length of binary heap
    def __len__(self):
        # as there is a dummy node in the binary heap, we will need to decrement the len value by 1
        return len(self.heap) - 1

    # check if the binary heap is empty
    def isEmpty(self):
        return self.__len__() == 0

    # insert a new node to the last position, then check for maintenence of the binary heap structure
    def insert(self, key, value):
        node = Node(key, value)
        # append will add the node at the end of the binary heap
        self.heap.append(node)
        # check and relocate newly inserted node if required
        self.move_up()
    
    # check if last node need to move up, perform steps accordingly
    def move_up(self):
        # check newly inserted element, which is at the last index
        # __len__() already decrement the lenght, hence can just take returned value as last index
        i = self.__len__()
        
        # while index is not 1 (root node) and 0 (dummy node), both cases do not have parent
        # technically index 1 have a parent node at index 0, but it is the dummy node (not meaningful)
        while i // 2 > 0:
            # check the value of the newly inserted element (last index) with its parent
            # floor division of index by 2, as the index of the parent node is 2x of the child index (by definition)
            if self.heap[i].value < self.heap[i // 2].value:
                # swap up with parent node if current node is less than parent
                self.heap[i // 2], self.heap[i] = self.heap[i], self.heap[i // 2]
            
            # move up to parent node to check if another rotate up is required
            i = i // 2

    # check if node on current index i, need to move down , perform steps accordingly
    def move_down(self, i):
        # while index i is not the last index
        while i * 2 <= self.__len__():
            # get the smallest child of node at index i
            min_child = self.getMinChild(i)
            # if node at index i is more than its smallest child
            if self.heap[i].value > self.heap[min_child].value:
                # swap down with child node 
                self.heap[i], self.heap[min_child] = self.heap[min_child], self.heap[i]
            
            i = min_child

    # return smallest child of node at index i
    def getMinChild(self, i):
        # if node does not have a right child, it only has a left child
        if i * 2 + 1 > self.__len__():
            # return the only left (smallest) child
            return i * 2
        
        # else it has both child
        # if left child is smaller than right child
        if self.heap[i * 2].value < self.heap[i * 2 + 1].value:
            # return left (smallest) child
            return i * 2
        # else right child is smaller, return right child
        return i * 2 + 1

    # return the smallest node's key (station index) and delete the smallest node in the binary heap
    def delete_min(self):
        # smallest node is the node at index 1, index 0 is dummy node
        min_node = self.heap[1]
        # slot in the last node at last index to the first position at index 1
        self.heap[1] = self.heap[self.__len__()]
        # remove the last node at the last index
        self.heap.pop()
        # check if the new first node need to be moved down
        self.move_down(1)
        # return the smallest node's key
        return min_node.key

    # return True if key (station index) is present in the binary heap, else return False
    def contains(self, key):
        # for all index
        for i in range(self.__len__()):
            # chick if node's key at index i equals to the key input
            if self.heap[i].key == key:
                # return True if matches
                return True
        #else no match found, return False
        return False

    # change the value (priority) of the node which matches the key input
    def change(self, key, value):
        # locate the node which matches the key input
        for i in range(self.__len__()):
            if self.heap[i].key == key:
                # change the value (priority) of the node
                self.heap[i].value = value
                # changed value is always smaller, only need to check if there is a need to rotate up
                while i // 2 > 0:
                    # if 
                    if self.heap[i].value < self.heap[i // 2].value:
                        # swap up with parent node if node is less than parent after change
                        self.heap[i // 2], self.heap[i] = self.heap[i], self.heap[i // 2]
                    # move up to parent node to check if another rotate up is required
                    i = i // 2

class Node:
    key = 0
    value = 0

    def __init__(self, key, value):
        self.key = key
        self.value = value