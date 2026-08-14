from triton.llm.ollama_interpreter import OllamaInterpreter

ollama = OllamaInterpreter()

response = ollama.ask("what is 2+2?")

print(response)