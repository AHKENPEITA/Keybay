#待完善：
#0.漏洞：账户数量/菜单选项数量>10时存在漏洞（目前的想法是分页列出，超过10以后就构建一个多页菜单，用[n]或[p]来翻页）
#1.校验码4位（大小写、数字两位）
#2.import统一到开头
#3.允许用户设置默认账户直接使用（c页）
#4.允许用户跳过开机动画（c页）
#5.允许用户选择直接复制还是打印出来（c页）
#6.完善著作权页（i页）
#7.完善使用引导（h页）
#8.创建用户时检查是否重名



import os
import pickle

#自定义类

class Account:#账户信息类
    def __init__(self,arg_name,arg_key,arg_digit,arg_text) -> None:
        self.name = arg_name
        self.key = arg_key
        self.digit = arg_digit
        self.text = arg_text

class Text:#密文信息类
    def __init__(self,arg_lines_list) -> None:#把所有段落集合成一个列表用来生成Text实例
        self.lines_list = arg_lines_list
        pass

    def line_count(self):#返回密文段落总数
        return len(self.lines_list)

    def char_count(self,line_number):#返回密文指定段落字符总数
        if line_number<self.line_count():
            return len(self.lines_list[line_number])
        else:
            return None

    def get_lines_list(self):
        return self.lines_list
    
class Printer:#集成了时停、自定义前缀、输入、选择、判断、特殊效果等功能的print方法类
  
    def __init__(self,arg_prefix) -> None:
        self.prefix = str(arg_prefix+"> ")

    def pause(self,*second):#使输出暂停一小会，让用户有连续感
        import time
        if len(second)==0:
            time.sleep(0.08)
        else:
            time.sleep(second[0])

    def wait(self):
        self.input("按回车(Enter)继续——>")

    def loading(self):#加载进度条，起到时间和空间上的分隔效果
        import sys
        import time
        def print_star(arg_count,arg_seconds):
            for i in range(arg_count):
                sys.stdout.write('=')
                sys.stdout.flush()
                time.sleep(arg_seconds)
        print_star(40,0.01)
        print()

    def print(self,arg_prompt):#不带前缀的打印
        self.pause()
        print(arg_prompt)

    def pre_print(self,arg_prompt):#带前缀打印
        self.pause()
        print(self.prefix+arg_prompt)

    def input(self,arg_prompt):#输入节点
        self.pause()
        return input(self.prefix+arg_prompt)
    
    def hidden_input(self,arg_prompt):#######################
        self.pause()
        import msvcrt
        import sys
        print(arg_prompt, end='', flush=True)
        chars = []
        while True:
            new_char = msvcrt.getch()
            if new_char in [b'\r', b'\n']:
                break
            elif new_char == b'\x08':  # 处理退格键
                if chars:
                    chars.pop()
                    # 清空当前行
                    sys.stdout.write('\r')
                    sys.stdout.write(' ' * 2*len(arg_prompt + ''.join(chars)) + '\r')
                    sys.stdout.write(arg_prompt + '*'*len(chars))
                    sys.stdout.flush()
                    

            else:
                chars.append(new_char.decode())
                sys.stdout.write('*')
                sys.stdout.flush()
        print()
        return ''.join(chars)

    def check(self,arg_prompt):#判断节点，根据输入'y'或'n'来返回true或false
        while True:
            flag = self.input(f""+arg_prompt+"[y/n]:")
            if flag =='y':
                return True
            elif flag =='n':
                return False
            else:
                self.pre_print("指令无法识别，请用'y'或'n'输入！")

    def select(self,*arg_prompts):#选择节点，第一个参数是提问,随后的是选项，选项至少有一个，以int类型返回用户选择
        if not len(arg_prompts)>=2:#Debug
            self.log_error(f"输入了无法进行选择的参数数量:"+str(len(arg_prompts))+"个, log_error()方法需要至少2个参数!")
        else:
            while True:
                self.pre_print(arg_prompts[0]) 
                for i in range(1,len(arg_prompts)):
                    self.pre_print(f"["+str(i)+"]:"+arg_prompts[i])
                ans = input()
                if not ans.strip():
                    self.pre_print("选项不能为空！")
                elif not ans.isdigit():
                    self.pre_print("检测到非法输入！请使用数字进行选择！")
                elif not int(ans) in range(1,len(arg_prompts)):
                    self.pre_print("选项超出范围！请输入一个在以上选项中列出的数字！")
                else:
                    return(int(ans))

    def select_2(self,arg_prompt,arg_options,*arg_break):#带跳出选项的选择节点，以char类型返回用户选择（即选项名字），参数分别是提词、常规选项、跳出选项
        if len(arg_break)==0:#无跳出循环需求
            while True:
                self.pre_print(arg_prompt)
                for i in range(len(arg_options)):
                    self.pre_print(f"["+str(i+1)+"]:"+arg_options[i])
                ans = input()
                if not ans.strip():
                    self.pre_print("选项不能为空！")
                elif not ans.isdigit():
                    self.pre_print("检测到非法输入！请使用数字进行选择！")
                elif not int(ans)-1 in range(len(arg_options)):
                    self.pre_print("选项超出范围！请输入一个在以上选项中列出的数字！")
                else:
                    #self.pre_print(f"选中["+ans+"]:"+arg_options[int(ans)-1])
                    return(arg_options[int(ans)-1])
        elif len(arg_break)==1:#有跳出循环需求
            while True:
                self.pre_print(arg_prompt)
                for i in range(len(arg_options)):
                    self.pre_print(f"["+str(i+1)+"]:"+arg_options[i])
                self.pre_print(f"[0]:"+arg_break[0])
                ans = input()
                if not ans.strip():
                    self.pre_print("选项不能为空！")
                elif not ans.isdigit():
                    self.pre_print("检测到非法输入！请使用数字进行选择！")
                elif not int(ans)-1 in range(len(arg_options)):
                    if int(ans)==0:
                        #self.pre_print(f"选中[0]:"+arg_break[0])
                        return(arg_break[0])
                    else:
                        self.pre_print("选项超出范围！请输入一个在以上选项中列出的数字！")
                else:
                    #self.pre_print(f"选中["+ans+"]:"+arg_options[int(ans)-1])
                    return(arg_options[int(ans)-1])

    def print_line(self,arg_list):#把list中所有char集中在一行打印输出
        line = ""
        for char in arg_list:
            line = line+char
        self.print(line)

    def print_lines(self,arg_list):#把list中所有str按行打印输出
        for i in range(len(arg_list)):
            self.print(arg_list[i])

    def log_error(self,arg_message):#输出错误信息并无限停机
        def count_chinese_characters(input_str):#检测中文字符数量（所有中文字符对应两个*）
            count = 0
            for char in input_str:
                if '\u4e00' <= char <= '\u9fff':
                    count += 1
            return count
        mes_len = len(arg_message)+count_chinese_characters(arg_message)
        self.print("*"*mes_len)
        self.print(arg_message)
        self.print("*"*mes_len)
        import time
        while True:
            time.sleep(1)  # 无限暂停
            pass


