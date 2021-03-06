import json
import requests
import pickle
import datetime
import smtplib

menu = '''
          welcome to the Application
1. Add a Plan
2. View existing plans                  
3. Edit existing plans            
4. Delete existing plan
5. Check weather details of desired city          
'''


def weather_details(city_name):
    api_key = "@@@@"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    comp_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(comp_url)
    x = response.json()
    if x["cod"] != "404":
        print("Temperature (in kelvin unit) = ", x['main']['temp'], "\nMinimum Temperature (in kelvin unit) = ",
              x['main']['temp_min'],
              "\nMaximum Temperature (in kelvin unit) = ", x['main']['temp_max'],
              "\nAtmospheric pressure (in hPa unit) = ",
              x['main']['pressure'], "\nHumidity (in percentage) =",
              x['main']['humidity'], "\nVisibility (in metre unit)=", x['visibility'], "\nWind speed(in km/hr unit) =",
              x['wind']['speed'],
              "\nDescription = ", x['weather'][0]["description"])
    else:
        print('city not found')


def view_plans():
    print("\nSAVED PLANS ARE SHOWN BELOW :")
    if i == -1:
        print("SORRY NO PLANS ARE SAVED")
    else:
        for t in range(i + 1):
            print(t + 1, ". ", plan[t]['temp'])


def retrieve_data():
    list = [[], -1]
    try:
        f = open("data.dat", 'rb')
        for c in range(2):
            try:
                list[c] = pickle.load(f)
            except EOFError:
                pass
        f.close()
    except FileNotFoundError:
        pass
    return list


def saving_changes(object, counter):
    f = open('data.dat', 'wb')
    pickle.dump(object, f)
    pickle.dump(counter, f)
    f.close()


def send_email(id, password, message, receiver):
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login(id, password)
    for q in receiver:
        s.sendmail(id, q, message)
    s.quit()


temp = retrieve_data()
plan = temp[0]
i = temp[1]

while 1:
    print(menu)
    while 1:
        try:
            choice = int(input("ENTER YOUR CHOICE:"))
            break
        except ValueError:
            print("values other than integer are not acceptable")

    if choice == 1:
        i = i + 1
        plan.append({})
        plan[i]["temp"] = input("\nENTER NAME BY WHICH YOU WANT TO CALL  YOUR PLAN:")
        plan[i]['city'] = input("ENTER DESIRED CITY :")
        plan[i]['place'] = input("ENTER DESIRED PLACE:")
        plan[i]['date'] = input("ENTER DATE IN FORMAT DD-MM-YY:")
        plan[i]['mail'] = [element for element in input("ENTER EMAIL ID OF OTHER MEMBERS  OF THE PLAN:\n").split()]
        print("\nYOUR PLAN HAS BEEN SUCCESSFULLY ADDED\n")
        x = int(input("TO GO BACK TO MENU PRESS 0 AND TO END PRESS 1"))
        if x == 0:
            continue
        else:
            break

    elif choice == 2:
        view_plans()
        if i != -1:
            while 1:
                try:
                    choice = int(input("ENTER WHICH PLAN YOU WANT TO SEE:"))
                    break
                except ValueError:
                    print("values other than integer are not acceptable")
            if 0 < choice <= i + 1:
                print("\nplan name:", plan[choice - 1]["temp"], "\nCity:", plan[choice - 1]["city"], "\nPlace:",
                      plan[choice - 1]["place"],
                      "\nDate:",
                      plan[choice - 1]["date"])
                print("email id:\n")
                for e in plan[choice - 1]['mail']:
                    print(e)
                print("\ncurrent weather conditions at this city is as follows:\n")
                weather_details(plan[choice - 1]["city"])
                print("\nDO YOU WANT TO SEND AN EMAIL AS REMINDER? PRESS Y FOR YES AND OTHER SOME CHARACTER FOR NO")
                choice2 = (input())
                if choice2.lower() == 'y':
                    print("\nTYPE THE MESSAGE THAT YOU WANT TO SEND: ")
                    message = input()
                    print("\nINPUT LOGIN CREDENTIALS :\n EMAIL ID:")
                    id = input()
                    print("\n PASSWORD:")
                    password = input()
                    send_email(id, password, message, plan[choice - 1]['mail'])
                    print("\n\nMESSAGE HAS BEEN SUCCESSFULLY SENT")
            else:
                print("INVALID CHOICE")
        x = int(input("TO GO BACK TO MENU PRESS 0 AND TO END PRESS 1"))
        if x == 0:
            continue
        else:
            break

    elif choice == 3:
        view_plans()
        if i != -1:
            while 1:
                try:
                    choice = int(input("ENTER WHICH PLAN YOU WANT TO EDIT:"))
                    break
                except ValueError:
                    print("values other than integer are not acceptable")
            if 0 < choice <= i + 1:
                while 1:
                    print("1. Edit Plan Name\n2. Edit City\n3. Edit Place\n4. Edit Date\n5. Edit Email Id")
                    while 1:
                        try:
                            ch2 = int(input("ENTER CHOICE(ENTER 0 IF YOU DON'T WANT TO EDIT MORE):"))
                            break
                        except ValueError:
                            print("values other than integer are not acceptable")
                    if ch2 == 1:
                        plan[choice - 1]['temp'] = input("ENTER NEW PLAN NAME")
                    elif ch2 == 2:
                        plan[choice - 1]['city'] = input("ENTER NEW CITY NAME")
                    elif ch2 == 3:
                        plan[choice - 1]['place'] = input("ENTER NEW PLACE NAME")
                    elif ch2 == 4:
                        plan[choice - 1]['date'] = input("ENTER NEW DATE NAME")
                    elif ch2 == 5:
                        plan[choice - 1]['mail'] = [element for element in
                                                    input("ENTER NEW SET OF EMAIL ID:\n").split()]
                    elif ch2 == 0:
                        break
                    else:
                        print("INVALID CHOICE")
            else:
                print("INVALID CHOICE")
        x = int(input("TO GO BACK TO MENU PRESS 0 AND TO END PRESS 1"))
        if x == 0:
            continue
        else:
            break

    elif choice == 4:
        view_plans()
        if i != -1:
            while 1:
                try:
                    choice = int(input("ENTER WHICH PLAN YOU WANT TO DELETE:"))
                    break
                except ValueError:
                    print("values other than integer are not acceptable")
            if 0 < choice <= i + 1:
                plan.pop(choice - 1)
                print("\nENTERED CHOICE HAS BEEN SUCCESSFULLY DELETED")
            else:
                print("INVALID CHOICE")
        x = int(input("TO GO BACK TO MENU PRESS 0 AND TO END PRESS 1"))
        if x == 0:
            continue
        else:
            break

    elif choice == 5:
        city_name = input("enter the name of city whose weather you want to check:")
        weather_details(city_name)
        print("\n")
        x = int(input("TO GO BACK TO MENU PRESS 0 AND TO END PRESS 1"))
        if x == 0:
            continue
        else:
            break
    else:
        print("\nINVALID CHOICE\n")
        x = int(input("TO GO BACK TO MENU PRESS 0 AND TO END PRESS 1"))
        if x == 0:
            continue
        else:
            break
saving_changes(plan, i)
