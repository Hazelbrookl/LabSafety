import pandas as pd
from prompt_templates import generate_procedure_extract_prompt
from llm import call_llm

procedures_file_path = "data/procedure.xlsx"
reports = pd.read_excel(procedures_file_path, sheet_name=None)

for sheet_name, df in reports.items():
    experiment_name = df["实验名称"].dropna().tolist()[0]
    step_descriptions = df["步骤描述"].dropna().tolist()
    with open(f"output/procedure.txt", "w", encoding="utf-8") as f:
        for step_description in step_descriptions:
            prompt = generate_procedure_extract_prompt(experiment_name, step_description)
            response = call_llm(prompt)
            f.write(response.choices[0].message.content + "\n\n")



