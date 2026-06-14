class TaskService:
    def __init__(self, task_store):
        self.task_store = task_store

    def get_tasks(self) -> list[dict]:
        return self.task_store.load()

    def add_task(self, title: str) -> dict:
        tasks = self.task_store.load()

        task = {
            "title": title,
            "completed": False
        }

        tasks.append(task)
        self.task_store.save(tasks)

        return task

    def get_incomplete_tasks(self) -> list[dict]:
        tasks = self.task_store.load()

        return [
            task for task in tasks
            if not task["completed"]
        ]

    def complete_task(self, task_number: int) -> dict | None:
        tasks = self.task_store.load()
        task_index = task_number - 1

        if task_index < 0 or task_index >= len(tasks):
            return None

        tasks[task_index]["completed"] = True
        self.task_store.save(tasks)

        return tasks[task_index]

    def remove_task(self, task_number: int) -> dict | None:
        tasks = self.task_store.load()
        task_index = task_number - 1

        if task_index < 0 or task_index >= len(tasks):
            return None

        removed_task = tasks.pop(task_index)
        self.task_store.save(tasks)

        return {
            "index": task_index,
            "task": removed_task
        }

    def restore_task(self, index: int, task: dict) -> None:
        tasks = self.task_store.load()

        tasks.insert(index, task)
        self.task_store.save(tasks)