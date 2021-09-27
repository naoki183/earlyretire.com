#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 00:23:04 2021

@author: yoshidanaoki
"""

from flask import Flask, redirect, render_template, request
import numpy.random as rd

app = Flask(__name__)



@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/model1", methods=["GET", "POST"])
def retire1():
    if request.method == "GET":
        return render_template("model1.html")
    #model1は大企業，独身を想定
    elif request.method == "POST":
        
       
        #毎年の支出
        spending = int(request.form.get("spending"))
        #投資の年率(%表記)
        rate = int(request.form.get("rate"))
        #今の年齢
        age1 = int(request.form.get("age_now"))
        #定年の年齢
        age2 = 65
        age3 = int(request.form.get("age_end"))
        if age3 > age2:
            #死ぬときに残しておきたい金額
            endmoney = int(request.form.get("endmoney"))
            #リタイアした後の収入
            wage1 = int(request.form.get("wage"))
            #年金
            wage2 = 130
            wage = []
            for i in range(age2 - age1):
                wage.append(wage1)
            for i in range(age3 - age2 + 1):
                wage.append(wage2)
                    
            age = []
            for i in range(age2 - age1 + 1):
                age.append(i + age1)
                
            spending2 = rd.poisson(1 / 20, 50 - age1 + 1)
            spending3 = rd.poisson(1 / 10, 70 - 51 + 1)
            spending4 = rd.poisson(1 / 5, age3 - 71 + 1)
            add_spending = []
            for i in range(len(spending2)):
                add_spending.append(spending2[i] * 300)
            for i in range(len(spending3)):
                add_spending.append(spending3[i] * 300)
            for i in range(len(spending4)):
                add_spending.append(spending4[i] * 300)
                
            #その年齢でfireに必要な金額
            money = [0] * (age2 - age1 + 1)
            for i in range(age2 - age1 + 1):
                #年齢はage2 - iで考える
                if i >= 1:
                    money[age2 - age1 - i] = money[age2 - age1 - i + 1]
                for j in range(10000):
                    #100*j万円がその時点の貯金額
                    r = 100 * j + money[age2 - age1 - i]
                    for n in range(age3 - (age2 - i) + 1):
                        r = r - (spending + add_spending[age2 - i + n - age1]) + wage[age2 - i + n - age1]
                        if r < 0:
                            break
                        r = r * (1 + rate / 100)
                    if r >= endmoney:
                        money[age2 - age1 - i] += 100 * j
                        break
                
            return render_template("model1_result.html", age1=age1, age3=age3, wage=wage1, endmoney=endmoney, spending=spending, rate=rate, age=age, money=money)
        elif age1 > age3:
            sentence="死ぬ年齢は今の年齢以上を入力してください"
            return render_template("model1.html", sentence=sentence)
        else:
            #死ぬときに残しておきたい金額
            endmoney = int(request.form.get("endmoney"))
            #リタイアした後の収入
            wage1 = int(request.form.get("wage"))
            #年金
            wage2 = 130
            wage = []
            for i in range(age3 - age1 + 1):
                wage.append(wage1)
                    
            age = []
            for i in range(age3 - age1 + 1):
                age.append(i + age1)
          
            spending2 = rd.poisson(1 / 20, 50 - age1 + 1)
            spending3 = rd.poisson(1 / 10, 70 - 51 + 1)
            add_spending = []
            for i in range(len(spending2)):
                add_spending.append(spending2[i] * 300)
            for i in range(len(spending3)):
                add_spending.append(spending3[i] * 300)
          
                    
            #その年齢でfireに必要な金額
            money = [0] * (age3 - age1 + 1)
            for i in range(age3 - age1 + 1):
                #年齢はage3 - iで考える
                if i >= 1:
                    money[age3 - age1 - i] = money[age3 - age1 - i + 1]
                for j in range(10000):
                    #100*j万円がその時点の貯金額
                    r = 100 * j + money[age3 - age1 - i]
                    for n in range(i + 1):
                        r = r - (spending + add_spending[age3 - i + n - age1]) + wage[age3 - i + n - age1]
                        if r < 0:
                            break
                        r = r * (1 + rate / 100)
                    if r >= endmoney:
                        money[age3 - age1 - i] += 100 * j
                        break
                    
            return render_template("model1_result.html", age1=age1, age3=age3, wage=wage1, endmoney=endmoney, spending=spending, rate=rate, age=age, money=money)

if __name__ == '__main__':
    app.run()
                
        
                    
                
            
            
        
        
        



