from triton.core.intent import Intent
from triton.core.response import Response
from triton.skills.base_skill import BaseSkill


class TaskSkill(BaseSkill):
    def __init__(self, session, task_service):
        self.session = session
        self.task_service = task_service

    def can_handle(self, intent: Intent) -> bool:
        if intent.name == "undo_action":
            return self.session.last_undo_action == "restore_task"

        return intent.name in [
            "add_task",
            "show_tasks",
            "show_incomplete_tasks",
            "complete_task",
            "remove_task"
        ]

    def execute(self, intent: Intent) -> Response:
        tasks = self.task_service.get_tasks()

        if intent.name == "undo_action":
            if self.session.last_undo_action != "restore_task":
                return Response(
                    message="There is nothing to undo right now.",
                    success=False
                )

            task = self.session.last_undo_data["task"]
            index = self.session.last_undo_data["index"]

            self.task_service.restore_task(index, task)

            self.session.last_undo_action = None
            self.session.last_undo_data = None

            return Response(
                message=f"Restored task: {task['title']}",
                success=True
            )

        if intent.name == "add_task":
            task = self.task_service.add_task(intent.text)

            return Response(
                message=f"Task added: {task['title']}",
                success=True
            )
        
        if intent.name == "show_incomplete_tasks":
            incomplete_tasks = self.task_service.get_incomplete_tasks()

            if len(incomplete_tasks) == 0:
                return Response(
                    message="You do not have any incomplete tasks.",
                    success=True
                )
            
            task_text = "\n".join(
                f"{index + 1}. {task['title']}"
                for index, task in enumerate(incomplete_tasks)
            )

            return Response(
                message=f"You still need to do: \n{task_text}",
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

            completed_task = self.task_service.complete_task(int(intent.text))

            if completed_task is None:
                return Response(
                    message="That task number does not exist.",
                    success=False
                )

            return Response(
                message=f"Completed task: {completed_task['title']}",
                success=True
            )

        if intent.name == "remove_task":
            if not intent.text.isdigit():
                return Response(
                    message="Please tell me the task number to remove, like: remove task 1",
                    success=False
                )

            removed_data = self.task_service.remove_task(int(intent.text))

            if removed_data is None:
                return Response(
                    message="That task number does not exist.",
                    success=False
                )

            self.session.last_undo_action = "restore_task"
            self.session.last_undo_data = removed_data

            return Response(
                message=f"Removed task: {removed_data['task']['title']}",
                success=True
            )

        return Response(
            message="I do not know how to handle that task command.",
            success=False
        )