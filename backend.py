from fastapi import FastAPI, File, UploadFile, Form, BackgroundTasks, Depends
import openai
import pandas as pd
import os

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

class AIInterpreter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_code(self, file_content: str, user_message: str) -> str:
        prompt = f"""
        You are a Python expert. Write a Python script to analyze the following CSV data:
        ```
        {file_content[:1000]}
        ```
        The user wants: "{user_message}". Ensure the code reads the CSV data and performs the requested action.
        Output results using print(). Use pandas, numpy, and matplotlib if needed.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=[{"role": "system", "content": "You are a helpful AI assistant."},
                      {"role": "user", "content": prompt}]
        )
        
        return response["choices"][0]["message"]["content"].strip()

class CodeExecutor:
   
    @staticmethod
    def execute_code(code: str, file_content: str) -> str:
        local_scope = {}
        try:
            exec(code, {"pd": pd, "csv_data": file_content}, local_scope)
            return local_scope.get("output", "Execution completed successfully, but no output was captured.")
        except Exception as e:
            return str(e)

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    user_message: str = Form(...),
    ai_interpreter: AIInterpreter = Depends(lambda: AIInterpreter(OPENAI_API_KEY)),
    code_executor: CodeExecutor = Depends(CodeExecutor)
):
    file_content = await file.read()
    file_content_str = file_content.decode("utf-8")
    
    generated_code = ai_interpreter.generate_code(file_content_str, user_message)
    result = code_executor.execute_code(generated_code, file_content_str)
    
    return {"generated_code": generated_code, "result": result}

@app.get("/")
def root():
    return {"message": "Chat Code-Interpreter API is running!"}
