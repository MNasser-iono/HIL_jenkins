from  serial_test_prot import *
import time
from Generate_Excel_report import *


NUM_RUN_TEST = 10
SRVD_file_name = "SRVD_HIL_Report"

CMD_FRAME   = 0x2
# CMD_FRAME   = 0x20
QUERY_FRAME = 0x4

index = 0x2000
index_high_byte = (index >> 8) & 0xFF
index_low_byte  = index & 0xFF
sub_index = 0x01
power_H = 0x02 ##750 = 0x2EE
power_L = 0xEE


Excepected_CMD_Angle_Frame      = [0x06,0x08,0x20,index_low_byte,index_high_byte,sub_index,power_L,power_H,0x00,0x00]
Excepected_QUERY_voltage_Frame  = [0x06,0x08,0x48,0x0D,0x21,0x02,0x00,0x00,0x00,0x00] # for voltage


Send_HALL_Volt_Frame = [0x05,0x88,0x48,0x0D,0x21,0x02,0x90,0x01,0x00,0x00]

JET_SRVD_CMD_SET_ANGLE = 0x03
SET = 0x01
NO_CHANGE = 0x00
# angle = 270
Angle_H = 0x01
Angle_L = 0x0E
Change_Angle_Frame =[0x00,20,0x00,JET_SRVD_CMD_SET_ANGLE,SET,Angle_H,Angle_L,NO_CHANGE,0x00,0x00] 

JET_SRVD_CMD_READ_VOLT = 24
Excepected_APP_Volt_frame = [JET_SRVD_CMD_READ_VOLT,24,0x01,0x90,22,0x00,0x00]

num_test = 0
num_recieved_CMD = 0

SRVD_recieve_CMD_correct = 0
SRVD_recieve_CMD_error = 0

SRVD_recieve_query_correct = 0
SRVD_recieve_query_error = 0

SRVD_recieve_APP_error = 0
SRVD_recieve_APP_correct = 0
SRVD_Send_APP_correct = 0
send_app_ctr = 0
recieved_Hall_ctr = 0


num_send_app = 1
num_run_send_CMD_test = 10
num_run_send_query_test = 10
Time_out_s = 2
###########################################################################################################################################################

def print_test_summary():
    print("\t------------------<<<<  TEST Summary >>>>>\n--------------------------------")
    print("SRVD RX HALL Query Error = ",SRVD_recieve_query_error)
    print("SRVD RX HALL Query correct = ",SRVD_recieve_query_correct)
    print("SRVD_recieve_APP_correct = ",SRVD_recieve_APP_correct)
    print("SRVD_recieve_APP_error = ",SRVD_recieve_APP_error)

    print("SRVD RX HALL command Error = ",SRVD_recieve_CMD_error)
    print("SRVD RX HALL command correct = ",SRVD_recieve_CMD_correct)
    print("Number of send SRVD APP frame ",SRVD_Send_APP_correct)

def Update_Excel_Sheet(  QueryORCommand , test_num):
    command_start_Row   = 3
    Query_start_Row     = 11
    
    if(QueryORCommand == "Query"):
        
        Write_atsheet(SRVD_file_name,"C"+str( Query_start_Row + test_num) ,num_run_send_query_test)
        Write_atsheet(SRVD_file_name,"D"+str( Query_start_Row + test_num ),SRVD_recieve_query_correct)
        Write_atsheet(SRVD_file_name,"E"+str( Query_start_Row + test_num ),SRVD_recieve_query_error)
        Write_atsheet(SRVD_file_name,"F"+str( Query_start_Row + test_num ),SRVD_recieve_APP_correct)
        Write_atsheet(SRVD_file_name,"G"+str( Query_start_Row + test_num ),SRVD_recieve_APP_error)

    if( QueryORCommand == "Command"):
        Write_atsheet(SRVD_file_name,"C"+ str( command_start_Row + test_num) ,num_run_send_CMD_test)
        Write_atsheet(SRVD_file_name,"D"+ str( command_start_Row + test_num) ,SRVD_recieve_CMD_correct)
        Write_atsheet(SRVD_file_name,"E"+ str( command_start_Row + test_num),SRVD_recieve_CMD_error)

