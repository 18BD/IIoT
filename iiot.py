from tkinter import *
from tkinter import messagebox
from parameters import *
import json as js
import matplotlib.pyplot as plt


def login():
	global login_entry, password_entry
	try:
		with open('users.json', 'r') as file:
			data = js.load(file)
			if login_entry.get() not in data.keys():
				messagebox.showerror('Ошибка', 'Неверный логин')
			else:
				if password_entry.get() not in data.values():
					messagebox.showerror('Ошибка', 'Неверный пароль')
				else:
					main_page()
	except FileNotFoundError:
		messagebox.showerror('Ошибка', 'Пользователи отсутствуют')


def register(user={}):
	global login_entry, password_entry, password_entry_2
	try:
		with open('users.json','r') as file:
			data = js.load(file)
			if login_entry.get() in data.keys():
				messagebox.showerror('Ошибка', 'Пользователь с таким именем уже существует')
			else:
				if password_entry.get() == password_entry_2.get():
					user[login_entry.get()] = password_entry.get()
					with open('users.json', 'w') as file:
						js.dump(user, file)
					messagebox.showinfo('ОК', 'Регистрация завершена')
					sign_in()
				else:
					messagebox.showerror('Ошибка', 'Пароли не совпадают')
	except FileNotFoundError:
		if password_entry.get() == password_entry_2.get():
			user[login_entry.get()] = password_entry.get()
			with open('users.json', 'w') as file:
				js.dump(user, file)
			messagebox.showinfo('ОК', 'Регистрация завершена')
			sign_in()
		else:
			messagebox.showerror('Ошибка', 'Пароли не совпадают')


def get_password():
	global login_entry, password_entry, password_entry_2
	try:
		with open('users.json','r+') as file:
			data = js.load(file)
			if login_entry.get() not in data.keys():
				messagebox.showerror('Ошибка', 'Данный пользователь не зарегистрирован')
			else:
				if password_entry.get() == password_entry_2.get():
					data[login_entry.get()] = password_entry.get()
					file.seek(0) 
					js.dump(data, file)
					file.truncate()
					messagebox.showinfo('ОК', 'Пароль изменён')
					sign_in()
				else:
					messagebox.showerror('Ошибка', 'Пароли не совпадают')
	except FileNotFoundError:
		messagebox.showerror('Ошибка', 'Пользователи отсутствуют')
		sign_in()


def show_diagram(colors=[]):
	global risks, ro
	if ro == 5:
		data = dict(list(risks.items())[:4])
	elif ro == 6:
		data = dict(list(risks.items())[:3])
	else:
		data = risks
	courses = list(data.keys())
	values = list(data.values())
	for value in values:
		if 0 <= value < 2:
			colors.append('#4dfa59')
		elif 2 <= value < 3.5:
			colors.append('#75fa7e')
		elif 3.5 <= value < 7.1:
			colors.append('#faf575')
		elif 7.1 <= value < 11:
			colors.append('#fc6d00')
		else:
			colors.append('#fc1900')
	fig = plt.figure(figsize = (10, 5))
	plt.bar(courses, values, color = colors, width = 0.2)
	plt.xlabel('Угрозы')
	plt.ylabel('Уровень риска')
	plt.title('Анализ рисков информационной безопасности в IIoT')
	plt.show()


def show_attacks():
	global var, ro, json
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	danger = Label(root, text='Угрозы', font=('Consolas', 20), bg='white', fg='#31b053')
	danger.place(x=210, y=150)
	x = 150
	y = 220
	for i,j in json.items():
		desc = Label(root, text=f'{i} - {j}', font=('Consolas', 15), bg='white', fg='#31b053')
		desc.place(x=x, y=y)
		y += 50
	root.mainloop()


def show_recommendations():
	file = open("recommendations.txt", encoding='UTF-8')
	data = file.read()
	file.close()
	root = Tk()
	root.resizable(False, False)
	widget = Text(root)
	scrollbar = Scrollbar(root)
	scrollbar.pack(side=RIGHT, fill=Y)
	widget.pack(side=LEFT, fill=Y)
	scrollbar.config(command=widget.yview)
	widget.config(yscrollcommand=scrollbar.set)
	widget.insert(END, data)
	root.mainloop()


def show_results():
	global root, risks, json
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	danger = Label(root, text='Угроза', font=('Consolas', 20), bg='white', fg='#31b053')
	risk_level = Label(root, text='Уровень риска', font=('Consolas', 20), bg='white', fg='#31b053')
	diagram_button = Button(root, text='Диаграмма', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=show_diagram)
	recommendations_button = Button(root, text='Рекомендации', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=show_recommendations)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=t_page_7)
	danger.place(x=80, y=150)
	risk_level.place(x=600, y=150)
	diagram_button.place(x=600, y=500)
	recommendations_button.place(x=370, y=500)
	back_button.place(x=200, y=500)
	x = 80
	y = 220
	for i,j in json.items():
		if 0 <= risks[i] < 0.2:
			risk = 'Очень низкий'
		elif 0.2 <= risks[i] < 3.5:
			risk = 'Низкий'
		elif 3.5 <= risks[i] < 7.1:
			risk = 'Средний'
		elif 7.1 <= risks[i] < 11:
			risk = 'Высокий'
		elif risks[i] >= 11:
			risk = 'Критически высокий'
		desc = Label(root, text=f'{j+" "*(53-len(j))} - {risk}', font=('Consolas', 15), bg='white', fg='black')
		desc.place(x=x, y=y)
		y += 50
	root.mainloop()


def calculate_risks():
	global risks
	risks = {'T1':0, 'T2':0, 'T3':0, 'T4':0, 'T5':0}
	risks['T1'] = (sum([cr_1_3['T1'][0]*cr_4_7['T1'][0], cr_1_3['T1'][1]*cr_4_7['T1'][1], cr_1_3['T1'][2]*cr_4_7['T1'][2]]) / 3) * 100
	risks['T2'] = (sum([cr_1_3['T2'][0]*cr_4_7['T2'][0], cr_1_3['T2'][1]*cr_4_7['T2'][1], cr_1_3['T2'][2]*cr_4_7['T2'][2]]) / 3) * 100
	risks['T3'] = (sum([cr_1_3['T3'][0]*cr_4_7['T3'][0], cr_1_3['T3'][1]*cr_4_7['T3'][1], cr_1_3['T3'][2]*cr_4_7['T3'][2]]) / 3) * 100
	risks['T4'] = (sum([cr_1_3['T4'][0]*cr_4_7['T4'][0], cr_1_3['T4'][1]*cr_4_7['T4'][1], cr_1_3['T4'][2]*cr_4_7['T4'][2]]) / 3) * 100
	risks['T5'] = (sum([cr_1_3['T5'][0]*cr_4_7['T5'][0], cr_1_3['T5'][1]*cr_4_7['T5'][1], cr_1_3['T5'][2]*cr_4_7['T5'][2]]) / 3) * 100
	show_results()


