from openai import OpenAI

DEEPSEEK_API_KEY = "sk-eee75b88a5114f58a151aab03ac9ab21"
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

def call_llm(prompt):
    response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个校园实验室安全分析助手，你将协助对实验安全分析报告进行评估，严格依据给定的标准对输入报告进行评估和判断。"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
    return response