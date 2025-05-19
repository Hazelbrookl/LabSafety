import streamlit as st
import pandas as pd
import json
from pdf_extract import extract_report_structure, step_risk_analyze, extract_checkbox
import concurrent.futures

def call_back_analyzeHazard(name, description, steps):
    results = [None] * len(steps)  # 预分配列表
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交所有任务，并记录它们的 index
        future_to_index = {
            executor.submit(step_risk_analyze, name, description, step): i
            for i, step in enumerate(steps)
        }
        # 按完成顺序获取结果，但按原始 index 存放
        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            results[index] = future.result()
    st.session_state.hazard_analysis = results


if __name__ == "__main__":

    st.set_page_config(
        page_title="Report Analysis",
        page_icon="",
        layout="wide",
    )

    if "hazard_analysis" not in st.session_state:
        st.session_state.hazard_analysis = None

    st.markdown('<h1 style="color: #5c307d;">实验安全报告分析</h1>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("选择一个文件", type=["pdf", "txt"])

    if uploaded_file is not None:
        file_content = json.loads(extract_report_structure(uploaded_file))
        df_step = pd.DataFrame(file_content['实验过程的风险分析'])
        df_step.index += 1
        checkbox = json.loads(extract_checkbox(uploaded_file))
        df_hazards = pd.DataFrame({
            "危险因素类别": list(checkbox['危险和有害因素'].keys()),
            "具体危险因素": [", ".join(items) if items else "无" for items in checkbox['危险和有害因素'].values()]
        })
        df_hazards.index += 1
        df_measures = pd.DataFrame({
            "防护措施类别": list(checkbox['基本防护要求'].keys()),
            "具体防护措施": [", ".join(items) if items else "无" for items in checkbox['基本防护要求'].values()]
        })
        df_measures.index += 1

        st.markdown("**课题名称**")
        st.markdown(file_content['课题名称'])
        st.markdown("**实验目标及过程简述**")
        st.markdown(file_content['实验目标及过程简述'])
        st.markdown("**实验过程的风险分析：**")
        st.table(df_step)
        st.markdown("**风险因素：**")
        st.table(df_hazards)
        st.table(df_measures)

        st.button("风险源分析", on_click=lambda: call_back_analyzeHazard(file_content['课题名称'], file_content['实验目标及过程简述'], file_content['实验过程的风险分析']))

        if st.session_state.hazard_analysis is not None:
            st.markdown("**分析结果：**")
            for index, result in enumerate(st.session_state.hazard_analysis):
                st.markdown("**实验步骤：**")
                st.table(df_step.loc[index + 1])
                r = json.loads(result)
                st.markdown("**风险因素分析：**")
                df_hazards_result = pd.DataFrame({
                    "危险因素类别": list(r['危险和有害因素'].keys()),
                    "具体危险因素": [", ".join(items) if items else "无" for items in r['危险和有害因素'].values()]
                })
                df_hazards_result.index += 1
                st.table(df_hazards_result)
                st.markdown("**防护措施分析：**")
                df_measures_result = pd.DataFrame({
                    "防护措施类别": list(r['基本防护要求'].keys()),
                    "具体防护措施": [", ".join(items) if items else "无" for items in r['基本防护要求'].values()]
                })
                df_measures_result.index += 1
                st.table(df_measures_result)
                st.markdown("**反馈意见：**")
                st.markdown(r['反馈意见'])