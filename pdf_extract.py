import pdfplumber
import re
import os
from prompt_templates import generate_risk_analyze_prompt, generate_pdf_analyze_prompt, generate_description_extract_prompt, generate_checkbox_extract_prompt, generate_step_analyze_prompt
from llm import call_llm
import json

# # PDF 文件所在目录
# dir_path = '一些专业的标准资料0301/2024年秋季学期-教师对电机系研究生安全分析报告的批改版本/selected'

# # 遍历目录下所有 PDF 文件
# for filename in os.listdir(dir_path):
#     if filename.lower().endswith('.pdf'):
#         pdf_path = os.path.join(dir_path, filename)
#         txt_filename = os.path.splitext(filename)[0] + '_pdfplumber.txt'
#         txt_path = os.path.join(dir_path, txt_filename)

#         with pdfplumber.open(pdf_path) as pdf, open(txt_path, 'w', encoding='utf-8') as txt_file:
#             content = ""
#             for page in pdf.pages:
#                 content += page.extract_text()
#                 # for pdf_table in page.extract_tables():
#                 #     table = []
#                 #     cells = []
#                 #     for row in pdf_table:
#                 #         if not any(row):
#                 #             if any(cells):
#                 #                 table.append(cells)
#                 #                 cells = []
#                 #         elif all(row):
#                 #             if any(cells):
#                 #                 table.append(cells)
#                 #                 cells = []
#                 #             table.append(row)
#                 #         else:
#                 #             if len(cells) == 0:
#                 #                 cells = row
#                 #             else:
#                 #                 for i in range(len(row)):
#                 #                     if row[i] is not None:
#                 #                         cells[i] = row[i] if cells[i] is None else cells[i] + row[i]
#                 #     for row in table:
#                 #         cleaned_row = [re.sub(r'\s+', '', cell) if cell is not None else '' for cell in row]
#                 #         txt_file.write(','.join(cleaned_row) + '\n')
#                 #     txt_file.write('----------judge----------\n')
            
#             prompt = generate_description_extract_prompt(content)
#             response = call_llm(prompt)
#             data = json.loads(response.choices[0].message.content.replace("```json", "").replace("```", "").strip())
#             for step in data['实验过程的风险分析']:
#                 prompt = generate_step_analyze_prompt(data['课题名称'], data['实验目标及过程简述'], step)
#                 response = call_llm(prompt)
#                 print(response.choices[0].message.content + "\n\n")
#             break
#             # txt_file.write(response.choices[0].message.content)

def extract_report_text(file):
    file.seek(0)  
    if file.name.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            content = ""
            for page in pdf.pages:
                content += page.extract_text()
    elif file.name.endswith('.txt'):
        content = file.read().decode('utf-8')
    return content
        
def extract_report_structure(file):   
    content = extract_report_text(file)
    prompt = generate_description_extract_prompt(content)
    response = call_llm(prompt)
    return response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
     
def extract_checkbox(file):
    content = extract_report_text(file)          
    prompt = generate_checkbox_extract_prompt(content)
    response = call_llm(prompt)
    return response.choices[0].message.content.replace("```json", "").replace("```", "").strip()

def step_risk_analyze(name, description, step):
    prompt = generate_step_analyze_prompt(name, description, step)
    response = call_llm(prompt)
    return response.choices[0].message.content.replace("```json", "").replace("```", "").strip()