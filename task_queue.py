"""
Task description:
* Requires a task queue with priorities and resource limits.
* Each task has a priority and the required amount of resources to process it.
* Publishers create tasks with specified resource limits, and put them in a task queue.
* Consumer receives the highest priority task that satisfies available resources.
* The queue is expected to contain thousands of tasks.
* Write a unit test to demonstrate the operation of the queue.
"""
import heapq
from dataclasses import dataclass


@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int


@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: str
    result: str

    def __lt__(self, other):
        # This ensures that the task with higher priority is considered 'smaller'
        # in the context of a min heap.
        return self.priority > other.priority

class TaskQueue:
    """
    This class implements a priority queue using a min heap.
    The heap invariant is that the root node is the smallest element in the heap.
    
    __init__(): Initializes the heap.
    add_task(): Adds a task to the heap.
    get_task(): Gets the task with the highest priority that fits the available resources.
    """
    
    def __init__(self):
        """
        Heap initialization.
        """
        self.tasks = []

    def add_task(self, task: Task):
        """
        Adds a task to the heap.

        Args:
            task (Task): The task to be added to the heap.
        """

        heapq.heappush(self.tasks, task)

    def get_task(self, available_resources: Resources) -> Task:
        """
        Gets the task with the highest priority that fits the available resources.

        Args:
            available_resources (Resources): The available resources.

        Returns:
            Task: The task with the highest priority that fits the available resources.
        """
        
        temp = []
        while self.tasks:
            task = heapq.heappop(self.tasks)
            if (task.resources.ram <= available_resources.ram and
                task.resources.cpu_cores <= available_resources.cpu_cores and
                task.resources.gpu_count <= available_resources.gpu_count):
                for item in temp:
                    heapq.heappush(self.tasks, item)
                return task
            else:
                temp.append(task)
        for item in temp:
            heapq.heappush(self.tasks, item)
        return None  # No task fits within the available resources