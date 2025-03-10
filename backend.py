from fastapi import FastAPI, File, UploadFile, Form, Depends,HTTPException
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
    The user wants: "{user_message}".

    ### Constraints:
    - The code **must use pandas (`pd`)** for reading the CSV data.
    - The CSV data is stored in a variable called **`csv_data`** (already provided).
    - The code **must store the final result in a variable named `output`**.
    - **Do not use `print()` statements**; only store the result in `output`.
    - If the operation results in a DataFrame, Series, or NumPy array, convert it to a **string format** before assigning it to `output`.

    ### Example:
    If the user wants "Calculate the sum of a column named 'Sales'", your code should be:
    ```python
    import pandas as pd
    from io import StringIO

    df = pd.read_csv(StringIO(csv_data))
    output = df['Sales'].sum()
    ```

    Ensure your response **only contains the Python code** without explanations.
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
async def upload_file(file: UploadFile = File(...),user_message: str = Form(...)):
    
    if not file.filename.endswith(".csv") or file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV files are allowed!")
    
    file_content = await file.read()
    file_content_str = file_content.decode("utf-8")
    
    ai_interpreter = AIInterpreter(OPENAI_API_KEY)
    code_executor = CodeExecutor()
    
    generated_code = ai_interpreter.generate_code(file_content_str, user_message)
    result = code_executor.execute_code(generated_code, file_content_str)
    
    return {"generated_code": generated_code, "result": result}
@app.get("/")
def root():
    return {"message": "Chat Code-Interpreter API is running!"}
