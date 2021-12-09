from py3pin.Pinterest import Pinterest
import json
import time
import random
import pathlib
import stringcase
import psycopg2
import sys
from psycopg2 import connect
from psycopg2 import OperationalError, errorcodes, errors
from psycopg2 import __version__ as psycopg2_version
from psycopg2 import OperationalError, errorcodes, errors
from psycopg2 import __version__ as psycopg2_version
import string




proxies={"http":"http://192.109.165.228:80"}

pinterest = Pinterest(email="LuzCHammond@outlook.com",
                      password="Savings$2022",
                      username="luzchammond",
                      cred_root='cred_root'
                      #,proxies=proxies
                      )

#pinterest.login(proxy='192.109.165.228:80')
pinterest.login()



# to release
# python3 setup.py sdist & twine upload --skip-existing dist/*
# proxies example:
# proxies = {"http":"http://username:password@proxy_ip:proxy_port"}
# Pinterest(email='emai', password='pass', username='name', cred_root='cred_root', proxies=proxies)


# login will obtain and store cookies for further use, they last around 15 days.
# NOTE: Since login will store the cookies in local file you don't need to call it more then 3-4 times a month.

def follow(user_id=''):
    # even if you already follow this user a successful message is returned
    return pinterest.follow_user(user_id=user_id)

# Careful with category names. They have different names than as shown on Pinterest
def create_board(name='',
                 description='',
                 category='other',
                 privacy='public',
                 layout='default'):
    return pinterest.create_board(name=name, description=description, category=category,
                                  privacy=privacy, layout=layout)

def search(max_items=1, scope='pins', query='food'):
    # After change in pinterest API, you can no longer search for users
    # Instead you need to search for something else and extract the user data from there.
    # current pinterest scopes are: pins, buyable_pins, my_pins, videos, boards
    results = []
    search_batch = pinterest.search(scope=scope, query=query)
    while len(search_batch) > 0 and len(results) < max_items:
        results += search_batch
        search_batch = pinterest.search(scope=scope, query=query)

    return results

def search_p(query='food'):
    # After change in pinterest API, you can no longer search for users
    # Instead you need to search for something else and extract the user data from there.
    # current pinterest scopes are: pins, buyable_pins, my_pins, videos, boards
    results = []
    search_batch = pinterest.search_pins(query=query)
    while len(search_batch) > 0 and len(results) < max_items:
        results += search_batch
        search_batch = pinterest.search_pins(query=query)

    return results

def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b]

def before(value, a):
    # Find first part and return slice before it.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    return value[0:pos_a]

def after(value, a):
    # Find and validate first part.
    pos_a = value.rfind(a)
    if pos_a == -1: return ""
    # Returns chars after the found string.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value): return ""
    return value[adjusted_pos_a:]

