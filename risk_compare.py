import pandas as pd
from prompt_templates import generate_risk_compare_prompt
from llm import call_llm

reports_file_path = "data/reports.xlsx"
reports = pd.read_excel(reports_file_path, sheet_name=None)
hazards_file_path = "data/hazards.xlsx"
hazards = pd.read_excel(hazards_file_path, sheet_name=None, dtype=str)
standards_file_path = "data/standards.xlsx"
standards = pd.read_excel(standards_file_path, sheet_name=None)

_, hazards_standard = list(standards.items())[0]
_, precautions_standard = list(standards.items())[1]
_, wastes_standard = list(standards.items())[2]

for (report_sheet, report_df), (hazard_sheet, hazard_df) in zip(reports.items(), hazards.items()):
    experiment_name = report_df["实验名称"].dropna().tolist()[0]
    step_names = report_df["简要实验步骤及具体的实验条件"].dropna().tolist()
    step_hazards = report_df["识别实验危险源"].dropna().tolist()
    step_evaluations = report_df["风险评估"].dropna().tolist()
    step_precautions = report_df["风险最小化措施"].dropna().tolist()
    step_reactions = report_df["应急处理"].dropna().tolist()
    physical_hazards = hazard_df["物理性"].fillna("").tolist()
    chemical_hazards = hazard_df["化学性"].fillna("").tolist()
    biological_hazards = hazard_df["生物性"].fillna("").tolist()
    environmental_hazards = hazard_df["环境"].fillna("").tolist()
    psychological_hazards = hazard_df["心理"].fillna("").tolist()
    behavioral_hazards = hazard_df["行为"].fillna("").tolist()
    hazards_descriptions = []
    for physical, chemical, biological, environmental, psychological, behavioral in zip(physical_hazards, chemical_hazards, biological_hazards, environmental_hazards, psychological_hazards, behavioral_hazards):
        hazards_description = ""
        for index in physical.split("#"):
            if index != "":
                hazards_description += hazards_standard["物理性"].tolist()[int(index)-1] + "\n"
        for index in chemical.split("#"):
            if index != "":
                hazards_description += hazards_standard["化学性"].tolist()[int(index)-1] + "\n"
        for index in biological.split("#"):
            if index != "":
                hazards_description += hazards_standard["生物性"].tolist()[int(index)-1] + "\n"
        for index in environmental.split("#"):
            if index != "":
                hazards_description += hazards_standard["环境"].tolist()[int(index)-1] + "\n"
        for index in psychological.split("#"):
            if index != "":
                hazards_description += hazards_standard["心理"].tolist()[int(index)-1] + "\n"
        for index in behavioral.split("#"):
            if index != "":
                hazards_description += hazards_standard["行为"].tolist()[int(index)-1] + "\n"
        hazards_descriptions.append(hazards_description)
    
    input_descriptions = [
    f"""\
简要实验步骤及具体的实验条件: {step}\n\
识别实验危险源: {hazard}\n\
风险评估: {evaluation}\n\
风险最小化措施: {precaution}\n\
应急处理: {reaction}\n\
可能风险源: \n\
{hazards_description}"""
    for step, hazard, evaluation, precaution, reaction, hazards_description in zip(
        step_names, step_hazards, step_evaluations, step_precautions, step_reactions, hazards_descriptions
    )
    ]
    with open(f"output/analysis_{report_sheet}.txt", "w", encoding="utf-8") as f:
        for input_description in input_descriptions:
            prompt = generate_risk_compare_prompt(experiment_name, input_description)
            response = call_llm(prompt)
            f.write(response.choices[0].message.content + "\n\n")