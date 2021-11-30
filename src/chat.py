from src.swen344_db_utils import connect
import csv
import os
def buildUserTables():
    """Build users table"""
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
            DROP TABLE IF EXISTS users CASCADE
        """
    create_sql = """
            CREATE TABLE users(
                id SERIAL PRIMARY KEY,username text, contact text,suspended_till TIMESTAMP NULL,suspended text);
        """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

def buildMesageTables():
    """Build messages table"""
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE IF EXISTS messages CASCADE
    """
    create_sql = """
        CREATE TABLE messages(id SERIAL PRIMARY KEY,sender int,receiver int, message text,date TIMESTAMP,channel_id int
        ,FOREIGN KEY(channel_id) REFERENCES channel(channel_id));
    """
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

def bulidCommunityTables():
    """Build community table"""
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
        DROP TABLE IF EXISTS community CASCADE
    """
    create_sql = """
        CREATE TABLE community(id SERIAL PRIMARY KEY,community_name text,FOREIGN KEY(id) REFERENCES community(id) ON DELETE CASCADE);
    """
    # ,user_id int, FOREIGN KEY(user_id) REFERENCES users(id))
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

def buildChannelTables():
    """Build channel table"""
    conn = connect()
    cur = conn.cursor()
    drop_sql = """
            DROP TABLE IF EXISTS channel CASCADE
        """
    create_sql = """CREATE TABLE channel(community_id int,channel_id SERIAL PRIMARY KEY ,channel_name text,type text,creator int,
    users text,FOREIGN KEY(community_id) REFERENCES community(id) ON DELETE CASCADE)"""

    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

def buildRoleTable():
    """create role table"""
    conn = connect()
    cur = conn.cursor()
    drop_sql = """DROP TABLE IF EXISTS role CASCADE"""
    create_sql = """CREATE TABLE role(id SERIAL PRIMARY KEY,user_id int,channel_id int,role text, FOREIGN KEY(user_id) 
    REFERENCES users(id))"""
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

def buildNicknameTable():
    """Create nickname table"""
    conn = connect()
    cur = conn.cursor()
    drop_sql = """DROP TABLE IF EXISTS nickname CASCADE"""
    create_sql = """CREATE TABLE nickname(user_id int PRIMARY KEY,nick_name text,community_id int, FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE);"""
    cur.execute(drop_sql)
    cur.execute(create_sql)
    conn.commit()
    conn.close()

def inser_to_nicknameTable(user_id,nick_name,community_id):
    """insert record to nickname table"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO nickname(user_id,nick_name,community_id)VALUES(%s,%s,%s);""",(user_id,nick_name,community_id))
    conn.commit()
    conn.close()

def insert_to_communityTable(community_id):
    """insert record to community table"""
    conn = connect()
    cur = conn.cursor()

    insert_sql = """INSERT INTO community(community_name)VALUES(%s);"""

    cur.execute(insert_sql, [community_id])
    conn.commit()
    conn.close()


def insert_to_channelTable(id,channel_name,type,creator,users):
    """Create new channel"""
    #if check_if_user_in_community(id, creator):
    conn = connect()
    cur = conn.cursor()
    insert_sql = """INSERT INTO channel(community_id,channel_name,type,creator,users)VALUES
        (%s,%s,%s,%s,%s)"""
    cur.execute(insert_sql,(id,channel_name,type,creator,users))
    conn.commit()
    conn.close()

def insert_to_userTable(name,contact,suspended_till,suspended):
    """Insert record to user table"""
    conn = connect()
    cur = conn.cursor()

    insert_sql = """
    INSERT  INTO users(username,contact,suspended_till,suspended)
    VALUES(%s,%s,%s,%s);
    """
    cur.execute(insert_sql,(name,contact,suspended_till,suspended))
    conn.commit()
    conn.close()
def insert_to_messageTable(sender,receiver,message,date,channel_id):
    """Insert record to messages table"""
    conn = connect()
    cur = conn.cursor()
    if check_if_user_exist(sender) and check_if_user_exist(receiver):
        result = check_if_suspended(sender)
        if not result == []:
            if result[0][1]=='True':
                print("User are suspended till %s."%result[0][0])

            insert_sql = """
                INSERT  INTO messages(sender,receiver,message,date,channel_id)
                VALUES(%s,%s,%s,%s,%s);
                """
            cur.execute(insert_sql,(sender, receiver, message,date,channel_id))
            conn.commit()

    conn.close()