def Reset_counters():
    global SRVD_recieve_CMD_correct,SRVD_recieve_CMD_correct,SRVD_recieve_CMD_error,SRVD_recieve_query_correct,SRVD_recieve_query_error,SRVD_recieve_APP_error
    global SRVD_recieve_APP_correct,SRVD_Send_APP_correct,send_app_ctr,recieved_Hall_ctr,num_test

    num_test = 0
    SRVD_recieve_CMD_correct = 0
    SRVD_recieve_CMD_error = 0
    SRVD_recieve_query_correct = 0
    SRVD_recieve_query_error = 0
    SRVD_recieve_APP_error = 0
    SRVD_recieve_APP_correct = 0
    SRVD_Send_APP_correct = 0
    send_app_ctr = 0
    recieved_Hall_ctr = 0

######################################################################<< Command Functions >>#####################################################################################

def SRVD_recieve_cmd_Fun(Excepected_CMD_Frame):
    global SRVD_recieve_CMD_correct,SRVD_recieve_CMD_error,Time_out_s
    start_time = time.time()
    end_time = 0
    time_out = 0

    while True:
        time_out = end_time - start_time
        SRVD_HALL_ID = Excepected_CMD_Frame[0] <<8 | Excepected_CMD_Frame[1] 
        ret_frame = Recive_CAN_data(SRVD_HALL_ID)

        if ret_frame == False:
            return False
            # break
        if ( ( ret_frame[2]>>4) == CMD_FRAME and ret_frame[3] == Excepected_CMD_Frame[3] ):
            #check if recived CMD is correct
            if ret_frame == Excepected_CMD_Frame:
                SRVD_recieve_CMD_correct +=1
                print(">>>>>>>>>>>>> recieved CMD frame success <<<<<<<<<<<<<<<<<")
            else:
                SRVD_recieve_CMD_error +=1
                print(">>>>>>>>>>>>> Wronge Recieved CMD Frame !!!!!!!!!!!!!!!!!!!!  <<<<<<<<<<<<<<<<<")
            return True
            break
        end_time = time.time()

        if time_out > Time_out_s:
            return "Time Out"
            break

def SRVD_Send_APP_Frame(send_APP_frame):
    global SRVD_Send_APP_correct

    LEN = 10
        # #### SEND APP Frame change Angle #####
    ret = Send_CAN_frame(LEN,send_APP_frame)
    if(ret == True):
        print("send APP frame Done")
        SRVD_Send_APP_correct += 1

def SRVD_test_send_CMD(Send_APP_Frame , Excepected_CMD_frame , ACK_CMD_Frame):
    global num_run_send_CMD_test,send_app_ctr,num_test,recieved_Hall_ctr,num_send_app    
    send_ACK_ctr = 0
    while num_test < num_run_send_CMD_test:
        while send_app_ctr < num_send_app:
            SRVD_Send_APP_Frame(Send_APP_Frame)
            send_app_ctr +=1
            time.sleep(0.1)
        while recieved_Hall_ctr < (num_send_app ):
            ret = SRVD_recieve_cmd_Fun(Excepected_CMD_frame)
            if ret != False and ret != "Time Out":
                # num_test +=1
                recieved_Hall_ctr +=1
            if ret == "Time Out":
                print("<<<< ____ TIME OUT ______>>>")
                print("SRVD RX HALL command Error = ",SRVD_recieve_CMD_error)
                print("SRVD RX HALL command correct = ",SRVD_recieve_CMD_correct)
                print("Number of send SRVD APP frame ",SRVD_Send_APP_correct)
                print("recieved_Hall_ctr = ",recieved_Hall_ctr  )
                break
            if ret == False:
                break
        # while send_ACK_ctr < num_send_app:
            if ret == True:
                ret_Err = Send_CAN_frame(10,ACK_CMD_Frame)
        #     send_ACK_ctr +=1
                if(ret_Err == True):
                    print("send ACK HALL Success ")
                    time.sleep(0.2)
        num_test +=1
        send_ACK_ctr = 0
        send_app_ctr = 0
        recieved_Hall_ctr = 0


