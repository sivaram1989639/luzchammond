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





pinterest = Pinterest(email="AliceASanders@outlook.com",
                      password="Savings$2021",
                      username="aliceasanders3236",
                      cred_root='cred_root')

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



def first_interaction(username):
    conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
    cur = conn.cursor()
    boards_list_info=[]

    file1 = open("boards.txt","r")
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

        #for i in boards_list_info:
        #    bad_chars = ['('', '',)']
        #    test_string = i
        #    test_string = ''.join(i for i in test_string if not i in bad_chars)
        #    boards_list_information[row]=str(test_string)
        #    row=row+1

    cur.close()
    conn.commit()
    conn.close()




    #    file8.close()
    #file9 = open("createdboards.txt","a")
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

        #        print(board_name_pascal_strip)
        #        if "\t" in board_name_pascal_strip:
        #            print("True")
        #print(board_list_wo_dup)


        if noboardsexist:
            print("Starting Inserting The Data")

        else:
            conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
            cur = conn.cursor()
            cur.execute(f"""select created_board_name from first_interaction where username='{username}' and created_board='True'""")
            boards_list_info=cur.fetchall()
            cur.close()
            conn.commit()
            conn.close()

        board_list_wo_dup=boards_list_info
        #print(board_list_wo_dup)

        print("------------------------------------------------------------")

        conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
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
            cur.execute(f"""insert into first_interaction(username, init_boards_name, created_board_name, created_board) values('{username}','{board_name_list}','{board_name_pascal_strip}','True')""")
            #cur.execute(f"""update first_interaction set created_board='{board_name_pascal_strip}', created_board_name='True' where username='{username}'""")
            #boards_list_info = cur.fetchall()
            pinterest.create_board(name=board_name_pascal_strip)
            print(f"Created The Board ->{board_name_pascal_strip}<-")
            print(board_name_pascal_strip)
            print("\n")
            #board_list_wo_dup.append(board_name_pascal_strip.strip)
            time.sleep(random.randint(12,15))
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
    conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
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
                    conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
                    cur = conn.cursor()
                    cur.execute(f""" insert into general_pin(username,board_id,pin_id,completed) values('{username}','{sel_board_id}','{pin_id}','true')  """)
                    cur.close()
                    conn.commit()
                    conn.close()

    conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
    cur = conn.cursor()
    cur.execute(f""" select * from general_pin where username='{username}' and board_id='{board_id}'  """)
    pin_records=cur.fetchall()
    selected=[]
    for i in pin_records:
        selected.append(i[2])

    i=1
    p=0
    range=random.randint(40,50)
    n=1
    key=0
    #    pos_a = board_id.find("\n")
    #    sel_board_id_ws=board_id[0:pos_a]
    #    sel_board_id=sel_board_id_ws.strip()




    while i <= len(selected) and p <= range:
        if (i < 5):
            #            print(f" The Selected pin: ->{selected[i]}<- is gonna be pinned")
            print("------------------------------------------------------------")
            #selected[i]=selected[i].strip('\n\r\t')
            #sel_pin_id=selected[i].strip()
            print(f" The Selected Board: ->{board_name}<- Board Id: ->{sel_board_id}<- is where the pin ->{selected[i]}<- is gonna be pinned")
            #            print(type(board_id))
            #            print(type(selected[i]))
            #            sel_board_id=board_id
            #            sel_pin_id=selected[i]
            #            board_id_sel= "\'"+sel_board_id+"\'"
            #            board_pin_sel="\'"+sel_pin_id+"\'"
            #            print(board_id_sel)
            #            print(board_pin_sel)

            #            pinterest.repin(board_id='1106619008376934285',pin_id='63613413476341119')


            #pos_b = selected[i].find("\n")
            #sel_pin_id=selected[i][0:pos_b]

            #            if "\n" in sel_board_id or "\n" in sel_pin_id:
            #                print("Error")
            #            else:
            #                print("Success")

            #            if "\t" in sel_board_id or "\t" in sel_pin_id:
            #                print("Error")
            #            else:
            #                print("Success")

            pinterest.repin(board_id=sel_board_id,pin_id=selected[i])
            time.sleep(random.randint(20,25))
            print(f"The board id is {sel_board_id}, the pin id is {selected[i]}")
            print(f" The Selected pin: ->{selected[i]}<- has been successfully pinned")
            p=p+1
            i=i+1
            print("------------------------------------------------------------")
        else:
            if key >= len(board_id):
                key=0
            index_pin=i + int(board_id[key])+n

            sel_pin_id_ab=selected[index_pin].strip('\n\r\t')
            sel_pin_id_ab=sel_pin_id_ab.strip()
            print("------------------------------------------------------------")
            #            print(f" The Selected pin: ->{sel_pin_id_ab}<- is gonna be pinned")
            print(f" The Selected Board: ->{board_name}<- Board Id: ->{sel_board_id}<- is where the pin ->{sel_pin_id_ab}<- is gonna be pinned")

            #            print(sel_pin_id_ab)
            #            print(board_id+":"+sel_pin_id_ab)
            #            print(type(str(board_id)))
            #            print(type(str(sel_pin_id_ab)))
            pinterest.repin(board_id=sel_board_id,pin_id=sel_pin_id_ab)
            time.sleep(random.randint(20,25))
            print(f"The board id is {sel_board_id}, the pin id is {sel_pin_id_ab}")
            print(f" The Selected pin: ->{sel_pin_id_ab}<- has been successfully pinned")
            n=n+1
            p=p+1
            i=i+1
            key=key+1
            print("------------------------------------------------------------")

    print(p)
    print(len(selected))

    pin_count=str(p)

    conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
    cur = conn.cursor()
    cur.execute(f""" delete from general_pin where username='{username}' and board_id='{sel_board_id}' """)
    cur.execute(f""" insert into general_pin(username,board_id,pin_id,completed, record_count) values('{username}','{sel_board_id}','{pin_id}','true','{pin_count}') """)
    cur.close()
    conn.commit()
    conn.close()

    #    print(selected[5])

    json_result=json.dumps(your_dict)
    print(type(your_dict))




