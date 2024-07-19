from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify, json
import pandas as pd
import os
from werkzeug.utils import secure_filename
from ai_match import *
import shutil
import requests
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import os
from ai_match import generate_ai_answer, compare_ask
from nltk.translate.bleu_score import sentence_bleu
from nltk.tokenize import word_tokenize



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'

# 用于存储进度的全局变量
progress = 0
total_questions = 0

# 主页
@app.route('/')
def index():
    tables = []
    history_path = 'data/history.csv'
    if os.path.exists(history_path):
        df = pd.read_csv(history_path)
        tables.append(df.to_html(classes='table table-bordered'))
    return render_template('index.html', tables=tables)





# 上传页面
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            #filename = secure_filename(file.filename)
            filename = "history.csv"
            source_file=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(source_file)
            destination_file = os.path.join('data', filename)
            shutil.copy2(source_file, destination_file)
            flash('文件上传成功！', 'success')
            return redirect(url_for('process_file', filename=filename))
        else:
            flash('请上传有效的 CSV 文件', 'danger')
    return render_template('upload.html')

# 处理文件
@app.route('/process/<filename>', methods=['GET', 'POST'])
def process_file(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    df = pd.read_csv(filepath)

    # 打印列名
    print(df.columns.tolist())
    
    
    # 模拟生成 AI 知识回答原文
    #df['AI知识回答原文'] = df['问题'].apply(lambda question: generate_ai_answer(question)[0])
    
    # 模拟比较结果
    df['Result'] = df.apply(lambda row: compare_answers(row['答案'], row['AI知识回答原文']), axis=1)

    # 保存历史记录
    history_path = 'data/history.csv'
    if os.path.exists(history_path):
        history_df = pd.read_csv(history_path)
        #history_df = pd.concat([history_df, df], ignore_index=True)
    else:
        history_df = df
    history_df.to_csv(history_path, index=False)

    return redirect(url_for('index'))

# 更新记录
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    history_path = 'data/history.csv'
    df = pd.read_csv(history_path)
    data = request.json
    df.loc[id, '问题'] = data['question']
    df.loc[id, '答案'] = data['standard_answer']
    df.loc[id, 'AI知识回答原文'] = data['aigc_answer']
    df.loc[id, '结果'] = data['result']
    df.to_csv(history_path, index=False)
    print("send_file(history_path, as_attachment=True)")
    row=df.loc[id].to_dict()
    row['success']=True
    for key,value in row.items():
        if str(value)=='nan':
            row[key]=" "
    return jsonify(row)

# 查看历史记录
@app.route('/history')
def history():
    history_path = 'data/history.csv'
    df = pd.read_csv(history_path)
    return render_template('history.html', df=df)

# 删除记录
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    history_path = 'data/history.csv'
    df = pd.read_csv(history_path)
    df = df.drop(id)
    df.to_csv(history_path, index=False)
    return jsonify(success=True)

# 导出数据
@app.route('/export')
def export():
    history_path = 'data/history.csv'
    df = pd.read_csv(history_path)
    export_df = df[['问题', '答案', 'AI知识回答原文', '结果']]
    export_path = 'data/export.csv'
    export_df.to_csv(export_path, index=False)
    return send_file(export_path, as_attachment=True)

#ai获取答案aigc
@app.route('/generate_ai_answer', methods=['POST'])
def generate_ai_answer_route():
    try:
        question = request.json.get('question')
        ai_answer, confidence = generate_ai_answer(question)
        return jsonify({'ai_answer': ai_answer, 'confidence': confidence})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

#人工标注列（包含三种情况）
"""
@app.route('/update_annotation/<int:index>', methods=['POST'])
def update_annotation(index):
    data = request.json
    annotation = data['annotation']
    history_path = 'data/history.csv'
    if os.path.exists(history_path):
        df = pd.read_csv(history_path)
        if index < len(df):
            df.at[index, '人工标注'] = annotation
            df.to_csv(history_path, index=False)
            return jsonify(success=True)
        else:
            return jsonify(success=False, message="Index out of bounds")
    return jsonify(success=False, message="File not found")
"""

#AI获取对比答案/api调用
@app.route('/get_AI_result', methods=['POST'])
def get_AI_result():
    data = request.json
    standard = data['standard']
    ai_answer = data['ai_answer']
    result=compare_ask(standard,ai_answer) 
    score = str(compare_score(standard,ai_answer))
    print(score)
    data={
        'result':result,
        'score':score
    }
    return jsonify(data)

# 比较答案函数
def compare_answers(standard_answer, aigc_answer):
    return '通过' if standard_answer == aigc_answer else '未通过'

@app.route('/progress', methods=['GET'])
def get_progress():
    return jsonify(progress=progress)
 
if __name__ == '__main__':
    app.run(debug=True,)
    