######################################################################<< Query Functions >>#####################################################################################

def SRVD_recieve_query_Fun(Excepected_QUERY_Frame):
    global SRVD_recieve_query_correct,SRVD_recieve_query_error,Time_out_s
    start_time = time.time()
    end_time = 0
    time_out = 0

    while True:
        time_out = end_time - start_time
        SRVD_HALL_ID = Excepected_QUERY_Frame[0] <<8 | Excepected_QUERY_Frame[1]  
        ret_frame = Recive_CAN_data(SRVD_HALL_ID)

        if ret_frame == False:
            return False
            # break
        if ( (ret_frame[2]>>4) == QUERY_FRAME and ret_frame[3] == Excepected_QUERY_Frame[3]):
            #check if recived Query is correct
            if ret_frame == Excepected_QUERY_Frame:
                SRVD_recieve_query_correct +=1
                print(">>>>>>>>>>>>> recieved Query frame success <<<<<<<<<<<<<<<<<")
            else:
                SRVD_recieve_query_error +=1
                print(">>>>>>>>>>>>> Wronge Recieved Query Frame !!!!!!!!!!!!!!!!!!!!  <<<<<<<<<<<<<<<<<")
            
            break
        end_time = time.time()

        if time_out > Time_out_s:
            return "Time Out"
            break

def SRVD_recieve_APP_frame(Excepected_APP_frame):
    global SRVD_recieve_APP_correct,SRVD_recieve_APP_error,Time_out_s
    start_time = time.time()
    end_time = 0
    time_out = 0

    while True:
        time_out = end_time - start_time 
        ret_frame = Recive_CAN_data(SRVD_APP_ID)

        end_time = time.time()

        if time_out > Time_out_s:
            return "Time Out"
            break
            # break

        if ret_frame == False:
            return False
            # break
        else:
            ret_frame = ret_frame[3:]
            #check if recived App frame is correct
            if ret_frame == Excepected_APP_frame:
                SRVD_recieve_APP_correct +=1
                print(">>>>>>>>>>>>> recieved APP frame success <<<<<<<<<<<<<<<<<")
            else:
                SRVD_recieve_APP_error +=1
                print(">>>>>>>>>>>>> Wronge Recieved APP Frame !!!!!!!!!!!!!!!!!!!!  <<<<<<<<<<<<<<<<<")
            
            return True 
        

def SRVD_test_send_Query(Excepected_QUERY_Frame,Send_HALL_Frame,Excepected_APP_frame):
    global num_run_send_query_test
    num_test = 0
    while num_test < num_run_send_query_test:
        ####    - Recived query from Tiva 
        ret = SRVD_recieve_query_Fun(Excepected_QUERY_Frame)
        if ret != False and ret !="Time Out":
            ####    - Then send frame with voltage = 400
            ret_err = Send_CAN_frame(10,Send_HALL_Frame)
            time.sleep(0.2)
            if ret_err == True:
                print("-------------------------<< Send HALL_Query_Frame Success >>-------------------------")
                ####    - Recived frame from APP with voltage = 400
                ret_app = SRVD_recieve_APP_frame(Excepected_APP_frame)
                # print("_____ reciecve APP frame ---------------------")
                if ret_app != False and ret_app !="Time Out":
                    # num_test +=1
                    pass
                elif ret_app == "Time Out":
                    print("\n\n<<<< ____ TIME OUT ______>>>\n\n")
                    ret = "Time Out" 
                    break

        elif ret == "Time Out":
            print("\n\n<<<< ____ TIME OUT ______>>>\n\n")
            break
        num_test +=1


######################################################<< Command Test Cases For SRVD_AZIMUTH is ENABLE >>####################################################################################

