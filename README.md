 # pvassistant
AI shell assistant, that works as a cli tool, runs fully offline and locally.


https://github.com/user-attachments/assets/1ba7abae-0ee5-4337-9b1d-5060e25389dd


<h3>Made for low-end machines</h3>
I have tried my best tuning it to make it usable and runnable on low end machines (For example my intel i5 8350U with iGPU), without lobotomizing it too much, but even after that, it sometimes spits out nonsense. If you happen to do it better, feel free to suggest a better approach.

For the model, the current deepseek-coder-1.3b-instruct.Q4_K_M.gguf [link here]([url](https://huggingface.co/TheBloke/deepseek-coder-1.3b-instruct-GGUF/blob/main/deepseek-coder-1.3b-instruct.Q4_K_M.gguf)), works like a charm.
You can try experimenting with other quantized models, but you will need to change the prompt formating and parameters.

<h3>!!!NOT WORKING!!! Pyinstaller prompt: (Change the library path!)</h3>
```
pyinstaller --onefile --add-data "...\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\LocalCache\local-packages\Python311\site-packages\llama_cpp;llama_cpp/lib" --collect-all numpy --collect-all llama_cpp main.py
```