def insert_to_messageTable_by_name(sender,receiver,message,date,channel_id):
    """Insert record to message table by name"""
    sender_id = get_user_id_by_name(sender)[0][0]
    receiver_id = get_user_id_by_name(receiver)[0][0]
    insert_to_messageTable(sender_id,receiver_id,message,date,channel_id)

def insert_to_roleTable(user_id,channel_id,role):
    """Insert record to role table"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""INSERT INTO role(user_id,channel_id,role)VALUES(%s,%s,%s)""",(user_id,channel_id,role))
    conn.commit()
    conn.close()

def get_user_id_by_name(name):
    """Retrieve user id by given name"""
    conn = connect()
    cur = conn.cursor()
    search_id_by_name = """SELECT id FROM users where username = %s"""
    cur.execute(search_id_by_name,([name]))
    result = cur.fetchall()
    conn.close()
    return result

def get_user_contact_by_id(id):
    """Retrieve contact by given id"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT contact from users where id = %s""",([id]))
    result = cur.fetchall()
    conn.close()
    return result

def find_user_by_id(id):
    """Retrieve user name by given id"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT username from users where id = %s;",([id]))
    result = cur.fetchall()
    conn.close()
    return result


def find_total_user():
    """Find number of users in user table"""
    conn = connect()
    cur = conn.cursor()
    get_total_user_sql = 'SELECT *FROM users;'
    cur.execute(get_total_user_sql)
    result = cur.fetchall()
    conn.close()
    return len(result)

def find_total_msg():
    """Find number of messsage in messages table"""
    conn = connect()
    cur = conn.cursor()
    get_total_message = """SELECT *FROM messages;"""
    cur.execute(get_total_message)
    result = cur.fetchall()
    conn.close()
    return result


def find_msg_from_user(id,start_date,end_date):
    """Retrieve message from a user by given id, start_date and end_date"""
    conn = connect()
    cur = conn.cursor()
    get_content_sql = """SELECT message from messages where date between %s and %s
            and sender = %s;"""
    cur.execute(get_content_sql,(start_date,end_date,id))
    result = cur.fetchall()
    conn.close()
    return result

def check_if_suspended(id):
    """Check if user is suspended by given id"""
    conn = connect()
    cur = conn.cursor()
    cur.execute('SELECT suspended_till,suspended FROM users where id = %s',([id]))
    result = cur.fetchall()
    conn.close()

    return result
def get_msg_by_date(id,date):
    """Retrieve msg from a user by given id and date"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT message from messages where sender = %s and date =%s;""",(id,date))
    result = cur.fetchall()
    conn.close()
    return result

def get_msg_between_user_with_keyword(sender,receiver,keyword):
    """Retrieve all msgs contain specific keyword between two users by given id and keyword"""
    conn = connect()
    cur = conn.cursor()
    like_keyword = "%"+keyword+"%"
    cur.execute("SELECT *FROM messages where sender = %s and receiver = %s and message like %s or sender = %s and receiver = %s and message like %s;",(sender,receiver,like_keyword,receiver,sender,like_keyword))
    result = cur.fetchall()
    conn.close()
    return result

def clear_suspension(id):
    """Change the state of user by given id"""
    result = check_if_suspended(id)
    if result[0][1]=="True":
        conn = connect()
        cur = conn.cursor()
        cur.execute("""UPDATE users set suspended_till = %s,suspended = 'False' where id = %s""",(None,id))
        conn.commit()
        conn.close()
    else:
        print("User's already suspension free.")

def suspend(suspend_id,moderator_id,date,channel_id):
    """Suspend a user(moderator) by given id and suspended_till date，"""

    role = get_role_by_id(moderator_id,channel_id)
    if role[0][0]=="moderator":
        result = check_if_suspended(suspend_id)
        if result[0][1]=="False":

            conn = connect()
            cur = conn.cursor()
            cur.execute("""UPDATE users set suspended_till = %s,suspended = 'True' where id = %s;""",(date,suspend_id))
            conn.commit()
            conn.close()
        else:
            print("User's already been suspended.")
    else:
        print("Regular user is not authorized to suspend user")

def delete_user(id):
    """Delete a user from a users tabel by given id."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""DELETE from users where id = %s;""",([id]))
    conn.commit()
    conn.close()