# ------------------------------
#### This Test:- (Test send Command )( jetson send to --> Tiva --> Roboteq )
# ----------------------------
####    - Send APP frame change Angle  To TivaC 
####    - TivaC will recieve APP frame then Send CMD frame to Roboteq at CAN Bus
####    - Recived CMD frame from TivaC and check if CMD frame is correct or not 
####    - Then send ACK Frame To TivaC 

def Test_CMD_case_1():
    global Change_Angle_Frame,Excepected_CMD_Angle_Frame

    index       = 0x2000
    sub_index   = 0x01

    index_high_byte = (index >> 8) & 0xFF
    index_low_byte  = index & 0xFF    
    
    ACK_CMD_Frame = [0x05,0x88,0x60,index_low_byte,index_high_byte,sub_index,0x00,0x00,0x00,0x00]

    SRVD_test_send_CMD(Change_Angle_Frame , Excepected_CMD_Angle_Frame ,ACK_CMD_Frame)
    Update_Excel_Sheet("Command",1)
    print_test_summary()
    time.sleep(2)
    Reset_counters()



def Test_CMD_case_2():
    # Safty Stop Test
    #################### << Change those prameter according index , subindex and ..... >> ###################### 
    index       = 0x202C
    sub_index   = 0x00
    APP_Value   = 0   #
    MOTOR_ID    = 0x08
    n = 3 
    CSS = CMD_FRAME
    
    JET_SRVD_CMD_SAFETY_STOP = 4
    CMD_Value  = 0x02EE  ##750 = 0x2EE

    ############################################################################################################ 
    APP_Value_High = (APP_Value >> 8) & 0xFF 
    APP_Value_Low = APP_Value & 0xFF
    index_high_byte = (index >> 8) & 0xFF
    index_low_byte  = index & 0xFF
    CMD_Value_H = (CMD_Value >> 8) & 0xFF
    CMD_Value_L = CMD_Value & 0xFF
    Byte0 = (n<<2)|(CSS<<4)

    SET = 0x01
    NO_CHANGE = 0x00
    ########################################## <<< Lists >>> ##################################################################

    Safety_stop_Frame =[0x00,20,0x00,JET_SRVD_CMD_SAFETY_STOP,0x00,0x00,0x00,0x00,0x00,0x00] 

    Excepected_CMD_Safety_stop_Frame    = [0x06,MOTOR_ID,Byte0,index_low_byte,index_high_byte,sub_index,0x00,0x00,0x00,0x00]

    ACK_CMD_Frame = [0x05,(0x80 + MOTOR_ID),0x60,index_low_byte,index_high_byte,sub_index,0x00,0x00,0x00,0x00]
    
    SRVD_test_send_CMD(Safety_stop_Frame , Excepected_CMD_Safety_stop_Frame , ACK_CMD_Frame)
    Update_Excel_Sheet("Command",2)
    Reset_counters()


##############################################<< Command Test Cases For SRVD_AZIMUTH and ElEIVTION are ENABLE >>####################################################################################

