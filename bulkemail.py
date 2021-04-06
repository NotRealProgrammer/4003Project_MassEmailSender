from getpass import getpass
import os.path
import os
from os import path
import xml.etree.ElementTree as ET
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import codecs
from glob import glob
import sys

_Username = None
authenticated = False
topcs_array = ["Topic1","Topic2","Topic3","Topic4"]
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def create_xml():
    if not path.exists("Accounts.xml"):
        data = ET.Element('DataAccount')
        items = ET.SubElement(data, 'firstmail')
        item1 = ET.SubElement(items, 'test')
        item1.set('name','item1')
        item1.text = 'firstmail'

       
        mydata = ET.tostring(data)
        with open("Accounts.xml", "wb") as f:
            f.write(mydata)
        
def add_users(username,password,email):
    tree = ET.parse('Accounts.xml')
    root = tree.getroot()
    att = {"Type":"Username"}
    element = root.makeelement(username,att)
    root.append(element)
    ET.SubElement(element,"Password").text = password
    ET.SubElement(element,"Email").text = email

    tree.write('Accounts.xml')


def Main_Load():
    create_xml()
    isaccountcreated = input("Do you have a account? (yes/no)")
    create_user(isaccountcreated)
    Main()

def Main():
    index = 0
   
    admin_tpcs = ["1. Send Mails","2. Delete Topic", "3. Delete User","4. Exit Program"]
    
    dashboard_opt = ["1. Select News","2. Cancel News subscription","3. Leave program"]
    if authenticated == True:
        print(" Welcome USER - \033[92m%s\033[0m to your dashboard" % _Username)
        print(" Select one of the followings ")
        if _Username != "root":
            for item in dashboard_opt:
                print(item)
            user_opt = int(input())
            if user_opt == 1:
                pass
            elif user_opt == 2:
                    tree = ET.parse('Accounts.xml')
                    parent = tree.find(_Username)
                    element = parent.find("Topic")
                    parent.remove(element)
                    tree.write("Accounts.xml")
                    Main()
            elif user_opt == 3:
                exit()
            else:
                os.system('cls')
                print("Can't find that option "+bcolors.FAIL+":("+bcolors.ENDC+" ! Try again")
                Main()
        else:
            for item in admin_tpcs:
                print(item)
            user_opt = int(input())
            if user_opt == 1:
                send_email()
               
                print(bcolors.OKGREEN + "All mails have been sent! Congratz your users have now receive their newsletters!"+bcolors.ENDC)
                Main()
            elif user_opt == 2:
                os.system('cls')
                counter = 0
                print("Select from the followings the topic that you want to delete:")
                for topic in topcs_array:
                    print(str(counter)+"." + topic)
                    counter += 1
                Ntpc = int(input())
                if Ntpc >= 0 and Ntpc < len(topcs_array):
                    topcs_array.pop(Ntpc)
                    os.system('cls')
                    print(bcolors.OKGREEN + "Topic Deleted sucessfully!" + bcolors.ENDC)
                    Main()
                else:
                    print(bcolors.FAIL + "Topic Not Found!" + bcolors.ENDC)
                    Main()

            elif user_opt == 3:
                os.system('cls')
                delete_user = input("Write the name of the user that you want to delete:")
                tree = ET.parse('Accounts.xml')
                element = tree.find(delete_user)
                if element != None:
                    root = tree.getroot()
                    root.remove(element)
                    tree.write("Accounts.xml")
                    Main()
                else:
                    os.system("cls")
                    print(bcolors.FAIL+ "No user with the name of "+delete_user+" found. Please try again!"+bcolors.ENDC)
                    Main()

            elif user_opt == 4:
                exit()
            else:
                os.system('cls')
                print(bcolors.FAIL+"Can't find the option you selected please try again!"+bcolors.ENDC)
                Main()

        


        os.system('cls')
        print(" Which of the following topics you want to receive news in your email?")
        for topics in topcs_array:
            print(str(index) + ": " + topics)
            index += 1
        choise = input()
        if int(choise) >= 0 and int(choise) < 4:
            Write_Topic(int(choise))
            Main()
        else:
            print(bcolors.FAIL + "That option does not exist!" + bcolors.ENDC)
            Main()
        
    else:
        os.system('cls')
        print(bcolors.WARNING + "Authentification failed! Please re-type your username and password.." + bcolors.ENDC)
        Main_Load()

