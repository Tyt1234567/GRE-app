import tkinter as tk
import os
from datetime import datetime
from docx import Document

class Generate_result:
    def __init__(self, root,paper,v1_user,v1_cor,q1_user,q1_cor,v2_user,v2_cor,q2_user,q2_cor):
        self.root = root
        self.paper = paper
        self.v1_user = v1_user
        self.v1_cor = v1_cor
        self.q1_user = q1_user
        self.q1_cor = q1_cor
        self.v2_user = v2_user
        self.v2_cor = v2_cor
        self.q2_user = q2_user
        self.q2_cor = q2_cor

        self.root.title("results")
        self.root.screen_width = self.root.winfo_screenwidth()
        self.root.screen_height = self.root.winfo_screenheight()
        self.root.attributes('-fullscreen', True)
        self.calculate_scores()


    def calculate_scores(self):
        v1_correct = 0
        for i, user_choice in enumerate(self.v1_user):
            if user_choice == self.v1_cor[i]:
                v1_correct+=1

        v2_correct = 0
        for i, user_choice in enumerate(self.v2_user):
            if user_choice == self.v2_cor[i]:
                v2_correct += 1

        q1_correct = 0
        for i, user_choice in enumerate(self.q1_user):
            if self.paper.get(f'section3 题目{i+1} 类型（单选，多选，填空）') == '填空':
                try:
                    if eval(user_choice) == eval(self.q1_cor[i]):
                        q1_correct += 1
                except Exception:
                    pass
            else:
                if user_choice == self.q1_cor[i]:
                    q1_correct += 1

        q2_correct = 0
        for i, user_choice in enumerate(self.q2_user):
            if self.paper.get(f'section5 题目{i+1} 类型（单选，多选，填空）') == '填空':
                try:
                    if eval(user_choice) == eval(self.q1_cor[i]):
                        q2_correct += 1

                except Exception:
                    pass
            else:
                if user_choice == self.q2_cor[i]:
                    q2_correct += 1

        if v1_correct<=4:
            if v2_correct<=1:
                v_score = 130
            elif v2_correct==2:
                v_score = 134
            elif v2_correct==3:
                v_score = 136
            elif 4<=v2_correct<=5:
                v_score = 138
            elif 6<=v2_correct<=7:
                v_score = 140
            elif 8<=v2_correct<=9:
                v_score = 142
            elif 10<=v2_correct<=11:
                v_score = 144
            elif 12<=v2_correct<=13:
                v_score = 146
            elif 14<=v2_correct<=15:
                v_score = 150

        if 5 <= v1_correct <= 8:
            if v2_correct<=1:
                v_score = 138
            elif v2_correct==2:
                v_score = 140
            elif v2_correct==3:
                v_score = 142
            elif 4<=v2_correct<=5:
                v_score = 145
            elif 6<=v2_correct<=7:
                v_score = 152
            elif 8<=v2_correct<=9:
                v_score = 155
            elif 10<=v2_correct<=11:
                v_score = 157
            elif 12<=v2_correct<=13:
                v_score = 158
            elif 14<=v2_correct<=15:
                v_score = 160

        if 9 <= v1_correct <= 12:
            if v2_correct<=1:
                v_score = 152
            elif v2_correct==2:
                v_score = 153
            elif v2_correct==3:
                v_score = 154
            elif 4<=v2_correct<=5:
                v_score = 155
            elif 6<=v2_correct<=7:
                v_score = 158
            elif 8<=v2_correct<=9:
                v_score = 160
            elif 10<=v2_correct<=11:
                v_score = 162
            elif 12<=v2_correct<=13:
                v_score = 165
            elif 14<=v2_correct<=15:
                v_score = 170

        q_score = 143+q1_correct+q2_correct

        v = tk.Text(self.root, font=('Arial', 28), wrap='word',bg='#f0f0f0',
                                     borderwidth=0, highlightthickness=0)
        v.place(x=500, y=400)
        v.insert('1.0', f'Verbal Reasoning:{v_score}')
        v.config(state=tk.DISABLED)

        q = tk.Text(self.root, font=('Arial', 28), wrap='word',bg='#f0f0f0',
                    borderwidth=0, highlightthickness=0)
        q.place(x=500, y=600)
        q.insert('1.0', f'Quantitative Reasoning:{q_score}')
        q.config(state=tk.DISABLED)

        name = self.paper.get('name')
        time = datetime.now().strftime('%Y-%m-%d')
        file_path = rf'results/{name}/{time}/result.doc'
        if os.path.exists(file_path):
            os.remove(file_path)
        doc = Document()
        text_content = ''
        text_content += f'Verbal Reasoning:{v_score}'
        text_content += '\n'
        text_content += f'Quantitative Reasoning:{q_score}'
        text_content += '\n'
        text_content += '\n'
        for i,choice in enumerate(self.v1_user):
            if choice == self.v1_cor[i]:
                whether_true = 'True'
            else:
                whether_true = 'False'

            if 0<=i<=2 or 5<=i<=8:
                question_type = '填空'
            if 3<=i<=4 or 9<=i<=11:
                question_type = '阅读'
            line = f'V1第{i+1}题 题型{question_type} 您的答案：{choice} 正确答案{self.v1_cor[i]}  对错{whether_true}'
            text_content += line
            text_content += '\n'
        text_content += '\n'

        for i,choice in enumerate(self.v2_user):
            if choice == self.v2_cor[i]:
                whether_true = 'True'
            else:
                whether_true = 'False'

            if 0<=i<=3 or 9<=i<=11:
                question_type = '填空'
            if 4<=i<=8 or 12<=i<=14:
                question_type = '阅读'
            line = f'V2第{i+1}题 题型：{question_type} 您的答案：{choice} 正确答案{self.v2_cor[i]}  对错{whether_true}'
            text_content += line
            text_content += '\n'
        text_content += '\n'

        for i,choice in enumerate(self.q1_user):
            if choice == self.q1_cor[i]:
                whether_true = 'True'
            else:
                whether_true = 'False'
            line = f'Q1第{i+1}题 您的答案：{choice} 正确答案{self.q1_cor[i]}  对错{whether_true}'
            text_content += line
            text_content += '\n'
        text_content += '\n'

        for i,choice in enumerate(self.q2_user):
            if choice == self.q2_cor[i]:
                whether_true = 'True'
            else:
                whether_true = 'False'
            line = f'Q2第{i+1}题 您的答案：{choice} 正确答案{self.q2_cor[i]}  对错{whether_true}'
            text_content += line
            text_content += '\n'
        text_content += '\n'
        # 添加文本到文档
        doc.add_paragraph(text_content)
        # 保存文档
        doc.save(file_path)