def Test_CMD_case_3():
    #################### << Change those prameter according index , subindex and ..... >> ###################### 
    index       = 0x2000
    sub_index   = 0x01
    APP_Value   = 270   # angle = 270
    MOTOR_ID    = 0x09

    JET_SRVD_CMD_SET_ANGLE = 0x03
    CMD_Value  = 0x02EE  ##750 = 0x2EE

    ############################################################################################################ 
    APP_Value_High = (APP_Value >> 8) & 0xFF 
    APP_Value_Low = APP_Value & 0xFF
    index_high_byte = (index >> 8) & 0xFF
    index_low_byte  = index & 0xFF

    CMD_Value_0 = CMD_Value & 0xFF
    CMD_Value_1 = (CMD_Value >> 8) & 0xFF
    CMD_Value_2 = (CMD_Value >> 16) & 0xFF
    CMD_Value_3 = (CMD_Value >> 24) & 0xFF
    
    SET = 0x01
    NO_CHANGE = 0x00
    ########################################## <<< Lists >>> ##################################################################
    
    Excepected_CMD_motorCommand_Frame    = [0x06,MOTOR_ID,0x20,index_low_byte,index_high_byte,sub_index,CMD_Value_0,CMD_Value_1,CMD_Value_2,CMD_Value_3]

    Change_Angle_Frame =[0x00,20,0x00,JET_SRVD_CMD_SET_ANGLE,NO_CHANGE,APP_Value_High,APP_Value_Low,SET,APP_Value_High,APP_Value_Low] 

    ACK_CMD_Frame = [0x05,(0x80 + MOTOR_ID),0x60,index_low_byte,index_high_byte,sub_index,0x00,0x00,0x00,0x00]
    #################################################### <<< Functions >>> ########################################################
    SRVD_test_send_CMD(Change_Angle_Frame , Excepected_CMD_motorCommand_Frame , ACK_CMD_Frame)

    Update_Excel_Sheet("Command",3)
    print_test_summary()
    time.sleep(2)
    Reset_counters()

######################################################################<< Query Test Cases >>#####################################################################################

# ------------------------------
#### This Test:- (Tiva send Query To --> Roboteq send response_data to  ---> Tiva --> jetson)
# ------------------------------
####    - TivaC send Query Frame at CAN Bus
####    - Recived Query Frame from TivaC and check if Query frame is correct or not  
####    - Then send frame with voltage = 400
####    - Recived frame from APP with voltage = 400 and  and check if App frame is correct or not 


##########################################################################################################

##### Test Voltage Query #####
def Test_Query_case_1():
    global Excepected_QUERY_voltage_Frame,Send_HALL_Volt_Frame,Excepected_APP_Volt_frame

    SRVD_test_send_Query(Excepected_QUERY_voltage_Frame,Send_HALL_Volt_Frame,Excepected_APP_Volt_frame)
    Update_Excel_Sheet("Query" , 1)

    print_test_summary()
    time.sleep(2)
    Reset_counters()

##### Test HAll_state Query #####
def Test_Query_case_2():
    # 0x2123
    JET_SRVD_CMD_READ_HALL_STATE = 23
    Excepected_QUERY_HALL_STATE_Frame = [0x06,0x08,0x4C,0x23,0x21,0x01,0x00,0x00,0x00,0x00] # for HALL States
    Send_HALL_STATES_Frame = [0x05,0x88,0x4C,0x23,0x21,0x01,0x00,0x00,0x00,0x00]
    Excepected_APP_HALL_frame = [JET_SRVD_CMD_READ_HALL_STATE,24,0x01,22,0,0x00,0x00]

    SRVD_test_send_Query(Excepected_QUERY_HALL_STATE_Frame,Send_HALL_STATES_Frame,Excepected_APP_HALL_frame)
    Update_Excel_Sheet("Query" , 2)
    print_test_summary()
    time.sleep(2)
    Reset_counters()



###########################################################################################################################################################

def Queries_Test_Cases():
    clear_Buffers()
    Test_Query_case_1()
    clear_Buffers()
    Test_Query_case_2()
    clear_Buffers()

def Commands_Test_Cases():
    clear_Buffers()
    Test_CMD_case_1()
    clear_Buffers()
    time.sleep(1)
    Test_CMD_case_2()
    clear_Buffers()
    Test_CMD_case_3()
    clear_Buffers()


def main():
    # Record the start time
    start_time = time.time()
    
    print("___________________________ START Commands_Test_Cases _________________________\n")   
    Commands_Test_Cases()
    
    print("___________________________ START Queries_Test_Cases _________________________\n")
    time.sleep(0.5)
    
    Queries_Test_Cases()

    # Record the end time
    end_time = time.time()
    # Calculate the elapsed time
    elapsed_time = end_time - start_time
    
    # print_test_summary()
    # Print the elapsed time
    print(f"\nElapsed time: {elapsed_time} seconds")
    print("---------------------------- End Test Cases -------------------------")





main()
