class Getter:#集成的获取用户输入信息的方法类

    def __init__(self,arg_printer) -> None:
        self.printer = arg_printer
        pass

    def get_name(self):#获取用户名，强制获取
        while True:
            name_input = self.printer.input("请输入用户名：")
            if not name_input.strip():
                self.printer.pre_print("用户名不能为空！")
            else:
                return name_input

    def get_digit(self):#获取密码位数（创建用户时Call，非强制获取）
        while True:
            key_input = self.printer.input("请输入希望生成密码的位数（范围是8-36，留空则是默认值12）：")
            if not key_input.strip():
                self.printer.pre_print("留空，选择默认值12")
                return 12
            elif not key_input.isdigit():
                self.printer.pre_print("输入的不是阿拉伯数字！请输入一个8-36范围内的阿拉伯数字，或留空以使用默认值12")
            elif int(key_input)<8:
                self.printer.pre_print("位数过小，无法保证安全性，请输入8-36间的数字！")
            elif int(key_input)>36:
                self.printer.pre_print("位数过大，超过密码长度上限，请输入8-36间的数字！")
            else:
                self.printer.pre_print(f"选中的密码位数是："+key_input)
                return int(key_input)

    def get_key(self):#获取密钥（创建用户时Call，非强制获取）###需升级：用户使用时Call，强制获取
        while True:
            key_input = self.printer.input("请输入密钥,或者留空以待使用时自行填入：")
            if not key_input.strip():
                self.printer.pre_print("密钥留空")
                return None
            elif not key_input.isdigit():
                self.printer.pre_print("输入的不是纯阿拉伯数字！若要定义密钥，请输入一串4-36位的纯阿拉伯数字，若不定义密钥，请留空")
            elif len(key_input)<4:
                self.printer.pre_print("密钥过短！若要定义密钥，请输入一串4-36位的阿拉伯数字")
            elif len(key_input)>36:
                self.printer.pre_print("密钥过长！若要定义密钥，请输入一串4-36位的阿拉伯数字")
            else:
                self.printer.pre_print(f"密钥是："+key_input)
                return key_input

    def get_key_force(self):#获取密钥(用户使用时Call，强制获取)
        while True:
            key_input = self.printer.input("请输入密钥：")
            if not key_input.strip():
                self.printer.pre_print("密钥不能为空！")
            elif not key_input.isdigit():
                self.printer.pre_print("输入的不是纯阿拉伯数字！若要定义密钥，请输入一串4-36位的纯阿拉伯数字！")
            elif len(key_input)<4:
                self.printer.pre_print("密钥过短！若要定义密钥，请输入一串4-36位的阿拉伯数字")
            elif len(key_input)>36:
                self.printer.pre_print("密钥过长！若要定义密钥，请输入一串4-36位的阿拉伯数字")
            else:
                return key_input

    def get_text(self):#获取密文内容，强制获取

        def input_is_directory(lines_list):#判断输入是地址还是文段

            def contains_special_chars(text):#检查一段字符串是否是路径（是否包含/、\、：）
                special_chars = {'/', '\\', ':'}
                for char in text:
                    if char in special_chars:
                        return True
                return False
            
            result = False
            for line in lines_list:
                if contains_special_chars(line):
                    result = True
            return result

        def directory_is_leagal_txt(arg_directory):#判断目标路径是否是合法的txt文档路径（路径是否存在，路径是否是txt文档）

            def is_txt_file(file_path):#检验路径指向的文件是否是txt文档
                # 获取文件扩展名并转换为小写字母
                ext = os.path.splitext(file_path)[1].lower()
                return ext == '.txt'
            
            if not os.path.exists(arg_directory):
                self.printer.pre_print(f"目录"+arg_directory+"不存在！")
                return False
            elif not is_txt_file(arg_directory):
                self.printer.pre_print(f""+arg_directory+"不是一个txt文档")
                return False
            else:
                self.printer.pre_print("从该地址读取密文")
                return True
        
        def read_lines_from_directory(arg_directory):  # 从合法的指定目录读取txt文档并生成Text类
            with open(arg_directory, 'rt', encoding='utf-8') as file:  # 打开txt文件并按行读取内容为列表，指定编码为utf-8
                file_lines = file.readlines()

            for i in range(len(file_lines)):  # 使用strip()方法去除每行末尾的换行符
                file_lines[i] = file_lines[i].strip()
            return file_lines

        def remove_non_alphanumeric(input_str):# 使用列表推导式来遍历字符串中的每个字符，只保留大小写字母和阿拉伯数字
            cleaned_str = ''.join(char for char in input_str if char.isalnum())
            return cleaned_str

        def remove_empty_lines(input_list):
            # 使用列表推导式遍历输入列表，跳过空行元素
            cleaned_list = [line for line in input_list if line.strip() != '']
            return cleaned_list

        while True:
            self.printer.pre_print("请输入文档的地址，也可以直接粘贴文档内容。程序将会根据你输入的信息自动识别文档信息。")
            self.printer.pre_print("输入方法：请粘贴文本，然后换行，按 Ctrl + Z(Windows)或Ctrl + D(Linux/macOS),再按回车(Enter)来结束输入:")
            # 逐行读取输入并存储在列表中
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:  # 捕获输入结束的异常
                pass
            except KeyboardInterrupt:  # 捕获^C导致的KeyboardInterrupt异常
                self.printer.pre_print("输入被中断")
            # 使用 splitlines() 方法按行分割输入内容
            lines_list = '\n'.join(lines).splitlines()
            lines_list = remove_empty_lines(lines_list)

            if len(lines_list)==0:
                self.printer.pre_print("输入不能为空，请重新输入！")
            else:
                if input_is_directory(lines_list):
                    if directory_is_leagal_txt(lines_list[0]):
                        lines = read_lines_from_directory(lines_list[0])
                        lines = remove_empty_lines(lines)
                else:
                    lines = lines_list



                for i in range(len(lines)):
                    lines[i] = remove_non_alphanumeric(lines[i])
                text = Text(lines)
                return text

    def get_operator(self):#获取运营商名称，强制获取
        while True:
            operator_input = self.printer.input("请输入运营商名称：")
            if not operator_input.strip():
                self.printer.pre_print("运营商名称不能为空！")
            else:
                return operator_input

