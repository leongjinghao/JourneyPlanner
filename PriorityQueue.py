class PriorityQueue:
    # binary heap
    heap = []

    # constructor for priority queue class
    def __init__(self, start):
        # insert dummy node on the first index, to facilitate subsequent math operations
        self.insert(None, None)
        # insert the starting vertix on construction, value default to 0
        self.insert(start, 0)

    # return length of priority queue
    def __len__(self):
        # as there is a dummy node in the priority list, we will need to decrement the len value
        return len(self.heap) - 1

    def isEmpty(self):
        return self.__len__() == 0

    def insert(self, key, value):
        node = Node(key, value)
        self.heap.append(node)
        # check and relocate newly inserted element if required
        self.rotate_up()
    
    def rotate_up(self):
        # check newly inserted element, which is at the last index
        i = self.__len__()
        
        while i // 2 > 0:
            if self.heap[i].value < self.heap[i // 2].value:
                # rotate up
                self.heap[i // 2], self.heap[i] = self.heap[i], self.heap[i // 2]
            # move up to check if another rotate up is required
            i = i // 2

    def rotate_down(self, i):
        while i * 2 <= self.__len__():
            min_child = self.getMinChild(i)
            if self.heap[i].value > self.heap[min_child].value:
                # rotate down
                self.heap[i], self.heap[min_child] = self.heap[min_child], self.heap[i]
            i = min_child

    def getMinChild(self, i):
        if i * 2 + 1 > self.__len__():
            return i * 2

        if self.heap[i * 2].value < self.heap[i * 2 + 1].value:
            return i * 2

        return i * 2 + 1

    def delete_min(self):
        min_node = self.heap[1]
        self.heap[1] = self.heap[self.__len__()]
        self.heap.pop()
        self.rotate_down(1)
        return min_node.key

    def contains(self, key):
        for i in range(self.__len__()):
            if self.heap[i].key == key:
                return True
        return False

    def change(self, key, value):
        for i in range(self.__len__()):
            if self.heap[i].key == key:
                self.heap[i].value = value
                # changed value is always smaller, check if there is a need to rotate up
                while i // 2 > 0:
                    if self.heap[i].value < self.heap[i // 2].value:
                        # rotate up
                        self.heap[i // 2], self.heap[i] = self.heap[i], self.heap[i // 2]
                    # move up to check if another rotate up is required
                    i = i // 2

class Node:
    key = 0
    value = 0

    def __init__(self, key, value):
        self.key = key
        self.value = value