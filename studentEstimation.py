'''
Created by Joann on Oct 29, 2019.
Student Estimation problem from CS602 fourth assignment:
    estimate the number of students who would be eligible for taking a specific course.

Input:
A list of courses included in two certificate programs of the school (descriptions 
of programs provided in program1.txt and program2.txt)
• Course prerequisites structure (prereqs.txt)
• Class lists, including grades, for students who took these courses in the past as \
well as those who are taking the courses now (2019-20). Each class list comes in a \
separate file, the first line of which includes the course number, preceded with letter \
‘c’, e.g. c1250. Each such file stores records of students who were/are enrolled in \
course number 1250. (those files that contain -1 instead of a grade are current \
semester files, for which grades have not been posted yet.)

'''

def main():
    '''
    This is the main function that process the program that estimate the number \
    of students who would be eligible for taking a specific course. 
    An eligible student:
        - has completed all prerequisites for the course, and
        - has not taken it in any prior semester
    This function will first: ask the user to specify the subfolder in the current \
    working directory, where the files are stored.
    second: ask the user for a course number, outputting the number of eligible \
    students in response. Incorrect course numbers would be ignored and the program \
    would go on. When the user does not specify any course number, pressing enter \
    instead, the program should stop.
    '''
    
    import os.path
    
    #ask the user to specify the subfolder in the current working directory, 
    #where the files are stored.
    #if the folder name doesn't exist, repeat the input question
    name = False
    while not name:
        filename = input('Please enter the name of the subfolder with files: ').strip()
        if not os.path.isdir(filename):
            print('File name', filename, 'doesn\'t exist.')
        else:
            name = True
    
    #get the course number and course name pair for easily retrieval later
    course = courseinfo(filename)
    
    #Controlling the Loop with a Sentinel Value
    enter = False
    while not enter:
        #ask the user for a course number
        coursen = input('Enter course number or press enter to stop: ')
        
        
        if coursen != '':
            stunum = len(estimateClass(coursen, filename))
            #if the course number is valid, outputting the number of eligible students in response. 
            if stunum != 0:
                print('There are ' + str(stunum) + ' students who could take course ' \
                      + coursen + ' ' + course[coursen])
                
            #incorrect course numbers would be ignored and the program would go on
            else:
                print('There are 0 students who could take course ' \
                      + coursen + ' None')
                
        #if the user press enter instead, the program would stop.
        else:
            enter = True
            
            
            
            
def processProgramFile(filepath):
    '''This function read information about programs and store it in \
    a dictionary for easily retrieval. It has a single parameter of \
    type str, providing the path to a program description file. The \
    dictionary has keys equal to the course numbers, and values for
    keys equal to the corresponding course titles. This function at the\
    end returns a tuple, consisting of the program name and the created dictionary.'''
    
    programdic = {}

    with open(filepath, 'r') as programfile:
        #get the program name in the first line
        line1 = programfile.readline().strip()
        
        #store the course number and course name in the output dictionary by slicing 
        #before the space and after the space
        for line in programfile:
            spacepos = line.find(' ')
            programdic[line[:spacepos]] = line[spacepos + 1 :].strip()
    
    #construct the tuple sonsisting of the program name the dictionary  
    programtup = line1, programdic
       
    return programtup


def processPrereqsFile(filepath):
    '''
    This function reads information about the prerequisites structure \
    and stores it in a dictionary, based on the information in the file, \
    for easily retrieval. It has a single parameter of type str, providing \
    the path to a file defining prerequisites. The form 1250: 1001 1100 \
    indicates that 1250 has two prerequisite courses: 1001 and 1100. \
    The dictionary has keys equal to the course number, and values for keys \
    equal to the corresponding prerequisite courses. Only courses that have \
    prerequisites are included in this dictionary.
    '''
    
    
    prereqs = {}
    with open(filepath, 'r') as prereqsfile:
        for line in prereqsfile:
            #store the course number and prerequisites in the output dictionary by slicing 
            #before the space and after the space
            spacepos = line.find(' ')
            prere = line[spacepos + 1:].strip().split()
            prereqs[line[:spacepos - 1]] = prere
            
        return prereqs
  