#通用小功能

def copy(arg_str):#复制到剪贴板
    import pyperclip
    pyperclip.copy(arg_str)

def create_directory(arg_printer,whole_directory):#创建指定目录
    try:
        os.mkdir(whole_directory)
        arg_printer.pre_print(f"目录'{whole_directory}'已创建.")
    except FileExistsError:
        arg_printer.pre_print(f"目录 '{whole_directory}' 已存在.")

def generate_directory(relative_path):#根据相对路径生成绝对路径
    current_directory = os.path.dirname(os.path.abspath(__file__))  # 获取软件所在目录
    directory = os.path.join(current_directory, relative_path)#生成绝对目录
    return directory




#以下是运行阶段

def start_animation():#标题和著作权页
    printer = Printer('主函数')
    LOGO = [
' .----------------.  .----------------.  .----------------.  .----------------.  .----------------.  .----------------. ',
'| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |',
'| |  ___  ____   | || |  _________   | || |  ____  ____  | || |   ______     | || |      __      | || |  ____  ____  | |',
'| | |_  ||_  _|  | || | |_   ___  |  | || | |_  _||_  _| | || |  |_   _ \    | || |     /  \     | || | |_  _||_  _| | |',
'| |   | |_/ /    | || |   | |_  \_|  | || |   \ \  / /   | || |    | |_) |   | || |    / /\ \    | || |   \ \  / /   | |',
'| |   |  __ \    | || |   |  _|  _   | || |    \ \/ /    | || |    |  __ \   | || |   / ____ \   | || |    \ \/ /    | |',
'| |  _| |  \ \_  | || |  _| |___/ |  | || |    _|  |_    | || |   _| |__) |  | || | _/ /    \ \_ | || |    _|  |_    | |',
'| | |____||____| | || | |_________|  | || |   |______|   | || |  |_______/   | || ||____|  |____|| || |   |______|   | |',
'| |              | || |              | || |              | || |              | || |              | || |              | |',
'| `--------------` || `--------------` || `--------------` || `--------------` || `--------------` || `--------------` |',
' `----------------`  `----------------`  `----------------`  `----------------`  `----------------`  `----------------` '
    ]
    printer.print_lines(LOGO)
    printer.pre_print('https://github.com/AHKENPEITA/Keybay.git')


    printer.wait()