def update_user_contact(id,contact):
    """Update user contact by given id and new contact info"""
    conn = connect()
    cur= conn.cursor()
    cur.execute("""UPDATE users set contact = %s where id = %s""",(contact,id))
    conn.commit()
    conn.close()

def get_role_by_id(user_id,channel_id):
    """check user role by given id and channel"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT role from role where user_id = %s and channel_id = %s;""",(user_id,channel_id))
    result = cur.fetchall()
    conn.close()
    return result;

def delete_messages_from_channel(channel_id,user_id,message_id):
    """Delete message by given channel_id,user_id and message_id"""
    role = get_role_by_id(user_id,channel_id)
    if role[0][0]=="moderator":

        delete_message(message_id)
    else:

        print("No authorized to delete messages.")



def delete_message(message_id):
    """Delete message by given message id"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""DELETE FROM messages where id = %s ;""",([message_id]))
    conn.commit()
    conn.close()

def check_if_user_is_allow_to_read_private_msg(community_id,channel_id,user_id):
    """check if user allow to read private message"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT users FROM channel where community_id = %s and channel_id =%s;""",(community_id,channel_id))
    result = cur.fetchall()
    conn.close()
    if not result == []:
        if str(user_id) in result[0][0]:
            return True
    return False


def get_messages_by_community_and_channel(community_id,channel_id,user_id):
    """get message by given community_Id,channel_id and user_id"""
    if check_if_user_is_allow_to_read_private_msg(community_id,channel_id,user_id):
        conn = connect()
        cur = conn.cursor()

        cur.execute("""SELECT message FROM messages where channel_id =%s;""",([channel_id]))
        result = cur.fetchall()
        conn.close()

        return result
    else:
        print("Not allow to read message.")
        return None

def allow_user_to_private_chat(community_id,channel_id, user_id):
    """Allow user to private chat"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT users FROM channel where community_id =%s and channel_id =%s;""",(community_id,channel_id))
    result = cur.fetchall()[0][0]
    allow_list=result
    allow_list= allow_list+","+str(user_id)
    cur.execute("""UPDATE channel SET users = %s where community_id =%s and channel_id =%s;""",(allow_list,community_id,channel_id))
    conn.commit()
    conn.close()
def check_if_user_exist(user_id):
    """Check if user exist"""
    conn = connect()
    cur = conn.cursor()
    search_sql = """SELECT id FROM users where id = %s;"""
    cur.execute(search_sql,([user_id]))
    result = cur.fetchall()
    if result == None:
        return False
    else:
        return True

def check_if_community_exist(community_id):
    """Check if community exist"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT id FROM community where id =%s;""",
                ([community_id]))
    result = cur.fetchall()
    if result==None:
        return False

    return True

def add_user_to_channel(community_id,channel_id,user_id):
    """Insert add user to channel"""
    if check_if_user_exist(user_id):
        conn = connect()
        cur = conn.cursor()
        user_list = ""
        cur.execute("SELECT users from channel where community_id = %s and channel_id = %s;",(community_id,channel_id))

        result = cur.fetchall()[0][0]

        result= str(result)+","+ str(user_id)

        cur.execute("""UPDATE channel set users = %s where community_id = %s and channel_id = %s;""",(result,community_id,channel_id))
        conn.commit()
        conn.close()

def fint_total_channel():
    """Find total number of channel"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT *FROM channel;""")
    result = cur.fetchall()
    conn.close()
    return result

def get_msg_by_date(id,date):
    """Retrieve msg from a user by given id and date"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT message from messages where sender = %s and date =%s;""",(id,date))
    result = cur.fetchall()
    conn.close()
    return result

def get_msg_between_user_with_keyword(sender,receiver,keyword):
    """Retrieve all msgs contain specific keyword between two users by given id and keyword"""
    conn = connect()
    cur = conn.cursor()
    like_keyword = "%"+keyword+"%"
    cur.execute("SELECT *FROM messages where sender = %s and receiver = %s and message like %s or sender = %s and receiver = %s and message like %s;",(sender,receiver,like_keyword,receiver,sender,like_keyword))
    result = cur.fetchall()
    conn.close()
    return result

def clear_suspension(id):
    """Change the state of user by given id"""
    result = check_if_suspended(id)
    if result[0][1]=="True":
        conn = connect()
        cur = conn.cursor()
        cur.execute("""UPDATE users set suspended_till = %s,suspended = 'False' where id = %s""",(None,id))
        conn.commit()
        conn.close()
    else:
        print("User's already suspension free.")



