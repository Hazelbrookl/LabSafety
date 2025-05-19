import pandas as pd
from prompt_templates import generate_risk_analyze_prompt
from llm import call_llm

reports_file_path = "data/reports.xlsx"
reports = pd.read_excel(reports_file_path, sheet_name=None)

for sheet_name, df in reports.items():
    experiment_name = df["实验名称"].dropna().tolist()[0]
    experiment_description = df["实验目标及过程简述"].dropna().tolist()[0]
    step_names = df["简要实验步骤及具体的实验条件"].dropna().tolist()
    step_hazards = df["识别实验危险源"].dropna().tolist()
    step_evaluations = df["风险评估"].dropna().tolist()
    step_precautions = df["风险最小化措施"].dropna().tolist()
    step_reactions = df["应急处理"].dropna().tolist()
    step_descriptions = [
    f"""\
简要实验步骤及具体的实验条件: {step}\n\
识别实验危险源: {hazard}\n\
风险评估: {evaluation}\n\
风险最小化措施: {precaution}\n\
应急处理: {reaction}"""
    for step, hazard, evaluation, precaution, reaction in zip(
        step_names, step_hazards, step_evaluations, step_precautions, step_reactions
    )
    ]
    with open(f"output/hazards_{sheet_name}.txt", "w", encoding="utf-8") as f:
        for step_description in step_descriptions:
            prompt = generate_risk_analyze_prompt(experiment_name, experiment_description, step_description)
            response = call_llm(prompt)
            f.write(response.choices[0].message.content + "\n\n")