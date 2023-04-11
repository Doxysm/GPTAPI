import tkinter as tk
from tkinter import ttk
import openai
import requests

api_key = "API KEY HERE"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",
}

def get_models():
    try:
        response = requests.get("https://api.openai.com/v1/engines", headers=headers)
        response.raise_for_status()
        return response.json()["data"]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

def send_query():
    prompt = input_text.get("1.0", tk.END).strip()

    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 50,
        "temperature": 0.5,
    }

    selected_model_id = [model['id'] for model in models if f"{model['id']} ({model.get('max_tokens', 'unknown')} tokens)" == model_var.get()][0]

    try:
        response = requests.post(
            f"https://api.openai.com/v1/engines/{selected_model_id}/completions",
            headers=headers,
            json=data,
        )
        response.raise_for_status()
        assistant_response = response.json()["choices"][0]["text"]
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, assistant_response.strip())
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def connect():
    global models
    global model_options

    models = get_models()
    model_options = [f"{model['id']} ({model.get('max_tokens', 'unknown')} tokens)" for model in models]

    if models:
        status_label.config(text="Connected", fg="green")
        model_dropdown.config(values=model_options)
        model_dropdown.current(0)
        send_button.config(state="normal")
    else:
        status_label.config(text="Not connected", fg="red")
        model_dropdown.config(values=["No models available"])
        model_dropdown.current(0)
        send_button.config(state="disabled")

root = tk.Tk()
root.title("Chat with GPT")

input_text = tk.Text(root, wrap="word", width=60, height=5)
input_text.pack(pady=(10, 5))

output_text = tk.Text(root, wrap="word", width=60, height=5, state="disabled")
output_text.pack(pady=(5, 10))

model_var = tk.StringVar()
model_dropdown = ttk.Combobox(root, textvariable=model_var, state="readonly")
model_dropdown.pack(pady=(0, 10))

status_label = tk.Label(root, text="Not connected", fg="red")
status_label.pack()

connect_button = tk.Button(root, text="Connect", command=connect)
connect_button.pack(pady=(0, 10))

send_button = tk.Button(root, text="Send", command=send_query, state="disabled")
send_button.pack()

root.mainloop()
