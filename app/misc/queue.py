from collections import deque


class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, x):
        self.queue.appendleft(x)

    def dequeue(self):
        self.queue.pop()

    def isEmpty(self):
        return len(self.queue) == 0

    def front(self):
        return self.queue[-1]

    def rear(self):
        return self.queue[0]