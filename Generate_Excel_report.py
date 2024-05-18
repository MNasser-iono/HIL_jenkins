from openpyxl import *  # Workbook



def Write_atsheet(file_name,cell_name,contant):
    
    workbook = load_workbook(file_name +".xlsx")
    sheet = workbook.active

    sheet[cell_name] = contant
    workbook.save(file_name +".xlsx")


x = 1
y = 1

# Write_atsheet("test_file","C"+str(x+y),100)
# test_file = "test_file"

# SRVD_recieve_CMD_correct = 0
# SRVD_recieve_CMD_error = 0

# SRVD_recieve_query_correct = 0
# SRVD_recieve_query_error = 0

# SRVD_recieve_APP_error = 0
# SRVD_recieve_APP_correct = 0
# SRVD_Send_APP_correct = 0

# send_app_ctr = 0
# recieved_Hall_ctr = 0
# num_send_app = 1
# num_run_send_CMD_test = 10
# num_run_send_query_test = 10

# def Update_Excel_Sheet(  QueryORCommand , test_num):
#     command_start_Row   = 5
#     Query_start_Row     = 7
    
#     if(QueryORCommand == "Query"):
        
#         Write_atsheet(test_file,"C"+str( Query_start_Row + test_num) ,num_run_send_query_test)
#         Write_atsheet(test_file,"D"+str( Query_start_Row + test_num ),SRVD_recieve_query_correct)
#         Write_atsheet(test_file,"E"+str( Query_start_Row + test_num ),SRVD_recieve_query_error)
#         Write_atsheet(test_file,"F"+str( Query_start_Row + test_num ),SRVD_recieve_APP_correct)
#         Write_atsheet(test_file,"G"+str( Query_start_Row + test_num ),SRVD_recieve_APP_error)

#     if( QueryORCommand == "Command"):
#         Write_atsheet(test_file,"C" + str( command_start_Row + test_num) ,num_run_send_CMD_test)
#         Write_atsheet(test_file,"D" + str( command_start_Row + test_num) ,SRVD_recieve_CMD_correct)
#         Write_atsheet(test_file,"E" + str( command_start_Row + test_num),SRVD_recieve_CMD_error)

# Update_Excel_Sheet("Command",6)

def func_te(cmdORQuery):

    if cmdORQuery == "cmd":
        print("command --------->")

    if cmdORQuery == "Query":
        print("Query --------->")
    