#def selected_pinning():



#results_board= create_board(name="Make Money Online SAHM Jobs")
#print(results_board)

#login("Emma.LiamCreative@outlook.com","Savings$2021","emmaliamcreative")

first_interaction(username='aliceasanders3236',)

boards_res=pinterest.boards_all(username='aliceasanders3236')
print(boards_res)
your_dict_boards = dict(enumerate(boards_res))
print(type(your_dict_boards))

#for key, value in your_dict_boards.items():
#    if type(value) is dict:
#        for t, c in value.items():
#            if(t == "owner"):
#                if type(c) is dict:
#                    for x, y in c.items():
#                        if(x == "full_name"):
#                            print("{1}".format(x, y))
#            if(t == "id"):
#                print("{0}:{1}".format(t, c))



username='aliceasanders3236'

board_info={}


board_name_flag=""
board_id_flag=""
#file1 = open("boards.txt","w")

conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
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
                    print("{0}:{1}".format(t, c))
                    conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
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
                    print(all_records)
                    cur.close()
                    conn.commit()
                    conn.close()


                    board_name_flag=c
                    print(board_name_flag)
                    i=i+1
                    if i == 2:
                        i=0;
                    #print(all_records)

                    #file1 = open("boards.txt","a")
                    #file1.write("name: " +c +"\n")
                    #print(results_str)
                if(t == "id"):
                    print("{0}:{1}".format(t, c))
                    conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
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
                    print(all_records)
                    cur.close()
                    conn.commit()
                    conn.close()

                    #print(board_name_flag)
                    print(c)
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

conn = psycopg2.connect(host="ec2-54-197-100-79.compute-1.amazonaws.com", port = 5432, database="d6svc3okiumk6p", user="ucycrefqyetxfv", password="61c0973167310cb897d5705fb3c20e5885b7c0d7188e096e1308fbb0fda80bc8")
cur = conn.cursor()
cur.execute(f""" select * from first_related_pins_pinning where username='{username}' """)
boards_list_info=cur.fetchall()
print(boards_list_info)


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
    else:
        print(related_pins_pinning_flag)




cur.close()
conn.commit()
conn.close()

#x=0
#while x < (len(boards_info)-1):
#    id="id"
#    if id in boards_info[x]:
#        swap=boards_info[x]
#        boards_info[x]=boards_info[x+1]
#        boards_info[x+1]=swap

#    boards_dict[between(boards_info[x],"name: ","\n")]=between(boards_info[x+1],"id: ","\n")
#    x=x+2

#empty_keys = [k for k,v in boards_dict.items() if not v]
#for k in empty_keys:
#    del boards_dict[k]

#print(boards_dict)

#keys=list(boards_dict.keys())
#values=list(boards_dict.values())

#for k,v in boards_dict.items():
#    first_related_pins_pinning(k,v,username)
#    print(k)

#print(keys)
#print(values)

#flag=0
#while flag <= len(boards_dict):
#    first_related_pins_pinning(keys[flag],values[flag])
#    flag=flag+1
#    print(keys[flag]," : ",values[flag])


#for x, y in board_info.items():
#    print("{0}:{1}".format(x, y))

#results=search(10,'pins','food')
#your_dict = dict(enumerate(results))
#print(type(your_dict))

#for key, value in your_dict.items():
#    if type(value) is dict:
#        for t, c in value.items():
#            if(t == "per_pin_analytics"):
#                if type(c) is dict:
#                    for x, y in c.items():
#                        #print("{1}".format(x, y))
#                        pin_id=between(y,"<Pin ",">")
#                        print(pin_id)
#                        for i in range(len(boards_info)):
#                            pinterest.repin(board_id=between(boards_info[i],"id: ","\t"),pin_id=pin_id)



#for i in range(len(boards_info)):
#    pinterest.repin(board_id=between(boards_info[i],"id: ","\n"),pin_id="639300109607275834")
#    time.sleep(random.randint(10,15))



#pinres=pinterest.repin(board_id="1042231607454367936",pin_id="43417583898440390")
#pinres=pinterest.repin(board_id="1042231607454367937",pin_id="43417583898440390")

#print(pinres)
#results_str=json.dumps(results)
#file2 = open("/Users/sivaramk1989/Documents/files_content/MyFile2.txt","w")
#file2.writelines(results_str)
#print(results_str)

#results=search_p('food recipes')
#print(results)
