import telebot
import pickle
token="my_token"
bot = telebot.TeleBot(token)
print("WORK")
def members_list_inp():
    with open('Members.txt','rb') as inp:
        all_members = pickle.load(inp)
    return all_members
def menu_list_inp():
    with open('Menu.txt','rb') as inp:
        all_menu = pickle.load(inp)
    return all_menu
def answer_list_inp():
    with open('Answer.txt','rb') as inp:
        all_answer = pickle.load(inp)
    return all_answer
def quiz_list_inp():
    with open('Quiz.txt','rb') as inp:
        all_quiz = pickle.load(inp)
    return all_quiz
def am_list_inp():
    with open('AM.txt','rb') as inp:
        administrator_list = pickle.load(inp)
    return administrator_list
def members_list_out(data):
    with open('Members.txt', 'wb') as out:
        pickle.dump(data, out)
def menu_list_out(data):
    with open('Menu.txt', 'wb') as out:
        pickle.dump(data, out)
def answer_list_out(data):
    with open('Answer.txt', 'wb') as out:
        pickle.dump(data, out)
def quiz_list_out(data):
    with open('Quiz.txt', 'wb') as out:
        pickle.dump(data, out)
def am_list_out(data):
    with open('AM.txt', 'wb') as out:
        pickle.dump(data, out)

def keybord_main(main_id, mes):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Чем занимается ОРМП?')
    user_markup.row('Где нас найти?')
    user_markup.row('Викторина')
    bot.send_message(main_id, mes, reply_markup=user_markup)
def update_menu_error(main_id):
    keybord_main(main_id, "Похоже данное меню только что обновилось.")

