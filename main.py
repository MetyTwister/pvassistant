from llama_cpp import Llama
import typer
import subprocess
import os
import contextlib
import sys

app = typer.Typer()

@app.command()

def say(message: list[str]):

    if getattr(sys, 'frozen', False): #Construction of absolute path to the model. Is file .exe or .py?
        BASE_DIR = os.path.dirname(sys.executable)
    else:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    model_path = os.path.join(BASE_DIR, "models", "deepseek-coder-1.3b-instruct.Q4_K_M.gguf")

    @contextlib.contextmanager #Clean the output from errors and stats -> stderr will get thrown away.
    def suppress_stderr():
        with open(os.devnull, "w") as devnull:
            old_stderr = sys.stderr
            sys.stderr = devnull
            try:
                yield
            finally:
                sys.stderr = old_stderr

    with suppress_stderr(): #Inicialization of Llama
        llm = Llama(
            model_path=model_path,
            n_ctx=1024,
            n_threads=4,
            log_level="ERROR"
        )

    system = ( #Prompt formatting
    "You are a terse Linux shell assistant. "
    "Output ONLY the raw command. NOTHING else. "
    "Do NOT give examles."
    "Do NOT add punctuation before the command."
    "Make the output only ONE sentence."
    )

    prompt = f"<|system|>{system}<|user|>{' '.join(message)}<|assistant|>"

    with suppress_stderr(): #Prompt parameters
        output = llm(
            prompt,
            max_tokens=100,
            temperature=0.2,
            top_p=0.8,
            repeat_penalty=1.2,
            stop=["<|user|>", "<|system|>", "\n\n"] #<-- This need tuning!!! (Sometimes the respose hides after <system>!!)
        )

    print("💬", output["choices"][0]["text"].strip()) #Cleans and prints output

if __name__ == "__main__":

    app()
