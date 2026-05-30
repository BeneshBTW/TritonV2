from triton.core.brain import Brain


def main():
    brain = Brain()

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