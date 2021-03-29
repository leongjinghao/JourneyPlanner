class PriorityQueue:
    heap = []

    def isEmpty(self):
        return len(self.heap) == 0

    def __init__(self, start):
        self.insert(start, 0)

    def rotate_up(self):
        # check newly inserted element
        i = len(self.heap) - 1
        while i // 2 > 0:
            if self.heap[i].value < self.heap[i // 2].value:
                # rotate up
                self.heap[i // 2], self.heap[i] = self.heap[i], self.heap[i // 2]
            # move up to check if another rotate up is required
            i = i // 2

    def insert(self, key, value):
        node = Node(key, value)
        self.heap.append(node)
        # check and relocate newly inserted element if required
        self.rotate_up()

    def rotate_down(self, i):
        while i * 2 <= len(self.heap) - 1:
            min_child = self.getMinChild(i)
            if self.heap[i].value > self.heap[min_child].value:
                # rotate down
                self.heap[i], self.items[min_child] = self.heap[min_child], self.heap[i]
            i = min_child


    def getMinChild(self, i):
        if i * 2 + 1 > len(self.heap) - 1:
            return i * 2

        if self.heap[i * 2] < self.heap[i * 2 + 1]:
            return i * 2

        return i * 2 + 1

    def delete_min(self):
        min_node = self.heap[0]
        self.heap[0] = self.heap[len(self.heap) - 1]
        self.heap.pop()
        self.rotate_down(0)
        return min_node.key

    def contains(self, key):
        for i in range(len(self.heap)):
            if self.heap[i].key == key:
                return True
        return False

    def change(self, key, value):
        for i in range(len(self.heap)):
            if heap[i].key == key:
                heap[i].value = value
                # check if there is a need to rotate up
                self.rotate_up()
                # check if there is a need to rotate down
                self.rotate_down()

class Node:
    key = 0
    value = 0

    def __init__(self, key, value):
        self.key = key
        self.value = value