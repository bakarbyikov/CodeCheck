from fastapi import FastAPI

app = FastAPI()


@app.get("/generate_problem")
def generate_problem(text: str):
    print(f"{text = }")
    return {
        "solution": 'print("Hello World!")',
        "tests": [
            ('1,2,3', '1'),
            ('2,3,4', '2')
        ]
    }

