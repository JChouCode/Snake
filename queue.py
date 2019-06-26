from collections import deque


class Queue:
    def __init__(self):
        self.items = deque()

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.popleft()

    def peek(self):
        return self.items[0]
