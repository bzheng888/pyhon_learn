import os, sys
import time
import random
import json
import pickle
import hashlib
import logging
import tkinter as tk
import re
window = tk.Tk()
window.title('计算器')
window.geometry('400x500')
symbol = ['+', '-', '*', '/','=', '7', '8', '9', '(',')', '4', '5', '6','%', 'Back', '1', '2', '3','0', 'C', '.']
'''
测试： 1-2*((60-30+(-40/5)*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))
'''
operator = {
    '+': lambda a, b: float(a) + float(b),
    '-': lambda a, b: float(a) - float(b),
    '*': lambda a, b: float(a) * float(b),
    '/': lambda a, b: float(a) / float(b),
}

def recover_symbol(exp):
    list = re.findall(r'(\+-|\*-|/-|--)', exp)
    if len(list) == 0:
        return exp
    exp = exp.replace('+-', '-')
    exp = exp.replace('--', '+')
    exp = exp.replace('*-', '<')
    exp = exp.replace('/-', '>')
    list = re.findall(r'[\+-]\d[\d.<>]+\d', exp)
    for li in list:
        tmp = li
        sum = li.count('>') + li.count('<')
        if sum % 2 != 0:
            if li[0] == '-':
                li = li.replace('-', '+')
            elif li[0] == '+':
                li = li.replace('+', '-')
        li = li.replace('<', '*')
        li = li.replace('>', '/')
        exp = exp.replace(tmp, li)
    print(exp)
    return exp

def compute_mul_div(exp):
    list = re.findall(r'[^\*/]+', exp)
    list_symbol = re.findall(r'[\*/]', exp)
    if len(list_symbol) == 0:
        return str(exp)
    i = 1
    j = 0
    tmp = list[0]
    while i < len(list):
        #print(tmp, list[i])
        tmp = str(operator[list_symbol[j]](tmp, list[i]))
        i += 1
        j += 1
    return tmp

def compute_add_min(exp):
    list = re.findall(r'[^\+-]+', exp)
    list_symbol = re.findall(r'[\+-]', exp)
    if list_symbol == None:
        return str(list)
    j = 0
    if exp[0] == '-' or exp[0] == '+':
        tmp = '0'
        i = 0
    else:
        tmp = list[0]
        i = 1
    while i < len(list):
        tmp = str(operator[list_symbol[j]](tmp, list[i]))
        i += 1
        j += 1
    return tmp

def compute_base_opt(exp):
    tmp = exp
    while True:
        obj = re.search(r'(\*|/)', tmp)
        if obj == None:
            a_e = re.search(r'[^()]+', tmp)#去掉括号
            ans = compute_add_min(a_e.group())
            return str(ans) #返回结果（不带括号）
        list = re.findall(r'[^()\+-]+', tmp) #匹配乘除法
        for li in list:
            ans = compute_mul_div(li) #先处理乘除法
            tmp = tmp.replace(str(li), ans)#替换字符串
def compute(exp):
    tmp = exp
    while True:
        list = re.findall(r'\([^()]+\)', tmp)##处理内层括号
        if len(list) == 0: #处理最后括号的表达式
            tmp_t = recover_symbol(tmp)
            ans = compute_base_opt(tmp_t)
            return str(ans)
        for li in list:
            pre_li = re.search(r'[^()]+', li)
            ans = recover_symbol(pre_li.group())
            li_tmp = li.replace(pre_li.group(), ans)
            print(li_tmp)
            ans = compute_base_opt(li_tmp)
            tmp = tmp.replace(str(li), ans)


def input_wrong(exp):
    brackets = []
    i = 0
    while i < len(exp):
        if exp[i] == '(':
            brackets.append('(')
        if exp[i] == ')':
            try:
                brackets.pop()
            except:
                return False
        i += 1
    try:
        brackets.pop()
    except:
        return True
    return False
def get_answer(exp):
    res = input_wrong(exp)
    if res == False:
        print("Invalid input.")
        entry.delete(0, 'end')
    else:
        ans = compute(exp)
        entry.delete(0, 'end')
        entry.insert('insert', ans)
    return
def button_press(arg):
    if arg == 'Back':
        index = entry.index('insert')
        entry.delete(index - 1, index)
        pass
    elif arg == 'C':
        entry.delete(0, 'end')
        pass
    elif arg == '=':
        exp = entry.get()
        get_answer(exp)
        pass
    else:
        entry.insert('insert', arg)
    return

button_number = []
cnt = 1
entry = tk.Entry(window, font = ('Arial', 14), bg = '#FAEBD7')
entry.place(x = 0, y = 0, width = 400, height = 260)
i = 0
j = 0
for c in symbol:
    b = tk.Button(window, text=c, font=('Arial', 12), command = lambda arg = c:button_press(arg))
    b.place(x = 80 * (i % 5), y = 260 + 60 * (j // 5) , width = 80, height = 60)
    if not c.isdigit():
        b.configure(bg="#B0C4DE")
    button_number.append(b)
    i += 1
    j += 1
window.mainloop()