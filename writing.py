import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font
from docx import Document
from datetime import datetime
from tkinter import font
import os
import v1
from tkinter import messagebox

class Writing:

    def __init__(self, root,file_contents):
        self.root = root
        self.root.bg_img = r'bg_img.png'
        self.file_contents = file_contents
        self.question = self.file_contents.get('写作section1 题目')

        # 获取屏幕宽度和高度
        self.root.screen_width = self.root.winfo_screenwidth()
        self.root.screen_height = self.root.winfo_screenheight()
        # 设置全屏
        self.root.attributes('-fullscreen', True)
        self.root.img_path = r'bg_img.png'
        self.root.canvas = tk.Canvas(self.root, width=self.root.screen_width, height=self.root.screen_height)
        self.root.canvas.pack(fill='both', expand=True)

        self.left_question_text = tk.Text(self.root, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                     borderwidth=0, highlightthickness=0)
        self.left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)

        # 加载背景图片
        image = Image.open(self.root.img_path)
        # 调整图像大小以适应屏幕
        image = image.resize((self.root.screen_width, self.root.screen_height), Image.LANCZOS)
        self.root.bg_img = ImageTk.PhotoImage(image)  # 保持引用防止被垃圾回收
        # 在 Canvas 上创建图像
        self.root.canvas.create_image(0, 0, image=self.root.bg_img, anchor='nw')

        self.save_button = tk.Button(self.root, text='Next', font=("Helvetica", 14), command=self.save_to_doc)
        self.save_button.place(relx=0.937317, rely=0.020833, relwidth=0.029291, relheight=0.020833)
        #添加倒计时
        # 初始化时间
        self.time_left = 30 * 60  # 30分钟的秒数
        # 创建标签显示剩余时间
        self.time_label = tk.Label(self.root, text=self.format_time(self.time_left), font=("Helvetica", 14),bg="#F0E1E4")
        self.time_label.place(relx = 0.9, rely = 0.075, relwidth = 0.05, relheight = 0.03)
        # 启动倒计时
        self.update_timer()
        self.create_writing_page()

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
        self.save_to_doc()
        for widget in self.root.winfo_children():
            widget.destroy()

        v1.V1(self.root, self.file_contents)

    def create_writing_page(self):
        # 创建滚动条
        frame = tk.Frame(self.root)
        frame.place(relx=0.017575, rely=0.130208, relwidth=0.468658, relheight=0.833333)
        text = tk.Text(frame, wrap='word', font=tkinter.font.Font(family='Helvetica', size=17), borderwidth=0,
                       highlightthickness=0)
        text.pack(side='left', fill='both', expand=True)
        scrollbar = tk.Scrollbar(frame, command=text.yview)
        scrollbar.pack(side='right', fill='y')
        text.config(yscrollcommand=scrollbar.set)
        article =  self.question
        text.insert('1.0', article)
        text.tag_configure('spacing', spacing3=20)
        text.tag_add('spacing', '1.0', 'end')
        text.config(state='disabled')

        self.left_question_text.insert('1.0', f'section1 Writing')

        #创建作文写入界面
        custom_font = font.Font(family='Arial', size=14)
        self.text_input = tk.Text(self.root, wrap='word', font=custom_font)
        self.text_input.place(relx=0.503808, rely=0.114583, relwidth=0.492091, relheight=0.875000)  # 设置文本框的位置和大小


    def save_to_doc(self):
        text_content = self.text_input.get("1.0", "end-1c")
        name = self.file_contents.get('name')
        time = datetime.now().strftime('%Y-%m-%d')
        file_path = rf'results/{name}/{time}/writing.doc'
        if os.path.exists(file_path):
            os.remove(file_path)
        doc = Document()
        # 添加文本到文档
        doc.add_paragraph(text_content)
        # 保存文档
        doc.save(file_path)
        self.go_to_v1()
    def go_to_v1(self):
        result = messagebox.askokcancel("确认", "你确定要进入Verbal1吗？")
        if result:
            for widget in self.root.winfo_children():
                widget.destroy()

            v1.V1(self.root, self.file_contents)




if __name__ == '__main__':
    root = tk.Tk()
    Writing(root,{'写作section1 题目':'This is writing questioon','name':'陶雨田'})
    root.mainloop()


