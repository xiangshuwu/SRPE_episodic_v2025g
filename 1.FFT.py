# The code below runs on PsychoPy
# and implements the experiment of De Loof and colleagues (2018, PLoS One)
# with the difference that dutch words are replaced by faces

# written by Cristian Buc Calderon and Esther De Loof, spring 2018
# revized by Esther De Loof for PsychoPy3, spring 2019
# some adaptations for iEEG experiment by Tom Verguts, spring 2021
# changed by zhaoxiaohui for iEEG experiment , spring 2021
# importing modules

from psychopy import visual, event, core, gui
import os,sys, pandas, numpy, random, time
import logging
from datetime import datetime

fMRI = 0 # fRMI (set to 1) or pilot (set to something else)
earlyExit = 0 # provide a short test while programming (if set to 1)
speedy = 0 # provide a speeded version of the experiment for debugging (if set to 1)


# set the directory
my_directory = os.getcwd()
data_dir     = os.path.join(my_directory, "data")
FaceTestDir  = os.path.join(data_dir, "FaceTest")
TrainDir     = os.path.join(data_dir, "train")
FacesDir     = os.path.join(my_directory, "Luminancescaled")
LogDir     = os.path.join(data_dir, "logfile")

[os.mkdir(Dir_loop) for Dir_loop in [data_dir, FaceTestDir, TrainDir,LogDir] if not os.path.isdir(Dir_loop)]

# data file
already_exists = True
while already_exists:
    
    # collect the participant info
    info      = {"Participant number": 99, "Age": 20, "Handedness": [ "right-handed","left-handed",], "Gender": ["female", "male"]}
    myDlg     = gui.DlgFromDict(dictionary = info, title = "Face Swahili iEEG study")

    # make the data file names
    exp_file_name           = FaceTestDir + "/exp_words_participant_"        + str(info["Participant number"]) + ".csv"
    FaceTest_file_name      = FaceTestDir + "/FaceTest_participant_"         + str(info["Participant number"]) + ".csv"
    learn_fMRI_file_name    = FaceTestDir + "/fMRI_data_set_participant_"    + str(info["Participant number"]) + ".csv"
    learn_train_file_name   = TrainDir    + "/Learning_training_participant_"+ str(info["Participant number"]) + ".csv"
    logging_file_name       = LogDir     + "/Log_participant_"          + str(info["Participant number"]) + ".log"

    # check whether the file names already exists
    if not os.path.isfile(exp_file_name) and not os.path.isfile(FaceTest_file_name) and not os.path.isfile(learn_fMRI_file_name) and not os.path.isfile(learn_train_file_name):
        already_exists = False
    # if they already exist, ask for another participant number
    else:
        myDlg2 = gui.Dlg(title = "出错")
        myDlg2.addText("该编号已使用，请换其他编号.")
        myDlg2.show()
    if not myDlg.OK:
        sys.exit()
        


        

logging.basicConfig(filename=logging_file_name, level=logging.INFO, format="%(asctime)s - %(message)s")
datetime.now()
logging.info("Famous face familar: started")
# set the timing of the experiment
if speedy != 1:
    Fixation_time   = 0.5
    Reading_time    = 4
    Anticipation_time   = 3
    feedback_time    = 3
    Encoding_time   = 5
    Money_time      = 2
else:
    Fixation_time   = 0
    Reading_time    = 0
    Anticipation_time    = 0
    feedback_time   = 0
    Encoding_time   = 0
    Money_time      = 0

# adapt the monetary reward for the pilot versus fMRI version of the experiment

money_inc = 0.30

# load in stimuli and set the stimulus parameters for the Swahili options
npractice       = 6
ntrialsone      = 35
ntrialstwo      = 35
all_faces       = npractice + ntrialsone + ntrialstwo
list_words      = pandas.read_csv(FacesDir + "/wordlist.csv", header = None, names = ["s"])
# in the script of Cris there was a randomization here, but I like to keep the stimuli in the training set constant
random.shuffle(list_words.s)
print(list_words.s[0:4])
practice_words  = list_words.s[0:npractice*4]
exp_words       = list_words.s[npractice*4:(npractice+ntrialsone+ntrialstwo)*4].reset_index(drop=True)

# saving the experimental words for the following learning task
exp_words.to_csv(exp_file_name, encoding='utf_8_sig')