def options_handle(check_list = []):
	if cnt == 0:
		check_list = [value_inside_1.get(), value_inside_2.get(), value_inside_3.get(), value_inside_4.get(), value_inside_5.get(), value_inside_6.get(), value_inside_7.get()]
		for i in check_list:
			if i in cr_options_default:
				messagebox.showerror("Ошибка", "Пожалуйста, заполните все параметры.")
				break
		else:
			t_page_1()
	else:
		if ro == 5:
			check_list = [value_1.get(), value_2.get(), value_3.get(), value_4.get()]
		elif ro == 6:
			check_list = [value_1.get(), value_2.get(), value_3.get()]
		else:
			check_list = [value_1.get(), value_2.get(), value_3.get(), value_4.get(), value_5.get()]
		for i in check_list:
			if i == 'Выбрать':
				messagebox.showerror("Ошибка", "Пожалуйста, заполните все параметры.")
				break
		else:
			if cnt == 1:
				t_page_2()
			elif cnt == 2:
				t_page_3()
			elif cnt == 3:
				t_page_4()
			elif cnt == 4:
				t_page_5()
			elif cnt == 5:
				t_page_6()
			elif cnt == 6:
				t_page_7()
			else:
				calculate_risks()


def t_page_7():
	global root, cnt, value_1, value_2, value_3, value_4, value_5, cr_4_7, page, t_values_6, t_values_7
	cnt = 7
	t_values_6 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()]]
	if ro != 6:
		t_values_6 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()]]
	if ro != 5 and ro != 6:
		t_values_6 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()], t_json[value_5.get()]]
	if page == 7:
		weight = cr_json[value_inside_7.get()]
		t1 = [i*weight for i in t_values_3[0]]
		cr_4_7['T1'] = [round(cr_4_7['T1'][0]-t1[0], 3), round(cr_4_7['T1'][1]-t1[1], 3), round(cr_4_7['T1'][2]-t1[2], 3)]
		t2 = [i*weight for i in t_values_3[1]]
		cr_4_7['T2'] = [round(cr_4_7['T2'][0]-t2[0], 3), round(cr_4_7['T2'][1]-t2[1], 3), round(cr_4_7['T2'][2]-t2[2], 3)]
		t3 = [i*weight for i in t_values_3[2]]
		cr_4_7['T3'] = [round(cr_4_7['T3'][0]-t3[0], 3), round(cr_4_7['T3'][1]-t3[1], 3), round(cr_4_7['T3'][2]-t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_values_3[3]]
			cr_4_7['T4'] = [round(cr_4_7['T4'][0]-t4[0], 3), round(cr_4_7['T4'][1]-t4[1], 3), round(cr_4_7['T4'][2]-t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_values_3[4]]
			cr_4_7['T5'] = [round(cr_4_7['T5'][0]-t5[0], 3), round(cr_4_7['T5'][1]-t5[1], 3), round(cr_4_7['T5'][2]-t5[2], 3)]
	page = 6
	try:
		weight = cr_json[value_inside_6.get()]
		t1 = [i*weight for i in t_json[value_1.get()]]
		cr_4_7['T1'] = [round(cr_4_7['T1'][0]+t1[0], 3), round(cr_4_7['T1'][1]+t1[1], 3), round(cr_4_7['T1'][2]+t1[2], 3)]
		t2 = [i*weight for i in t_json[value_2.get()]]
		cr_4_7['T2'] = [round(cr_4_7['T2'][0]+t2[0], 3), round(cr_4_7['T2'][1]+t2[1], 3), round(cr_4_7['T2'][2]+t2[2], 3)]
		t3 = [i*weight for i in t_json[value_3.get()]]
		cr_4_7['T3'] = [round(cr_4_7['T3'][0]+t3[0], 3), round(cr_4_7['T3'][1]+t3[1], 3), round(cr_4_7['T3'][2]+t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_json[value_4.get()]]
			cr_4_7['T4'] = [round(cr_4_7['T4'][0]+t4[0], 3), round(cr_4_7['T4'][1]+t4[1], 3), round(cr_4_7['T4'][2]+t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_json[value_5.get()]]
			cr_4_7['T5'] = [round(cr_4_7['T5'][0]+t5[0], 3), round(cr_4_7['T5'][1]+t5[1], 3), round(cr_4_7['T5'][2]+t5[2], 3)]
	except KeyError:
		pass
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	criterion = Label(root, text='Критерий:', font=('Consolas', 20), bg='white', fg='#31b053')
	danger = Label(root, text='Угроза:', font=('Consolas', 20), bg='white', fg='#31b053')
	cr = Label(root, text='Предыдущие угрозы', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=options_handle)
	show_t = Button(root, text='Список угроз', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=show_attacks)
	show_t.place(x=370, y=500)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=t_page_6)
	criterion.place(x=50, y=100)
	cr.place(x=300, y=100)
	danger.place(x=50, y=200)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	x = 200
	for i in json.keys():
		threat = Label(root, text=f'{i}', font=('Consolas', 20), bg='white', fg='grey')
		threat.place(x=x, y=200)
		x += 150
	value_1 = StringVar(root)
	value_1.set('Выбрать')
	cr_menu_1 = OptionMenu(root, value_1, *t_list)
	cr_menu_1.config(bg='white')
	cr_menu_1.config(width=10)
	cr_menu_1.config(height=2)
	value_2 = StringVar(root)
	value_2.set('Выбрать')
	cr_menu_2 = OptionMenu(root, value_2, *t_list)
	cr_menu_2.config(bg='white')
	cr_menu_2.config(width=10)
	cr_menu_2.config(height=2)
	value_3 = StringVar(root)
	value_3.set('Выбрать')
	cr_menu_3 = OptionMenu(root, value_3, *t_list)
	cr_menu_3.config(bg='white')
	cr_menu_3.config(width=10)
	cr_menu_3.config(height=2)
	value_4 = StringVar(root)
	value_4.set('Выбрать')
	cr_menu_4 = OptionMenu(root, value_4, *t_list)
	cr_menu_4.config(bg='white')
	cr_menu_4.config(width=10)
	cr_menu_4.config(height=2)
	value_5 = StringVar(root)
	value_5.set('Выбрать')
	cr_menu_5 = OptionMenu(root, value_5, *t_list)
	cr_menu_5.config(bg='white')
	cr_menu_5.config(width=10)
	cr_menu_5.config(height=2)
	cr_menu_1.place(x=160, y=300)
	cr_menu_2.place(x=310, y=300)
	cr_menu_3.place(x=460, y=300)
	if ro != 6:
		cr_menu_4.place(x=610, y=300)
	if ro != 5 and ro != 6:
		cr_menu_5.place(x=760, y=300)
	root.mainloop()


def t_page_6():
	global root, cnt, value_1, value_2, value_3, value_4, value_5, cr_4_7, page, t_values_5, t_values_6
	cnt = 6
	t_values_5 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()]]
	if ro != 6:
		t_values_5 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()]]
	if ro != 5 and ro != 6:
		t_values_5 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()], t_json[value_5.get()]]
	if page == 6:
		weight = cr_json[value_inside_6.get()]
		t1 = [i*weight for i in t_values_3[0]]
		cr_4_7['T1'] = [round(cr_4_7['T1'][0]-t1[0], 3), round(cr_4_7['T1'][1]-t1[1], 3), round(cr_4_7['T1'][2]-t1[2], 3)]
		t2 = [i*weight for i in t_values_3[1]]
		cr_4_7['T2'] = [round(cr_4_7['T2'][0]-t2[0], 3), round(cr_4_7['T2'][1]-t2[1], 3), round(cr_4_7['T2'][2]-t2[2], 3)]
		t3 = [i*weight for i in t_values_3[2]]
		cr_4_7['T3'] = [round(cr_4_7['T3'][0]-t3[0], 3), round(cr_4_7['T3'][1]-t3[1], 3), round(cr_4_7['T3'][2]-t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_values_3[3]]
			cr_4_7['T4'] = [round(cr_4_7['T4'][0]-t4[0], 3), round(cr_4_7['T4'][1]-t4[1], 3), round(cr_4_7['T4'][2]-t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_values_3[4]]
			cr_4_7['T5'] = [round(cr_4_7['T5'][0]-t5[0], 3), round(cr_4_7['T5'][1]-t5[1], 3), round(cr_4_7['T5'][2]-t5[2], 3)]
	page = 5
	try:
		weight = cr_json[value_inside_5.get()]
		t1 = [i*weight for i in t_json[value_1.get()]]
		cr_4_7['T1'] = [round(cr_4_7['T1'][0]+t1[0], 3), round(cr_4_7['T1'][1]+t1[1], 3), round(cr_4_7['T1'][2]+t1[2], 3)]
		t2 = [i*weight for i in t_json[value_2.get()]]
		cr_4_7['T2'] = [round(cr_4_7['T2'][0]+t2[0], 3), round(cr_4_7['T2'][1]+t2[1], 3), round(cr_4_7['T2'][2]+t2[2], 3)]
		t3 = [i*weight for i in t_json[value_3.get()]]
		cr_4_7['T3'] = [round(cr_4_7['T3'][0]+t3[0], 3), round(cr_4_7['T3'][1]+t3[1], 3), round(cr_4_7['T3'][2]+t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_json[value_4.get()]]
			cr_4_7['T4'] = [round(cr_4_7['T4'][0]+t4[0], 3), round(cr_4_7['T4'][1]+t4[1], 3), round(cr_4_7['T4'][2]+t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_json[value_5.get()]]
			cr_4_7['T5'] = [round(cr_4_7['T5'][0]+t5[0], 3), round(cr_4_7['T5'][1]+t5[1], 3), round(cr_4_7['T5'][2]+t5[2], 3)]
	except KeyError:
		pass
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	criterion = Label(root, text='Критерий:', font=('Consolas', 20), bg='white', fg='#31b053')
	danger = Label(root, text='Угроза:', font=('Consolas', 20), bg='white', fg='#31b053')
	cr = Label(root, text='Ущерб репутации', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=options_handle)
	show_t = Button(root, text='Список угроз', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=show_attacks)
	show_t.place(x=370, y=500)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=t_page_5)
	criterion.place(x=50, y=100)
	cr.place(x=300, y=100)
	danger.place(x=50, y=200)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	x = 200
	for i in json.keys():
		threat = Label(root, text=f'{i}', font=('Consolas', 20), bg='white', fg='grey')
		threat.place(x=x, y=200)
		x += 150
	value_1 = StringVar(root)
	value_1.set('Выбрать')
	cr_menu_1 = OptionMenu(root, value_1, *t_list)
	cr_menu_1.config(bg='white')
	cr_menu_1.config(width=10)
	cr_menu_1.config(height=2)
	value_2 = StringVar(root)
	value_2.set('Выбрать')
	cr_menu_2 = OptionMenu(root, value_2, *t_list)
	cr_menu_2.config(bg='white')
	cr_menu_2.config(width=10)
	cr_menu_2.config(height=2)
	value_3 = StringVar(root)
	value_3.set('Выбрать')
	cr_menu_3 = OptionMenu(root, value_3, *t_list)
	cr_menu_3.config(bg='white')
	cr_menu_3.config(width=10)
	cr_menu_3.config(height=2)
	value_4 = StringVar(root)
	value_4.set('Выбрать')
	cr_menu_4 = OptionMenu(root, value_4, *t_list)
	cr_menu_4.config(bg='white')
	cr_menu_4.config(width=10)
	cr_menu_4.config(height=2)
	value_5 = StringVar(root)
	value_5.set('Выбрать')
	cr_menu_5 = OptionMenu(root, value_5, *t_list)
	cr_menu_5.config(bg='white')
	cr_menu_5.config(width=10)
	cr_menu_5.config(height=2)
	cr_menu_1.place(x=160, y=300)
	cr_menu_2.place(x=310, y=300)
	cr_menu_3.place(x=460, y=300)
	if ro != 6:
		cr_menu_4.place(x=610, y=300)
	if ro != 5 and ro != 6:
		cr_menu_5.place(x=760, y=300)
	root.mainloop()


def t_page_5():
	global root, cnt, value_1, value_2, value_3, value_4, value_5, cr_4_7, page, t_values_4, t_values_5
	cnt = 5
	t_values_4 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()]]
	if ro != 6:
		t_values_4 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()]]
	if ro != 5 and ro != 6:
		t_values_4 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()], t_json[value_5.get()]]
	if page == 5:
		weight = cr_json[value_inside_5.get()]
		t1 = [i*weight for i in t_values_3[0]]
		cr_4_7['T1'] = [round(cr_4_7['T1'][0]-t1[0], 3), round(cr_4_7['T1'][1]-t1[1], 3), round(cr_4_7['T1'][2]-t1[2], 3)]
		t2 = [i*weight for i in t_values_3[1]]
		cr_4_7['T2'] = [round(cr_4_7['T2'][0]-t2[0], 3), round(cr_4_7['T2'][1]-t2[1], 3), round(cr_4_7['T2'][2]-t2[2], 3)]
		t3 = [i*weight for i in t_values_3[2]]
		cr_4_7['T3'] = [round(cr_4_7['T3'][0]-t3[0], 3), round(cr_4_7['T3'][1]-t3[1], 3), round(cr_4_7['T3'][2]-t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_values_3[3]]
			cr_4_7['T4'] = [round(cr_4_7['T4'][0]-t4[0], 3), round(cr_4_7['T4'][1]-t4[1], 3), round(cr_4_7['T4'][2]-t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_values_3[4]]
			cr_4_7['T5'] = [round(cr_4_7['T5'][0]-t5[0], 3), round(cr_4_7['T5'][1]-t5[1], 3), round(cr_4_7['T5'][2]-t5[2], 3)]
	page = 4
	try:
		weight = cr_json[value_inside_4.get()]
		t1 = [i*weight for i in t_json[value_1.get()]]
		cr_4_7['T1'] = [round(cr_4_7['T1'][0]+t1[0], 3), round(cr_4_7['T1'][1]+t1[1], 3), round(cr_4_7['T1'][2]+t1[2], 3)]
		t2 = [i*weight for i in t_json[value_2.get()]]
		cr_4_7['T2'] = [round(cr_4_7['T2'][0]+t2[0], 3), round(cr_4_7['T2'][1]+t2[1], 3), round(cr_4_7['T2'][2]+t2[2], 3)]
		t3 = [i*weight for i in t_json[value_3.get()]]
		cr_4_7['T3'] = [round(cr_4_7['T3'][0]+t3[0], 3), round(cr_4_7['T3'][1]+t3[1], 3), round(cr_4_7['T3'][2]+t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_json[value_4.get()]]
			cr_4_7['T4'] = [round(cr_4_7['T4'][0]+t4[0], 3), round(cr_4_7['T4'][1]+t4[1], 3), round(cr_4_7['T4'][2]+t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_json[value_5.get()]]
			cr_4_7['T5'] = [round(cr_4_7['T5'][0]+t5[0], 3), round(cr_4_7['T5'][1]+t5[1], 3), round(cr_4_7['T5'][2]+t5[2], 3)]
	except KeyError:
		pass
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	criterion = Label(root, text='Критерий:', font=('Consolas', 20), bg='white', fg='#31b053')
	danger = Label(root, text='Угроза:', font=('Consolas', 20), bg='white', fg='#31b053')
	cr = Label(root, text='Временные издержки', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=options_handle)
	show_t = Button(root, text='Список угроз', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=show_attacks)
	show_t.place(x=370, y=500)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=t_page_4)
	criterion.place(x=50, y=100)
	cr.place(x=300, y=100)
	danger.place(x=50, y=200)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	x = 200
	for i in json.keys():
		threat = Label(root, text=f'{i}', font=('Consolas', 20), bg='white', fg='grey')
		threat.place(x=x, y=200)
		x += 150
	value_1 = StringVar(root)
	value_1.set('Выбрать')
	cr_menu_1 = OptionMenu(root, value_1, *t_list)
	cr_menu_1.config(bg='white')
	cr_menu_1.config(width=10)
	cr_menu_1.config(height=2)
	value_2 = StringVar(root)
	value_2.set('Выбрать')
	cr_menu_2 = OptionMenu(root, value_2, *t_list)
	cr_menu_2.config(bg='white')
	cr_menu_2.config(width=10)
	cr_menu_2.config(height=2)
	value_3 = StringVar(root)
	value_3.set('Выбрать')
	cr_menu_3 = OptionMenu(root, value_3, *t_list)
	cr_menu_3.config(bg='white')
	cr_menu_3.config(width=10)
	cr_menu_3.config(height=2)
	value_4 = StringVar(root)
	value_4.set('Выбрать')
	cr_menu_4 = OptionMenu(root, value_4, *t_list)
	cr_menu_4.config(bg='white')
	cr_menu_4.config(width=10)
	cr_menu_4.config(height=2)
	value_5 = StringVar(root)
	value_5.set('Выбрать')
	cr_menu_5 = OptionMenu(root, value_5, *t_list)
	cr_menu_5.config(bg='white')
	cr_menu_5.config(width=10)
	cr_menu_5.config(height=2)
	cr_menu_1.place(x=160, y=300)
	cr_menu_2.place(x=310, y=300)
	cr_menu_3.place(x=460, y=300)
	if ro != 6:
		cr_menu_4.place(x=610, y=300)
	if ro != 5 and ro != 6:
		cr_menu_5.place(x=760, y=300)
	root.mainloop()


def t_page_4():
	global root, cnt, value_1, value_2, value_3, value_4, value_5, cr_4_7, page, t_values_3, t_values_4
	cnt = 4
	t_values_3 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()]]
	if ro != 6:
		t_values_3 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()]]
	if ro != 5 and ro != 6:
		t_values_3 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()], t_json[value_5.get()]]
	cr_4_7 = {'T1':[0, 0, 0], 'T2':[0, 0, 0], 'T3':[0, 0, 0], 'T4':[0, 0, 0], 'T5':[0, 0, 0]}
	page = 3
	try:
		weight = cr_json[value_inside_3.get()]
		t1 = [i*weight for i in t_json[value_1.get()]]
		cr_1_3['T1'] = [round(cr_1_3['T1'][0]+t1[0], 3), round(cr_1_3['T1'][1]+t1[1], 3), round(cr_1_3['T1'][2]+t1[2], 3)]
		t2 = [i*weight for i in t_json[value_2.get()]]
		cr_1_3['T2'] = [round(cr_1_3['T2'][0]+t2[0], 3), round(cr_1_3['T2'][1]+t2[1], 3), round(cr_1_3['T2'][2]+t2[2], 3)]
		t3 = [i*weight for i in t_json[value_3.get()]]
		cr_1_3['T3'] = [round(cr_1_3['T3'][0]+t3[0], 3), round(cr_1_3['T3'][1]+t3[1], 3), round(cr_1_3['T3'][2]+t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_json[value_4.get()]]
			cr_1_3['T4'] = [round(cr_1_3['T4'][0]+t4[0], 3), round(cr_1_3['T4'][1]+t4[1], 3), round(cr_1_3['T4'][2]+t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_json[value_5.get()]]
			cr_1_3['T5'] = [round(cr_1_3['T5'][0]+t5[0], 3), round(cr_1_3['T5'][1]+t5[1], 3), round(cr_1_3['T5'][2]+t5[2], 3)]
	except KeyError:
		pass
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	criterion = Label(root, text='Критерий:', font=('Consolas', 20), bg='white', fg='#31b053')
	danger = Label(root, text='Угроза:', font=('Consolas', 20), bg='white', fg='#31b053')
	cr = Label(root, text='Финансовые  затраты', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=options_handle)
	show_t = Button(root, text='Список угроз', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=show_attacks)
	show_t.place(x=370, y=500)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=t_page_3)
	criterion.place(x=50, y=100)
	cr.place(x=300, y=100)
	danger.place(x=50, y=200)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	x = 200
	for i in json.keys():
		threat = Label(root, text=f'{i}', font=('Consolas', 20), bg='white', fg='grey')
		threat.place(x=x, y=200)
		x += 150
	value_1 = StringVar(root)
	value_1.set('Выбрать')
	cr_menu_1 = OptionMenu(root, value_1, *t_list)
	cr_menu_1.config(bg='white')
	cr_menu_1.config(width=10)
	cr_menu_1.config(height=2)
	value_2 = StringVar(root)
	value_2.set('Выбрать')
	cr_menu_2 = OptionMenu(root, value_2, *t_list)
	cr_menu_2.config(bg='white')
	cr_menu_2.config(width=10)
	cr_menu_2.config(height=2)
	value_3 = StringVar(root)
	value_3.set('Выбрать')
	cr_menu_3 = OptionMenu(root, value_3, *t_list)
	cr_menu_3.config(bg='white')
	cr_menu_3.config(width=10)
	cr_menu_3.config(height=2)
	value_4 = StringVar(root)
	value_4.set('Выбрать')
	cr_menu_4 = OptionMenu(root, value_4, *t_list)
	cr_menu_4.config(bg='white')
	cr_menu_4.config(width=10)
	cr_menu_4.config(height=2)
	value_5 = StringVar(root)
	value_5.set('Выбрать')
	cr_menu_5 = OptionMenu(root, value_5, *t_list)
	cr_menu_5.config(bg='white')
	cr_menu_5.config(width=10)
	cr_menu_5.config(height=2)
	cr_menu_1.place(x=160, y=300)
	cr_menu_2.place(x=310, y=300)
	cr_menu_3.place(x=460, y=300)
	if ro != 6:
		cr_menu_4.place(x=610, y=300)
	if ro != 5 and ro != 6:
		cr_menu_5.place(x=760, y=300)
	root.mainloop()


def t_page_3():
	global root, cnt, value_1, value_2, value_3, value_4, value_5, cr_1_3, page, t_values_2, t_values_3
	cnt = 3
	t_values_2 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()]]
	if ro != 6:
		t_values_2 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()]]
	if ro != 5 and ro != 6:
		t_values_2 = [t_json[value_1.get()], t_json[value_2.get()], t_json[value_3.get()], t_json[value_4.get()], t_json[value_5.get()]]
	if page == 3:
		weight = cr_json[value_inside_3.get()]
		t1 = [i*weight for i in t_values_3[0]]
		cr_1_3['T1'] = [round(cr_1_3['T1'][0]-t1[0], 3), round(cr_1_3['T1'][1]-t1[1], 3), round(cr_1_3['T1'][2]-t1[2], 3)]
		t2 = [i*weight for i in t_values_3[1]]
		cr_1_3['T2'] = [round(cr_1_3['T2'][0]-t2[0], 3), round(cr_1_3['T2'][1]-t2[1], 3), round(cr_1_3['T2'][2]-t2[2], 3)]
		t3 = [i*weight for i in t_values_3[2]]
		cr_1_3['T3'] = [round(cr_1_3['T3'][0]-t3[0], 3), round(cr_1_3['T3'][1]-t3[1], 3), round(cr_1_3['T3'][2]-t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_values_3[3]]
			cr_1_3['T4'] = [round(cr_1_3['T4'][0]-t4[0], 3), round(cr_1_3['T4'][1]-t4[1], 3), round(cr_1_3['T4'][2]-t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_values_3[4]]
			cr_1_3['T5'] = [round(cr_1_3['T5'][0]-t5[0], 3), round(cr_1_3['T5'][1]-t5[1], 3), round(cr_1_3['T5'][2]-t5[2], 3)]
	page = 2
	try:
		weight = cr_json[value_inside_2.get()]
		t1 = [i*weight for i in t_json[value_1.get()]]
		cr_1_3['T1'] = [round(cr_1_3['T1'][0]+t1[0], 3), round(cr_1_3['T1'][1]+t1[1], 3), round(cr_1_3['T1'][2]+t1[2], 3)]
		t2 = [i*weight for i in t_json[value_2.get()]]
		cr_1_3['T2'] = [round(cr_1_3['T2'][0]+t2[0], 3), round(cr_1_3['T2'][1]+t2[1], 3), round(cr_1_3['T2'][2]+t2[2], 3)]
		t3 = [i*weight for i in t_json[value_3.get()]]
		cr_1_3['T3'] = [round(cr_1_3['T3'][0]+t3[0], 3), round(cr_1_3['T3'][1]+t3[1], 3), round(cr_1_3['T3'][2]+t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_json[value_4.get()]]
			cr_1_3['T4'] = [round(cr_1_3['T4'][0]+t4[0], 3), round(cr_1_3['T4'][1]+t4[1], 3), round(cr_1_3['T4'][2]+t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_json[value_5.get()]]
			cr_1_3['T5'] = [round(cr_1_3['T5'][0]+t5[0], 3), round(cr_1_3['T5'][1]+t5[1], 3), round(cr_1_3['T5'][2]+t5[2], 3)]
	except KeyError:
		pass
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	criterion = Label(root, text='Критерий:', font=('Consolas', 20), bg='white', fg='#31b053')
	danger = Label(root, text='Угроза:', font=('Consolas', 20), bg='white', fg='#31b053')
	cr = Label(root, text='Существующий контроль', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=options_handle)
	show_t = Button(root, text='Список угроз', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=show_attacks)
	show_t.place(x=370, y=500)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=t_page_2)
	criterion.place(x=50, y=100)
	cr.place(x=300, y=100)
	danger.place(x=50, y=200)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	x = 200
	for i in json.keys():
		threat = Label(root, text=f'{i}', font=('Consolas', 20), bg='white', fg='grey')
		threat.place(x=x, y=200)
		x += 150
	value_1 = StringVar(root)
	value_1.set('Выбрать')
	cr_menu_1 = OptionMenu(root, value_1, *t_list)
	cr_menu_1.config(bg='white')
	cr_menu_1.config(width=10)
	cr_menu_1.config(height=2)
	value_2 = StringVar(root)
	value_2.set('Выбрать')
	cr_menu_2 = OptionMenu(root, value_2, *t_list)
	cr_menu_2.config(bg='white')
	cr_menu_2.config(width=10)
	cr_menu_2.config(height=2)
	value_3 = StringVar(root)
	value_3.set('Выбрать')
	cr_menu_3 = OptionMenu(root, value_3, *t_list)
	cr_menu_3.config(bg='white')
	cr_menu_3.config(width=10)
	cr_menu_3.config(height=2)
	value_4 = StringVar(root)
	value_4.set('Выбрать')
	cr_menu_4 = OptionMenu(root, value_4, *t_list)
	cr_menu_4.config(bg='white')
	cr_menu_4.config(width=10)
	cr_menu_4.config(height=2)
	value_5 = StringVar(root)
	value_5.set('Выбрать')
	cr_menu_5 = OptionMenu(root, value_5, *t_list)
	cr_menu_5.config(bg='white')
	cr_menu_5.config(width=10)
	cr_menu_5.config(height=2)
	cr_menu_1.place(x=160, y=300)
	cr_menu_2.place(x=310, y=300)
	cr_menu_3.place(x=460, y=300)
	if ro != 6:
		cr_menu_4.place(x=610, y=300)
	if ro != 5 and ro != 6:
		cr_menu_5.place(x=760, y=300)
	root.mainloop()


def t_page_2():
	global root, cnt, value_1, value_2, value_3, value_4, value_5, cr_1_3, page, t_values_2
	cnt = 2
	if page == 2:
		weight = cr_json[value_inside_2.get()]
		t1 = [i*weight for i in t_values_2[0]]
		cr_1_3['T1'] = [round(cr_1_3['T1'][0]-t1[0], 3), round(cr_1_3['T1'][1]-t1[1], 3), round(cr_1_3['T1'][2]-t1[2], 3)]
		t2 = [i*weight for i in t_values_2[1]]
		cr_1_3['T2'] = [round(cr_1_3['T2'][0]-t2[0], 3), round(cr_1_3['T2'][1]-t2[1], 3), round(cr_1_3['T2'][2]-t2[2], 3)]
		t3 = [i*weight for i in t_values_2[2]]
		cr_1_3['T3'] = [round(cr_1_3['T3'][0]-t3[0], 3), round(cr_1_3['T3'][1]-t3[1], 3), round(cr_1_3['T3'][2]-t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_values_2[3]]
			cr_1_3['T4'] = [round(cr_1_3['T4'][0]-t4[0], 3), round(cr_1_3['T4'][1]-t4[1], 3), round(cr_1_3['T4'][2]-t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_values_2[4]]
			cr_1_3['T5'] = [round(cr_1_3['T5'][0]-t5[0], 3), round(cr_1_3['T5'][1]-t5[1], 3), round(cr_1_3['T5'][2]-t5[2], 3)]
	page = 0
	try:
		weight = cr_json[value_inside_1.get()]
		t1 = [i*weight for i in t_json[value_1.get()]]
		cr_1_3['T1'] = [round(cr_1_3['T1'][0]+t1[0], 3), round(cr_1_3['T1'][1]+t1[1], 3), round(cr_1_3['T1'][2]+t1[2], 3)]
		t2 = [i*weight for i in t_json[value_2.get()]]
		cr_1_3['T2'] = [round(cr_1_3['T2'][0]+t2[0], 3), round(cr_1_3['T2'][1]+t2[1], 3), round(cr_1_3['T2'][2]+t2[2], 3)]
		t3 = [i*weight for i in t_json[value_3.get()]]
		cr_1_3['T3'] = [round(cr_1_3['T3'][0]+t3[0], 3), round(cr_1_3['T3'][1]+t3[1], 3), round(cr_1_3['T3'][2]+t3[2], 3)]
		if ro != 6:
			t4 = [i*weight for i in t_json[value_4.get()]]
			cr_1_3['T4'] = [round(cr_1_3['T4'][0]+t4[0], 3), round(cr_1_3['T4'][1]+t4[1], 3), round(cr_1_3['T4'][2]+t4[2], 3)]
		if ro != 5 and ro != 6:
			t5 = [i*weight for i in t_json[value_5.get()]]
			cr_1_3['T5'] = [round(cr_1_3['T5'][0]+t5[0], 3), round(cr_1_3['T5'][1]+t5[1], 3), round(cr_1_3['T5'][2]+t5[2], 3)]
	except KeyError:
		pass
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	criterion = Label(root, text='Критерий:', font=('Consolas', 20), bg='white', fg='#31b053')
	danger = Label(root, text='Угроза:', font=('Consolas', 20), bg='white', fg='#31b053')
	cr = Label(root, text='Уязвимость', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=options_handle)
	show_t = Button(root, text='Список угроз', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=show_attacks)
	show_t.place(x=370, y=500)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=t_page_1)
	criterion.place(x=50, y=100)
	cr.place(x=300, y=100)
	danger.place(x=50, y=200)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	x = 200
	for i in json.keys():
		threat = Label(root, text=f'{i}', font=('Consolas', 20), bg='white', fg='grey')
		threat.place(x=x, y=200)
		x += 150
	value_1 = StringVar(root)
	value_1.set('Выбрать')
	cr_menu_1 = OptionMenu(root, value_1, *t_list)
	cr_menu_1.config(bg='white')
	cr_menu_1.config(width=10)
	cr_menu_1.config(height=2)
	value_2 = StringVar(root)
	value_2.set('Выбрать')
	cr_menu_2 = OptionMenu(root, value_2, *t_list)
	cr_menu_2.config(bg='white')
	cr_menu_2.config(width=10)
	cr_menu_2.config(height=2)
	value_3 = StringVar(root)
	value_3.set('Выбрать')
	cr_menu_3 = OptionMenu(root, value_3, *t_list)
	cr_menu_3.config(bg='white')
	cr_menu_3.config(width=10)
	cr_menu_3.config(height=2)
	value_4 = StringVar(root)
	value_4.set('Выбрать')
	cr_menu_4 = OptionMenu(root, value_4, *t_list)
	cr_menu_4.config(bg='white')
	cr_menu_4.config(width=10)
	cr_menu_4.config(height=2)
	value_5 = StringVar(root)
	value_5.set('Выбрать')
	cr_menu_5 = OptionMenu(root, value_5, *t_list)
	cr_menu_5.config(bg='white')
	cr_menu_5.config(width=10)
	cr_menu_5.config(height=2)
	cr_menu_1.place(x=160, y=300)
	cr_menu_2.place(x=310, y=300)
	cr_menu_3.place(x=460, y=300)
	if ro != 6:
		cr_menu_4.place(x=610, y=300)
	if ro != 5 and ro != 6:
		cr_menu_5.place(x=760, y=300)
	root.mainloop()


def t_page_1():
	global root, cnt, value_1, value_2, value_3, value_4, value_5, cr_1_3
	cnt = 1
	cr_1_3 = {'T1':[0, 0, 0], 'T2':[0, 0, 0], 'T3':[0, 0, 0], 'T4':[0, 0, 0], 'T5':[0, 0, 0]}
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	criterion = Label(root, text='Критерий:', font=('Consolas', 20), bg='white', fg='#31b053')
	danger = Label(root, text='Угроза:', font=('Consolas', 20), bg='white', fg='#31b053')
	cr = Label(root, text='Привлекательность актива', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=options_handle)
	show_t = Button(root, text='Список угроз', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=show_attacks)
	show_t.place(x=370, y=500)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=cr_page)
	criterion.place(x=50, y=100)
	cr.place(x=300, y=100)
	danger.place(x=50, y=200)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	x = 200
	for i in json.keys():
		threat = Label(root, text=f'{i}', font=('Consolas', 20), bg='white', fg='grey')
		threat.place(x=x, y=200)
		x += 150
	value_1 = StringVar(root)
	value_1.set('Выбрать')
	cr_menu_1 = OptionMenu(root, value_1, *t_list)
	cr_menu_1.config(bg='white')
	cr_menu_1.config(width=10)
	cr_menu_1.config(height=2)
	value_2 = StringVar(root)
	value_2.set('Выбрать')
	cr_menu_2 = OptionMenu(root, value_2, *t_list)
	cr_menu_2.config(bg='white')
	cr_menu_2.config(width=10)
	cr_menu_2.config(height=2)
	value_3 = StringVar(root)
	value_3.set('Выбрать')
	cr_menu_3 = OptionMenu(root, value_3, *t_list)
	cr_menu_3.config(bg='white')
	cr_menu_3.config(width=10)
	cr_menu_3.config(height=2)
	value_4 = StringVar(root)
	value_4.set('Выбрать')
	cr_menu_4 = OptionMenu(root, value_4, *t_list)
	cr_menu_4.config(bg='white')
	cr_menu_4.config(width=10)
	cr_menu_4.config(height=2)
	value_5 = StringVar(root)
	value_5.set('Выбрать')
	cr_menu_5 = OptionMenu(root, value_5, *t_list)
	cr_menu_5.config(bg='white')
	cr_menu_5.config(width=10)
	cr_menu_5.config(height=2)
	cr_menu_1.place(x=160, y=300)
	cr_menu_2.place(x=310, y=300)
	cr_menu_3.place(x=460, y=300)
	if ro != 6:
		cr_menu_4.place(x=610, y=300)
	if ro != 5 and ro != 6:
		cr_menu_5.place(x=760, y=300)
	root.mainloop()


def cr_page():
	global root, cnt, value_inside_1, value_inside_2, value_inside_3, value_inside_4, value_inside_5, value_inside_6, value_inside_7
	cnt = 0
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	importance = Label(root, text='Важность каждого критерия', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=options_handle)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=attacks_page)
	importance.place(x=250, y=150)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	value_inside_1 = StringVar(root)
	value_inside_1.set('Привлекательность актива')
	cr_menu_1 = OptionMenu(root, value_inside_1, *options_list)
	cr_menu_1.config(bg='white')
	cr_menu_1.config(width=25)
	cr_menu_1.config(height=2)
	value_inside_2 = StringVar(root)
	value_inside_2.set('Уязвимость')
	cr_menu_2 = OptionMenu(root, value_inside_2, *options_list)
	cr_menu_2.config(bg='white')
	cr_menu_2.config(width=25)
	cr_menu_2.config(height=2)
	value_inside_3 = StringVar(root)
	value_inside_3.set('Существующий контроль')
	cr_menu_3 = OptionMenu(root, value_inside_3, *options_list)
	cr_menu_3.config(bg='white')
	cr_menu_3.config(width=25)
	cr_menu_3.config(height=2)
	value_inside_4 = StringVar(root)
	value_inside_4.set('Финансовые  затраты')
	cr_menu_4 = OptionMenu(root, value_inside_4, *options_list)
	cr_menu_4.config(bg='white')
	cr_menu_4.config(width=25)
	cr_menu_4.config(height=2)
	value_inside_5 = StringVar(root)
	value_inside_5.set('Временные издержки')
	cr_menu_5 = OptionMenu(root, value_inside_5, *options_list)
	cr_menu_5.config(bg='white')
	cr_menu_5.config(width=25)
	cr_menu_5.config(height=2)
	value_inside_6 = StringVar(root)
	value_inside_6.set('Ущерб репутации')
	cr_menu_6 = OptionMenu(root, value_inside_6, *options_list)
	cr_menu_6.config(bg='white')
	cr_menu_6.config(width=25)
	cr_menu_6.config(height=2)
	value_inside_7 = StringVar(root)
	value_inside_7.set('Предыдущие угрозы')
	cr_menu_7 = OptionMenu(root, value_inside_7, *options_list)
	cr_menu_7.config(bg='white')
	cr_menu_7.config(width=25)
	cr_menu_7.config(height=2)
	cr_menu_1.place(x=150, y=250)
	cr_menu_2.place(x=350, y=250)
	cr_menu_3.place(x=550, y=250)
	cr_menu_4.place(x=150, y=330)
	cr_menu_5.place(x=350, y=330)
	cr_menu_6.place(x=550, y=330)
	cr_menu_7.place(x=350, y=410)
	root.mainloop()


def attacks_page():
	global root, var, ro, json, category
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	ro = var.get()
	if ro == 1:
		json = json_1
		category = 1
	elif ro == 2:
		json = json_2
		category = 2
	elif ro == 3:
		json = json_3
		category = 3
	elif ro == 4:
		json = json_4
		category = 4
	elif ro == 5:
		json = json_5
		category = 5
	elif ro == 6:
		json = json_6
		category = 6
	else:
		json = json_7
		category = 7
	danger = Label(root, text='Угрозы', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=cr_page)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=main_page)
	danger.place(x=210, y=150)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	x = 150
	y = 220
	for i,j in json.items():
		desc = Label(root, text=f'{i} - {j}', font=('Consolas', 15), bg='white', fg='#31b053')
		desc.place(x=x, y=y)
		y += 50
	root.mainloop()


def checkbox_handle():
	if var.get() == 0:
		messagebox.showerror("Ошибка", "Пожалуйста, выберите категорию.")
	else:
		attacks_page()

def main_page():
	global root, var
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	assets = Label(root, text='Активы', font=('Consolas', 20), bg='white', fg='#31b053')
	next_button = Button(root, text='Далее', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=checkbox_handle)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=sign_in)
	var = IntVar()
	check1 = Checkbutton(root, text='Промышленные системы управления (ICS)', variable=var, font=('Consolas', 15), bg='white', fg='#31b053')
	check2 = Checkbutton(root, text='Оконечные устройства IIoT', variable=var, font=('Consolas', 15), bg='white', fg='#31b053', onvalue=2)
	check3 = Checkbutton(root, text='Коммуникационные сети и компоненты промышленной системы управления', variable=var, font=('Consolas', 15), bg='white', fg='#31b053', onvalue=3)
	check4 = Checkbutton(root, text='Информация', variable=var, font=('Consolas', 15), bg='white', fg='#31b053', onvalue=4)
	check5 = Checkbutton(root, text='Серверы и системы', variable=var, font=('Consolas', 15), bg='white', fg='#31b053', onvalue=5)
	check6 = Checkbutton(root, text='Человеческие ресурсы', variable=var, font=('Consolas', 15), bg='white', fg='#31b053', onvalue=6)
	check7 = Checkbutton(root, text='Программное обеспечение и лицензии', variable=var, font=('Consolas', 15), bg='white', fg='#31b053', onvalue=7)
	assets.place(x=100, y=70)
	check1.place(x=70, y=150)
	check2.place(x=70, y=200)
	check3.place(x=70, y=250)
	check4.place(x=70, y=300)
	check5.place(x=70, y=350)
	check6.place(x=70, y=400)
	check7.place(x=70, y=450)
	next_button.place(x=600, y=500)
	back_button.place(x=200, y=500)
	root.mainloop()