def self_inspection():#启动自检###施工中
    printer = Printer('主函数')
    printer.loading()
    config_directory = generate_directory(config_relative_path)
    account_directory = generate_directory(account_relative_path)
    if not os.path.exists(config_directory): 
        printer.pre_print("未找到配置文件，即将自动创建")
        if printer.check('检测到您是第一次使用该程序，是否想要观看功能介绍？'):
            introduce()
            printer.loading()
    
    printer.pre_print("正在加载配置")
    printer.wait()

def main_manue_loop():#主菜单循环
    def check_account():#加载账户信息
        if not os.path.exists(account_directory): 
            return -1       # 没有账户目录
        else:
            contents = os.listdir(account_directory)
            if not contents:  
                return 0    # 有账户目录但没有账户
            else:
                return 1    # 有账户目录且有账户

    while True:#选项循环
        printer = Printer("菜单页面")
        printer.loading()
        account_check = check_account()
        manue_options = []
        match account_check:
            case -1:
                manue_options = ['建立账户','匿名模式','设置界面']
            case 0:
                manue_options = ['新建账户','匿名模式','设置界面']
            case 1:
                manue_options = ['选择账户','新建账户','匿名模式','设置界面']

        match printer.select_2("选择你的操作:",manue_options,'退出程序'):
            case '建立账户':
                create_directory(printer,account_directory)
                creat_new_account()
            case '新建账户':
                creat_new_account()
            case '匿名模式':
                anonymous_mode()
            case '选择账户':
                select_account()
            case '设置界面':
                setting()
            case '退出程序':
                exit()