def Write_Topic(choise):
    tree = ET.parse('Accounts.xml')
    element = tree.find(_Username)
    tpc_text = topcs_array[choise]
    if element.find("Topic") == None:
        ET.SubElement(element,"Topic").text = tpc_text
        ET.SubElement(element,"Confirmation").text = "Not Confirmed"
        tree.write('Accounts.xml')
        print("You choose "+tpc_text+"")
        os.system('cls')
        print(bcolors.OKGREEN + "From now on you will receive news from this topic! If you want to cancel just go back to your dashboard and "+bcolors.FAIL+"cancel it" + bcolors.ENDC)
    elif element.findtext("Topic").strip() == tpc_text.split():
        os.system('cls')
        print(bcolors.WARNING + "You're choosing the same topic that is already on your account please, choose another!"+bcolors.ENDC)
        Main()
    else:
        print(bcolors.BOLD + "You changed from "+element.find("Topic").text.strip()+" to "+tpc_text+". You will receive this kind of topics from now on" + bcolors.ENDC)


def send_email():
    
    me = "4003newsletter@gmail.com"
    root = ET.parse('Accounts.xml').getroot()
    element = root.find("Email")
    Email_Dictionary = {Topic:[] for Topic in os.listdir("Topics")}
    for item in root.iter():
        try:
            if item.attrib["Type"] == "Username":
                Email_Dictionary[""+item.findtext("Topic")+""].append(item.findtext("Email"))
        except:
            continue

 
    Topics_path = [Topic for Topic in os.listdir("Topics")]
    for key,value in Email_Dictionary.items():
        if key != "None":
            try:
                for email in value:
                    you = email
                    images_path = [os.path.join("Topics/"+key+"/images", i) for i in os.listdir("Topics/"+key+"/images")]
                    images_name = [images for images in os.listdir("Topics/"+key+"/images")]
                    msg = MIMEMultipart('alternative')
                    msg['Subject'] = key
                    msg['From'] = me
                    msg['To'] = you
                    htmlcode = codecs.open("Topics/"+key+"/test.html", 'r')
                    part2 = MIMEText(htmlcode.read(), 'html')
                    msg.attach(part2)
                
                    for (path, name) in zip(images_path,images_name):
                    
                        with open('{}'.format(path), "rb") as attachment:
                            msgImage = MIMEImage(attachment.read(),_subtype="png")

                        msgImage.add_header('Content-ID', '<{}>'.format(name))
                        msg.attach(msgImage)

                    s = smtplib.SMTP_SSL('smtp.gmail.com')
                    s.login(me, "123test123")

                    s.sendmail(me, you, msg.as_string())
                    s.quit()
                else:
                    print(bcolors.WARNING+"User with email "+value+" dindn't choose his topic yet!"+bcolors.ENDC)
                    continue
            except:
                continue

def auth_user():
    global _Username
    global authenticated
    username = input("Username:")
    _Username = username
    password = getpass()
    tree = ET.parse('Accounts.xml')
   
    for item in tree.findall(username):
        if item.findtext("Password").strip() == password.strip():
            authenticated=True
            Main()
            break

        else:
            authenticated=False
            Main()
            break
    

def create_user(isaccountcreated):
    if isaccountcreated == "no":
        username = input("Username:")
        if not username.isalpha():
            print(bcolors.FAIL+"You can't use special characters or numeric! Please try again"+bcolors.ENDC)
            create_user("no")
        password = getpass()
        email = input("Email:")
        add_users(username,password,email)
        auth_user()
    else:
        auth_user()

Main_Load()