def forget_password():
	global root, login_entry, password_entry, password_entry_2
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	sign_in_label = Label(root, text='Восстановление', font=('Consolas', 40), bg='white', fg='#31b053')
	login_label = Label(root, text='Логин', font=('Consolas', 20), bg='white', fg='#31b053')
	password_label = Label(root, text='Новый пароль', font=('Consolas', 20), bg='white', fg='#31b053')
	password_label_2 = Label(root, text='Подтвердите пароль', font=('Consolas', 20), bg='white', fg='#31b053')
	login_entry = Entry(root, width=30)
	password_entry = Entry(root, width=30)
	password_entry_2 = Entry(root, width=30)
	password_button = Button(root, text='Сменить пароль', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=get_password)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=sign_in)
	sign_in_label.place(x=270, y=150)
	login_label.place(x=320, y=250)
	password_label.place(x=220, y=300)
	password_label_2.place(x=130, y=350)
	login_entry.place(x=450, y=260)
	password_entry.place(x=450, y=310)
	password_entry_2.place(x=450, y=360)
	password_button.place(x=380, y=430)
	back_button.place(x=420, y=490)
	root.mainloop()


def sign_up():
	global root, login_entry, password_entry, password_entry_2
	root.destroy()
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	sign_up_label = Label(root, text='Регистрация', font=('Consolas', 40), bg='white', fg='#31b053')
	login_label = Label(root, text='Логин', font=('Consolas', 20), bg='white', fg='#31b053')
	password_label = Label(root, text='Новый пароль', font=('Consolas', 20), bg='white', fg='#31b053')
	password_label_2 = Label(root, text='Подтвердите пароль', font=('Consolas', 20), bg='white', fg='#31b053')
	login_entry = Entry(root, width=30)
	password_entry = Entry(root, width=30)
	password_entry_2 = Entry(root, width=30)
	create_button = Button(root, text='Создать', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=register)
	back_button = Button(root, text='Назад', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=sign_in)
	sign_up_label.place(x=300, y=150)
	login_label.place(x=320, y=250)
	password_label.place(x=220, y=300)
	password_label_2.place(x=130, y=350)
	login_entry.place(x=450, y=260)
	password_entry.place(x=450, y=310)
	password_entry_2.place(x=450, y=360)
	create_button.place(x=400, y=430)
	back_button.place(x=407, y=490)
	root.mainloop()


