import chainlit as cl
import requests
import io

BACKEND_URL = "http://localhost:8000/upload/"

@cl.on_message
async def handle_message(message: cl.Message):
    if not message.files:
        await cl.Message(content="Please upload a CSV file.").send()
        return

    file = message.files[0]  # Handling the first uploaded file
    user_message = message.content

    # Convert file content to bytes
    file_bytes = io.BytesIO(file.content)

    # Prepare the file and user message for backend request
    files = {"file": (file.name, file_bytes, file.mime)}
    data = {"user_message": user_message}

    response = requests.post(BACKEND_URL, files=files, data=data)

    if response.status_code == 200:
        result = response.json()
        await cl.Message(content=f"**Generated Code:**\n```python\n{result['generated_code']}\n```").send()
        await cl.Message(content=f"**Execution Result:**\n{result['result']}").send()
    else:
        await cl.Message(content="Error processing the file. Please try again.").send()

cl.run(name="Chat Code Interpreter")