def follow(username):
    #conn = psycopg2.connect(host="ec2-34-233-105-94.compute-1.amazonaws.com", port = 5432, database="dfavl1irjtv2gv", user="laudpederxikmf", password="08ef57382ac0892ecbe700c0baadf1c65152e80ed333e440d5eb406c278e475f")
    #cur = conn.cursor()
    #followers_list_info=[]

    own_username=username
    file1 = open("follow_lindajhawkinson.txt","r")
    followed_followers_list_info_file=file1.readlines()
    followed_followers_list_gather_metadata=[]
    followed_followers_list_gather=[]
    followed_followers_list_real=[]

    for followed_followers in followed_followers_list_info_file:
        followed_followers=str(followed_followers)
        followed_followers=followed_followers.strip()
        followed_followers_strip=followed_followers.strip('\n\r\t')

        followers_batch = pinterest.get_user_followers(username=followed_followers_strip)
        print(f"Got the followers for {followed_followers_strip}. Taking between 1 minute break.")
        time.sleep(random.randint(50,70))
        while len(followers_batch) > 0:
            for followers_list in followers_batch:
                dict_followers_list=dict(followers_list)
                for key, value in dict_followers_list.items():
                    followed_followers_list_gather_metadata.append(followed_followers_strip)
                    if(key == "username"):
                        value=str(value)
                        value=value.strip('\n\r\t')
                        followed_followers_username=value
                        print(f"The username is {value}")
                        followed_followers_list_gather_metadata.append(value)
                        followed_followers_list_gather.append(value)
                    if(key == "follower_count"):
                        value=str(value)
                        value=value.strip('\n\r\t')
                        print(f"The follower count is {value}")
                        followed_followers_list_gather_metadata.append(value)
                flag_follower_existence=False
                print(f"Checking whether {followed_followers_username} is followed by your account: {own_username}")
                s_following_batch = pinterest.get_following(username=own_username)
                print(f"Got the following list for your account: {own_username}. Taking between 1 minute break.")
                time.sleep(random.randint(50,70))
                while len(s_following_batch) > 0:
                    for s_following_list in s_following_batch:
                        s_dict_following_list=dict(s_following_list)
                        for key, value in s_dict_following_list.items():
                            if(key == "username"):
                                value=str(value)
                                value=value.strip('\n\r\t')
                                if(value == followed_followers_username):
                                    flag_follower_existence=True
                                    print(f"{followed_followers_username} Already Found in Your Following List for the account: {own_username}")
                    s_following_batch = pinterest.get_following(username=own_username)

                if not flag_follower_existence:
                    print(f"{followed_followers_username} Not Found in Your Following List for the account: {own_username}, So Following the same username")
                    pinterest.follow_user(followed_followers_username)
                    followed_followers_list_real.append(followed_followers_username)
                    print(f"Done with following {followed_followers_username} by your account: {own_username}")
                    print("----------------------------------------------------------")
                    print(f"Following list for the {own_username} right now:")
                    print(followed_followers_list_real)
                    print("----------------------------------------------------------")
                    return

                print("*********************************************************")
                print(f"Username list for the {followed_followers_strip} right now:")
                print(followed_followers_list_gather)
                print(len(followed_followers_list_gather))
                print("*********************************************************")
            followers_batch = pinterest.get_user_followers(username=followed_followers_strip)

    file1.close()
    print(followed_followers_list_gather_metadata)