# load in stimuli and set the stimulus parameters for the face recognition
names           = pandas.read_csv(FacesDir + "/names.csv", sep = ';', header = None, names = ["Names", "Names1", "Names2", "Names3"]) 
pictures        = pandas.read_csv(FacesDir + "/pictures.csv",         header = None, names = ["numbers"])
feedback_list   = ["错误", "正确", "+ 0 元", "+ " + str(money_inc) + " 元"]
colorword       = (1,1,1)
colorbackground = (-1,-1,-1)
pos1            = (-0.4,-0.4)
pos2            = (-0.4,-0.7)
pos3            = ( 0.4,-0.7)
pos4            = ( 0.4,-0.4)
width_box       = 0.5
height_box      = 0.2
total_money     = 0
my_clock        = core.Clock()
keyList         = ["d", "c", "n", "j", "escape"]
globalClock     = core.Clock()
keyList         = ["d", "c", "n", "j", "escape"]

# initialize the window
win = visual.Window([1920, 1080], color = colorbackground, fullscr = True)

# hide mouse cursor
win.mouseVisible = False

# prepare graphical elements
box_encode      = visual.Rect(      win, lineWidth = 6,                             width = 1.1,        height = 0.7)
box1            = visual.Rect(      win,                    pos = pos1,             width = width_box,  height = height_box)
box2            = visual.Rect(      win,                    pos = pos2,             width = width_box,  height = height_box)
box3            = visual.Rect(      win,                    pos = pos3,             width = width_box,  height = height_box)
box4            = visual.Rect(      win,                    pos = pos4,             width = width_box,  height = height_box)
name1           = visual.TextStim(  win, text = "",         pos = pos1,             color = colorword)
name2           = visual.TextStim(  win, text = "",         pos = pos2,             color = colorword)
name3           = visual.TextStim(  win, text = "",         pos = pos3,             color = colorword)
name4           = visual.TextStim(  win, text = "",         pos = pos4,             color = colorword)
message         = visual.TextStim(  win, text = "",         pos = ( 0   , 0   ),    color = colorword)
Anticipation    = visual.TextStim(  win, text = "…",        pos = ( 0   , 0   ),    color = colorword)
feedback1       = visual.TextStim(  win, text = "",         pos = ( 0   , 0.2 ),    color = colorword)
feedback2       = visual.TextStim(  win, text = "",         pos = ( 0   , 0.1 ),    color = colorword)
money_feedback  = visual.TextStim(  win, text = "",         pos = ( 0   , 0 ),    color = colorword)
fix             = visual.TextStim(  win, text = "+",        pos = ( 0   ,-0.55),    color = colorword)
word_encode     = visual.TextStim(  win, text = "",         pos = ( 0.2 , 0   ),    color = colorword)
picture         = visual.ImageStim( win, size = (1.0,1.2),  pos = ( 0   , 0.4 ),    image = FacesDir + "/" + str(1) + ".jpg")
face_encode     = visual.ImageStim( win, size = (0.5,0.7),  pos = (-0.3 , 0   ),    image = FacesDir + "/" + str(1) + ".jpg")
certainty       = visual.ImageStim( win, size = (1.5,1.5),  pos = ( 0   , 0   ),    image = my_directory + "/instructions/Recognition_certainty.jpg")
instructions    = visual.ImageStim( win, size = (1.5,1.5),  pos = ( 0   , 0   ),    image = my_directory + "/instructions/Welcome.jpg")

# Cris used a random seed here, but I don't see a reason to use it in this version of the experiment
# set random seed
#random.seed(int(info["Participant number"]))

# make a function to display the instructions via jpg's
def display_instructions(file = "instructions.jpg"):
    
    instructions.image = file
    instructions.draw()
    win.flip()
    if speedy != 1:
        event.clearEvents(eventType = "keyboard")
        event.waitKeys(keyList = "space")

# make a function to count down 5 seconds
def countdown():
    
    message.text = "请集中注意力，练习将在5秒后开始..."
    message.draw()
    win.flip()
    if speedy != 1:
        time.sleep(4) # left on purpose one more second :)
    
    for i in range(2):
        message.text = str(2-i)
        message.draw()
        win.flip()
        if speedy != 1:
            time.sleep(1)

# create the trials (ns stands for non shuffled)
df_ns               = pandas.DataFrame()
df_ns["Pictures"]   = pictures.numbers.loc[:]
df_ns["Names"]      = names.Names.loc[:]
df_ns["Names1"]     = names.Names1.loc[:]
df_ns["Names2"]     = names.Names2.loc[:]
df_ns["Names3"]     = names.Names3.loc[:]

