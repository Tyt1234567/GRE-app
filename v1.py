import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font
import q1
from tkinter import messagebox

class V1:
    def __init__(self, root, paper):
        self.root = root
        self.paper = paper
        self.root.title("section 2")
        self.root.screen_width = self.root.winfo_screenwidth()
        self.root.screen_height = self.root.winfo_screenheight()
        self.root.attributes('-fullscreen', True)

        # 用于阅读的背景
        self.image1 = Image.open('bg_img.png')
        self.image1 = self.image1.resize((self.root.screen_width, self.root.screen_height), Image.LANCZOS)
        self.bg_img1 = ImageTk.PhotoImage(self.image1)  # 保持引用防止被垃圾回收

        # 用于填空的背景
        self.image2 = Image.open('bg_img2.png')
        self.image2 = self.image2.resize((self.root.screen_width, self.root.screen_height), Image.LANCZOS)
        self.bg_img2 = ImageTk.PhotoImage(self.image2)  # 保持引用防止被垃圾回收

        self.current_page_index = 0
        self.pages = []

        self.v1_user_choice=['none']*12
        self.v1_answer_choice=['none']*12

        self.create_pages()

        # 添加倒计时
        # 初始化时间
        self.time_left = 18*60  # 18分钟的秒数
        # 创建标签显示剩余时间
        self.time_label = tk.Label(self.root, text=self.format_time(self.time_left), font=("Helvetica", 14), bg="#F0E1E4")
        #self.time_label.place(relx=0.937317, rely=0.072917, relwidth=0.029291, relheight=0.020833)
        self.time_label.place(relx = 0.93, rely = 0.073, relwidth = 0.03, relheight = 0.022)
        self.change_page_buttons = []
        self.create_navigation_buttons()


        # 启动倒计时
        self.update_timer()
        self.display_page(self.current_page_index)

    def create_navigation_buttons(self):
        for index in range(len(self.pages)):
            change_page_button = tk.Button(self.root, text=str(index + 1), bg='red',
                                           command=lambda idx=index: self.change_page(idx))
            change_page_button.place(relx=0.146456 + 0.0293 * index, rely=0.016667, relwidth=0.023433, relheight=0.041667)
            self.change_page_buttons.append(change_page_button)

    def create_one_choice_pages(self,i,question,choices):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.root.screen_width, height=self.root.screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg_img2, anchor='nw')

        # 添加按钮
        back_button = tk.Button(page_frame, text="Back", command=self.go_back)
        back_button.place(relx=0.879, rely=0.021, relwidth=0.03, relheight=0.03)
        next_button = tk.Button(page_frame, text="Next", command=self.go_next)
        next_button.place(relx=0.937, rely=0.021, relwidth=0.03, relheight=0.03)


        left_question_text = tk.Text(page_frame, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                          borderwidth=0, highlightthickness=0)
        left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)
        left_question_text.insert('1.0',f'Verbal question {i} of 12')


        question_text = tk.Text(page_frame, wrap='word',  font=tkinter.font.Font(family='Helvetica', size=18), borderwidth=0, highlightthickness=0)
        question_text.place(relx=0.175747, rely=0.208333, relwidth=0.644405, relheight=0.312500)
        question_text.insert('1.0',question)

        options = choices.split('\n')
        while '' in options:
            options.remove('')

        # 创建一个 Tkinter 变量，用于存储选中的值
        var = tk.StringVar(value="Option 1")

        def selection():
            selected_value = var.get()
            self.v1_user_choice[i-1]=selected_value
            self.change_page_buttons[i-1].config(bg='green')


        # 创建单选按钮
        A = tk.Radiobutton(page_frame, text=options[0], variable=var, value="A", command=selection,font=("Helvetica", 15), bg='white')
        A.place(relx=0.175747, rely=0.520833)

        B = tk.Radiobutton(page_frame, text=options[1], variable=var, value="B", command=selection,font=("Helvetica", 15), bg='white')
        B.place(relx=0.175747, rely=0.572917)

        C = tk.Radiobutton(page_frame, text=options[2], variable=var, value="C", command=selection,font=("Helvetica", 15), bg='white')
        C.place(relx=0.175747, rely=0.625000)

        D = tk.Radiobutton(page_frame, text=options[3], variable=var, value="D", command=selection,font=("Helvetica", 15), bg='white')
        D.place(relx=0.175747, rely=0.677083)

        E = tk.Radiobutton(page_frame, text=options[4], variable=var, value="E", command=selection,font=("Helvetica", 15), bg='white')
        E.place(relx=0.175747, rely=0.729167)
        return page_frame

    def create_three_choices_pages(self,i,question,choices):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.root.screen_width, height=self.root.screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg_img2, anchor='nw')

        # 添加按钮
        back_button = tk.Button(page_frame, text="Back", command=self.go_back)
        back_button.place(relx=0.879, rely=0.021, relwidth=0.03, relheight=0.03)
        next_button = tk.Button(page_frame, text="Next", command=self.go_next)
        next_button.place(relx=0.937, rely=0.021, relwidth=0.03, relheight=0.03)

        left_question_text = tk.Text(page_frame, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                     borderwidth=0, highlightthickness=0)
        left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)
        left_question_text.insert('1.0', f'Verbal question {i} of 12')

        question_text = tk.Text(page_frame, wrap='word',
                                font=tkinter.font.Font(family='Helvetica', size=18), borderwidth=0,
                                highlightthickness=0)
        question_text.place(relx=0.175747, rely=0.208333, relwidth=0.644405, relheight=0.312500)
        question_text.insert('1.0', question)

        # 绘制竖线
        canvas.create_line(550, 400, 550, 650, fill='black')
        canvas.create_line(850, 400, 850, 650, fill='black')

        options = choices.split('\n')
        while '' in options:
            options.remove('')

        # 创建一个 Tkinter 变量，用于存储选中的值
        var1 = tk.StringVar(value="Option 1")
        var2 = tk.StringVar(value="Option 2")
        var3 = tk.StringVar(value="Option 2")


        def update_three_blank_user_choice():

            try:
                selected_values = selected_value1 + selected_value2 + selected_value3
                self.v1_user_choice[i - 1] = selected_values
                self.change_page_buttons[i - 1].config(bg='green')


            except NameError:
                pass

        def selection1():
            global selected_value1
            selected_value1 = var1.get()
            update_three_blank_user_choice()
        def selection2():
            global selected_value2
            selected_value2 = var2.get()
            update_three_blank_user_choice()
        def selection3():
            global selected_value3
            selected_value3 = var3.get()
            update_three_blank_user_choice()




        # 创建单选按钮
        A = tk.Radiobutton(page_frame, text=options[0], variable=var1, value="A", command=selection1, font=("Helvetica", 15),
                           bg='white')
        A.place(relx=0.175747, rely=0.520833)

        B = tk.Radiobutton(page_frame, text=options[1], variable=var1, value="B", command=selection1, font=("Helvetica", 15),
                           bg='white')
        B.place(relx=0.175747, rely=0.572917)

        C = tk.Radiobutton(page_frame, text=options[2], variable=var1, value="C", command=selection1, font=("Helvetica", 15),
                           bg='white')
        C.place(relx=0.175747, rely=0.625000)

        D = tk.Radiobutton(page_frame, text=options[3], variable=var2, value="D", command=selection2, font=("Helvetica", 15),
                           bg='white')
        D.place(relx=0.351494, rely=0.520833)

        E = tk.Radiobutton(page_frame, text=options[4], variable=var2, value="E", command=selection2, font=("Helvetica", 15),
                           bg='white')
        E.place(relx=0.351494, rely=0.572917)

        F = tk.Radiobutton(page_frame, text=options[5], variable=var2, value="F", command=selection2, font=("Helvetica", 15),
                           bg='white')
        F.place(relx=0.351494, rely=0.625000)

        G = tk.Radiobutton(page_frame, text=options[6], variable=var3, value="G", command=selection3, font=("Helvetica", 15),
                           bg='white')
        G.place(relx=0.527241, rely=0.520833)

        H = tk.Radiobutton(page_frame, text=options[7], variable=var3, value="H", command=selection3, font=("Helvetica", 15),
                           bg='white')
        H.place(relx=0.527241, rely=0.572917)

        I = tk.Radiobutton(page_frame, text=options[8], variable=var3, value="I", command=selection3, font=("Helvetica", 15),
                           bg='white')
        I.place(relx=0.527241, rely=0.625000)
        return page_frame

    def create_two_choices_pages(self,i,question,choices):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.root.screen_width, height=self.root.screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg_img2, anchor='nw')

        # 添加按钮
        back_button = tk.Button(page_frame, text="Back", command=self.go_back)
        back_button.place(relx=0.879, rely=0.021, relwidth=0.03, relheight=0.03)
        next_button = tk.Button(page_frame, text="Next", command=self.go_next)
        next_button.place(relx=0.937, rely=0.021, relwidth=0.03, relheight=0.03)

        left_question_text = tk.Text(page_frame, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                     borderwidth=0, highlightthickness=0)
        left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)
        left_question_text.insert('1.0', f'Verbal question {i} of 12')

        question_text = tk.Text(page_frame, wrap='word',
                                font=tkinter.font.Font(family='Helvetica', size=18), borderwidth=0,
                                highlightthickness=0)
        question_text.place(relx=0.175747, rely=0.208333, relwidth=0.644405, relheight=0.312500)
        question_text.insert('1.0', question)

        # 绘制竖线
        canvas.create_line(550, 400, 550, 650, fill='black')

        options = choices.split('\n')
        while '' in options:
            options.remove('')

        # 创建一个 Tkinter 变量，用于存储选中的值
        var1 = tk.StringVar(value="Option 1")
        var2 = tk.StringVar(value="Option 2")


        def selection1():
            global selected_value1

            selected_value1 = var1.get()
            update_two_blank_user_choice()

        def selection2():
            global selected_value2

            selected_value2 = var2.get()
            update_two_blank_user_choice()


        def update_two_blank_user_choice():
            try:
                selected_values = selected_value1 + selected_value2

                self.v1_user_choice[i - 1] = selected_values
                self.change_page_buttons[i - 1].config(bg='green')

            except NameError:
                pass



        # 创建单选按钮
        A = tk.Radiobutton(page_frame, text=options[0], variable=var1, value="A", command=selection1, font=("Helvetica", 15),
                           bg='white')
        A.place(relx=0.175747, rely=0.520833)

        B = tk.Radiobutton(page_frame, text=options[1], variable=var1, value="B", command=selection1, font=("Helvetica", 15),
                           bg='white')
        B.place(relx=0.175747, rely=0.572917)

        C = tk.Radiobutton(page_frame, text=options[2], variable=var1, value="C", command=selection1, font=("Helvetica", 15),
                           bg='white')
        C.place(relx=0.175747, rely=0.625000)

        D = tk.Radiobutton(page_frame, text=options[3], variable=var2, value="D", command=selection2, font=("Helvetica", 15),
                           bg='white')
        D.place(relx=0.351494, rely=0.520833)

        E = tk.Radiobutton(page_frame, text=options[4], variable=var2, value="E", command=selection2, font=("Helvetica", 15),
                           bg='white')
        E.place(relx=0.351494, rely=0.572917)

        F = tk.Radiobutton(page_frame, text=options[5], variable=var2, value="F", command=selection2, font=("Helvetica", 15),
                           bg='white')
        F.place(relx=0.351494, rely=0.625000)
        return page_frame

    def create_six_choose_two_pages(self,page,question,choices):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.root.screen_width, height=self.root.screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg_img2, anchor='nw')
        # Add navigation buttons
        back_button = tk.Button(page_frame, text="Back", command=self.go_back)
        back_button.place(relx=0.879, rely=0.021, relwidth=0.03, relheight=0.03)
        next_button = tk.Button(page_frame, text="Next", command=self.go_next)
        next_button.place(relx=0.937, rely=0.021, relwidth=0.03, relheight=0.03)
        # Question label
        left_question_text = tk.Text(page_frame, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                     borderwidth=0, highlightthickness=0)
        left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)
        left_question_text.insert('1.0', f'Verbal question {page} of 12')

        # Question text
        question_text = tk.Text(page_frame, wrap='word',
                                font=tkinter.font.Font(family='Helvetica', size=18), borderwidth=0,
                                highlightthickness=0)
        question_text.place(relx=0.175747, rely=0.208333, relwidth=0.644405, relheight=0.312500)
        question_text.insert('1.0', question)

        # Options
        options = choices.split('\n')
        while '' in options:
            options.remove('')

        vars = [tk.IntVar() for _ in range(6)]

        def show_selection():
            selected_options = [chr(65 + i) for i, var in enumerate(vars) if var.get()]
            select_text = ''
            for selected_option in selected_options:
                select_text+=selected_option
            self.v1_user_choice[page-1] = select_text
            self.change_page_buttons[page - 1].config(bg='green')



        for i, option in enumerate(options[:6]):
            cb = tk.Checkbutton(page_frame, text=option, variable=vars[i], command=show_selection,
                                font=("Helvetica", 15), bg='white')
            cb.place(relx=0.175747, rely=0.520833 + i * 0.05208)

        return page_frame


    def create_reading_choose_one_pages(self,page,passage,question,choices):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.root.screen_width, height=self.root.screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg_img1, anchor='nw')

        # 添加按钮
        back_button = tk.Button(page_frame, text="Back", command=self.go_back)
        back_button.place(relx=0.879, rely=0.021, relwidth=0.03, relheight=0.03)
        next_button = tk.Button(page_frame, text="Next", command=self.go_next)
        next_button.place(relx=0.937, rely=0.021, relwidth=0.03, relheight=0.03)

        left_question_text = tk.Text(page_frame, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                     borderwidth=0, highlightthickness=0)
        left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)
        left_question_text.insert('1.0', f'Verbal question {page} of 12')

        # 创建阅读文章显示界面
        text = tk.Text(page_frame, wrap='word', font=tkinter.font.Font(family='Helvetica', size=17), borderwidth=0,
                       highlightthickness=0)
        text.place(relx=0.035149, rely=0.114583, relwidth=0.439367, relheight=1.041667)
        scrollbar = tk.Scrollbar(page_frame, command=text.yview)
        scrollbar.pack(side='right', fill='y')
        text.config(yscrollcommand=scrollbar.set)
        article =  passage
        text.insert('1.0', article)


        options = choices.split('\n')

        while '' in options:
            options.remove('')
        option_text = ''
        for option in options:
            option_text+=option
            option_text += '\n'
            option_text += '\n'

        question_text = tk.Text(page_frame, wrap='word',
                                font=tkinter.font.Font(family='Helvetica', size=18), borderwidth=0,
                                highlightthickness=0)
        question_text.place(relx=0.503808, rely=0.114583, relwidth=0.492091, relheight=0.729167)
        question = question+'\n'+'\n'+'\n'+option_text
        question_text.insert('1.0', question)


        var = tk.StringVar(value="Option 1")

        def selection():
            selected_value = var.get()
            self.v1_user_choice[page-1] = selected_value
            self.change_page_buttons[page - 1].config(bg='green')


        abcdefgh = ['A','B','C','D','E','F','G','H','I','J']
        # 创建单选按钮
        for i in range(len(options)):
            button = tk.Radiobutton(page_frame, text=abcdefgh[i], variable=var, value=abcdefgh[i], command=selection, font=("Helvetica", 15),
                           bg='white')
            button.place(relx=0.527241+0.041*i,rely=0.833333)
        return page_frame

    def create_reading_choose_multiple_pages(self, page, passage, question, choices):
        page_frame = tk.Frame(self.root)
        canvas = tk.Canvas(page_frame, width=self.root.screen_width, height=self.root.screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg_img1, anchor='nw')

        # 添加按钮
        back_button = tk.Button(page_frame, text="Back", command=self.go_back)
        back_button.place(relx=0.879, rely=0.021, relwidth=0.03, relheight=0.03)
        next_button = tk.Button(page_frame, text="Next", command=self.go_next)
        next_button.place(relx=0.937, rely=0.021, relwidth=0.03, relheight=0.03)

        left_question_text = tk.Text(page_frame, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                     borderwidth=0, highlightthickness=0)
        left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)
        left_question_text.insert('1.0', f'Verbal question {page} of 12')

        # 创建阅读文章显示界面
        text = tk.Text(page_frame, wrap='word', font=tkinter.font.Font(family='Helvetica', size=17), borderwidth=0,
                       highlightthickness=0)
        text.place(relx=0.035149, rely=0.114583, relwidth=0.439367, relheight=1.041667)
        scrollbar = tk.Scrollbar(page_frame, command=text.yview)
        scrollbar.pack(side='right', fill='y')
        text.config(yscrollcommand=scrollbar.set)
        article = passage
        text.insert('1.0', article)

        options = choices.split('\n')
        while '' in options:
            options.remove('')

        question_text = tk.Text(page_frame, wrap='word',
                                font=tkinter.font.Font(family='Helvetica', size=18), borderwidth=0,
                                highlightthickness=0)
        question_text.place(relx=0.503808, rely=0.114583, relwidth=0.492091, relheight=0.729167)
        question = question + '\n' + '\n' + '\n' + '\n'.join(options)
        question_text.insert('1.0', question)

        var_dict = {}
        abcdefgh = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

        def selection():
            selected_options = [key for key, var in var_dict.items() if var.get()]
            select_text = ''
            for selected_option in selected_options:
                select_text+=selected_option
            self.v1_user_choice[page-1] = select_text
            self.change_page_buttons[page - 1].config(bg='green')


        # 创建多选按钮
        for i, option in enumerate(options):
            var = tk.BooleanVar()
            var_dict[abcdefgh[i]] = var
            button = tk.Checkbutton(page_frame, text=abcdefgh[i], variable=var, command=selection,
                                    font=("Helvetica", 15), bg='white')
            button.place(relx=0.527241 + 0.041 * i, rely=0.833333)
        return page_frame


    def change_page(self,index):
        for widget in self.root.winfo_children():
            widget.forget()
        self.current_page_index = index
        self.display_page(index)
    def display_page(self, index):
        # Display new page
        if 0 <= index < len(self.pages):
            page = self.pages[index]
            if page:
                page.pack(fill='both', expand=True)

    def go_next(self):

        if self.current_page_index < len(self.pages) - 1:
            for widget in self.root.winfo_children():
                widget.forget()
            self.current_page_index += 1
            self.display_page(self.current_page_index)
        else:
            print(self.current_page_index)
            self.go_to_q1()

    def go_back(self):
        if self.current_page_index > 0:
            for widget in self.root.winfo_children():
                widget.forget()
            self.current_page_index -= 1
            self.display_page(self.current_page_index)

    def go_to_q1(self):
        result = messagebox.askokcancel("确认", "你确定要进入Quantity1吗？")

        if result:
            for widget in self.root.winfo_children():
                widget.destroy()
            q1.Q1(self.root,self.paper,self.v1_user_choice,self.v1_answer_choice)


    def create_pages(self):

        for i in range(1,13):
            question_type = self.paper.get(f'section2 题目{i} 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）')

            if question_type[:2]  == '单空':
                question = self.paper.get(f'section2 题目{i} 题干')
                choices = self.paper.get(f'section2 题目{i} 选项')
                answers = self.paper.get(f'section2 题目{i} 答案')
                self.v1_answer_choice[i-1]=answers
                page = self.create_one_choice_pages(i,question,choices)
                self.pages.append(page)

            if question_type[:2]  == '双空':
                question = self.paper.get(f'section2 题目{i} 题干')
                choices = self.paper.get(f'section2 题目{i} 选项')
                answers = self.paper.get(f'section2 题目{i} 答案')
                self.v1_answer_choice[i-1] = answers
                page = self.create_two_choices_pages(i,question,choices)
                self.pages.append(page)
            if question_type[:2]  == '三空':
                question = self.paper.get(f'section2 题目{i} 题干')
                choices = self.paper.get(f'section2 题目{i} 选项')
                answers = self.paper.get(f'section2 题目{i} 答案')
                self.v1_answer_choice[i-1] = answers
                page = self.create_three_choices_pages(i,question,choices)
                self.pages.append(page)

            if question_type[:3]  == '六选二':
                question = self.paper.get(f'section2 题目{i} 题干')
                choices = self.paper.get(f'section2 题目{i} 选项')
                answers = self.paper.get(f'section2 题目{i} 答案')
                self.v1_answer_choice[i-1] = answers
                page = self.create_six_choose_two_pages(i,question,choices)
                self.pages.append(page)

            if question_type[:4]  == '阅读单选' or question_type[:5]  == '阅读选句子':
                passage = self.paper.get(f'section2 题目{i} 阅读文章（没有为空）')
                question = self.paper.get(f'section2 题目{i} 题干')
                choices = self.paper.get(f'section2 题目{i} 选项')
                answers = self.paper.get(f'section2 题目{i} 答案')
                self.v1_answer_choice[i-1] = answers
                page = self.create_reading_choose_one_pages(i,passage,question,choices)
                self.pages.append(page)

            if question_type[:4]  == '阅读多选':
                passage = self.paper.get(f'section2 题目{i} 阅读文章（没有为空）')
                question = self.paper.get(f'section2 题目{i} 题干')
                choices = self.paper.get(f'section2 题目{i} 选项')
                answers = self.paper.get(f'section2 题目{i} 答案')
                self.v1_answer_choice[i-1] = answers
                page = self.create_reading_choose_multiple_pages(i,passage,question,choices)
                self.pages.append(page)



    def format_time(self, seconds):
        """将秒数格式化为分钟和秒数"""
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def update_timer(self):
        """更新倒计时"""
        try:
            if self.time_left > 0:
                self.time_left -= 1
                if self.time_label:
                    self.time_label.config(text=self.format_time(self.time_left))
                self.timer_id = self.root.after(1000, self.update_timer)  # 每秒调用一次更新函数
            else:
                self.on_time_up()
        except tk.TclError:
            # 忽略 TclError 错误
            pass

    def on_time_up(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        q1.Q1(self.root, self.paper, self.v1_user_choice, self.v1_answer_choice)




if __name__ == '__main__':
    root = tk.Tk()
    V1(root,)
    root.mainloop()