def first_interaction(username):
    conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
    cur = conn.cursor()
    boards_list_info=[]

    file1 = open("boards_luzchammond.txt","r")
    #file8 = open("createdboards.txt","r")
    cur.execute(f"""select created_board_name from first_interaction where username='{username}' and created_board='True'""")
    boards_list_info = cur.fetchone()
    print(boards_list_info)
    boards_list_information=[]
    if boards_list_info == None:
        #boards_list_information=[]
        noboardsexist=True
    else:
        print(boards_list_info)
        noboardsexist=False

    cur.close()
    conn.commit()
    conn.close()

    board_num=0
    #boards_sync= True
    create_board=False
    boards_list_info_file=file1.readlines()

    for board_name_list in boards_list_info_file:
        temp_list=  board_name_list.split()
        list= []
        board_name_pascal=""
        for i in temp_list:
            list.append(stringcase.pascalcase(i))
        #            print(list)
        for i in list:
            board_name_pascal+=str(i) + " "
        board_name_pascal=board_name_pascal.strip()
        board_name_pascal_strip=board_name_pascal.strip('\n\r\t')


        if noboardsexist:
            print("Starting Inserting The Data")

        else:
            conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
            cur = conn.cursor()
            cur.execute(f""" select created_board_name from first_interaction where username='{username}' and created_board='True' """)
            boards_list_info=cur.fetchall()
            cur.close()
            conn.commit()
            conn.close()

        board_list_wo_dup=boards_list_info
        #print(board_list_wo_dup)

        print("------------------------------------------------------------")

        conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
        cur = conn.cursor()
        #if board_list_wo_dup:
        #    if board_num == len(board_list_wo_dup):
        #        boards_sync=False

        if not board_list_wo_dup:
            create_board=True

        if board_list_wo_dup:
            print(board_name_pascal_strip.strip())
            print(board_list_wo_dup)
            #if board_name_pascal_strip.strip() in board_list_wo_dup:
            #    print(f"The board: ->{board_name_pascal_strip}<- does already exist")
            for i in board_list_wo_dup:
                #print(i)
                bad_chars = ['('', '',)']
                test_string = i
                test_string = ''.join(i for i in test_string if not i in bad_chars)
                #print(str(test_string))
                #print(f"->{board_name_pascal_strip}<- and ->{str(test_string)}<-")
                if board_name_pascal_strip == str(test_string):
                    print(f"The board: ->{board_name_pascal_strip}<- does already exist")
                    board_num=board_num+1
                    print(board_num)
                    print(len(board_list_wo_dup))
                    print(str(test_string))
                    noboardsexist=False
                    create_board=False
                    #print(create_board)
                    break
                else:
                    create_board=True
                    #print(create_board)

        if create_board:
            #print(board_name_list)
            #print(boards_list_info)
            #else:
            print(create_board)
            print(f"Creating A Board: ->{board_name_pascal_strip}<-")
            #cur.execute(f"""update first_interaction set created_board='{board_name_pascal_strip}', created_board_name='True' where username='{username}'""")
            #boards_list_info = cur.fetchall()
            pinterest.create_board(name=board_name_pascal_strip)
            cur.execute(f"""insert into first_interaction(username, init_boards_name, created_board_name, created_board) values('{username}','{board_name_list}','{board_name_pascal_strip}','True')""")
            print(f"Created The Board ->{board_name_pascal_strip}<-")
            print(board_name_pascal_strip)
            print("\n")
            #board_list_wo_dup.append(board_name_pascal_strip.strip)
            time.sleep(random.randint(7,10))
            #boards_list_information.append(board_name_pascal_strip)
            noboardsexist=False
            cur.close()
            conn.commit()
            conn.close()
        print("------------------------------------------------------------")



    file1.close()

#        while True:
#            try:
#              pinterest.create_board(name=board_name_list)
#                time.sleep(random.randint(12,15))
#            except:
#                continue
#            results=search(scope='pins',query=board_name_list)



