from os import path
from os.path import isfile
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import pickle
import os.path
from operator import itemgetter

times=['08:45 AM','09:45 AM','11:00 AM','12:00 PM','01:00 PM','02:00 PM','03:15 PM','04:15 PM']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def fun(course):
    timing=course[1]
    temp=timing.split(" ")
    temp2=temp[0].split(":")
    hr=temp2[0]
    return int(hr)

def sort_the_timetable(tt_list): # function to sort the timetable based on the timings of the class
    tt=[]
    ams=[] #contains all the am courses in the format ('<course-name>','<time>')
    pms=[] #contains all the pm courses in the format ('<course-name>','<time>')
    for course in tt_list:
        timing=course[1]
        temp1=timing.split(" ")
        if temp1[1] == 'AM':
            ams.append(course) #splitting the times based on am/pm
        elif temp1[1] == 'PM':
            pms.append(course)
    #print('ams',ams)
    #print('pms',pms)
    t1=sorted(ams,key=fun)
    t2=sorted(pms,key=fun)
    #print('sorted ams',t1)
    #print('sorted pms',t2)
    # t2 has 12pm courses at the last, so we're gonna fix that below
    final_t2=[]
    if t2[len(t2)-1][1].startswith('12'):
        final_t2.append(t2[len(t2)-1])
        for i in range(len(t2)-1):
            final_t2.append(t2[i])
    final_t2=t2
    #print('super sorted pms',final_t2)
    # append the sorted courses am first and pm last to tt and return it
    for course in t1:
        tt.append(course)
    for course in final_t2:
        tt.append(course)
    return tt

if __name__ == "__main__":
    courses = []
    if os.path.isfile(os.getcwd()+'\\timetables\\'+'courses'+'.pkl') is True:
        inp_course = open(os.getcwd()+'\\timetables\\'+'courses'+'.pkl',"rb")
        courses = pickle.load(inp_course)
        inp_course.close()

    for i in days:
        dir = os.getcwd()+'\\timetables\\'+i+'.pkl'
        if os.path.isfile(dir) is False:
            print('Enter the timetable for '+i)
            print('If there are no courses for the day, type nill as course code')
            temp = []
            flag = 'y'
            while(flag == 'y'):
                cc = None
                time = None
                try:
                    cc = prompt('Enter the course code: ',completer=WordCompleter(courses))
                    if cc == 'nill':
                        temp = []
                        break
                    if cc not in courses:
                        courses.append(cc)
                    time = prompt('Enter the time: ',completer=WordCompleter(times))
                except:
                    print('Error occured')
                temp.append((cc,time))
                flag = input('Do you want to add another course? (y/n)')
            ############################################################################################################
            #                ADD A CODE HERE THAT FORMATS THE LIST TEMP, IN ORDER OF THE CLASSES,                      #
            #     THE LIST WILL HAVE TUPLES IN IT IN THE DESIGN OF [('cse308', '08.45 am'), ('cse301', '11.00 am')]    #
            #                       COMPARE THE TIMES OF EACH TUPLE[1] AND SORT THEM                                   #
            #       NOTE THE AM AND PM, SO SORT THEM SEPARATELY, MAINTAINGING THEIR OWN ORDER OF FIRST AM THEN PM      #
            #              ALSO NOTE THIS FUNCTION HAS TO BE IN THE FOR LOOP - OUTSIDE THE WHILE LOOP                  #
            ############################################################################################################
            final_tt = sort_the_timetable(temp)

            #attempting to save
            print('Saving',i,'\b'+'s timetable')
            try:
                file_object = open(dir,'wb')
                pickle.dump(final_tt,file_object)
                file_object.close()
                print('Successfully saved '+i)
            except:
                print('Failed to save')
    
    dirc = os.getcwd()+'\\timetables\\'+'courses'+'.pkl'
    if courses is not []:    
        file_object = open(dirc,'wb')
        pickle.dump(courses,file_object)
        file_object.close()