# place the famous faces in random order
df = df_ns.iloc[numpy.random.permutation(len(df_ns))]
df.reset_index(drop = True)

# displaying the instructions
display_instructions(file = my_directory + "/instructions/Welcome.jpg")
display_instructions(file = my_directory + "/instructions/FT_1.jpg")

# present the famous faces to check whether the participant knows the faces
for i in range(df.shape[0]):
    
    # getting the names (and shuffling them) and correct response
    list_names = [df.Names.iloc[i], df.Names1.iloc[i], df.Names2.iloc[i], df.Names3.iloc[i]]
    random.shuffle(list_names)
    
    # fixation cross PreStim
    fix.draw()
    win.flip()
    time.sleep(Fixation_time)
    
    # load the response options for the famous face on the screen
    name1.text = list_names[0]
    name2.text = list_names[1]
    name3.text = list_names[2]
    name4.text = list_names[3]
    name1.draw()
    name2.draw()
    name3.draw()
    name4.draw()
    
    # load the famous face on the screen 
    picture.image = FacesDir + "/" + str(int(df.Pictures.iloc[i])) + ".jpg"
    picture.draw()
    win.flip()
    
    # wait for the response
    event.clearEvents(eventType = "keyboard")
    my_clock.reset()
    if speedy != 1:
        keys = event.waitKeys(keyList = keyList)
    else:
        keys = "d"
    
    # register the response for the face name
    df.loc[[i], 'RT']                   = my_clock.getTime()
    df.loc[[i], 'Response']             = keys[0]
    
    # add an escape option
    if keys[0] == "escape":
        break
    
    # translate the response key (d, c, n, j) to an index (0, 1, 2, 3)
    position = keyList.index(keys[0]) 
    
    # checking for the certainty
    certainty.draw()
    win.flip()
    event.clearEvents(eventType = "keyboard")
    my_clock.reset()
    if speedy != 1:
        keys = event.waitKeys(keyList = keyList)
    else:
        keys = "d"
    
    # register the response for the certainty
    df.loc[[i], 'RT_certainty']         = my_clock.getTime()
    df.loc[[i], 'Response_certainty']   = keys[0]
        
    # add an escape option
    if keys[0] == "escape":
        break
    
    # translate the response key (d, c, n, j) to an index (0, 1, 2, 3)
    position_certainty = keyList.index(keys[0])
    
    # check whether the correct name has been chosen
    if (df.Names.iloc[i] == list_names[position]): 
        accuracy = 1
    else:
        accuracy = 0
    
    # check whether the subject is fairly or highly certain of the correct answer
    # only those stimuli are regarded as knowledge (not just a correct guess)
    if (accuracy == 1) & (position_certainty > 1):
        knowledge = 1
    else:
        knowledge = 0
    
    # register the accuracy
    df.loc[[i], 'Accuracy']             = accuracy
    
    # register the knowledge (i.e. if correct and rated highly certain)
    df.loc[[i], 'Knowledge']            = knowledge
    
    # register the metadata
    df.loc[[i], 'Subject']              = info["Participant number"] 
    df.loc[[i], 'Sex']                  = info["Gender"]
    df.loc[[i], 'Age']                  = info["Age"]
    df.loc[[i], 'Handedness']           = info["Handedness"]

    # implement early exit
    if earlyExit == 1 and i > 2:
        break

# saving the data from the face test
df.to_csv(FaceTest_file_name, encoding='utf_8_sig')

# selecting only the famous faces that people accurately identified and are certain of
list_acc = df.loc[df["Knowledge"] == 1]

# make sure we have 76 trials
if list_acc.shape[0] > all_faces:
    
    # taking a random subset of 76 of these famous faces
    trial_set_fMRI  = list_acc.sample(n = all_faces)

else:
    
    # taking a random subset of 76 of these famous faces
    list_no_acc     = df.loc[df["Knowledge"] == 0]
    add_list        = list_no_acc.sample(n = all_faces - len(list_acc))
    frames          = [list_acc, add_list]
    trial_set_fMRI  = pandas.concat(frames)

# save the dataframe for the following script
trial_set_fMRI.to_csv(learn_fMRI_file_name, encoding='utf_8_sig')

# set the continuation value
allow = 1

