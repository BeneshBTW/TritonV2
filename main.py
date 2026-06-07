from triton.core.brain import Brain
from triton.core.reminder_engine import ReminderEngine
from triton.memory.reminder_store import ReminderStore

import threading
import time
import winsound

def reminder_loop(reminder_engine: ReminderEngine):
    while True:
        due_reminders = reminder_engine.check_due_reminders()

        for reminder_text in due_reminders:
            winsound.Beep(1000, 700)
            print(f"\n🔔 Reminder: {reminder_text}")

        time.sleep(5)


def main():
    brain = Brain()
    reminder_engine = ReminderEngine(ReminderStore())

    reminder_thread = threading.Thread(
        target=reminder_loop,
        args=(reminder_engine,),
        daemon=True
    )

    reminder_thread.start()

    print("Triton v2 online. Type 'exit' to shut down.")

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Triton: Shutting down.")
            break

        response = brain.process(user_input)
        print(f"Triton: {response.message}")


if __name__ == "__main__":
    main()