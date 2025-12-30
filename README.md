# pvassistant
AI shell assistant, that works as a cli tool, and runs fully offline and locally.
 
<h3>Made for low-end machines</h3>
I have tried my best tuning it to make it usable and runnable on low end machines, without lobotomizing it too much, but even after that, it sometimes spits out nonsense. If you happen to do it better, feel free to suggest a better approach.

For the model, the current deepseek-coder-1.3b-instruct.Q4_K_M.gguf, works like a charm.
You can try experimenting with other quantized models, but you will need to change the prompt formating and parameters.

Working pyinstaller prompt: (Change the library path!)
```
pyinstaller --onefile --add-data "...\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\llama_cpp;llama_cpp/lib" --collect-all numpy --collect-all llama_cpp main.py
```
