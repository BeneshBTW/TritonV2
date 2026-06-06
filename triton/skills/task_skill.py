from triton.core.intent import Intent
from triton.core.response import Response
from triton.skills.base_skill import BaseSkill


class TaskSkill(BaseSkill):
    def __init__(self, session, task_store):
        self.session = session
        self.task_store = task_store

    def can_handle(self, intent: Intent) -> bool:
        if intent.name == "undo_action":
            return self.session.last_undo_action == "restore_task"

        return intent.name in [
            "add_task",
            "show_tasks",
            "complete_task",
            "remove_task"
        ]

    def execute(self, intent: Intent) -> Response:
        tasks = self.task_store.load()

        if intent.name == "undo_action":
            if self.session.last_undo_action != "restore_task":
                return Response(
                    message= "There is nothing to undo right now.",
                    success=False
                )
            
            task = self.session.last_undo_data["task"]
            index = self.session.last_undo_data["index"]

            tasks.insert(index, task)
            self.task_store.save(tasks)

            self.session.last_undo_action = None
            self.session.last_undo_data = None

            return Response(
                message=f"Restored Task: {task['title']}",
                success=True
            )

        if intent.name == "add_task":
            task = {
                "title": intent.text,
                "completed": False
            }

            tasks.append(task)
            self.task_store.save(tasks)

            return Response(
                message=f"Task added: {intent.text}",
                success=True
            )

        if intent.name == "show_tasks":
            if len(tasks) == 0:
                return Response(
                    message="You do not have any tasks yet.",
                    success=True
                )

            task_text = "\n".join(
                f"{index + 1}. {'[x]' if task['completed'] else '[ ]'} {task['title']}"
                for index, task in enumerate(tasks)
            )

            return Response(
                message=f"Here are your tasks:\n{task_text}",
                success=True
            )

        if intent.name == "complete_task":
            if not intent.text.isdigit():
                return Response(
                    message="Please tell me the task number to complete, like: complete task 1",
                    success=False
                )

            task_index = int(intent.text) - 1

            if task_index < 0 or task_index >= len(tasks):
                return Response(
                    message="That task number does not exist.",
                    success=False
                )

            tasks[task_index]["completed"] = True
            self.task_store.save(tasks)

            return Response(
                message=f"Completed task: {tasks[task_index]['title']}",
                success=True
            )

        if intent.name == "remove_task":
            if not intent.text.isdigit():
                return Response(
                    message="Please tell me the task number to remove, like: remove task 1",
                    success=False
                )

            task_index = int(intent.text) - 1

            if task_index < 0 or task_index >= len(tasks):
                return Response(
                    message="That task number does not exist.",
                    success=False
                )

            removed_task = tasks.pop(task_index)

            self.session.last_undo_action = "restore_task"
            self.session.last_undo_data = {
                "index" :  task_index,
                "task" : removed_task
            }

            self.task_store.save(tasks)

            return Response(
                message=f"Removed task: {removed_task['title']}",
                success=True
            )

        return Response(
            message="I do not know how to handle that task command.",
            success=False
        )