def processClassFiles(subfolder):
    '''
    This function constructs a dictionary with keys corresponding to course numbers. \
    and the value for each key is equal to the set of students who have taken or are \
    taking the course designated by the key. It must be passed a single parameter, \
    defining the subfolder with the class list files. '''
    
    import os.path
    
    courseStudent = {}
      
    #set the current working directory to the subfolder with the class list files
    filepath = os.path.join(os.getcwd(), subfolder)
    #get the all the files' names inside the class list files
    filelist = os.listdir(filepath)
    #make a copy of the file list to avoid unintended changes
    filelistcopy = filelist.copy()
    
    #remove the program and prerequisite text
    filelistcopy.remove('prereqs.txt')
    filelistcopy.remove('program1.txt')
    filelistcopy.remove('program2.txt')

    for text in filelistcopy:
        with open(os.path.join(filepath,text), 'r') as textfile:
            #store the course number in the first line of each file
            coursenum = textfile.readline().strip()[1:]
            studentname = set()

            #if the course number is already in the dictionary, store the students' 
            #name in the tuple corresponding to the course number key
            if coursenum in courseStudent:
                for line in textfile:
                    spacepos = line.find(' ')
                    #get the value as tuple 
                    stutuple = courseStudent.get(coursenum)
                    #add the students' name into the tuple 
                    stutuple.add(line[:spacepos])
                #renew the corresponding value of the existing key in the dictionary
                courseStudent[coursenum] = stutuple
            
            #if the course number is not in the dictionary, construct a new key using
            #the course number and store the student into the tuple
            else:
                for line in textfile:
                    spacepos = line.find(' ')
                    studentname.add(line[:spacepos])
        
                courseStudent[coursenum] = studentname  
    
    return courseStudent          


def initFromFiles(subfolder):
    '''
    The purpose of this function is to create data structures with the \
    information that is currently available in files by calling the functions \
    identified above. This function has a single parameter, defining the \
    subfolder with the files. The function would return a tuple with the \
    constructed dictionaries for program courses, class lists and prerequisites.
    
    '''
    import os.path
    #get the programs courses and their prerequisite courses
    programpath1 = os.path.join(os.getcwd(), subfolder, 'program1.txt')
    programpath2 = os.path.join(os.getcwd(), subfolder, 'program2.txt')
    prereqspath = os.path.join(os.getcwd(), subfolder, 'prereqs.txt')
    #call the functions above to data structure for the courses' information
    program1file = processProgramFile(programpath1)
    program2file = processProgramFile(programpath2)
    prereqsfile = processPrereqsFile(prereqspath)
    classfile = processClassFiles(subfolder)
    #store the information in a tuple
    fromfile = program1file, program2file, prereqsfile, classfile
    return fromfile


def courseinfo(subfolder):
    '''
    This function construct a dictionary storing the course number as the key,\
    and its corresponding course name as the value, for easily retrieval. It has \
    one parameter defining the subfolder with the files. It return a dictionary.
    '''
    allinfo = initFromFiles(subfolder)
    coursedic = {}
    #construct the key value pairs by looping each of the two elements in
    #the tuple returned by calling the above function
    for p in range(2):
        for k, v in allinfo[p][1].items():
            coursedic[k] = v
    
    return coursedic
   

def estimateClass(coursenum, subfolder):
    '''
    This function returns a list of eligible students for a given class in the \
    next semester. It has two parameters, a course number and the subfolder with the \
    file. If the parameter does not refer to a valid course number, the function \
    would return an empty list. 
    
    '''
    
    students = set()
    eligiblestu = set()
    allinfo = initFromFiles(subfolder)
#     print(allinfo)
    
    classtook = allinfo[3]
    coursedic = courseinfo(subfolder)
    
    #put all the students' name in a set
    for names in classtook.values():
        for s in names:
            students.add(s)
    
    #if the course number is valid, execute to get the students' name
    #who have taken the prerequisite courses but not that course
    if coursenum in coursedic:       
        for s in students:
            
            #when the course has no prerequisite course
            if coursenum not in allinfo[2]:
                #append the students' name in the eligible list if the students has not taken the course
                if s not in classtook[coursenum]:
                    eligiblestu.add(s)
                    
            #when the course has prerequisite course
            else:
                #find the prerequisite course list and loop the course to see whether the student has taken it
                prereqs = allinfo[2][coursenum]
                
                #to make sure the student has taken all the prerequisite course/courses
                if s not in classtook[coursenum]:
                    count = 0
                    for p in prereqs:
                        if s in classtook[p]:
                            count += 1
                    #add the student name into the set if he/she is eligible
                    if count == len(prereqs):    
                        eligiblestu.add(s)
    
        #sort the list of eligible students name
        eligiblelst = sorted(list(eligiblestu))
        
    #if the course number is invalid, return a blank list
    else:
        eligiblelst = []   
        
    return eligiblelst

 

# print(estimateClass('1100', 'files-small'))             
main()
    