def sign_in():
	global root, login_entry, password_entry
	try:
		root.destroy()
	except AttributeError:
		pass
	root = Tk()
	root.title('Анализ рисков IIoT')
	root.geometry('900x700')
	root.resizable(False, False)
	root.config(bg='white')
	sign_in_label = Label(root, text='Вход', font=('Consolas', 40), bg='white', fg='#31b053')
	login_label = Label(root, text='Логин', font=('Consolas', 20), bg='white', fg='#31b053')
	password_label = Label(root, text='Пароль', font=('Consolas', 20), bg='white', fg='#31b053')
	login_entry = Entry(root, width=30)
	password_entry = Entry(root, width=30)
	sign_in_button = Button(root, text='Войти', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=login)
	sign_up_button = Button(root, text='Регистрация', bg='white', fg='#31b053', borderwidth=0, command=sign_up)
	password_button = Button(root, text='Забыл пароль', font=('Consolas', 14), bg='white', fg='#31b053', borderwidth=0, command=forget_password)
	sign_in_label.place(x=400, y=150)
	login_label.place(x=300, y=250)
	password_label.place(x=300, y=300)
	login_entry.place(x=410, y=260)
	password_entry.place(x=410, y=310)
	sign_in_button.place(x=330, y=410)
	sign_up_button.place(x=405, y=370)
	password_button.place(x=450, y=410)
	root.mainloop()


def main():	
	sign_in()


if __name__ == '__main__':
	main()
