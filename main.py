from llama_cpp import Llama
import typer
import subprocess
import os
import contextlib
import sys

app = typer.Typer()

@app.command()

def say(message: list[str]):

    os.environ["LLAMA_LOG_LEVEL"] = "ERROR"

    @contextlib.contextmanager
    def suppress_stderr():
        with open(os.devnull, "w") as devnull:
            old_stderr = sys.stderr
            sys.stderr = devnull
            try:
                yield
            finally:
                sys.stderr = old_stderr

    with suppress_stderr():
        llm = Llama(
            model_path="models/deepseek-coder-1.3b-instruct.Q4_K_M.gguf",
            n_ctx=1024,
            n_threads=4
        )

    system = (
    "You are a terse Linux shell assistant. "
    "Output ONLY the raw command. NOTHING else. "
    "Do NOT start with words, explanations, or labels. "
    "Do not add punctuation before the command."
    "Make the output only ONE sentence."
    )

    prompt = f"<|system|>{system}<|user|>{' '.join(message)}<|assistant|>"

    with suppress_stderr():
        output = llm(
            prompt,
            max_tokens=100,
            temperature=0.2,
            top_p=0.8,
            repeat_penalty=1.2,
            stop=["<|user|>", "<|system|>", "\n\n"] #<-- Tohle chce doladit!!! (často se odpověd skryje za <system>!!)
        )

    print("💬", output["choices"][0]["text"].strip())

if __name__ == "__main__":
    app()