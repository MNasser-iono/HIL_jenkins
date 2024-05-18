import serial
import time
 # Configure the serial port
port_UART= serial.Serial('COM3', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
port_CAN = serial.Serial('COM6', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)

#IDs
#define    JET_RS_SRVD_ID_TX       1
#define    JET_RS_WIND_ID_TX       2
#define    JET_RS_GYRO_ID_TX       3
#define    JET_RS_LASER_ID_TX      4

SRVD_APP_ID         = 0x01
WIND_APP_ID         = 0x02
JET_RS_GYRO_ID_TX   = 0x03
JET_RS_LASER_ID_TX  = 0x04

JET_RS_SRVD_RX      = 20
SRVD_HALL_AZIMUTH_ID        = 0x608
SRVD_HALL_ELEVATION_ID      = 0x609

#IDs
# id1 = SRVD_HALL_ID
# id2 = SRVD_APP_ID  # assigen ID 
# id3 = Wind_APP_ID  # assigen ID
# id4 = JET_RS_GYRO_ID_TX
# id5 = JET_RS_LASER_ID_TX

SRVD_HALL_AZIMUTH_Buffer = []
SRVD_HALL_ELEVATION_Buffer = []
WIND_APP_Buffer  = [] # 
SRVD_APP_Buffer  = [] #
GYRO_APP_Buffer  = []
LASER_APP_Buffer = []
SRVD_APP_Buffer  = []

#CAN Dictionaries:
CAN_DIC= {SRVD_HALL_AZIMUTH_ID:SRVD_HALL_AZIMUTH_Buffer,SRVD_HALL_ELEVATION_ID:SRVD_HALL_ELEVATION_Buffer,WIND_APP_ID:WIND_APP_Buffer,SRVD_APP_ID:SRVD_APP_Buffer,JET_RS_GYRO_ID_TX:GYRO_APP_Buffer,JET_RS_LASER_ID_TX:LASER_APP_Buffer,JET_RS_SRVD_RX:SRVD_APP_Buffer}



def Send_UART_Data(Data_arr):
    # Convert the array to bytes
    data_bytes = bytes(Data_arr)

    # Send the array over the serial connection
    ret_E = port_UART.write(data_bytes)
    
    if ret_E == 9:
        print("wind send frame = ",data_bytes)
        return True
    else:
        return False
    
def Send_CAN_frame(size , Data_arr):
    # Convert the array to bytes
    data_bytes = bytes(Data_arr)

    # Send the array over the serial connection
    ret = port_CAN.write(data_bytes)

    if (ret == size ):
        return True
    else:
        return False

def Recive_UART_data(Header , size):
    # Wait for data to be available
    while port_UART.in_waiting == size:
        pass
    # Wait for the start byte (0)
    start_byte = port_UART.read()
    start_byte = int.from_bytes(start_byte, byteorder='big')
    if start_byte == Header:
        # Read the remaining  bytes
        ret_data = [start_byte] + list(port_UART.read(size-1))
        # Print the received data
        print("Received UART data:", ret_data)
        return (ret_data)
    else:
        return(False)


def Check_recived_data(data_list,excepted_list):    
    if data_list == excepted_list:
        return True
    else:
        return False
    

def Receive_SRVD_viaCAN(size):
    # Wait for data to be available
    if port_CAN.in_waiting >= size:
        # Read the received data
        received_bytes = port_CAN.read(size)

        # Convert the bytes to a list
        ret_data = list(received_bytes)
        print("Received CAN data ---->>>>>:",ret_data)
        print("in hex = ")
        for i in range(0,size):
            print(hex(ret_data[i]) )
        # print("type ----> should be list ",type(ret_data))
        # print("type ----> should be int ",type(ret_data[0]))
        if ret_data != None:
            return (ret_data)        
        else:
            return(False)
    else:
        return(False)

def recieve_response_srvd(message_ID_high ,message_ID_low):
    ret_frame = Read_Serial_Port(port_CAN,10)
    if(ret_frame[0] == message_ID_high and ret_frame[1] == message_ID_low):
        
        return ret_frame
    else:
        return False

############################## Read Serial ###################################### 
def Read_Serial_Port(serial_type,Data_Len):
    print(">>>>>>>>>>>>>>>>> Before len Buffer = ",port_CAN.in_waiting)
    Serial_Value = serial_type.read(Data_Len)
    Serial_Value_len = len(Serial_Value)
    while Serial_Value_len < 0:
        Serial_Value = serial_type.read(Data_Len)
        Serial_Value_len = len(Serial_Value)
        print(">>>>> stack >> wait complete Frame ")
    
    print(">>>>>>>>>>>>>>>>> After len Buffer = ",port_CAN.in_waiting)
    return Serial_Value         
    # return Serial_Value

def Recive_CAN_frame(message_ID,size):
    # ret_message_id = 0
    #check if there data buffered 
    if len(CAN_DIC[message_ID] ) > 0 :
        print("Received CAN data ---->>>>>:",ret_data)
        return (CAN_DIC[message_ID].pop(0))

    else:
        # Wait for data to be available
        # print("port can in wating = ",port_CAN.in_waiting )
        if port_CAN.in_waiting >= size:
            # print("Entered if cond port can in wating = ",port_CAN.in_waiting )
            # Read the received data
            received_bytes = port_CAN.read(size)
            # Convert the bytes to a list
            ret_data = list(received_bytes)
            # ret_message_id = ret_data[0]<<8 | ret_data[1]

            # if ret_message_id in CAN_DIC:
                # Read the remaining  bytes
                # ret_data = [ret_data[0]] +[ret_data[1]]+ list(port_CAN.read(size-2))
            print("Received CAN data ---->>>>>:",ret_data)
            # print("in hex = ")
            # for i in range(0,size):
            #     print(hex(ret_data[i]) )
            
                #parssing data
            ret_message_id = ret_data[0]<<8 | ret_data[1]
                
                # CAN_DIC[ret_message_id ] = ret_data 
                
            if(ret_message_id == message_ID):
                return (ret_data)
            else:
                if ret_message_id in CAN_DIC:
                    CAN_DIC[ret_message_id ].append(ret_data)
                else:
                    print("stack in can recieve , ID out of range or Data shifted ")
                    while True:
                        pass
                    # port_CAN.flushOutput()
                    # port_CAN.flushInput()
                return (False)        
        
        else:
            return (False)


def Recive_CAN_data(ID):
    SIZE = 10
    recieved_ID = 0x00
    start_time = time.time()
    end_time = 0
    time_out = 0

    # print(">>>>>>>>>>>>>>>>> Before len Buffer = ",port_CAN.in_waiting)
    # Wait for data to be available
    while port_CAN.in_waiting == SIZE:
        pass
    
    # print(">>>>>>>>>>>>>>>>> After len Buffer = ",port_CAN.in_waiting)
    while True:
        time_out = end_time - start_time 
        end_time = time.time()
        ret_bytes = port_CAN.read(SIZE)
        # Convert the bytes to a list
        ret_frame = list(ret_bytes)

        recieved_ID = ret_frame[0] <<8 | ret_frame[1]
        if ID == recieved_ID:
            # ret_bytes = port_CAN.read(SIZE - 2)
            # Convert the bytes to a list
            # ret_frame[2:] = list(ret_bytes)
            print(" >>>>> ret CAN frame With your ID ({}) is = {}".format(ID,ret_frame) ) 
            break
        elif recieved_ID not in CAN_DIC:
            print("stack in can recieve , ID out of range or Data shifted ")
            print(">>>> ---------------- Error recieved Frame = ",ret_frame," ------------------------<<<<<<")
            clear_Buffers()
            time.sleep(1)
            ret_frame = False
            break           
            # while True:
                # pass
        else:
            # ret_bytes = port_CAN.read(SIZE - 2)
            # Convert the bytes to a list
            # ret_frame[2:] =  list(ret_bytes)
            print(" ret CAN frame With other ID({}) is {}= ".format(ID,ret_frame) )
        if time_out > 3:
            print("_________TIME OUT__***_________")
            return (False)
            break
    return ( ret_frame )




def Receive_data_viaCAN(message_ID,size):
    ret_data = None
    recieved_ID = 0x00
    # Wait for data to be available
    if port_CAN.in_waiting >= size:
        
        # Read the received data
        received_bytes = port_CAN.read(size)

        # Convert the bytes to a list
        ret_data = list(received_bytes)
        print("Received CAN data ---->>>>>:",ret_data)
        # print("in hex = ")
        # for i in range(0,8):
        #     print(hex(ret_data[i]) )
        # print("type ----> should be list ",type(ret_data))
        # print("type ----> should be int ",type(ret_data[0]))

        # index_high_byte = (index >> 8) & 0xFF
        # index_low_byte  = index & 0xFF

        recieved_ID = ret_data[0] <<8 | ret_data[1]
        print("ID = ",hex(recieved_ID))
    if (ret_data != None) and ( recieved_ID == message_ID ):
        return (ret_data[3:])        
    else:
        return(False)
  
def clear_Buffers():
    # Clear the input buffer
    port_CAN.flushInput()
    port_UART.flushInput()

    # Clear the output buffer
    port_CAN.flushOutput()
    port_UART.flushInput()

# for item in ret_data:
#     print(hex(item))
# return (ret_data)

# # Wait for the start byte 
# start_byte = port_CAN.read()
#     # Read the received data
# received_bytes = port_CAN.read(size-1)
# # Convert the bytes to a list
# ret_data = list(received_bytes)
# print("Received CAN data ---->>>>>:", ret_data)
# return (ret_data)

# print("Received start byte:", start_byte)
# start_byte = int.from_bytes(start_byte, byteorder='big')
# if start_byte == Header:
#     # Read the remaining  bytes
#     ret_data = [start_byte] + list(port_CAN.read(size-1))
#     # Print the received data
#     print("Received CAN data:", ret_data)
#     return (ret_data)
# else:
#     return False

# # Read the received data
# received_bytes = port_CAN.read(size+1)

# # Convert the bytes to a list
# ret_data = list(received_bytes)