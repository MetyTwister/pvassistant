from llama_cpp import Llama
import typer
import subprocess
import os
import contextlib
import sys
import time
import threading

def loader(stop_event):
    frames =  [
			"( ●    )",
			"(  ●   )",
			"(   ●  )",
			"(    ● )",
			"(     ●)",
			"(    ● )",
			"(   ●  )",
			"(  ●   )",
			"( ●    )",
			"(●     )"
		]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write("\r⚙ Thinking " + frames[i % len(frames)])
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    sys.stdout.write("\r" + " " * 40 + "\r")

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

    result_holder = {}
    stop = threading.Event()

    def run_llm():
        with suppress_stderr(): #Prompt parameters
            result_holder["out"] = llm(
                prompt,
                max_tokens=100,
                temperature=0.2,
                top_p=0.8,
                repeat_penalty=1.2,
                stop=["<|user|>", "<|system|>", "\n\n"] #<-- This need tuning!!! (Sometimes the respose hides after <system>!!)
            )
            stop.set()

    worker = threading.Thread(target=run_llm)
    worker.start()

    loader(stop)
    worker.join()

    out = result_holder["out"]["choices"][0]["text"].strip()

    print("💬", out)
    #print("💬", output["choices"][0]["text"].strip()) #Cleans and prints output

if __name__ == "__main__":

    app()
