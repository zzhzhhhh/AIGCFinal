import pandas as pd
from openai import OpenAI
import requests
from bert_score import score

# 设置 API 密钥
api_key = "sk-2baf614283014a79ae289505d7798d07"
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


#HARDCODED_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJsb2dpblR5cGUiOiJsb2dpbiIsImxvZ2luSWQiOjEsInJuU3RyIjoiRWVsSHRhUUdabkwzaXlEc3RTN2QxMmFzaXowYVE3Z3kiLCJ0ZW5hbnRJZCI6MSwiZW1wbG95ZWVOdW1iZXIiOiIwMDEiLCJkZXB0SWQiOjEsImxvZ2luTmFtZSI6ImFkbWluIiwidXNlck5hbWUiOiLlkJHlt40iLCJ1c2VyUGhvbmUiOiIxODgxMDY1MTkwMSIsImRhdGFTcGFjZSI6NSwiaXNSb290IjoxLCJjdXN0b21EYXRhIjoiMywyLDEiLCJkZXB0Q2hpbGRzIjoiMyJ9.2tZNn__ohRJoVYUYDB39MXXijR3ggGe4udi9ev2kSv4"

 
def get_user_token():
    url = "https://ai-know-test.cscec3b-iti.com/api/auth/loginByAccount"
    headers = {'Content-Type': 'application/json'}
    data = {
        "loginName": "admin",
       "userPwd": "79b13034248e75a431248e6386a96a59"
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # 这将为HTTP错误抛出异常
        return response.json().get('userToken', None)
    except requests.RequestException as e:
        print(f"登录失败: {e}")
        print("响应文本:", response.text)
        return None

user_token = get_user_token()
print("User Token:", user_token)

 
def generate_ai_answer(question):
    url = 'https://ai-know-test.cscec3b-iti.com/answers'
    data = {'question': question}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {user_token}'
    }
    try:
        response = requests.post(url, json=data, headers=headers, verify= False)
        response.raise_for_status()
        response_data = response.json()
        ai_answer = response_data.get('answer', 'No answer found')
        confidence = response_data.get('confidence', 0)
        print("AI Answer:", ai_answer)  # 调试信息
    except requests.RequestException as e:
        print(f"Error: {e}")  # 打印错误信息
        ai_answer = 'Error fetching answer'
        confidence = 0
    return ai_answer, confidence




def compare_ask(e_col,k_col): 
    prompt = f"""
    请你判断以下AI的答案是否满足标准答案，并根据判断结果标注"通过"、"不通过"或"不确定"。
    ### 标准答案：
    标准答案是：{e_col}
    ### AI的答案：
    AI的答案是：{k_col}
    ### 判断标准：
    1. 如果 AI 的答案与标准答案在意义上完全相同，则标注为"通过"。
    2. 如果 AI 的答案与标准答案在意义上完全不同，则标注为"不通过"。但是如果标准答案未给出，需要标注为“不确定”。
    3. 如果 AI 的答案与标准答案在意义上部分相同，但不完全一致，则标注为"不确定"。
    你只需要回答"通过"、"不通过"或"不确定"中的一个选项。不需要给出推导过程。
    ### 判断结果：
    """  
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
        {"role": "system", "content": prompt}
        ],
        stream=False
    )
    result=response.choices[0].message.content
    print(result,len(e_col),len(k_col))
    return result

def compare_score(standard,ai_answer):
    # 确保BERT模型只被加载一次，例如使用before_first_request或类似机制
    P, R, F1 = score([ai_answer], [standard], lang="en", model_type="bert-base-uncased")
    # 转换F1得分为百分比
    confidence = (F1.mean().item() * 100)  # 将得分转换为百分比形式
    return int(confidence)