def first_related_pins_pinning(board_name,board_id,username):

    Boards_exists=False
    conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
    cur = conn.cursor()

    cur.execute(f""" select record_count from general_pin where username='{username}' and board_id='{board_id}' """)
    #boards_list_info=cur.fetchone()
    #boards_list_info=cur.fetchone()

    i=cur.fetchone()

    if i:
        bad_chars = ['('', '',)']
        test_string = i
        test_string = ''.join(i for i in test_string if not i in bad_chars)
        print(int(test_string))
        record_count=int(test_string)
    else:
        record_count=0

    cur.close()
    conn.commit()
    conn.close()

    boards_dict={}

    if record_count > 30:
        Boards_exists=True
    #print(Boards_exists)

    boards_dict={}

    if Boards_exists:
        print("The Board exists with the enough pins...")
        return

    results=search(10,'pins',board_name)
    your_dict = dict(enumerate(results))

    sel_board_id=board_id.strip('\n\r\t')
    sel_board_id=sel_board_id.strip()

    for key, value in your_dict.items():
        if type(value) is dict:
            for t, c in value.items():
                if(t == "id"):
                    pin_id=c.strip('\n\r\t')
                    pin_id=pin_id.strip()
                    print(f" The username is '{username}', the board id is '{board_id}' and the pin id is '{pin_id}' ")
                    conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
                    cur = conn.cursor()
                    cur.execute(f""" insert into general_pin(username,board_id,pin_id,completed) values('{username}','{sel_board_id}','{pin_id}','true')  """)
                    cur.close()
                    conn.commit()
                    conn.close()

    conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
    cur = conn.cursor()
    cur.execute(f""" select * from general_pin where username='{username}' and board_id='{board_id}'  """)
    pin_records=cur.fetchall()
    selected=[]
    for i in pin_records:
        selected.append(i[2])

    i=1
    p=0
    range_interval=random.randint(70,80)
    n=1
    key=0


    start=time.time()
    while i <= len(selected) and p <= range_interval:

        if (i == 1):
            print("------------------------------------------------------------")
            daily_interaction_file = open("dailypins_luzchammond.txt", "r")
            pins_list_info = daily_interaction_file.readlines()
            daily_interaction_file.close()
            list = []
            for pin_list in pins_list_info:
                pin_split_list=pin_list.split(",")
                print(pin_split_list)
                for i in range(len(pin_split_list)):
                    if i == 0:
                        temp_pin_id=pin_split_list[0]
                        temp_pin_id=temp_pin_id.strip()
                        temp_pin_id=temp_pin_id.strip('\n\r\t')
                        print(temp_pin_id)
                        list.append(temp_pin_id)

                    if i == 1:
                        temp_desc=pin_split_list[1]
                        temp_desc=temp_desc.strip()
                        temp_desc=temp_desc.strip('\n\r\t')
                        print(temp_desc)
                        list.append(temp_desc)

            for i in range(len(list)):
                if i % 2 == 0:
                    print(f" The Selected Board: ->{board_name}<- Board Id: ->{sel_board_id}<- is where the pin ->{list[i]}<- is gonna be pinned")
                    pinterest.repin(board_id=sel_board_id,pin_id=str(list[i]))
                    print(f" The Selected pin: ->{list[i]}<- has been successfully pinned.")
                    print(f" Going to take between 30 to 40 seconds. I'm so tired !!!")
                    time.sleep(random.randint(30,40))

        if (i < 5):
            #            print(f" The Selected pin: ->{selected[i]}<- is gonna be pinned")
            print(selected[i].isnumeric())
            if selected[i].isnumeric():
                print("------------------------------------------------------------")
                #selected[i]=selected[i].strip('\n\r\t')
                #sel_pin_id=selected[i].strip()
                print(f" The Selected Board: ->{board_name}<- Board Id: ->{sel_board_id}<- is where the pin ->{selected[i]}<- is gonna be pinned")
                pinterest.repin(board_id=sel_board_id,pin_id=selected[i])
                print(f" The Selected pin: ->{selected[i]}<- has been successfully pinned.")
                print(f" Going to take between 30 to 40 seconds. I'm so tired !!!")
                time.sleep(random.randint(30,40))
                #print(f"The board id is {sel_board_id}, the pin id is {selected[i]}")        
                p=p+1

            elif not selected[i].isnumeric():
                if len(str(selected[i])) > 30:
                    print("------------------------------------------------------------")
                    print(f" The Selected Board: ->{board_name}<- Board Id: ->{sel_board_id}<- is where the pin ->{selected[i]}<- is gonna be pinned")
                    pinterest.repin(board_id=sel_board_id,pin_id=selected[i])
                    print(f" The Selected pin: ->{selected[i]}<- has been successfully pinned")
                    print(f" Going to take between 30 to 40 seconds. I'm so tired !!!")
                    time.sleep(random.randint(30,40))
                    p=p+1
      
            i=i+1
            print("------------------------------------------------------------")
        else:
            
            if n >= 5:
                n=0

            
            index_pin=i + n

            sel_pin_id_ab=selected[index_pin].strip('\n\r\t')
            sel_pin_id_ab=sel_pin_id_ab.strip()

            print("->"+str(sel_pin_id_ab)+"<-")
            if str(sel_pin_id_ab).isnumeric():
                print(sel_pin_id_ab.isnumeric())
                print("------------------------------------------------------------")
                print(f" The Selected Board: ->{board_name}<- Board Id: ->{sel_board_id}<- is where the pin ->{sel_pin_id_ab}<- is gonna be pinned")
                pinterest.repin(board_id=sel_board_id,pin_id=sel_pin_id_ab)
                print(f" The Selected pin: ->{sel_pin_id_ab}<- has been successfully pinned")
                print(f" Going to take between 30 to 40 seconds. I'm so tired !!!")
                time.sleep(random.randint(30,40))      
                p=p+1
            elif not str(sel_pin_id_ab).isnumeric():
                if len(str(sel_pin_id_ab)) > 30:
                    print(sel_pin_id_ab.isalnum())
                    print("------------------------------------------------------------")
                    print(f" The Selected Board: ->{board_name}<- Board Id: ->{sel_board_id}<- is where the pin ->{sel_pin_id_ab}<- is gonna be pinned")
                    pinterest.repin(board_id=sel_board_id,pin_id=sel_pin_id_ab)
                    print(f" The Selected pin: ->{sel_pin_id_ab}<- has been successfully pinned")
                    print(f" Going to take between 30 to 40 seconds. I'm so tired !!!")
                    time.sleep(random.randint(30,40))     
                    p=p+1
            n=n+1
            i=i+1
            key=key+1
            print("------------------------------------------------------------")

        end=time.time()
        delta=end-start
        time_interval_delta=int(delta)
        if time_interval_delta > 21600:
            time.sleep(3600)
            start=time.time()

    print(p)
    print(len(selected))

    pin_count=str(p)

    conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
    cur = conn.cursor()
    cur.execute(f""" delete from general_pin where username='{username}' and board_id='{sel_board_id}' """)
    cur.execute(f""" insert into general_pin(username,board_id,pin_id,completed, record_count) values('{username}','{sel_board_id}','','true','{pin_count}') """)
    cur.close()
    conn.commit()
    conn.close()

    #    print(selected[5])

    json_result=json.dumps(your_dict)
    print(type(your_dict))


