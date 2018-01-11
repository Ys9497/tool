#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import commands
import os
import difflib as dif
import re
#======prepare======
PATTERN = re.compile("COMMAND([1-9]{1,2})")
def chkprint(args, PATTERN):
    """
    引数から{番号:コマンド}と番号のリストを作る関数
    """
    flg = 1
    name_list = []
    dict_list ={}
    target = [k
              for obj in args
              for k,v in globals().items() if id(v) == id(obj)]
    command_list = [j for j in args]
#    for obj in args: #argment の変数値を1個ずつ取り出す
#       print target
    for line in target:
           if flg == 1:
               name_match=re.search(PATTERN,line)
               if name_match:
                   t = name_match.group(1)
                   name_list.append(t)
                   #dict.update({t:command_list[j-1]})
               flg = 0
           else:
               name_match=re.search(PATTERN,line)
               if name_match:
                   t = name_match.group(1)
                   name_list.append(t)
                   #dict.update({t:command_list[j-1]})
                   #j= j + 1
    dict_list = dict(zip(name_list, command_list))
    return dict_list, name_list
#======COMMAND======

COMMAND1 = "~/NXS/bin/nxs.sh status+"
COMMAND2 = "~/NXS/bin/nxs.sh command mccb2bua show rtpproxylist"
COMMAND3 = "~/NXS/bin/nxs.sh command ham switchover"
COMMAND11 = "ls"
COMMAND12 = "ls ~/NXS/tmp/ |grep core"
COMMAND23 = "python test.py"

#======list(0-9)=======
Command_ListA = [COMMAND1, COMMAND2, COMMAND3]
#======list(10-19)
Command_ListB = [COMMAND11,COMMAND12]
#======list(20-29)
Command_ListC = [COMMAND23]
#======File Path=====
FilePath = "/home/nextgen/work/python/logtool/status.txt"


#=========
DICA, NameA_List=chkprint(Command_ListA, PATTERN)
diff_key_list =  [DICA[str(i)] for i in range(1,len(Command_ListA))]
diff_list = ["" for i in range(len(Command_ListA)+1)]
diff_dic = dict(zip(diff_key_list, diff_list))
#========
DICB, NameB_List=chkprint(Command_ListB, PATTERN)
DICC, NameC_List=chkprint(Command_ListC, PATTERN)
DIC_other = {"0":"EXIT", "99":"SIT"}

#yes/no dic
yn_dic={'y':True,'yes':True,'n':False,'no':False}

def PrintCommand(dic, number):
	for i in number:
	   if dic.has_key(i):
	      print "  %s :    %s"%(i,dic[i])

#choose command, return string corresponding to number
def commandChoose(dicA, A_List, dicB, B_List, dicC, C_List, DIC_other, Situation, FilePath, DDIC):
    while True:
       count = 0
       print "number : command"
       print "  0 :   \"exit\""
       PrintCommand(dicA, A_List)
       PrintCommand(dicB, B_List)
       PrintCommand(dicC, C_List)
       print "  99 :   \"enter the situation(Current status:%s)\""%(Situation)
       print "Please enter the number corresponding to the command you want to execute."
       while True:
           try:
               Input_number = raw_input('>>> ')
               if Input_number.isdigit():
                  if Input_number in A_List:
                        Output = commands.getoutput(dicA[Input_number])
                        print Output
                        DDIC = WriteAndDiff(Output, dicA[Input_number], FilePath, Situation, DDIC)
                        print "====================================="
                  elif Input_number in B_List:
                        os.system(dicB[Input_number])
                        print "====================================="
                  elif Input_number in C_List:
                        os.system(dicC[Input_number])
                        print "====================================="
                  elif Input_number in DIC_other:
                        if Input_number == "99":
                            print ("Please enter the situation.")
                            Situation = raw_input('situation:')
                            print "====================================="
                            break
                        else:
                            print "finish!"
                            sys.exit(0)
                  else:
                      print "error:\"%s\" is not registered number."%(Input_number)
               # else:
               #    print "error:\"%s\" is Invalid String."%(Input_number)
           except ValueError:
               print "error:\"%s\" is Invalid String."%(Input_number)
           except IOError:
               print "error:\"%s\" is Incorrect String."%(Input_number)

       # while True:
	   #    try:
       #           Input_number = raw_input('>>> ')
       #           if Input_number.isdigit():
       #               if Input_number in A_List:
  	   # 	                 Output = commands.getoutput(dicA[Input_number])
  		#                  print Output
  		#                  DDIC = WriteAndDiff(Output, dicA[Input_number], FilePath, Situation, DDIC)
  	   #               elif Input_number in B_List:
  		#                  os.system(dicB[Input_number])
  	   #               elif Input_number in C_List:
  	   #                   os.system(dicC[Input_number])
  	   #               elif Input_number in DIC_other:
  		#                  if Input_number == "99":
  		#                      print ("Please enter the situation.")
       #                       Situation = raw_input('situation:')
  		#                   else:
       #                       print "finish!"
       #                       sys.exit(0)
       #               else:
  	   #                   print "error:\"%s\" is not registered number."%(Input_number)
       #           print "====================================="
       #    except ValueError:
       #        print "error:\"%s\" is Invalid String."%(Input_number)
    return input_number

def WriteAndDiff(Output, Command_Name, FilePath, Situation, DDIC):
    with open(FilePath, mode = 'a') as file:
            file.write("=================================================\n")
            file.write("situation: %s\n"%(Situation))
            file.write("command: %s\n"%(Command_Name))
            file.write("date: %s\n"%(commands.getoutput("date")))
            file.write("=================================================\n")
            file.write(Output+"\n")
            file.write("\n")
            if DDIC[Command_Name] != "":#if you ran this command in the past...
                Before_Status = DDIC[Command_Name].splitlines(1)
                After_Status = Output.splitlines(1)
                result = dif.unified_diff(Before_Status, After_Status,fromfile='before', tofile='after')
                Diff_result = ''.join(result)
                if Diff_result != "":
                   print "================diff==================="
                   print Diff_result
                   file.write("================%s:diff===================\n"%(Command_Name))
                   file.write(Diff_result)
                   file.write("\n")
                DDIC[Command_Name] = Output
            else:
                DDIC[Command_Name] = Output
            return DDIC


if __name__ == "__main__":
    Situation = "試験前"
    commandChoose(DICA, NameA_List, DICB, NameB_List, DICC, NameC_List, DIC_other, Situation, FilePath, diff_dic)
    #commandChoose2(DICA, DIC_other, FilePath, yn_dic, diff_dic)
    print "finish!"
    sys.exit(0)