def keybord_general(main_id,user_id,members=None,id_menu_for_new_buttons=None,mode=None,question_number=None,quiz_answer=None,mes=None):#Mode=1 - Список викторин, Mode=2 - Виктарина
    try:
        result_was=False
        if (id_menu_for_new_buttons!=list(members[user_id][1][0].keys())[0])and(id_menu_for_new_buttons!=None):# Проверка обращений к разным меню
            update_menu_error(main_id)
            members[user_id][1] = [{}]
            members_list_out(members)
        else:
            photo=[]
            if mode==1: #Данные для списка викторин
                buttons_for_add = quiz_answer.keys()
                mes ="Выберите викторину:"
            elif mode==2: #Идет викторина
                count_answer=quiz_answer[list(members[user_id][1][0].keys())[0][0:-5]][0]
                if int(question_number)>len(count_answer):
                    result_from_base=members[user_id][2][0][list(members[user_id][1][0].keys())[0]][0]
                    mes="Тест пройден. Ваш результат: {0} из {1}".format(result_from_base, len(count_answer))
                    quiz_answer_for_this_qwiz=quiz_answer[list(members[user_id][1][0].keys())[0][0:-5]]
                    if len(quiz_answer_for_this_qwiz)>1:#Проверка на наличие дополнительного тектса к результату/наличие фото к результату
                        if ("right_count" in quiz_answer_for_this_qwiz[1].keys()):
                            if (result_from_base>=quiz_answer_for_this_qwiz[1]["right_count"]):#Количество правильных ответов больше или равно задданного
                                if ("right_answer" in quiz_answer_for_this_qwiz[1].keys()):
                                    if ("photo" in quiz_answer_for_this_qwiz[1]["right_answer"].keys()):
                                        for i in quiz_answer_for_this_qwiz[1]["right_answer"]["photo"]:
                                            bot.send_photo(main_id,i)
                                    if ("text" in quiz_answer_for_this_qwiz[1]["right_answer"].keys()):
                                        for i in quiz_answer_for_this_qwiz[1]["right_answer"]["text"]:
                                            mes+="\n"+i
                            elif (result_from_base<quiz_answer_for_this_qwiz[1]["right_count"]):#Количество правильных ответов меньше задданного
                                if ("bad_answer" in quiz_answer_for_this_qwiz[1].keys()):
                                    if ("photo" in quiz_answer_for_this_qwiz[1]["bad_answer"].keys()):
                                        for i in quiz_answer_for_this_qwiz[1]["bad_answer"]["photo"]:
                                            bot.send_photo(main_id, i)
                                    if ("text" in quiz_answer_for_this_qwiz[1]["bad_answer"].keys()):
                                        for i in quiz_answer_for_this_qwiz[1]["bad_answer"]["text"]:
                                            mes += "\n"+i
                    keybord_main(main_id,mes=mes)
                    members[user_id][1]=[{},0]
                    members_list_out(members)
                    result_was=True
                else:#Данные для вопроса в викторине
                    buttons_for_add = quiz_answer[list(members[user_id][1][0].keys())[0][0:-5]][0][question_number][1]
                    mes = "Вопрос номер {0}.\n{1}".format(question_number,quiz_answer[list(members[user_id][1][0].keys())[0][0:-5]][0][question_number][0][0])
                    #quiz_answer={"Первая викторина":[{"1":[["Какая это викторина?"],["2","1","3","4"],["1"],[{"photo":["AgACAgIAAxkBAAIHSl-aqCQq3FAOXTnjH_tiqmcJPkWZAALSsDEbUTnQSPYKa0ziNLzw9wZtly4AAwEAAwIAA20AAwVwAgABGwQ"]}]],
                    if len(quiz_answer[list(members[user_id][1][0].keys())[0][0:-5]][0][question_number])>=4:
                        if "photo" in quiz_answer[list(members[user_id][1][0].keys())[0][0:-5]][0][question_number][3][0].keys():
                            photo=quiz_answer[list(members[user_id][1][0].keys())[0][0:-5]][0][question_number][3][0]["photo"]
            else:
                menu_list=menu_list_inp()
                buttons_for_add=menu_list[id_menu_for_new_buttons][0]
                mes=menu_list[id_menu_for_new_buttons][1]
            if result_was==False:#Вывод всех меню, кроме результатов к викторине
                buttons_added = [[], [], [],[]]
                four_rez = buttons_for_add
                if len(buttons_for_add) > 4:
                    four_rez = buttons_for_add[members[user_id][1][0][id_menu_for_new_buttons]:members[user_id][1][0][id_menu_for_new_buttons] + 4]
                e = 0
                for i in four_rez:
                    if len(buttons_added[e]) < 1:
                        buttons_added[e].append(i)
                    else:
                        e += 1
                        buttons_added[e].append(i)
                user_markup = telebot.types.ReplyKeyboardMarkup(True)
                user_markup.row(*buttons_added[0])
                user_markup.row(*buttons_added[1])
                user_markup.row(*buttons_added[2])
                user_markup.row(*buttons_added[3])
                if (len(buttons_for_add) > 4) and (mode!=2):
                    if members[user_id][1][0][id_menu_for_new_buttons]==0:
                        buttons_to_next=[" ","Далее"]
                    elif members[user_id][1][0][id_menu_for_new_buttons]+4>=len(buttons_for_add):
                        buttons_to_next=["Назад"," "]
                    else:
                        buttons_to_next=["Назад","Далее"]
                    user_markup.row(*buttons_to_next)
                user_markup.row("К главному меню")
                if len(photo)>0:
                    if len(photo)==1:
                        bot.send_photo(main_id,photo[0],caption=mes,reply_markup=user_markup)
                    elif len(photo)>1:
                        bot.send_photo(main_id, photo[0], caption=mes, reply_markup=user_markup)
                        del photo[0]
                        for i in photo:
                            bot.send_photo(main_id,i)
                elif len(photo)==0:
                    bot.send_message(main_id, mes, reply_markup=user_markup)
    except Exception as Error:
        bot.send_message(main_id,"Похоже произошёл сбой. Попробуйте ещё раз. Если ошибка останется - свяжитесь с нами.")
        print(Error)
def answer_for_menu(main_id,user_id,id_answer_for_return):
    mes = answer_list_inp()[id_answer_for_return]
    bot.send_message(main_id, mes)
@bot.message_handler(commands=['start'])
def handle_start(message):
    keybord_main(message.chat.id,"Привет. Я бот от отдела по реализации молодежной политики ДГТУ.")
    members = members_list_inp()
    if message.chat.id in members.keys():
        members[message.chat.id][1]=[{},0]
    else:
        members[message.chat.id]=[["0"],[{},0],[{}],[message.from_user.id],[message.from_user.username]]
    members_list_out(members)