def creat_new_account():#创建用户通道
    
    def check_loop(arg_account):
        printer.loading()
        account_info_check = False
        while not account_info_check:
            printer.pre_print("以下是你的用户信息，请再次检查是否正确：")
            printer.pre_print(f"用户名："+arg_account.name)
            printer.pre_print(f"密码位数："+str(arg_account.digit))
            if arg_account.key ==None:
                printer.pre_print("密钥留空")
            else:
                printer.pre_print(f"密钥："+arg_account.key)
            printer.pre_print("密文内容：")
            printer.print_lines(arg_account.text.lines_list)

            if printer.check("以上用户信息是否正确？"):
                account_info_check = True
            else:
                match printer.select("需要修正哪一项？","用户名","密码位数","密钥","密文内容"):
                    case 1:
                        arg_account.name = getter.get_name()
                    case 2:
                        arg_account.digit = getter.get_digit()
                    case 3:
                        arg_account.key = getter.get_key()
                    case 4:
                        arg_account.text = getter.get_text()  
                printer.loading()
        return arg_account

    def save_account(arg_account):
        account_file_directory = os.path.join(generate_directory(account_relative_path),str(arg_account.name+".pkl"))
        printer.pre_print(f"账户储存为"+account_file_directory)
        with open(account_file_directory, 'wb') as file:
            pickle.dump(arg_account, file)
        
    printer = Printer("创建账户")
    getter = Getter(printer)
    printer.loading()

    name = getter.get_name()
    digit = getter.get_digit()
    key = getter.get_key()
    text = getter.get_text()

    account = check_loop(Account(name,key,digit,text))
    printer.pre_print("正在将账户信息存至目录...")
    save_account(account)
    printer.pre_print("创建成功！")

    if printer.check('直接以账户'+account.name+'开始使用？'):
        account_use(account)
    else:
        printer.pre_print("即将退回主菜单")

def use_loop(arg_printer,arg_text,arg_digit,arg_key):#生成密码循环
    def str2num_list(arg_str):
        def char2number(arg_char):
            char_map = {
                **{chr(ord('0') + i): i for i in range(10)},
                **{chr(ord('a') + i): i + 10 for i in range(26)},
                **{chr(ord('A') + i): i + 36 for i in range(26)}
            }
            return char_map.get(arg_char)
        result = []
        for char in arg_str:
            number = char2number(char)
            if number is not None:
                result.append(number)
            else:
                print(f"字符'{char}'无法转换为数字。")
        return result
 
    def num_list2str(arg_num_list):
        def num2char(arg_num):
            if arg_num in range(0,9):
                return chr((int(arg_num))+ord('0'))
            elif arg_num in range(10,35):
                return chr((int(arg_num)-10)+ord('a'))
            elif arg_num in range(36,62):
                return chr ((int(arg_num)-36)+ord('A'))
            else:
                print (arg_num)
                arg_printer.log_error('无法将数字转为字符')
        str = ''
        for num in arg_num_list:
            str = str+num2char(num)
        return str

    def char_cipher(char,arg_key):
        key = int(arg_key)
        if char.isupper():
            return chr((ord(char) - ord('A') + key) % 26 + ord('A'))
        elif char.islower():
            return chr((ord(char) - ord('a') + key) % 26 + ord('a'))
        elif char.isdigit():
            return (int(char) + key) % 10
        else:
            print("无法处理的字符类型")
            return None
        
    def char_list2str(char_list):
        str = ''
        for char in char_list:
            str = str+char
        return str


    def add_check_code(arg_password_char_list):#校验码（保证字符种类多样性以及验证密码正确性）
        def get_capital_check_char():
            code = 0
            for char in arg_password_char_list:
                if char.isupper():
                    code=((code+ord(char) - ord('Z')) %26)
            return chr((code-1)%26+ord('A'))
        
        def get_lowercase_check_char():
            code = 0
            for char in arg_password_char_list:
                if char.islower():
                    code=((code+ord(char) - ord('z')) %26)
            return chr((code-1)%26+ord('a'))

        def get_number_check_char():
            code = 0
            for char in arg_password_char_list:
                if char.isdigit():
                    code=((code+int(char))%10)
            return str(code)

        capital_check_char = get_capital_check_char()
        lowercase_check_char = get_lowercase_check_char()
        number_check_char = get_number_check_char()
        check_code = [capital_check_char, lowercase_check_char, number_check_char]
        return arg_password_char_list+check_code
   

    #获取必要信息
    getter = Getter(arg_printer)
    operator_name = getter.get_operator()
    opn_len = len(operator_name)#运营商名称字长
    opn_code = str2num_list(operator_name)#运营商名称字权列表
    opn_sum = sum(opn_code)#运营商名称字权总和值

    line_index = (opn_len*opn_sum-1)%arg_text.line_count()#使用第几行作为密码(从0计数)
    line_count = line_index+1#使用第几行作为密码(从1计数)
    print(line_count)

    char_index = (opn_sum-1)%arg_text.char_count(line_index)#使用该行的第几个字符作为密码开始字符(从0计数)
    char_count = char_index+1#使用该行的第几个字符作为密码开始字符(从1计数)
    print(char_count)

    #anonymous_printer.pre_print(f"第["+str(line_count)+"]行第["+str(char_count)+"]个字符开始数["+str(arg_digit)+"]位")

    #读取密文生成密码(不区分大小写方案)
    # password_char_list = []
    # for i in range(int(arg_digit)):
    #     password_char_list.append(arg_text.get_lines_list()[line_index][(i+char_index)%arg_text.char_count(line_index)])
    # for i in range (int(arg_digit-3)):#需要去掉3位校验码位置
    #     password_char_list[i] = char_cipher(password_char_list[i],arg_key[i%len(arg_key)])
    # add_check_code(password_char_list)

    #读取密文生成密码(区分大小写方案)
    password_char_list = []
    for i in range(int(arg_digit)):
        password_char_list.append(arg_text.get_lines_list()[line_index][(i+char_index)%arg_text.char_count(line_index)])

    password_str = ''.join(password_char_list)
    password_code = str2num_list(password_str)
    
    for i in range(int(arg_digit)):
        password_code[i] = (int(password_code[i])+int(arg_key[(i%len(arg_key))]))%62
    
    password_str = num_list2str(password_code)#将ASKII码转回字符

    password_char_list = add_check_code(list(password_str))
    password = ''.join(password_char_list)

    
    #依据配置设置启用该栏
    # anonymous_printer.pre_print("你的"+operator_name+"账户密码是:")
    # anonymous_printer.pre_print(password)

    copy(password)
    arg_printer.pre_print("密码已复制到剪贴板，请直接粘贴使用")