def delete_user(id):
    """Delete a user from a users tabel by given id."""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""DELETE from users where id = %s;""",([id]))
    conn.commit()
    conn.close()

def update_user_contact(id,contact):
    """Update user contact by given id and new contact info"""
    conn = connect()
    cur= conn.cursor()
    cur.execute("""UPDATE users set contact = %s where id = %s""",(contact,id))
    conn.commit()
    conn.close()


def import_csv_data(file_name):
    """Read csv file,parse it and put a data into messages table"""
    csv_file = os.path.join(os.path.dirname(__file__), '../%s'%(file_name))
    with open(csv_file) as csvfile:
        reader  = csv.reader(csvfile,delimiter =',')
        next(reader)
        data = []
        for row in reader:
            data.append(row)
        sender_name = data[0][0]
        receiver_name= data[1][0]

        for i in range(0,len(data)):
            if data[i][0]== sender_name:
                sender_message = data[i][1]
                insert_to_messageTable_by_name(sender_name,receiver_name,sender_message,"1936-07-27 00:00:00")
            elif data[i][0]==receiver_name:
                sender_message=data[i][1]
                insert_to_messageTable_by_name(receiver_name,sender_name,sender_message,"1936-07-27 00:00:00")
            elif data[i][0]=="Both":
                sender_message = data[i][1]
                insert_to_messageTable_by_name(sender_name, receiver_name, sender_message, "1936-07-27 00:00:00")
                insert_to_messageTable_by_name(receiver_name, sender_name, sender_message, "1936-07-27 00:00:00")


def import_csv_data(file_name):
    """Read csv file,parse it and put a data into messages table"""
    if file_name =="whos_on_first.csv":
        csv_file = os.path.join(os.path.dirname(__file__), '../%s'%(file_name))
        with open(csv_file) as csvfile:
            reader  = csv.reader(csvfile,delimiter =',')
            next(reader)
            data = []
            for row in reader:
                data.append(row)

            sender_name = data[0][0]
            receiver_name= data[1][0]

            for i in range(0,len(data)):
                if data[i][0]== sender_name:
                    sender_message = data[i][1]
                    insert_to_messageTable_by_name(sender_name,receiver_name,sender_message,"1936-07-27 00:00:00",3)
                elif data[i][0]==receiver_name:
                    sender_message=data[i][1]
                    insert_to_messageTable_by_name(receiver_name,sender_name,sender_message,"1936-07-27 00:00:00",3)
                elif data[i][0]=="Both":
                    sender_message = data[i][1]
                    insert_to_messageTable_by_name(sender_name, receiver_name, sender_message, "1936-07-27 00:00:00",3)
                    insert_to_messageTable_by_name(receiver_name, sender_name, sender_message, "1936-07-27 00:00:00",3)

    elif file_name=="db3_test_data.csv":

        csv_file = os.path.join(os.path.dirname(__file__), '../%s' % (file_name))
        with open(csv_file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row[0]== "Community":
                    community= row[1]
                    insert_to_communityTable(community)
                elif row[0]=="Channel":
                    insert_to_channelTable(row[1],row[2],row[3],row[4],row[5])
                elif row[0]=="User":
                    if row[3]=='None'and row[4]=="FALSE":
                        insert_to_userTable(row[1],row[2],None,str(row[4]).lower().replace('f',"F"))
                    else:
                        insert_to_userTable(row[1], row[2], row[3], str(row[4]).lower().replace('t', "T"))
                elif row[0]=="Role":
                    insert_to_roleTable(row[1],row[2],row[3])
                elif row[0]=="Massage":
                    insert_to_messageTable(row[1],row[2],row[3],row[4],row[5])

def build_all_table():
    """Build all tables"""
    buildUserTables()
    buildNicknameTable()
    bulidCommunityTables()
    buildChannelTables()
    buildMesageTables()
    buildRoleTable()


def hard_code_data():
    """Prepare data for unit test"""

    buildUserTables()
    buildNicknameTable()
    bulidCommunityTables()
    buildChannelTables()
    buildMesageTables()
    buildRoleTable()

    insert_to_communityTable("SWEN-331")
    insert_to_communityTable("SWEN-440")
    insert_to_communityTable("SWEN-344")

    insert_to_channelTable(1, "General", "public", 1, "1")
    insert_to_channelTable(1, "TAs", "public", 1, "1")
    insert_to_channelTable(1, "Random", "public", 1, "1")
    insert_to_channelTable(2, "General", "public", 1, "1")
    insert_to_channelTable(2, "TAs", "public", 1, "1")
    insert_to_channelTable(2, "Random", "public", 1, "1")
    insert_to_channelTable(3, "General", "public", 2, "2")
    insert_to_channelTable(3, "TAs", "public", 2, "2")
    insert_to_channelTable(3, "Random", "public", 2, "2")


    insert_to_userTable("Abbott", "638-968-0879", None, "False")
    insert_to_userTable("Costello", "718-089-0014",None, "False")
    insert_to_userTable("Moe", "646-092-7654", None, "False")
    insert_to_userTable("Larry", "783-011-3414", None, "False")
    insert_to_userTable("Curly", "918-199-0123", "2060-01-01 00:00:00", "True")
    insert_to_userTable("Michael", "917-199-0123", None, "False")

    inser_to_nicknameTable(1, "nick_name_for_id1", 1)

    insert_to_roleTable(1,1,"regular")
    insert_to_roleTable(1, 2, "regular")
    insert_to_roleTable(1, 3, "regular")
    insert_to_roleTable(1, 4, "regular")
    insert_to_roleTable(1, 5, "regular")
    insert_to_roleTable(1, 6, "regular")
    insert_to_roleTable(1, 7, "regular")
    insert_to_roleTable(1, 8, "regular")
    insert_to_roleTable(1, 9, "regular")

    """Code prevent db0-d3 test cases failed."""
    insert_to_roleTable(6, 9, "moderator")
    add_user_to_channel(3, 9, 6)
    add_user_to_channel(3, 9, 1)

    insert_to_messageTable(1, 2, "Hello,How are you?", "1938-08-23 00:00:00",1)
    insert_to_messageTable(1, 3, "How have you been?", "1941-08-29 00:00:00",2)
    insert_to_messageTable(2, 3, "Good morning!", "1935-08-30 00:00:00",2)
    insert_to_messageTable(3, 4, "Test message", "1936-07-27 00:00:00",3)
    insert_to_messageTable(3, 5, "Test message?", "1937-07-28 00:00:00",3)
    insert_to_messageTable(4, 5, "Test message", "1938-07-26 00:00:00",1)
    insert_to_messageTable(4, 5, "Test message", "1939-07-27 00:00:00",1)
    insert_to_messageTable(4, 5, "Test message?", "1940-07-28 00:00:00",7)

def check_if_user_in_channel(user_id,channel_id):
    """check if user in sepcific channel"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT users FROM channel where channel_id =%s;""",([channel_id]))
    result = cur.fetchall()[0][0]
    if str(user_id) in result:
        return True

    return False