@bot.message_handler(content_types=['text'])
def handle_start(message):
    try:
        members = members_list_inp()
        chat_id = message.chat.id
        if (message.chat.id in members.keys())==False:
            members[message.chat.id]=[["0"],[{},0],[{}],[message.from_user.id],[message.from_user.username]]
            members_list_out(members)
            update_menu_error(chat_id)
        elif message.text.lower()== 'К главному меню'.lower():
            keybord_main(message.chat.id, "Привет. Я бот от отдела по реализации молодежной политики ДГТУ.")
            members[chat_id][1] = [{}]
            members_list_out(members)
        elif message.text.lower()=='Викторина'.lower():
            members[chat_id][1][0]["choice_QUIZ"]=0
            members_list_out(members)
            quiz_answer = quiz_list_inp()
            keybord_general(chat_id, chat_id,mode=1,members=members,quiz_answer=quiz_answer)
        elif message.text.lower() in menu_list_inp().keys():
            members[chat_id][1][0][message.text.lower()]=0
            members_list_out(members)
            members = members_list_inp()
            keybord_general(chat_id,chat_id,id_menu_for_new_buttons=message.text.lower(),members=members)
        elif message.text.lower() in answer_list_inp().keys():
            answer_for_menu(chat_id,chat_id,message.text.lower())
        elif len(members[chat_id][1][0].keys())>0:
            quiz_answer = quiz_list_inp()
            name_menu=list(members[chat_id][1][0].keys())[0]
            if name_menu.endswith("_QUIZ"):
                if name_menu=="choice_QUIZ":
                    if message.text in list(quiz_answer.keys()):
                        checking_the_number_of_times=True
                        if "{0}_QUIZ".format(message.text) in members[chat_id][2][0].keys():
                            if len(quiz_answer["{0}_QUIZ".format(message.text)[0:-5]]) > 0:  # НЕОБХОДИМО УСЛОВИЕ ПРОВЕРКИ КОЛИЧЕСТВА ПРОЙДЕННЫХ РАЗ ОДНОЙ ВИКТОРИНЫ
                                if len(quiz_answer["{0}_QUIZ".format(message.text)[0:-5]])>1:
                                    if quiz_answer["{0}_QUIZ".format(message.text)[0:-5]][1]["count"] <= members[chat_id][2][0]["{0}_QUIZ".format(message.text)][1]:#Если верно, то вывод сообщения о привышении количества попыток к викторине
                                        checking_the_number_of_times=False
                                    else:
                                        members[chat_id][2][0]["{0}_QUIZ".format(message.text)] = [0,members[chat_id][2][0]["{0}_QUIZ".format(message.text)][1] + 1]
                                else:
                                    members[chat_id][2][0]["{0}_QUIZ".format(message.text)] = [0, members[chat_id][2][0]["{0}_QUIZ".format(message.text)][1] + 1]
                            else:
                                members[chat_id][2][0]["{0}_QUIZ".format(message.text)] = [0, members[chat_id][2][0]["{0}_QUIZ".format(message.text)][1]+1]
                        else:
                            members[chat_id][2][0]["{0}_QUIZ".format(message.text)] = [0,1]
                        if checking_the_number_of_times==True:
                            members[chat_id][1] = [{}]
                            members[chat_id][1][0]["{0}_QUIZ".format(message.text)] = 0
                            if len(members[chat_id][1])==2:
                                members[chat_id][1][-1]="1"
                            elif len(members[chat_id][1])==1:
                                members[chat_id][1].append("1")
                            members_list_out(members)
                            keybord_general(chat_id, chat_id, mode=2,question_number="1",members=members,quiz_answer=quiz_answer)
                        elif checking_the_number_of_times==False:
                            bot.send_message(chat_id, "Вы уже прошли викторину максимальное количество раз.")
                    else:
                        update_menu_error(chat_id)
                elif name_menu[0:-5] in list(quiz_answer.keys()):
                    if len(members[chat_id][1]) == 2:
                        if message.text==quiz_answer[list(members[chat_id][1][0].keys())[0][0:-5]][0][str(members[chat_id][1][1])][2][0]:
                            members[chat_id][2][0][name_menu][0] +=1
                        members[chat_id][1][-1] = str(int(members[chat_id][1][1]) + 1)
                        members_list_out(members)
                    keybord_general(chat_id, chat_id, mode=2, question_number=str(int(members[chat_id][1][1])),members=members,quiz_answer=quiz_answer)
                else:
                    update_menu_error(chat_id)
    except Exception as Error:
        bot.send_message(message.chat.id,"Похоже произошёл сбой. Попробуйте ещё раз. Если ошибка останется - свяжитесь с нами.")
        print(Error)
bot.polling(none_stop=True)