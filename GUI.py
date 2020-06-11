# -*- coding: utf-8 -*-
from tkinter import *
import serial
import time
import threading

LOG_LINE_NUM = 0
PRINT_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("无人机集群地面站程序")           #窗口名
        # self.init_window_name.geometry('320x160+10+10')  # 290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1000x550+10+10')
        # self.init_window_name["bg"] = "CornflowerBlue"  #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)        #虚化，值越小虚化程度越高

        self.flag_point = 1
        self.ser1 = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)

        #标签名称
        self.init_data_label = Label(self.init_window_name, text="任务航点列表")
        self.init_data_label.grid(row=2, column=0)
        self.result_data_label = Label(self.init_window_name, text="操作反馈")
        self.result_data_label.grid(row=10, column=0)
        self.log_label = Label(self.init_window_name, text="无人机群实时监控")
        self.log_label.grid(row=0, column=8)
        self.j_label = Label(self.init_window_name, text="经度.后6位")
        self.j_label.grid(row=0, column=1)
        self.w_label = Label(self.init_window_name, text="纬度.后6位")
        self.w_label.grid(row=0, column=0)
        self.h_label = Label(self.init_window_name, text="高度")
        self.h_label.grid(row=0, column=2)
        #文本框
        self.point_show = Listbox(self.init_window_name, width=40, height=10)  #任务航点显示框
        self.point_show.grid(row=3, column=0, rowspan=6, columnspan=5)
        self.result_data_Text = Text(self.init_window_name, width=60, height=11)  #处理结果显示
        self.result_data_Text.grid(row=11, column=0, columnspan=6)
        self.log_data_Text = Text(self.init_window_name, width=55, height=33)  # 无人机群实时监控
        self.log_data_Text.grid(row=1, column=8, rowspan=20, columnspan=10)
        #输入
        self.vj = StringVar()
        self.vw = StringVar()
        self.vh = StringVar()
        self.point_set_w = Entry(self.init_window_name, width=12, textvariable=self.vw).grid(row=1, column=0)
        self.point_set_j = Entry(self.init_window_name, width=12, textvariable=self.vj).grid(row=1, column=1)
        self.point_set_h = Entry(self.init_window_name, width=5, textvariable=self.vh).grid(row=1, column=2)
        #按钮
        self.watch_button1 = Button(self.init_window_name, text="开启监视", bg="SeaShell", width=10,
                                       command=self.watch_all)  # 调用内部方法  加()为直接调用
        self.watch_button1.grid(row=0, column=9)
        # self.watch_button2 = Button(self.init_window_name, text="关闭监视", bg="LightGreen", width=10,
        #                                 command=self.watch_all_close)  # 调用内部方法  加()为直接调用
        # self.watch_button2.grid(row=1, column=9)

        self.add_point_button = Button(self.init_window_name, text="添加航点", bg="LightGreen", width=10,
                                              command=self.make_point)  # 调用内部方法  加()为直接调用
        self.add_point_button.grid(row=1, column=4)
        self.link_UAV = Button(self.init_window_name, text="连接主机", bg="Wheat", width=10,
                               command=self.send_link_main_uav)  # 调用内部方法  加()为直接调用
        self.link_UAV.grid(row=3, column=5)
        self.try_link= Button(self.init_window_name, text="开始组网", bg="Wheat", width=10,
                                              command=self.send_link_all)  # 调用内部方法  加()为直接调用
        self.try_link.grid(row=4, column=5)
        self.ask_link = Button(self.init_window_name, text="查询组网", bg="Wheat", width=10,
                               command=self.ask_uav_s)  # 调用内部方法  加()为直接调用
        self.ask_link.grid(row=5, column=5)
        self.set_point = Button(self.init_window_name, text="设定航点", bg="Lavender", width=10,
                               command=self.send_point)  # 调用内部方法  加()为直接调用
        self.set_point.grid(row=9, column=0)
        self.cancel_point = Button(self.init_window_name, text="清空航点", bg="Lavender", width=10,
                               command=self.clear_point)  # 调用内部方法  加()为直接调用
        self.cancel_point.grid(row=9, column=1)
        self.start_mission = Button(self.init_window_name, text="开始任务", bg="lightblue", width=10,
                                   command=self.send_mission_start)  # 调用内部方法  加()为直接调用
        self.start_mission.grid(row=6, column=5)
        self.cancel_mission = Button(self.init_window_name, text="取消任务", bg="Tomato", width=10,
                                   command=self.send_mission_cancel)  # 调用内部方法  加()为直接调用
        self.cancel_mission.grid(row=0, column=11)
        self.ask_mission = Button(self.init_window_name, text="任务进度", bg="lightblue", width=10,
                                     command=self.ask_mission_s)  # 调用内部方法  加()为直接调用
        self.ask_mission.grid(row=7, column=5)

        self.vm = IntVar()
        self.click_radio = Radiobutton(self.init_window_name, text='伴飞模式', variable=self.vm, value=0,)
        self.click_radio.grid(row=9, column=4)
        self.click_radio2 = Radiobutton(self.init_window_name, text='多任务模式', variable=self.vm, value=1,)
        self.click_radio2.grid(row=9, column=5)


    def make_point(self):
        j = self.vj.get()
        w = self.vw.get()
        h = self.vh.get()
        point = "%s:w%sj%sh%s" % (self.flag_point, w, j, h)
        self.point_show.insert(END, point)
        self.flag_point += 1

    def clear_point(self):
        self.point_show.delete(0, END)
        message = lora_pack("Cb", '01 01 1C')
        # self.print_to_Text(message)
        self.ser1.write(message)
        self.print_to_Text("[s] 航点双清完成")

    def send_point(self):
        for i in self.point_show.get(0, END):
            message0 = "Ca%s" % i[2:]
            message = lora_pack(message0, '01 01 1C')
            # self.print_to_Text(message)
            self.ser1.write(message)
            time.sleep(0.2)
        self.print_to_Text("[s] 航点任务设置完成")

    def send_link_main_uav(self):
        message = lora_pack("A1", '01 01 1C')
        # self.print_to_Text(message)
        self.ser1.write(message)
        self.print_to_Text("[s] 连接主无人机...")

    def send_link_all(self):
        message = lora_pack("A2", '01 01 1C')
        # self.print_to_Text(message)
        self.ser1.write(message)
        self.print_to_Text("[s] 开始尝试组网...")

    def ask_uav_s(self):
        message = lora_pack("B1", '01 01 1C')
        # self.print_to_Text(message)
        self.ser1.write(message)
        self.print_to_Text("[s] 已查询组网信息...")

    def ask_mission_s(self):
        message = lora_pack("B2", '01 01 1C')
        # self.print_to_Text(message)
        self.ser1.write(message)
        self.print_to_Text("[s] 已查询任务情况...")

    def send_mission_start(self):
        message = lora_pack("S1", '01 01 1C')
        # self.print_to_Text(message)
        self.ser1.write(message)
        self.print_to_Text("[s] 任务开始......")
        m = self.vm.get()
        if m == 1:
            message2 = lora_pack("M2", '01 01 1C')
            self.ser1.write(message2)
            self.print_to_Text("[s] 模式为M2")
        else:
            message2 = lora_pack("M1", '01 01 1C')
            self.ser1.write(message2)
            self.print_to_Text("[s] 模式为M1")


    def send_mission_cancel(self):
        message = lora_pack("S2", '01 01 1C')
        # self.print_to_Text(message)
        self.ser1.write(message)
        self.print_to_Text("[s] 任务取消......")


    #功能函数
    #获取当前时间戳并翻译
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    #实时反馈
    def print_to_Text(self,logmsg):
        global PRINT_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if PRINT_LINE_NUM <= 10:
            self.result_data_Text.insert(END, logmsg_in)
            PRINT_LINE_NUM = PRINT_LINE_NUM + 1
        else:
            self.result_data_Text.delete(1.0, 2.0)
            self.result_data_Text.insert(END, logmsg_in)

    def print_all_time(self):
        self.write_log_to_Text("123")

    def watch_all(self):
        global timer
        read1 = message_receive(self.ser1)
        if read1:
            self.write_log_to_Text(read1)
        timer = threading.Timer(0.5, self.watch_all)
        timer.start()



    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 40:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()
    test = MY_GUI(init_window)
    test.set_init_window()
    init_window.mainloop()

def lora_pack(message, target):
    new_line = '0D 0A'  # 使接收时readline不用等待超时500ms，更具效率
    message_hex = message.encode().hex()
    pack_hex_b = bytes.fromhex('%s%s%s' % (target, message_hex, new_line))
    return pack_hex_b


def message_receive(ser1):
    count = ser1.inWaiting()
    if count > 0:
        ser1.flush()
        recv = ser1.readline()
        recv1 = bytes.decode(recv)
        ser1.flushInput()
        message = recv1
        return message
    else:
        return 0







if __name__ == '__main__':

    gui_start()

