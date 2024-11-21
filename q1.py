import tkinter as tk
from PIL import Image, ImageTk
import calculator
import v2
from tkinter import messagebox

class Q1:
    def __init__(self, root, paper,v1_user_choices,v1_right_choices):
        self.root = root
        self.paper = paper
        self.root.title("section 2")
        self.root.screen_width = self.root.winfo_screenwidth()
        self.root.screen_height = self.root.winfo_screenheight()
        self.root.attributes('-fullscreen', True)


        # 用于填空的背景
        self.image = Image.open('bg_img2.png')
        self.image = self.image.resize((self.root.screen_width, self.root.screen_height), Image.LANCZOS)
        self.bg_img = ImageTk.PhotoImage(self.image)  # 保持引用防止被垃圾回收

        self.current_page_index = 0
        self.pages = []
        self.v1_user_choice = v1_user_choices
        self.v1_answer_choice = v1_right_choices

        self.q1_user_choice = ['none'] * 12
        self.q1_answer_choice = ['none'] * 12

        self.create_pages()


        # 添加倒计时
        # 初始化时间
        self.time_left = 21 * 60  # 21分钟的秒数
        # 创建标签显示剩余时间
        self.time_label = tk.Label(self.root, text=self.format_time(self.time_left), font=("Helvetica", 14),bg="#F0E1E4")
        self.time_label.place(relx = 0.9, rely = 0.075, relwidth = 0.05, relheight = 0.03)
        self.change_page_buttons = []
        self.create_navigation_buttons()

        def open_calc():
            """点击按钮时创建并显示 Calc 窗口。"""
            calc = calculator.Calculator()


        btn_open_calc = tk.Button(root, text="calculator", command=open_calc)
        btn_open_calc.place(relx=0.820152, rely=0.020833, relwidth=0.035149, relheight=0.031250)
        # 启动倒计时
        self.update_timer()
        self.display_page(self.current_page_index)

    def create_navigation_buttons(self):
        for index in range(len(self.pages)):
            change_page_button = tk.Button(self.root, text=str(index + 1), bg='red',
                                           command=lambda idx=index: self.change_page(idx))
            change_page_button.place(relx=0.146456 + 0.02929 * index, rely=0.016667, relwidth=0.023433, relheight=0.041667)
            self.change_page_buttons.append(change_page_button)
    def resize_image(self,image, max_width, max_height):
        """按比例缩放图片，确保不超过最大宽度和高度。"""
        img_width, img_height = image.size
        ratio = min(max_width / img_width, max_height / img_height)
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def create_one_choice_pages(self, i, diagram, choice_number):
        page_frame = tk.Frame(self.root)
        page_frame.pack_propagate(False)
        canvas = tk.Canvas(page_frame, width=self.root.screen_width, height=self.root.screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg_img, anchor='nw')

        # 添加按钮
        back_button = tk.Button(page_frame, text="Back", command=self.go_back)
        back_button.place(relx=0.879, rely=0.021, relwidth=0.03, relheight=0.03)
        next_button = tk.Button(page_frame, text="Next", command=self.go_next)
        next_button.place(relx=0.937, rely=0.021, relwidth=0.03, relheight=0.03)

        left_question_text = tk.Text(page_frame, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                     borderwidth=0, highlightthickness=0)
        left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)
        left_question_text.insert('1.0', f'Quantity question {i} of 12')


        # 加载图片
        original_image = Image.open(fr"{diagram}")
        # 调整图片大小
        resized_image = self.resize_image(original_image, 1000, 600)
        photo_image = ImageTk.PhotoImage(resized_image)
        # 保持对图片的引用
        canvas.image = photo_image
        # 在 Canvas 中插入图片
        canvas.create_image(200, 150, anchor=tk.NW, image=photo_image)

        # 创建一个 Tkinter 变量，用于存储选中的值
        var = tk.StringVar(value="Option 1")

        def selection():
            selected_value = var.get()
            self.q1_user_choice[i - 1] = selected_value
            self.change_page_buttons[i - 1].config(bg='green')


        # 创建单选按钮
        A = tk.Radiobutton(page_frame, text='A', variable=var, value="A", command=selection,
                           font=("Helvetica", 15), bg='white')
        A.place(relx=0.175747, rely=0.781250)

        B = tk.Radiobutton(page_frame, text='B', variable=var, value="B", command=selection,
                           font=("Helvetica", 15), bg='white')
        B.place(relx=0.222613, rely=0.781250)

        C = tk.Radiobutton(page_frame, text='C', variable=var, value="C", command=selection,
                           font=("Helvetica", 15), bg='white')
        C.place(relx=0.269479, rely=0.781250)

        D = tk.Radiobutton(page_frame, text='D', variable=var, value="D", command=selection,
                           font=("Helvetica", 15), bg='white')
        D.place(relx=0.316344, rely=0.781250)
        if choice_number == 5:
            E = tk.Radiobutton(page_frame, text='E', variable=var, value="E", command=selection,
                            font=("Helvetica", 15), bg='white')
            E.place(relx=0.363210, rely=0.781250)
        return page_frame

    def create_multiple_choices_pages(self, page, diagram, choice_number):
        page_frame = tk.Frame(self.root)
        page_frame.pack_propagate(False)
        canvas = tk.Canvas(page_frame, width=self.root.screen_width, height=self.root.screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg_img, anchor='nw')

        # 添加按钮
        back_button = tk.Button(page_frame, text="Back", command=self.go_back)
        back_button.place(relx=0.879, rely=0.021, relwidth=0.03, relheight=0.03)
        next_button = tk.Button(page_frame, text="Next", command=self.go_next)
        next_button.place(relx=0.937, rely=0.021, relwidth=0.03, relheight=0.03)

        left_question_text = tk.Text(page_frame, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                     borderwidth=0, highlightthickness=0)
        left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)
        left_question_text.insert('1.0', f'Quantity question {page} of 12')

        # 加载图片
        original_image = Image.open(fr"{diagram}")
        # 调整图片大小
        resized_image = self.resize_image(original_image, 1000, 600)
        photo_image = ImageTk.PhotoImage(resized_image)
        # 保持对图片的引用
        canvas.image = photo_image
        # 在 Canvas 中插入图片
        canvas.create_image(200, 150, anchor=tk.NW, image=photo_image)



        var_dict = {}
        abcdefgh = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']

        def selection():
            selected_options = [key for key, var in var_dict.items() if var.get()]
            select_text = ''
            for selected_option in selected_options:
                select_text += selected_option
            self.q1_user_choice[page - 1] = select_text
            self.change_page_buttons[page - 1].config(bg='green')

        # 创建多选按钮
        for i in range(choice_number):
            var = tk.BooleanVar()
            var_dict[abcdefgh[i]] = var
            button = tk.Checkbutton(page_frame, text=abcdefgh[i], variable=var, command=selection,
                                    font=("Helvetica", 15), bg='white')
            button.place(relx=0.175747 + 0.046865 * i, rely=0.781250)
        return page_frame

    def create_fill_blank_pages(self, page, diagram):
        page_frame = tk.Frame(self.root)
        page_frame.pack_propagate(False)
        canvas = tk.Canvas(page_frame, width=self.root.screen_width, height=self.root.screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas.create_image(0, 0, image=self.bg_img, anchor='nw')

        # 添加按钮
        back_button = tk.Button(page_frame, text="Back", command=self.go_back)
        back_button.place(relx=0.879, rely=0.021, relwidth=0.03, relheight=0.03)
        next_button = tk.Button(page_frame, text="Next", command=self.go_next)
        next_button.place(relx=0.937, rely=0.021, relwidth=0.03, relheight=0.03)

        left_question_text = tk.Text(page_frame, bg="#F0E1E4", fg='black', font=('Arial', 18), wrap='word',
                                     borderwidth=0, highlightthickness=0)
        left_question_text.place(relx=0.000000, rely=0.072917, relwidth=0.292912, relheight=0.031250)
        left_question_text.insert('1.0', f'Quantity question {page} of 12')

        # 加载图片
        original_image = Image.open(fr"{diagram}")
        # 调整图片大小
        resized_image = self.resize_image(original_image, 1000, 600)
        photo_image = ImageTk.PhotoImage(resized_image)
        # 保持对图片的引用
        canvas.image = photo_image
        # 在 Canvas 中插入图片
        canvas.create_image(200, 150, anchor=tk.NW, image=photo_image)

        def on_enter_pressed(event):
            """当用户按下回车键时，打印输入框的内容。"""
            user_input = entry.get()
            self.q1_user_choice[page-1] = user_input
            self.change_page_buttons[page - 1].config(bg='green')
        entry = tk.Entry(page_frame, font=('Arial', 18),borderwidth=2, highlightthickness=2)
        entry.place(relx=0.175747,rely=0.781250)
        entry.bind('<KeyRelease>', on_enter_pressed)
        return page_frame




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
            self.go_to_v2()

    def go_back(self):
        if self.current_page_index > 0:
            for widget in self.root.winfo_children():
                widget.forget()
            self.current_page_index -= 1
            self.display_page(self.current_page_index)

    def go_to_v2(self):
        result = messagebox.askokcancel("确认", "你确定要进入Verbal2吗？")
        if result:
            for widget in self.root.winfo_children():
                widget.destroy()
            v2.V2(self.root,self.paper,self.v1_user_choice,self.v1_answer_choice,self.q1_user_choice,self.q1_answer_choice)


    def create_pages(self):

        for i in range(1, 13):
            question_type = self.paper.get(f'section3 题目{i} 类型（单选，多选，填空）')
            diagram  = self.paper.get(f'section3 题目{i} 题目（填路径）')
            choice_number = self.paper.get(f'section3 题目{i} 选项个数（填数字）')
            answers = self.paper.get(f'section3 题目{i} 答案')

            if question_type[:2] == '单选':
                self.q1_answer_choice[i - 1] = answers
                page = self.create_one_choice_pages(i, diagram, int(choice_number))
                self.pages.append(page)


            if question_type[:2] == '多选':
                self.q1_answer_choice[i - 1] = answers
                page = self.create_multiple_choices_pages(i, diagram, int(choice_number))
                self.pages.append(page)


            if question_type[:2] == '填空':
                self.q1_answer_choice[i - 1] = answers
                page = self.create_fill_blank_pages(i, diagram)
                self.pages.append(page)

    def change_page(self,index):
        for widget in self.root.winfo_children():
            widget.forget()
        self.current_page_index = index
        self.display_page(index)

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
        v2.V2(self.root,self.paper,self.v1_user_choice,self.v1_answer_choice,self.q1_user_choice,self.q1_answer_choice)



if __name__ == '__main__':
    root = tk.Tk()
    Q1(root,{'写作section1 题目': 'Some people believe that in order to thrive, a society must put its own overall success before the well-being of its individual citizens. Others believe that the well-being of a society can only be measured by the general welfare of all its people.\nWrite a response in which you discuss which view more closely aligns with your own position and explain your reasoning for the position you take. In developing and supporting your position, you should address both of the views presented.', 'section2 题目1 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '单空', 'section2 题目1 阅读文章（没有为空）': '', 'section2 题目1 题干': "1.Marvin's mother thought that his______quiet, imaginative reverie would eventually lead him to become an artist, or perhaps a philosopher.", 'section2 题目1 选项': 'A.aversion to\nB.apathy toward\nC.befuddlement by\nD.vexation with\nE.penchant for', 'section2 题目1 答案': 'E', 'section2 题目2 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '双空', 'section2 题目2 阅读文章（没有为空）': '', 'section2 题目2 题干': '2. The idea that arguments based on probability are deployed only by (i)______ persons is (ii)______ even among scientists. Perhaps such an evaluation has partly to do with the origins of the subject in the mathematics of gambling games, not generally regarded as pastimes for people of good character.', 'section2 题目2 选项': 'A. exacting\nB. disreputable\t\nC. prominent\nD. widespread\nE. controversial\t\nF. deplored', 'section2 题目2 答案': 'BE', 'section2 题目3 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '三空', 'section2 题目3 阅读文章（没有为空）': '', 'section2 题目3 题干': "3. Divided into separate essays on different aspects of Jacques-Louis David's late career, Bordes' catalog (i)_____a great deal of knowledge, never providing a full introduction to the painter's life or to the period in which he lived Yet while the book may (ii)_____, the casual reader, cognoscenti will delight in the wonderfully complete detail on each picture, not to mention the caustic little jabs at colleagues that Bordes occasionally delivers. The world of David scholarship. as befits its subject, is not a (iii)_____place.", 'section2 题目3 选项': 'A. contains\nB. assumes\nC. disputes\nD. satisfy\nE. frustrate\nF. address\nG. gentle\nH. competitive\nI. sophisticated', 'section2 题目3 答案': 'AEI', 'section2 题目4 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '阅读单选', 'section2 题目4 阅读文章（没有为空）': 'In late imperial China (circa 1650-1850), excessive exploitation came not from the sovereign but from his agents, who had shorter-term goals and narrower interests than their ruler did. While the emperor\'s interest in preempting rebellion militated against overtaxation, his agents had incentives to exploit the taxpayers for their own benefit. Due to weak oversight, the emperor had to keep the taxes low and his bureaucracy small to mitigate this "tyranny at the bottom" effect. This fiscal weakness of the Chinese state had long been masked by its huge tax base; however, the economic expansion of the eighteenth century exacerbated the problems of administrative control, further squeezing the nation\'s finances and leaving China ill prepared for the challenges of the nineteenth century. ', 'section2 题目4 题干': '4.it can be inferred that the author assumes which of the following about the emperor\'s strategy of keeping "the taxes low and his bureaucracy small"?', 'section2 题目4 选项': "A.It was implemented with little understanding of its consequences.\nB.It was a concession made to ameliorate an unacceptable situation.\nC.It was an indication of the emperor's refusal to compromise his principles.\nD.It was a rare success in a policy area characterized by failure.\nE.It was a choice of the common good over the emperor's personal interests.", 'section2 题目4 答案': 'B', 'section2 题目5 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '阅读单选', 'section2 题目5 阅读文章（没有为空）': 'In late imperial China (circa 1650-1850), excessive exploitation came not from the sovereign but from his agents, who had shorter-term goals and narrower interests than their ruler did. While the emperor\'s interest in preempting rebellion militated against overtaxation, his agents had incentives to exploit the taxpayers for their own benefit. Due to weak oversight, the emperor had to keep the taxes low and his bureaucracy small to mitigate this "tyranny at the bottom" effect. This fiscal weakness of the Chinese state had long been masked by its huge tax base; however, the economic expansion of the eighteenth century exacerbated the problems of administrative control, further squeezing the nation\'s finances and leaving China ill prepared for the challenges of the nineteenth century. ', 'section2 题目5 题干': '5.It can be inferred from the passage that the Chinese emperor and the bureaucracy differed with respect to the', 'section2 题目5 选项': 'A.priority each placed on preventing popular rebellion\nB.aversion of each to economic and bureaucratic reform\nC.interest each showed in addressing the fiscal weakness of the state\nD.willingness of each to encourage economic stability through large tax revenues\nE.enthusiasm each had for the expansion of the Chinese economy', 'section2 题目5 答案': 'A', 'section2 题目6 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '六选二', 'section2 题目6 阅读文章（没有为空）': '', 'section2 题目6 题干': '6. Viruses are generally regarded as being on the far side of the demarcation between living and nonliving things, yet newly discovered giant viruses have longer genomes than some bacteria, whose status as living entities is______ .（选出2个正确选项）', 'section2 题目6 选项': 'A. elusive\nB. incontrovertible\nC. underestimated\nD. questionable\nE. indisputable\nF. debatable', 'section2 题目6 答案': 'BE', 'section2 题目7 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '六选二', 'section2 题目7 阅读文章（没有为空）': '', 'section2 题目7 题干': '7. Concerned to upend the standard top-down approach to game design, Flanagan calls on game designers to_____ the typical model with one that is less hierarchical. （选出2个正确选项）', 'section2 题目7 选项': 'A. augment\nB. supplant\nC. assail\nD. amplify\nE. modify\nF. replace', 'section2 题目7 答案': 'BF', 'section2 题目8 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '六选二', 'section2 题目8 阅读文章（没有为空）': '', 'section2 题目8 题干': '8. In nineteenth-century Puerto Rico, the consumption of salted cod spread among the entire population; on the tables of humbler families it became _____ food, adding flavor to other products and supplying much-needed protein.（选出2个正确选项）', 'section2 题目8 选项': 'A. an exotic\nB. an affordable\nC. an essential\nD. a supplemental \nE. a complementary\nF. a commonplace', 'section2 题目8 答案': 'BF', 'section2 题目9 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '六选二', 'section2 题目9 阅读文章（没有为空）': '', 'section2 题目9 题干': '9. Baker was struck by the amount of ______she saw at the renowned medical facility; for all their experience, the physicians could not seem to agree on the correct diagnosis for any given patient.（选出2个正确选项）', 'section2 题目9 选项': 'A. discordance\nB. contention\nC. quackery\nD. nepotism\nE. indecision\nF. cronyism', 'section2 题目9 答案': 'AB', 'section2 题目10 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '阅读单选', 'section2 题目10 阅读文章（没有为空）': 'Garlic mustard-a plant native to western Eurasia-has been successful as an invasive species in the United States. Garlic mustard contains a variety of plant secondary compounds that lower its palatability to herbivores. In addition, recent studies suggest that these secondary compounds affect the seed germination and growth of native plants and alter the activity of soil organisms, raising the possibility that secondary compounds in garlic mustard contribute to its overall success as an invader. Although it remains unclear exactly how these secondary compounds penetrate into the soil. their presence appears to affect surrounding plants. Prati and Bossdorf found that the germination rate of a native woodland herb, rough avens, was significantly reduced when grown in soils that had been previously occupied by garlic mustard. To test for the specific effects of root exudates (substances slowly released by roots), they mixed experimental soil samples with activated carbon, a material that binds organic compounds in soil and thereby decreases their activity. They found that more seeds germinated in soils with activated carbon than in soils without activated carbon, suggesting that organic compounds released in the exudates of garlic mustard had a negative effect on the seed germination of native species.', 'section2 题目10 题干': "10.It can be inferred from the passage that Prati and Bossdorf's experiments with activated carbon were intended to determine which of the following?", 'section2 题目10 选项': 'A.How the presence of garlic mustard affects the growth rates of other non-native plant species\nB.Why the presence of activated carbon decreases the activity of organic compounds\nC.Whether the root exudates of garlic mustard negatively affect the germination rates of native plants\nD.Whether the germination of garlic mustard is affected by the activity of soil organisms\nE.Which secondary compounds found in garlic mustard most lower its palatability to herbivores', 'section2 题目10 答案': 'C', 'section2 题目11 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '阅读多选', 'section2 题目11 阅读文章（没有为空）': 'Garlic mustard-a plant native to western Eurasia-has been successful as an invasive species in the United States. Garlic mustard contains a variety of plant secondary compounds that lower its palatability to herbivores. In addition, recent studies suggest that these secondary compounds affect the seed germination and growth of native plants and alter the activity of soil organisms, raising the possibility that secondary compounds in garlic mustard contribute to its overall success as an invader. Although it remains unclear exactly how these secondary compounds penetrate into the soil. their presence appears to affect surrounding plants. Prati and Bossdorf found that the germination rate of a native woodland herb, rough avens, was significantly reduced when grown in soils that had been previously occupied by garlic mustard. To test for the specific effects of root exudates (substances slowly released by roots), they mixed experimental soil samples with activated carbon, a material that binds organic compounds in soil and thereby decreases their activity. They found that more seeds germinated in soils with activated carbon than in soils without activated carbon, suggesting that organic compounds released in the exudates of garlic mustard had a negative effect on the seed germination of native species.', 'section2 题目11 题干': 'According to the passage, which of the following statements about the plant secondary compounds found in garlic mustard is true?（不定项选择题，答案个数不一定，选出所有可能正确的选项）', 'section2 题目11 选项': 'A.They make garlic mustard less appetizing to plant-eating animals.\nB.They alter the activity of soil-dwelling organisms.\nC.They appear to decrease the germination rates of native plant species.', 'section2 题目11 答案': 'ABC', 'section2 题目12 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '阅读单选', 'section2 题目12 阅读文章（没有为空）': 'Garlic mustard-a plant native to western Eurasia-has been successful as an invasive species in the United States. Garlic mustard contains a variety of plant secondary compounds that lower its palatability to herbivores. In addition, recent studies suggest that these secondary compounds affect the seed germination and growth of native plants and alter the activity of soil organisms, raising the possibility that secondary compounds in garlic mustard contribute to its overall success as an invader. Although it remains unclear exactly how these secondary compounds penetrate into the soil. their presence appears to affect surrounding plants. Prati and Bossdorf found that the germination rate of a native woodland herb, rough avens, was significantly reduced when grown in soils that had been previously occupied by garlic mustard. To test for the specific effects of root exudates (substances slowly released by roots), they mixed experimental soil samples with activated carbon, a material that binds organic compounds in soil and thereby decreases their activity. They found that more seeds germinated in soils with activated carbon than in soils without activated carbon, suggesting that organic compounds released in the exudates of garlic mustard had a negative effect on the seed germination of native species.', 'section2 题目12 题干': '12.According to the passage, which of the following occurred during Prati and Bossdorfs experiments?', 'section2 题目12 选项': 'A.Rough avens plants that had already germinated grew more quickly in soils that contained activated carbon than they did in soils that did not contain it.\nB.More rough avens seeds sprouted in soil with decreased organic compound activity than did seeds in soil with higher levels of organic compound activity.\nC.The growth rate of rough avens plants that had already germinated decreased significantly when the plants were grown in soil that had been previously occupied by garlic mustard.\nD.The presence of activated carbon negatively affected both the seed germination rates and the plant growth rates of garlic mustard.\nE.The activities of soil organisms necessary for the flourishing of rough avens were enhanced by the presence of garlic mustard.', 'section2 题目12 答案': 'B', 'section3 题目1 类型（单选，多选，填空）': '单选', 'section3 题目1 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-1.png', 'section3 题目1 选项个数（填数字）': '4', 'section3 题目1 答案': 'D', 'section3 题目2 类型（单选，多选，填空）': '单选', 'section3 题目2 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-2.png', 'section3 题目2 选项个数（填数字）': '4', 'section3 题目2 答案': 'A', 'section3 题目3 类型（单选，多选，填空）': '单选', 'section3 题目3 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-3.png', 'section3 题目3 选项个数（填数字）': '4', 'section3 题目3 答案': 'A', 'section3 题目4 类型（单选，多选，填空）': '单选', 'section3 题目4 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-4.png', 'section3 题目4 选项个数（填数字）': '4', 'section3 题目4 答案': 'C', 'section3 题目5 类型（单选，多选，填空）': '多选', 'section3 题目5 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-5.png', 'section3 题目5 选项个数（填数字）': '4', 'section3 题目5 答案': 'ABC', 'section3 题目6 类型（单选，多选，填空）': '单选', 'section3 题目6 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-6.png', 'section3 题目6 选项个数（填数字）': '5', 'section3 题目6 答案': 'B', 'section3 题目7 类型（单选，多选，填空）': '单选', 'section3 题目7 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-7.png', 'section3 题目7 选项个数（填数字）': '5', 'section3 题目7 答案': 'C', 'section3 题目8 类型（单选，多选，填空）': '单选', 'section3 题目8 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-8.png', 'section3 题目8 选项个数（填数字）': '5', 'section3 题目8 答案': 'D', 'section3 题目9 类型（单选，多选，填空）': '单选', 'section3 题目9 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-9.png', 'section3 题目9 选项个数（填数字）': '5', 'section3 题目9 答案': 'E', 'section3 题目10 类型（单选，多选，填空）': '单选', 'section3 题目10 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-10.png', 'section3 题目10 选项个数（填数字）': '5', 'section3 题目10 答案': 'D', 'section3 题目11 类型（单选，多选，填空）': '单选', 'section3 题目11 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-11.png', 'section3 题目11 选项个数（填数字）': '5', 'section3 题目11 答案': 'A', 'section3 题目12 类型（单选，多选，填空）': '填空', 'section3 题目12 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\1-12.png', 'section3 题目12 选项个数（填数字）': '', 'section3 题目12 答案': '110', 'section4 题目1 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '单空', 'section4 题目1 阅读文章（没有为空）': '', 'section4 题目1 题干': '1.The efficacy of a placebo may not______ deception: inert sugar pills have been shown to reduce the symptoms of irritable bowel syndrome even in patients who were explicitly told they were receiving a placebo.', 'section4 题目1 选项': 'A.justify\nB.preclude\nC.require\nD.mitigate\nE.circumvent', 'section4 题目1 答案': 'C', 'section4 题目2 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '单空', 'section4 题目2 阅读文章（没有为空）': '', 'section4 题目2 题干': '2.One baffling aspect of the novel is its capacity to generate emotional power from a plot that lacks the most elementary______: readers must accept not an occasional coincidence, but a continuous stream of them.', 'section4 题目2 选项': 'A.synergy\nB.continuity\nC.naivete\nD.premise\nE.credibility', 'section4 题目2 答案': 'E', 'section4 题目3 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '双空', 'section4 题目3 阅读文章（没有为空）': '', 'section4 题目3 题干': '3.Many scholars have argued that the United States Supreme Court usually (i)______ public opinion in its decisions because it fears that it will (ii)______ if it does not; when it does depart from public opinion, it whips up political maelstroms.', 'section4 题目3 选项': 'A. comments on\nB. hews to\nC. overrides\nD. lose public support\nE. mitigate public anger\nF. create public indifference', 'section4 题目3 答案': 'BD', 'section4 题目4 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '三空', 'section4 题目4 阅读文章（没有为空）': '', 'section4 题目4 题干': '4.When he talks about his childhood, his lack of formal education is a theme he (i)______,usually to cast it as (ii)______. He says that because he felt the need to (iii)______ it, he read much more prodigiously than he might have and without the narrowness of focus he notices in many conventionally learned people.', 'section4 题目4 选项': 'A. returns to\nB. skips over\nC. laments\nD. an insurmountable barrier\nE. an inadvertent gift\nF. an insignificant event\nG. yield to\nH. brag about\nI. compensate for', 'section4 题目4 答案': 'AEI', 'section4 题目5 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '阅读单选', 'section4 题目5 阅读文章（没有为空）': "The scandal caused by Gustave Courbet's 1850 painting A Burial at Ornans cannot be attributed to its subject-other artists' depictions of regional life had gained acceptance in Paris art circles-or to critics' assessments of Courbet's skill. Rather, by representing an ordinary burial in a provincial town on the large scale normally reserved for prestigious history paintings, Courbet had departed from a polite kind of Realism that had only recently become acceptable, where both the subject-virtuous peasant life-and the dimensions were modest. Courbet sought to do something more ambitious than a painter like Leleux, who depicted everyday life faithfully and without exaggeration: Courbet wished to paint his contemporaries with the seriousness normally reserved for kings and heroes.", 'section4 题目5 题干': '5.The author of the passage mentions Leleux primarily in order to', 'section4 题目5 选项': "A.underscore the point that A Burial at Ornans violated certain conventions dominant in Courbet's Paris\nB.suggest that some aspects of Leleux's depictions of everyday life were less realistic than Courbet's depictions of such subjects\nC.raise the possibility that Leleux was influenced by Courbet in his choice of subject matter for some of his paintings\nD.identify an aspect of peasant life that some of Courbet's contemporaries found appealing as subject matter for paintings\nE.highlight some ways in which A Burial at Ornans resembled the work of other painters working in the Realist mode ", 'section4 题目5 答案': 'A', 'section4 题目6 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '单空', 'section4 题目6 阅读文章（没有为空）': "The scandal caused by Gustave Courbet's 1850 painting A Burial at Ornans cannot be attributed to its subject-other artists' depictions of regional life had gained acceptance in Paris art circles-or to critics' assessments of Courbet's skill. Rather, by representing an ordinary burial in a provincial town on the large scale normally reserved for prestigious history paintings, Courbet had departed from a polite kind of Realism that had only recently become acceptable, where both the subject-virtuous peasant life-and the dimensions were modest. Courbet sought to do something more ambitious than a painter like Leleux, who depicted everyday life faithfully and without exaggeration: Courbet wished to paint his contemporaries with the seriousness normally reserved for kings and heroes.", 'section4 题目6 题干': '6.In the context in which it appears, "seriousness" most nearly means', 'section4 题目6 选项': 'A.danger\nB.gravity\nC.grimness\nD.learnedness\nE.genuineness', 'section4 题目6 答案': 'B', 'section4 题目7 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '单空', 'section4 题目7 阅读文章（没有为空）': "In 1776, the state of New Jersey adopted a constitution that ignored gender in its suffrage clause, defining voters simply as adult residents worth at least fifty pounds. After 1776 women routinely participated in the state's electoral process, until, in 1807, the state legislature passed a law redefining voters solely as adult White male taxpaying citizens. Political historians have been perplexed by New Jersey's deviation from the established norm of exclusive male suffrage, finding no sign of public agitation either for or against the voting rights of women prior to their enfranchisement in 1776 or disenfranchisement in 1807. Consequently historians, downplaying the extent to which women actually voted, have treated female suffrage as the result of careless constitutional construction and viewed the 1807 disenfranchisement as a legislative effort to remedy this carelessness. Yet examination of revolutionary-era manuscripts indicates that the 1776 suffrage clause underwent close legislative scrutiny that led to several significant changes; thus, the absence of gender references in the final version was probably not accidental. Indeed, the evidence suggests that New Jersey's legislators believed that all who possessed sufficient net worth were entitled to vote. However, they also saw the net worth qualification as serving to prevent an overdemocratization of the voting process.", 'section4 题目7 题干': '7.The author of the passage takes the "significant changes" to be an indication of which of the following?', 'section4 题目7 选项': 'A.That the 1776 suffrage clause was not established without critical examination\nB.That there was little consensus among legislators regarding the final version of the 1776 suffrage clause\nC.That the 1776 suffrage clause was not a deviation from the norm that prevailed in other states\nD.That there was at least some public agitation in favor of voting rights for women prior to 1776\nE.That legislators in 1776 were seriously concerned about the overdemocratization of the voting process', 'section4 题目7 答案': 'A', 'section4 题目8 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '', 'section4 题目8 阅读文章（没有为空）': "In 1776, the state of New Jersey adopted a constitution that ignored gender in its suffrage clause, defining voters simply as adult residents worth at least fifty pounds. After 1776 women routinely participated in the state's electoral process, until, in 1807, the state legislature passed a law redefining voters solely as adult White male taxpaying citizens. Political historians have been perplexed by New Jersey's deviation from the established norm of exclusive male suffrage, finding no sign of public agitation either for or against the voting rights of women prior to their enfranchisement in 1776 or disenfranchisement in 1807. Consequently historians, downplaying the extent to which women actually voted, have treated female suffrage as the result of careless constitutional construction and viewed the 1807 disenfranchisement as a legislative effort to remedy this carelessness. Yet examination of revolutionary-era manuscripts indicates that the 1776 suffrage clause underwent close legislative scrutiny that led to several significant changes; thus, the absence of gender references in the final version was probably not accidental. Indeed, the evidence suggests that New Jersey's legislators believed that all who possessed sufficient net worth were entitled to vote. However, they also saw the net worth qualification as serving to prevent an overdemocratization of the voting process.", 'section4 题目8 题干': '8.Which of the following best describes the function of the last sentence of the passage?', 'section4 题目8 选项': 'A.To suggest that New Jersey legislators in 1776 were insincere in their commitment to voting rights for women\nB.To indicate that there was a lack of consensus among New Jersey legislators regarding the final version of the 1776 suffrage clause\nC.To indicate that the New Jersey legislators in 1776 did not favor unqualified access to voting rights\nD.To undermine the evidence suggesting that New Jersey legislators in 1776 believed that all who possessed sufficient net worth were entitled to vote\nE.To suggest that the absence of gender references in the final version of the 1776 suffrage clause may have been accidental', 'section4 题目8 答案': 'C', 'section4 题目9 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '', 'section4 题目9 阅读文章（没有为空）': "In 1776, the state of New Jersey adopted a constitution that ignored gender in its suffrage clause, defining voters simply as adult residents worth at least fifty pounds. After 1776 women routinely participated in the state's electoral process, until, in 1807, the state legislature passed a law redefining voters solely as adult White male taxpaying citizens. Political historians have been perplexed by New Jersey's deviation from the established norm of exclusive male suffrage, finding no sign of public agitation either for or against the voting rights of women prior to their enfranchisement in 1776 or disenfranchisement in 1807. Consequently historians, downplaying the extent to which women actually voted, have treated female suffrage as the result of careless constitutional construction and viewed the 1807 disenfranchisement as a legislative effort to remedy this carelessness. Yet examination of revolutionary-era manuscripts indicates that the 1776 suffrage clause underwent close legislative scrutiny that led to several significant changes; thus, the absence of gender references in the final version was probably not accidental. Indeed, the evidence suggests that New Jersey's legislators believed that all who possessed sufficient net worth were entitled to vote. However, they also saw the net worth qualification as serving to prevent an overdemocratization of the voting process.", 'section4 题目9 题干': '9.The author of the passage suggests that if there had been public agitation regarding voting rights for women in New Jersey prior to1776, then this agitation would have', 'section4 题目9 选项': "A.been largely in opposition to voting rights for women rather than in favor of those rights\nB.exerted an important influence on the final version of the 1776 New Jersey suffrage clause\nC.potentially provided historians with an explanation for the New Jersey legislature's decision in 1776 regarding voting rights\nD.made New Jersey's political culture less unusual in comparison to other states\nE.made it less likely that New Jersey would disenfranchise women sometime after 1776", 'section4 题目9 答案': 'C', 'section4 题目10 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '六选二', 'section4 题目10 阅读文章（没有为空）': '', 'section4 题目10 题干': '10.The ocean surf zone is a very______ research setting: it is almost impossible to install and maintain instruments that will give valid readings there. （选出2个正确选项）', 'section4 题目10 选项': 'A.unpredictable\nB.prosaic\nC.worthwhile\nD.hostile\nE.pedestrian\nF.inhospitable', 'section4 题目10 答案': 'DF', 'section4 题目11 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '六选二', 'section4 题目11 阅读文章（没有为空）': '', 'section4 题目11 题干': "11.In contrast to the novel's scenic realism and precise characterization is its persistent philosophical______.（选出2个正确选项）", 'section4 题目11 选项': 'A.naturalism\nB.abstraction\nC.generality\nD.impartiality\nE.sincerity\nF.objectivity', 'section4 题目11 答案': 'BC', 'section4 题目12 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '六选二', 'section4 题目12 阅读文章（没有为空）': '', 'section4 题目12 题干': '12.  It is possible to mistake the constant stimulation offered by the Internet for ______: we can come to believe that if we are busy, we are focused. （选出2个正确选项）', 'section4 题目12 选项': 'A. amusement\nB. involvement\nC. progress\nD. engagement\nE. productivity\nF. improvement', 'section4 题目12 答案': 'BD', 'section4 题目13 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '阅读单选', 'section4 题目13 阅读文章（没有为空）': 'Many tadpoles live in temporary ponds-ponds that dry up for part of each year. When the dry season comes, those tadpoles that have not yet developed into frogs die. A tadpole can only develop rapidly if it spends much of its time feeding. generally by scraping food off decaying leaves. Nevertheless, those tadpoles in a temporary pond that spend the most time feeding have relatively poor chances of developing into frogs.', 'section4 题目13 题干': '13. which of the following, if true, most helps to explain the poor survival rate of the tadpoles that spend the greatest amount of time feeding?', 'section4 题目13 选项': 'A.The animals that eat tadpoles in temporary ponds tend to be much smaller than those that cat tadpoles in permanent ponds.\nB.The animals that eat tadpoles can only locate their prey when the tadpoles are moving.\nC.Some ponds that support populations of tadpoles dry up in some years and not in others.\nD.Some of the animals that prey on tadpoles in permanent ponds cannot survive in temporary ponds.\nE.Frogs that as tadpoles grew up in temporary ponds do not survive to reproduce unless they can live for long periods without a pond nearby.', 'section4 题目13 答案': 'B', 'section4 题目14 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '阅读单选', 'section4 题目14 阅读文章（没有为空）': "Astronomers who study planet formation once believed that comets---because they remain mostly in the distant Oort cloud, where temperatures are close to absolute zero--must be pristine relics of the material that formed the outer planets. The conceptual shift away from seeing comets as pristine relics began in the 1970s，when laboratory simulations revealed there was sufficient ultraviolet radiation reaching comets to darken their surfaces and there were sufficient cosmic rays to alter chemical bonds or even molecular structure near the surface. Nevertheless, astronomers still believed that when a comet approached the Sun--where they could study it一the Sun's intense heat would remove the corrupted surface layer, exposing the interior. About the same time, though, scientists realized comets might contain decaying radioactive isotopes that could have warmed cometary interiors to temperatures that caused the interiors to evolve.", 'section4 题目14 题干': '14. The author suggests that the realization described in the final sentence of the passage had which of the following effects?', 'section4 题目14 选项': "A. It introduced a new topic for study by astronomers interested in planetary formation.\nB. It led astronomers to adopt a number of different strategies in trying to determine the composition of cometary interiors.\nC. It called into question an assumption that astronomers had made about comets.\nD. It cast doubt on astronomers' ability to study the interior parts of comets.\nE. It caused astronomers to revise their account of the composition of the outer planets.", 'section4 题目14 答案': 'C', 'section4 题目15 类型（单空，双空，三空，六选二，阅读单选，阅读多选，阅读选句子）': '阅读多选', 'section4 题目15 阅读文章（没有为空）': "Astronomers who study planet formation once believed that comets---because they remain mostly in the distant Oort cloud, where temperatures are close to absolute zero--must be pristine relics of the material that formed the outer planets. The conceptual shift away from seeing comets as pristine relics began in the 1970s，when laboratory simulations revealed there was sufficient ultraviolet radiation reaching comets to darken their surfaces and there were sufficient cosmic rays to alter chemical bonds or even molecular structure near the surface. Nevertheless, astronomers still believed that when a comet approached the Sun--where they could study it一the Sun's intense heat would remove the corrupted surface layer, exposing the interior. About the same time, though, scientists realized comets might contain decaying radioactive isotopes that could have warmed cometary interiors to temperatures that caused the interiors to evolve.", 'section4 题目15 题干': '15. It can be inferred that the author would agree with which of the following statement about the “laboratory simulations” （不定项选择题，答案个数不一定，选出所有可能正确的选项）', 'section4 题目15 选项': 'A. The simulations showed that despite the low temperatures in a Oort cloud, there was sufficient energy there to other comets.\nB. Astronomers were initially reluctant to accept what the simulation showed about the composition of comet.\nC. The simulations themselves did not eliminate the possibility that comets contain pristine relics of material from the early solar systems.', 'section4 题目15 答案': 'AC', 'section5 题目1 类型（单选，多选，填空）': '单选', 'section5 题目1 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-1.png', 'section5 题目1 选项个数（填数字）': '4', 'section5 题目1 答案': 'B', 'section5 题目2 类型（单选，多选，填空）': '单选', 'section5 题目2 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-2.png', 'section5 题目2 选项个数（填数字）': '4', 'section5 题目2 答案': 'D', 'section5 题目3 类型（单选，多选，填空）': '单选', 'section5 题目3 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-3.png', 'section5 题目3 选项个数（填数字）': '4', 'section5 题目3 答案': 'C', 'section5 题目4 类型（单选，多选，填空）': '单选', 'section5 题目4 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-4.png', 'section5 题目4 选项个数（填数字）': '4', 'section5 题目4 答案': 'A', 'section5 题目5 类型（单选，多选，填空）': '单选', 'section5 题目5 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-5.png', 'section5 题目5 选项个数（填数字）': '4', 'section5 题目5 答案': 'D', 'section5 题目6 类型（单选，多选，填空）': '单选', 'section5 题目6 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-6.png', 'section5 题目6 选项个数（填数字）': '5', 'section5 题目6 答案': 'C', 'section5 题目7 类型（单选，多选，填空）': '单选', 'section5 题目7 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-7.png', 'section5 题目7 选项个数（填数字）': '5', 'section5 题目7 答案': 'B', 'section5 题目8 类型（单选，多选，填空）': '单选', 'section5 题目8 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-8.png', 'section5 题目8 选项个数（填数字）': '5', 'section5 题目8 答案': 'C', 'section5 题目9 类型（单选，多选，填空）': '单选', 'section5 题目9 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-9.png', 'section5 题目9 选项个数（填数字）': '5', 'section5 题目9 答案': 'C', 'section5 题目10 类型（单选，多选，填空）': '填空', 'section5 题目10 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-10.png', 'section5 题目10 选项个数（填数字）': ' ', 'section5 题目10 答案': '-0.75', 'section5 题目11 类型（单选，多选，填空）': '单选', 'section5 题目11 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-11.png', 'section5 题目11 选项个数（填数字）': '5', 'section5 题目11 答案': 'B', 'section5 题目12 类型（单选，多选，填空）': '多选', 'section5 题目12 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-12.png', 'section5 题目12 选项个数（填数字）': '5', 'section5 题目12 答案': 'ACE', 'section5 题目13 类型（单选，多选，填空）': '单选', 'section5 题目13 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-13.png', 'section5 题目13 选项个数（填数字）': '5', 'section5 题目13 答案': 'A', 'section5 题目14 类型（单选，多选，填空）': '单选', 'section5 题目14 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-14.png', 'section5 题目14 选项个数（填数字）': '5', 'section5 题目14 答案': 'E', 'section5 题目15 类型（单选，多选，填空）': '', 'section5 题目15 题目（填路径）': 'paper_source\\question_pictures\\入学测试\\2-15.png', 'section5 题目15 选项个数（填数字）': '', 'section5 题目15 答案': '9'},
1,1)

    root.mainloop()