def daily_interaction_pinning(username,pin_id, pin_description):
    conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
    cur = conn.cursor()
    cur.execute(
        f""" select count(*) from first_related_pins_pinning where username='{username}'  """)
    i = cur.fetchone()[0]
    print(i)
    if i > 0:
        boards_exist= True
    else:
        boards_exist=False

    if boards_exist:
        cur.execute(
            f""" select created_board_name, created_board_id from first_related_pins_pinning where username='{username}'  """)
        j=cur.fetchall()
        board_name_id_info=[]
        for k in j:
            board_name_id_info.append(k[0])
            board_name_id_info.append(k[1])

        for x in range(len(board_name_id_info)):
            if x % 2 == 0 or x == 0:
                temp_pin_desc=pin_description.split()
                pin_desc_temp_list=[]
                pin_desc_temp_str=""
                for y in temp_pin_desc:
                    pin_desc_temp_list.append(stringcase.pascalcase(y))
                for z in pin_desc_temp_list:
                    pin_desc_temp_str=pin_desc_temp_str+str(z)+" "
                stripped_p_pin_desc=pin_desc_temp_str.strip()
                print(f"pin desc {stripped_p_pin_desc}")
                print(f"board name info {board_name_id_info[x]}")


                if stripped_p_pin_desc in board_name_id_info[x]:
                    board_stripped_id=str(board_name_id_info[x+1]).strip()
                    board_stripped_id=board_stripped_id.strip('\n\r\t')
                    print(f"The board id is ->{board_stripped_id}<- and the pin id is ->{str(pin_id)}<-")
                    pinterest.repin(board_id=board_stripped_id, pin_id=str(pin_id))
                    time.sleep(random.randint(7,10))
    else:
        print(f"Boards don't exist for the username: {username}. So, daily pins can't be pinned at the moment")

    cur.close()
    conn.commit()
    conn.close()



start=time.time()

username='luzchammond'

first_interaction(username='luzchammond',)

boards_res=pinterest.boards_all(username='luzchammond')

your_dict_boards = dict(enumerate(boards_res))

board_info={}


board_name_flag=""
board_id_flag=""
#file1 = open("boards.txt","w")

conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
cur = conn.cursor()
cur.execute(f""" select * from first_related_pins_pinning where username='{username}' """)
query_results_flag = cur.fetchone()
cur.close()
conn.commit()
conn.close()