def anonymous_mode():#匿名使用通道
    printer = Printer("匿名模式")
    getter = Getter(printer)
    printer.loading()

    text = getter.get_text()
    digit = getter.get_digit()
    key = getter.get_key()
    use_loop(printer,text,digit,key)

    pass

def select_account():#选择账户通道

    def load_account():#加载账户
        contents = os.listdir(account_directory)
        account_list = []
        for file_name in contents:
            account_file_directory = os.path.join(account_directory,file_name)
            with open(account_file_directory, 'rb') as file:
                account_list.append(pickle.load(file))
        return account_list


    printer = Printer('选择账户')
    printer.loading()

    account_list =load_account()
    name_list = []
    for account in account_list:
        name_list.append(account.name)
    ans = printer.select_2('选择一个账户进行使用：',name_list,'回主菜单')
    if ans == '回主菜单':
        pass
    else:
        for account in account_list:
            if ans == account.name:
                account_use(account)
                break

def account_manage():#账户管理通道
    printer = Printer('账户管理')
    printer.loading()
    printer.pre_print('账户管理模式')
    printer.wait()

def account_use(arg_account):#用户使用通道
    printer = Printer('用户 '+arg_account.name)
    getter = Getter(printer)
    printer.loading()
    key = arg_account.key
    digit = arg_account.digit
    text = arg_account.text

    if key:
        printer.pre_print('预设的密钥为:'+key)
    else:
        printer.pre_print('用户未定义密钥，需要零时输入')
        key = getter.get_key_force()

    while True:
        use_loop(printer,text,digit,key)
        if not printer.check('继续以当前账户生成密码？'):
            break

def introduce():#功能介绍通道###施工中
    printer = Printer('功能介绍')
    printer.loading()
    printer.pre_print('以下是功能介绍：')
    printer.wait()

def setting():#设置界面通道，在这里调整配置和修改账户###施工中
    printer = Printer('设置界面')
    printer.loading()
    printer.pre_print('以下是设置界面：')
    printer.wait()

def exit():#退出程序
    printer = Printer('主函数')
    printer.pre_print("正在退出")
    printer.loading()
    quit()

# 以下是引导程序

global account_relative_path
global config_relative_path
account_relative_path = "account"  #账户目录相对路径
config_relative_path = "config" #配置目录相对路径

account_directory = generate_directory(account_relative_path)
start_animation()
self_inspection()
main_manue_loop()








