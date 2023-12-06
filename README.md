# Task Queue with Priorities and Resource Limits

This is a Python implementation of a task queue with priorities and resource limits. The task queue allows publishers to create tasks with specified resource limits and put them in the queue. The consumer then receives the highest priority task that satisfies the available resources.

## Features

- Each task has a priority and the required amount of resources to process it.
- The queue is implemented using a min heap, ensuring that the task with the highest priority is always at the top.
- The queue can handle thousands of tasks efficiently.
- The task queue is designed to be used in a multi-threaded environment.

## Usage

To use the task queue, follow these steps:

1. Import the necessary classes from the `task_queue` module:

    ```
    from task_queue import TaskQueue, Task, Resources
    ```
2. Create a task queue object:

    ```
    task_queue = TaskQueue()
    ```

3. Create a task object with the required resources and priority:

    ```
    task1 = Task(id=1, priority=1, resources=Resources(ram=4, cpu_cores=2, gpu_count=1), content="Task 1", result="")
    task2 = Task(id=2, priority=2, resources=Resources(ram=8, cpu_cores=4, gpu_count=2), content="Task 2", result="")
    ```

    The get_task() method returns None if there are no tasks in the queue or if no task fits the available resources.

## Unit Test
A unit test is provided in the test_task_queue.py file to demonstrate the operation of the task queue. You can run the test using pytest framework:

```
pytest test_task_queue.py
```