i=0
if query_results_flag == None:
    for key, value in your_dict_boards.items():
        n=1
        if type(value) is dict:
            for t, c in value.items():
                if(t == "name"):
                    #print("{0}:{1}".format(t, c))
                    conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
                    cur = conn.cursor()
                    cur.execute(f""" select * from first_related_pins_pinning """)
                    query_results = cur.fetchone()
                    #print(query_results)
                    if query_results == None or i == 0:
                        cur.execute(f"""insert into first_related_pins_pinning(username, created_board_name, created_board_id) values('{username}','{c}','')""")
                        #all_records=cur.fetchall()
                        #cur.close()
                        #conn.commit()
                    else:
                        cur.execute(f"""update first_related_pins_pinning set created_board_name='{c}' where username='{username}' and created_board_id='{board_id_flag}' """)
                        #cur.close()
                        #conn.commit()

                    cur = conn.cursor()
                    cur.execute(f"""select * from first_related_pins_pinning""")
                    all_records=cur.fetchall()
                    #print(all_records)
                    cur.close()
                    conn.commit()
                    conn.close()


                    board_name_flag=c
                    #print(board_name_flag)
                    i=i+1
                    if i == 2:
                        i=0;
                    #print(all_records)

                    #file1 = open("boards.txt","a")
                    #file1.write("name: " +c +"\n")
                    #print(results_str)
                if(t == "id"):
                    #print("{0}:{1}".format(t, c))
                    conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
                    cur = conn.cursor()

                    cur.execute(f"""select * from first_related_pins_pinning""")
                    query_results = cur.fetchone()
                    #print(query_results)
                    #print(board_name_flag)

                    if query_results == None or i == 0 :
                        cur.execute(f"""insert into first_related_pins_pinning(username, created_board_name, created_board_id) values('{username}','','{c}')""")
                        #cur.close()
                        #conn.commit()
                        #all_records=cur.fetchall()
                    else:
                        #print(c)
                        cur.execute(f"""update first_related_pins_pinning set created_board_id='{c}' where username='{username}' and created_board_name='{board_name_flag}' """)
                        #cur.close()
                        #conn.commit()

                    cur = conn.cursor()
                    cur.execute(f"""select * from first_related_pins_pinning""")
                    all_records=cur.fetchall()
                    #print(all_records)
                    cur.close()
                    conn.commit()
                    conn.close()

                    #print(board_name_flag)
                    #print(c)
                    board_id_flag=c
                    i=i+1
                    if i == 2:
                        i=0;
                    #print(all_records)

                    #file1 = open("boards.txt","a")
                    #file1.write("id: " +c +"\n")
                n=n+1
#file1.close()

#print('\n')
#file2 = open("boards.txt","r")
#boards_info=file2.readlines()
#print(boards_info)
#file2.close()

conn = psycopg2.connect(host="ec2-54-198-213-75.compute-1.amazonaws.com", port = 5432, database="de6khoqqpj6tpb", user="lbhcvcvywzwbvk", password="001668df93b9fc5559940707765fc58bad4ce615dcdb4270e4977e91518fda05")
cur = conn.cursor()
cur.execute(f""" select * from first_related_pins_pinning where username='{username}' """)
boards_list_info=cur.fetchall()
#print(boards_list_info)


boards_dict={}


for i in boards_list_info:
    print(f"Name is ->{i[1]}<- and id is ->{i[2]}<-")
    cur.execute(f""" select count(*) from general_pin where username='{username}' and board_id='{i[2]}' """)
    related_pins_pinning_flag=cur.fetchone()[0]

    #cur.execute(f""" select record_count from general_pin where username='{username}' and board_id='{i[2]}' """)
    #record_count_flag=cur.fetchone()

    print(related_pins_pinning_flag)

    if related_pins_pinning_flag == 0:
        cur.execute(f""" select count(*) from general_pin where username='{username}' and board_id='{i[2]}' """)
        print(related_pins_pinning_flag)
        first_related_pins_pinning(i[1],i[2],username)
        #time.sleep(random.randint(240,340))
    else:
        print(related_pins_pinning_flag)




cur.close()
conn.commit()
conn.close()