# allowing the training if the participant recognized suffient faces
# in this version of the experiment the answer was always "allow" 
if allow == 1:
    
    # creating the dataframe for the training session
    df = pandas.DataFrame()
    
    # adding different type of info 
    df["NOptions"]   = [1] * 2  + [2] * 2  + [4] * 2
    df["Correct"]    = [1] * 2  + [0] * 1  + [1] * 1  + [0] * 1  + [1] * 1
    df["SRPE"]       = [float(df.loc[i,["Correct"]]) - float(1/df.loc[i,["NOptions"]]) for i in range(df.shape[0])]
    
    # adding the Swahili words
    df["Face"]       = trial_set_fMRI.Pictures.iloc[0:npractice].reset_index(drop=True)    
    df["Swahili1"]   = practice_words.iloc[npractice*0:npractice*1].reset_index(drop=True)
    df["Swahili2"]   = practice_words.iloc[npractice*1:npractice*2].reset_index(drop=True)
    df["Swahili3"]   = practice_words.iloc[npractice*2:npractice*3].reset_index(drop=True)
    df["Swahili4"]   = practice_words.iloc[npractice*3:npractice*4].reset_index(drop=True)
    
    # place the same Swahili words in random order for the test trials
    df["TestSwahili1"] = ""
    df["TestSwahili2"] = ""
    df["TestSwahili3"] = ""
    df["TestSwahili4"] = ""
    four = [0, 1, 2, 3]
    for i in range(npractice):
        FourWords = df.loc[i,["Swahili1","Swahili2","Swahili3","Swahili4"]]
        random.shuffle(four)
        df.loc[i,"TestSwahili1"] = FourWords[four[0]]
        df.loc[i,"TestSwahili2"] = FourWords[four[1]]
        df.loc[i,"TestSwahili3"] = FourWords[four[2]]
        df.loc[i,"TestSwahili4"] = FourWords[four[3]]
    
    # add the color of the frames around the options
    df["Color1"] = ""
    df["Color2"] = ""
    df["Color3"] = ""
    df["Color4"] = ""
    df.loc[df["NOptions"] == 4, ["Color1","Color2","Color3","Color4"]] = "white"
    oneOptions = ["white","black","black","black"]
    twoOptions = ["white","white","black","black"]
    for i in range(npractice):
        if df.loc[i,"NOptions"] == 1:
            random.shuffle(oneOptions)
            df.loc[i,["Color1","Color2","Color3","Color4"]] = oneOptions
        elif df.loc[i,"NOptions"] == 2:
            random.shuffle(twoOptions)
            df.loc[i,["Color1","Color2","Color3","Color4"]] = twoOptions
    
   
    
    # shuffle the dataframe
    df = df.sample(frac = 1).reset_index(drop = True)
        
    # instructions for the training session
    display_instructions(file = my_directory + "/instructions/TS_1.jpg")
    display_instructions(file = my_directory + "/instructions/TS_2.jpg")
    display_instructions(file = my_directory + "/instructions/TS_3.jpg")
    display_instructions(file = my_directory + "/instructions/TS_4.jpg")
    display_instructions(file = my_directory + "/instructions/TS_5.jpg")
    if fMRI == 1:
        display_instructions(file = my_directory + "/instructions/TS_6_fMRI.jpg")
    else:
        display_instructions(file = my_directory + "/instructions/TS_6.jpg")
    
    # start of the trial loop for the training session
    for j in range(npractice):
        
        # getting a list of the words and color boxes in order to index them later in the loop
        list_words      = [df.Swahili1.iloc[j], df.Swahili2.iloc[j], df.Swahili3.iloc[j], df.Swahili4.iloc[j]]
        list_colorbox   = [df.Color1.iloc[j],   df.Color2.iloc[j],   df.Color3.iloc[j],   df.Color4.iloc[j]]
        
        # getting the position of the white and black boxes
        position_bbox   = [i            for i, x in enumerate(list_colorbox) if x == "black"]
        position_wbox   = [keyList[i]   for i, x in enumerate(list_colorbox) if x == "white"]
        
        # add an escape option
        position_wbox.append("escape")
        
        # fixation cross PreStim
        fix.draw()
        win.flip()
        time.sleep(Fixation_time)
        
        # load the words on the screen
        name1.text = str(list_words[0]).capitalize()
        name2.text = str(list_words[1]).capitalize()
        name3.text = str(list_words[2]).capitalize()
        name4.text = str(list_words[3]).capitalize()
        name1.draw()
        name2.draw()
        name3.draw()
        name4.draw()
        
        # load the face on the screen (and prepare for the feedback display)
        picture.image       = FacesDir + "/" + str(int(df.Face.iloc[j])) + ".jpg"
        face_encode.image   = FacesDir + "/" + str(int(df.Face.iloc[j])) + ".jpg"
        picture.draw()
        
        # display the image and names
        fix.draw()
        win.flip()
        time.sleep(Reading_time)
        
        # load the boxes
        box1.lineColor = str(list_colorbox[0])
        box2.lineColor = str(list_colorbox[1])
        box3.lineColor = str(list_colorbox[2])
        box4.lineColor = str(list_colorbox[3])
        box1.draw()
        box2.draw()
        box3.draw()
        box4.draw()
        name1.draw()
        name2.draw()
        name3.draw()
        name4.draw()
        picture.draw()
        fix.draw()
        
        # display the stimuli on the screen
        win.flip()
        
        # wait for the response
        event.clearEvents(eventType = "keyboard")
        my_clock.reset()
        if speedy != 1:
            keys = event.waitKeys(keyList = position_wbox)
        else:
            keys = "d"
        
        # add an escape option
        if keys[0] == "escape":
            break
        
        # register the response
        df.loc[[j], 'RT']               = my_clock.getTime()
        df.loc[[j], 'Response']         = keys[0]

       # Anticipation before the feedback
        Anticipation.draw()
        win.flip()
        AnticipationOnset = globalClock.getTime()
        time.sleep(Anticipation_time)
       
       
        
        # getting the position of the response so not to select the associated word if trial is incorrect
        position_response = [keyList.index(keys[0])]
        
        # concatenating the indexes we want to remove from the list of words
        position_tot = position_response + position_bbox
        
        # sorting the list from smallest to largest
        position_tot.sort()
        
        # determine the feedback
        if df.Correct.iloc[j] == 1: 
            
            fb_color        = "green"
            feedback1.text  = feedback_list[1]
            feedback2.text  = feedback_list[3]
            
            word_selected   = list_words[position_response[0]]
            
        elif df.Correct.iloc[j] == 0:
            
            fb_color        = "red"
            feedback1.text  = feedback_list[0]
            feedback2.text  = feedback_list[2]
            
            
            # we delete the words that cannot be taken as correct, i.e. the one selected and those "grey boxed"
            words_left      = [x for i, x in enumerate(list_words) if i not in position_tot]
            
            # we randomly select one word from those who are left
            word_selected   = random.choice(words_left)
        
        # store the information on the selected word
        df.loc[[j], 'SelectedWord']     = word_selected
        
        # set the feedback properties
        word_encode.text        = ">      " + str(word_selected).capitalize()
        word_encode.color       = fb_color
        box_encode.lineColor    = fb_color
        feedback1.color         = fb_color
        feedback2.color         = fb_color
        
        # provide correct answer
        feedback1.draw()
        feedback2.draw()
        win.flip()
        feedbackOnset = globalClock.getTime()
        time.sleep(feedback_time) 
       # provide correct answer
        word_encode.draw()
        face_encode.draw()
        box_encode.draw()
        win.flip()
        EncodeOnset = globalClock.getTime()
        time.sleep(Encoding_time)
        
        # determine the money feedback
        if df.Correct.iloc[j] == 1:
            total_money     = total_money + money_inc
        elif df.Correct.iloc[j] == 0:
            total_money     = total_money + 0
            
        # set the money feedback
        money_feedback.text     = "总金额: " + str('%.1f' % total_money) + " 元"
        
        # display money feedback
        money_feedback.draw()
        win.flip()
        moneyOnset = globalClock.getTime()
        time.sleep(Money_time)
        
        # implement early exit
        if earlyExit == 1 and j > 2:
            break

# saving the data from the learning phase training
df.to_csv(learn_train_file_name, encoding='utf_8_sig')

# announce the end of the experiment
message.text = "您好，第一阶段测试已完成！"
message.draw()
win.flip()
event.clearEvents(eventType = "keyboard")
event.waitKeys(keyList = "space")
logging.basicConfig(filename=logging_file_name, level=logging.INFO, format="%(asctime)s - %(message)s")
datetime.now()
logging.info("Famous face familar: end")
# close the experiment window
win.close()
