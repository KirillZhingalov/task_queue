import random
from task_queue import TaskQueue, Task, Resources  

def create_task(id, priority, ram, cpu, gpu):
    return Task(id, priority, Resources(ram, cpu, gpu), f"Task {id}", "")


class TestTaskQueue:

    def test_basic_functionality(self):
        queue = TaskQueue()
        queue.add_task(create_task(1, 5, 2, 2, 1))
        task = queue.get_task(Resources(3, 3, 2))
        assert task.id == 1

    def test_resource_limitations(self):
        queue = TaskQueue()
        queue.add_task(create_task(2, 10, 4, 4, 2))
        task = queue.get_task(Resources(3, 3, 1))
        assert task is None  # Task exceeds available resources

    def test_priority_handling(self):
        queue = TaskQueue()
        queue.add_task(create_task(3, 1, 1, 1, 1))
        queue.add_task(create_task(4, 10, 1, 1, 1))
        task = queue.get_task(Resources(2, 2, 1))
        assert task.id == 4  # Higher priority task should be chosen

    def test_empty_queue(self):
        queue = TaskQueue()
        task = queue.get_task(Resources(1, 1, 1))
        assert task is None  # No tasks in queue

    def test_multiple_resource_types(self):
        queue = TaskQueue()
        queue.add_task(create_task(5, 3, 2, 1, 0))
        queue.add_task(create_task(6, 4, 0, 2, 1))
        task = queue.get_task(Resources(2, 2, 1))
        assert task.id == 6  # Task 6 has higher priority and fits the resources

    def test_no_suitable_task_available(self):
        queue = TaskQueue()
        queue.add_task(create_task(7, 5, 5, 5, 5))
        queue.add_task(create_task(8, 6, 6, 6, 6))
        task = queue.get_task(Resources(4, 4, 4))
        assert task is None  # No task fits within the available resources

    def test_task_order_preservation(self):
        queue = TaskQueue()
        queue.add_task(create_task(9, 7, 1, 1, 1))
        queue.add_task(create_task(10, 7, 1, 1, 1))
        task1 = queue.get_task(Resources(2, 2, 2))
        task2 = queue.get_task(Resources(2, 2, 2))
        assert task1.id == 9 and task2.id == 10  # Tasks should be retrieved in the order they were added

    def test_all_tasks_retrieved(self):
        queue = TaskQueue()
        for i in range(11, 16):
            queue.add_task(create_task(i, i, 1, 1, 1))

        retrieved_tasks = set()
        for _ in range(5):
            task = queue.get_task(Resources(2, 2, 2))
            retrieved_tasks.add(task.id)

        assert retrieved_tasks == set(range(11, 16))  # All tasks should be retrieved

    def test_stress(self):
        queue = TaskQueue()
        for i in range(10000):
            queue.add_task(create_task(i, i % 10, 1, 1, 1))
        for _ in range(10000):
            task = queue.get_task(Resources(2, 2, 2))
            assert task is not None

    def test_large_scale_priority_handling(self):
        queue = TaskQueue()
        for i in range(10001, 20000):
            priority = random.randint(1, 100)
            queue.add_task(create_task(i, priority, 1, 1, 1))
        high_priority_task = create_task(20001, 101, 1, 1, 1)
        queue.add_task(high_priority_task)

        task = queue.get_task(Resources(2, 2, 2))
        assert task.id == 20001  # The high priority task should be retrieved first

    def test_repeated_resource_checks(self):
        queue = TaskQueue()
        for i in range(20002, 30000):
            queue.add_task(create_task(i, i % 100, 2, 2, 2))
        
        for _ in range(100):
            task = queue.get_task(Resources(1, 1, 1))
            assert task is None  # None of the tasks fit the limited resources

    def test_bulk_task_addition_and_retrieval(self):
        queue = TaskQueue()
        for i in range(30001, 40001):
            queue.add_task(create_task(i, random.randint(1, 100), 1, 1, 1))
        
        retrieved_tasks = 0
        while True:
            task = queue.get_task(Resources(2, 2, 2))
            if task is None:
                break
            retrieved_tasks += 1

        assert retrieved_tasks == 10000  # All tasks should be retrieved
