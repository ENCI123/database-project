import unittest
from src.chat import *
from src.swen344_db_utils import connect
from datetime import datetime
class TestChat(unittest.TestCase):

    def setUp(self) -> None:
        """Prepare test data"""
        hard_code_data()


    def test_target_user_in_the_table(self):
        """Test if Abbott and Costello are users from users table"""
        abbott = find_user_by_id(1)
        costello = find_user_by_id(2)
        self.assertEqual('Abbott',abbott[0][0])
        self.assertEqual('Costello', costello[0][0], "Costello does not exist in the users table")

    def test_num_of_users(self):
        """Test total number of users from users table"""
        total = find_total_user()
        self.assertEqual(6,total,"Error,total number of users is 6 instead of %s"%(total))

    def test_num_of_msg(self):
        """Test total number of msg from the messages table"""
        total = find_total_msg()
        self.assertEqual(8,len(total),"Error,total number of messages is 8 instead of %s"%(total))

    def test_total_msg_from_given_year(self):
        """Test total number of msg from Larry, Curly, and Moe"""
        larry = find_msg_from_user(3,'01-01-1934 00:00:00','12-31-1946 00:00:00')
        curly = find_msg_from_user(4, '01-01-1934 00:00:00', '12-31-1946 00:00:00')
        moe = find_msg_from_user(5, '01-01-1934 00:00:00', '12-31-1946 00:00:00')
        total = len(larry)+len(curly)+len(moe)
        self.assertEqual(5,total, "Error,number of message does not match from larry curly and moe.")

    def test_curly_is_suspended(self):
        """Test if Curly is suspended till 2060-01-01"""
        result = check_if_suspended(5)
        self.assertEqual("2060-01-01 00:00:00",result[0][0].strftime("%Y-%m-%d %H:%M:%S"),"Error, Curly should be suspended until 01-20-2060 00:00:00.")
        self.assertEqual("True", result[0][1], "Error, Curly should be suspended.")

    def test_get_user_id_by_name(self):
        """Test if get_user_by_name is working"""
        id = get_user_id_by_name('Abbott')[0][0]
        self.assertEqual(1,id,"Error,id does not match.")


    def test_for_db2_Bob(self):
        """Test all functions for Bob"""
        insert_to_userTable("Bob", "917-199-0123", None, "False")

        update_user_contact(7, "bob@gmail.com")
        new_contact = get_user_contact_by_id(7)[0][0]
        self.assertEqual(new_contact, "bob@gmail.com", "update contact for user Bob failed.")

        delete_user(7)
        result = find_user_by_id(7)
        self.assertEqual([], result, "Error Bob should be deleted")



        suspend(1,6,"2060-01-01 00:00:00",9)
        result = check_if_suspended(1)
        self.assertEqual("2060-01-01 00:00:00", result[0][0].strftime("%Y-%m-%d %H:%M:%S"),
                         "Error, Abbott should be suspended until 01-20-2060 00:00:00.")
        self.assertEqual("True", result[0][1], "Error, Abbott should be suspended.")

        clear_suspension(1)
        result = check_if_suspended(1)
        self.assertEqual(None, result[0][0],
                         "Error, Abbott should be suspended until 01-20-2060 00:00:00.")
        self.assertEqual("False", result[0][1], "Error, Abbott should not be suspended.")

    def test_for_db2_Curly(self):
        """Test all functions for Curly"""
        #Suspend Curly
        suspend(5,6,"2060-01-01 00:00:00",9)
        #Check if Curly is suspended
        flag = check_if_suspended(5)
        #if suspended
        if flag[0][1]=="True":
            insert_to_messageTable(5, 2, "Hi there.", "2020-09-13 00:00:00",1)
            self.assertEqual("2060-01-01 00:00:00",flag[0][0].strftime("%Y-%m-%d %H:%M:%S"),"Error suspended_till does not match.")

        #clear suspension for Curyly
        clear_suspension(5)
        #check if Curly is suspension free
        flag = check_if_suspended(5)
        #if not suspended
        if flag[0][1]=="False":
            insert_to_messageTable(5, 2, "Hi there.", "2020-09-13 00:00:00",1)
            msg = get_msg_by_date(5, "2020-09-13 00:00:00")
            self.assertEqual(flag[0][1], "False", "Error,Curly should not be suspended")
            self.assertEqual(msg[0][0], "Hi there.", "Error,sent data does not match the record")

    def test_for_db2_Abbott_Costello(self):
        """Test for finding key Naturally"""
        import_csv_data('whos_on_first.csv')
        result = get_msg_between_user_with_keyword(1,2,"Naturally")
        self.assertEqual(11,len(result),"Error,total message should be 11 instead of %s"%(len(result)))



    def test_for_db3(self):
        """Test for db3"""
        #Change user name
        change_user_name(1, "test_change_user_name")
        self.assertEqual("test_change_user_name", get_user_name(1)[0][0], "Failed to change user name.")


        #get message from community
        result = get_messages_from_community(1)
        self.assertEqual(7,len(result),"Error")

        #change nick name
        change_nick_name(1,"new_nick_name",1)
        self.assertEqual("new_nick_name",get_nick_name(1,1)[0][0],"Error")

        #Create new user name Lex and assign rolw to moderator
        insert_to_userTable("Lex", "lex@gmail.com", None, "False")
        insert_to_roleTable(get_user_id_by_name("Lex")[0][0],3,"moderator")

        #Check if create user successfully and assign role correctly
        self.assertEqual(7,get_user_id_by_name("Lex")[0][0],"Error, user id should be 7 instead of %s."%get_user_id_by_name("Lex")[0][0])
        self.assertEqual("moderator",get_role_by_id(get_user_id_by_name("Lex")[0][0],3)[0][0],"Erorr, Lex should be moderator instead of %s."%get_role_by_id(get_user_id_by_name("Lex")[0][0],3)[0][0])

        #let user other than Lex to delete the message
        delete_messages_from_channel(3,1,8)
        #the user should not be able to delete th message
        self.assertEqual(8,len(find_total_msg()),"user id 1 is not able to delete message")
        #let Lex delete one message
        delete_messages_from_channel(3,7,8)
        #Lex deleted message successfully
        self.assertEqual(7, len(find_total_msg()),"user id 7 should be able to delete message")

        #Let Lex create a new channel named Kill_Superman in SWEN-344,community id = 3
        insert_to_channelTable(3,"Kill_Superman","public",get_user_id_by_name("Lex")[0][0],get_user_id_by_name("Lex")[0][0])
        self.assertEqual(10,len(fint_total_channel()),"Failed to add channel")
        self.assertEqual("Kill_Superman",get_channel_name_by_channel_id(10)[0][0],"Error")
        #Let Lex create a identical channel named Kill_Superman in SWEN-440,community id =2
        insert_to_channelTable(2,"Kill_Superman","public",get_user_id_by_name("Lex")[0][0],get_user_id_by_name("Lex")[0][0])
        self.assertEqual(11, len(fint_total_channel()), "Failed to add channel")
        self.assertEqual("Kill_Superman", get_channel_name_by_channel_id(11)[0][0], "Error")

        #Creat a user named i_told_u_1nce"
        insert_to_userTable("i_told_u_1nce","i@gmail.com",None,"False")
        self.assertEqual(8, get_user_id_by_name("i_told_u_1nce")[0][0],
                         "Error, user id should be 8 instead of %s." % get_user_id_by_name("i_told_u_1nce")[0][0])
        #Let i_told_u_1nce create a private channel
        insert_to_channelTable(3,"Argument Clinic","private",get_user_id_by_name("i_told_u_1nce")[0][0],get_user_id_by_name("i_told_u_1nce")[0][0])
        self.assertEqual(12, len(fint_total_channel()), "Failed to add channel")
        self.assertEqual("Argument Clinic", get_channel_name_by_channel_id(12)[0][0], "Error")

        #Create user ReallyItsJohnCleese
        insert_to_userTable("ReallyItsJohnCleese","re@gmail.com",None,"False")
        self.assertEqual(9, get_user_id_by_name("ReallyItsJohnCleese")[0][0],
                         "Error, user id should be 9 instead of %s." % get_user_id_by_name("ReallyItsJohnCleese")[0][0])
        #Add ReallyItsJohnCleese to channel
        add_user_to_channel(3,12,get_user_id_by_name("ReallyItsJohnCleese")[0][0])
        #Check if authorized user is able to read the message
        self.assertEqual(True,check_if_user_is_allow_to_read_private_msg(3,12,get_user_id_by_name("ReallyItsJohnCleese")[0][0]),"Failed to add user to channel")

        #Create user named ICameHereForAnArgument
        insert_to_userTable("ICameHereForAnArgument","ic@gmail.com",None,"False")
        self.assertEqual(10, get_user_id_by_name("ICameHereForAnArgument")[0][0],
                        "Error, user id should be 10 instead of %s." % get_user_id_by_name("ICameHereForAnArgument")[0][0])
        #Let unauthorized user to read the message from channel
        insert_to_messageTable(8,9,"that was never five minutes just now","1938-08-23 00:00:00",12)
        self.assertEqual(8,len(find_total_msg()),"Error total message should be 8 instead of %s"%len(find_total_msg()))

        # Let unauthorized user "ICameHereForAnArgument" to read the message from channel
        msg1 = get_messages_by_community_and_channel(3,12,10)
        self.assertEqual(None,msg1,"Error user should not able to read from private")

        #Allow user "ICameHereForAnArgument" to private chat
        allow_user_to_private_chat(3,12,10)
        msg1 = get_messages_by_community_and_channel(3,12,10)
        self.assertEqual("that was never five minutes just now", msg1[0][0], "Error user should able to read from private")


    def test_for_using_personal_csv(self):
        """Test if each channel has at least 10 messages"""
        build_all_table()

        import_csv_data('db3_test_data.csv')


        self.assertEqual(10,len(get_messages_from_channel(1)),"Error")
        self.assertEqual(11, len(get_messages_from_channel(2)), "Error")
        self.assertEqual(13, len(get_messages_from_channel(3)), "Error")
        self.assertEqual(10, len(get_messages_from_channel(4)), "Error")
        self.assertEqual(10, len(get_messages_from_channel(5)), "Error")
        self.assertEqual(10, len(get_messages_from_channel(6)), "Error")
        self.assertEqual(11, len(get_messages_from_channel(7)), "Error")
        self.assertEqual(10, len(get_messages_from_channel(8)), "Error")
        self.assertEqual(11, len(get_messages_from_channel(9)), "Error")



        """Test if Curly,Moe and Lurry are in SWEN-331 and SWEN-440"""
        self.assertEqual(True,check_if_user_in_channel(3,1),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(3,2),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(3,3),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(3,4),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(3,5),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(3,6),"Error user should be in this channel")

        self.assertEqual(True, check_if_user_in_channel(4,1),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(4,2),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(4,3),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(4,4),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(4,5),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(4,6),"Error user should be in this channel")

        self.assertEqual(True, check_if_user_in_channel(5,1),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(5,2),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(5,3),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(5,4),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(5,5),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(5,6),"Error user should be in this channel")

        """Test if Abbott and Costello are in SWEN-344"""
        self.assertEqual(True, check_if_user_in_channel(1, 7),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(1, 8),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(1, 9),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(2, 7),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(2, 8),"Error user should be in this channel")
        self.assertEqual(True, check_if_user_in_channel(2, 9),"Error user should be in this channel")