def get_channel_name_by_channel_id(channel_id):
    """get channel name"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT channel_name FROM channel where channel_id = %s""", ([channel_id]))
    result = cur.fetchall()
    return result


def get_messages_from_channel(channel_id):
    """get message from channel by check channel_id"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT message FROM messages where channel_id = %s""",([channel_id]))
    result = cur.fetchall()
    return result

def get_messages_from_community(communit_id):
    """get message from community by check community id"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT message FROM messages inner join channel on channel.channel_id = messages.channel_id where channel.community_id = %s;""",([communit_id]))
    result = cur.fetchall()
    return result


def change_user_name(user_id,new_name):
    """change user name by given new name and user_id"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""UPDATE users SET username = %s where id = %s;""",(new_name,user_id))
    conn.commit()
    conn.close()

def change_nick_name(user_id,nick_name,community_id):
    """change nick name in community"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""UPDATE nickname SET nick_name= %s where user_id = %s and community_id =%s;""", (nick_name,user_id,community_id))
    conn.commit()
    conn.close()

def get_nick_name(user_id,community_id):
    """get nick_name"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT nick_name FROM nickname where user_id = %s and community_id =%s;""",(user_id, community_id))
    result = cur.fetchall()
    conn.close()
    return result


def get_user_name(user_id):
    """Retrieve user name by user_id"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("""SELECT username FROM users where id = %s;""",([user_id]))
    result = cur.fetchall()
    conn.close()
    return result
def delete_all_data():
    """Delete all records from both tables"""
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    cur.execute("DELETE FROM messages")
    conn.close()
