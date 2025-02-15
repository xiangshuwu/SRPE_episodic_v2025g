# The code below runs on PsychoPy
# and implements the experiment of De Loof and colleagues (2018, PLoS One)
# with the difference that dutch words are replaced by faces

# written by Cristian Buc Calderon and Esther De Loof, spring 2018
# revized by Esther De Loof for PsychoPy3, spring 2019
# some changes by Tom Verguts, spring 2021
# changed by zhaoxiaohui for iEEG experiment , spring 2021


# importing modules
from psychopy import core, event, visual, gui, logging
import os,sys, pandas, numpy, random, time

import logging
from datetime import datetime


iEEG = 1  # iEEG (set to 1) or pilot (set to something else)
earlyExit = 0 # provide a short test while programming (if set to 1)
speedy = 0 # provide a speeded version of the experiment for debugging (if set to 1)


# set the directory
my_directory = os.getcwd()
dataDir     = os.path.join(my_directory, "data")
FacesDir     = os.path.join(my_directory, "Luminancescaled")
FaceTestDir  = os.path.join(dataDir, "FaceTest")
LearnDir     = os.path.join(dataDir, "exp")
LogDir     = os.path.join(dataDir, "logfile")


if not os.path.isdir(LearnDir):
    os.mkdir(LearnDir)

# data file
already_exists = True
while already_exists:
    
    # collect the participant info
    info    = {"Participant number": 99, "Age": 20, "Handedness": ["right-handed","left-handed"], "Gender": ["female", "male"]}
    myDlg   = gui.DlgFromDict(dictionary = info, title = "Face Swahili fMRI study")
    
    # make the data file names
    exp_file_name           = my_directory + "/data/FaceTest/exp_words_participant_"    + str(info["Participant number"]) + ".csv"
    exptwo_file_name        = my_directory + "/data/FaceTest/exptwo_words_participant_"     + str(info["Participant number"]) + ".csv"
    learn_fMRI_file_name    = my_directory + "/data/FaceTest/fMRI_data_set_participant_"+ str(info["Participant number"]) + ".csv"
    learn_file_name         = my_directory     + "/data/exp/Learning_participant_"          + str(info["Participant number"]) + ".csv"
    logging_file_name       = LogDir     + "/Log_participant_"          + str(info["Participant number"]) + ".log"
    # check whether the file names already exists
    if not os.path.isfile(learn_file_name):
        already_exists = False
    # if they already exist, ask for another participant number
    else:
        myDlg2 = gui.Dlg(title = "Error")
        myDlg2.addText("This number was already used. Please enter another participant number.")
        myDlg2.show()

    if not myDlg.OK:  # 用户点击了“取消”或关闭按钮（X）
        sys.exit()


if iEEG ==  1:
    import serial
    s = serial.Serial('COM4', 115200, timeout=1) 
    marker_delay = 0.05
else:
    marker_delay = 0


logging.basicConfig(filename=logging_file_name, level=logging.INFO, format="%(asctime)s - %(message)s")

if iEEG == 1:
    s.write(bytes([50]))
    time.sleep(0.5)
    s.write(bytes([0]))
datetime.now()
logging.info("Learning-1: started")

# set the timing of the experiment
if speedy != 1:
    Fixation_time   = 0.5
    Reading_time    = 4
    Anticipation_time   = 3
    feedback_time    = 3
    Encoding_time   = 5
    Money_time      = 2
else:
    Fixation_time   = 0.1
    Reading_time    = 0.1
    Anticipation_time    = 0.1
    feedback_time   = 0.1
    Encoding_time   = 0.1
    Money_time      = 0.1

# adapt the monetary reward for the pilot versus fMRI version of the experiment
money_inc = 0.30

# load in stimuli and set the stimulus parameters for the Swahili options
nexpone         = 35
nexptwo         = 35

# load the list of words for the experiment
all_faces       = nexpone + nexptwo
list_words      = pandas.read_csv(exp_file_name, sep = ",", header = None, names =["s"])
expone_words        = list_words.s[0:nexpone*4-1] 
# print(list_words.s[0:nexpone*4])
exptwo_words        = list_words.s[nexpone*4:(nexpone+nexptwo)*4-1].reset_index(drop=True)

# saving the exp two  words for the following learning task
exptwo_words.to_csv(exptwo_file_name, encoding='utf_8_sig')

# load in stimuli and set the stimulus parameters for the face recognition
feedback_list   = ["错误", "正确", "+ 0 元", "+ " + str(money_inc) + " 元" ]
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
globalClock     = core.Clock()
keyList         = ["d", "c", "n", "j", "escape"]




# initialize the window
win = visual.Window([1000, 700], color = colorbackground, fullscr = True)
 
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
feedback1       = visual.TextStim(  win, text = "",         pos = ( 0   , 0.1 ),    color = colorword)
feedback2       = visual.TextStim(  win, text = "",         pos = ( 0   , 0 ),    color = colorword)
word_encode     = visual.TextStim(  win, text = "",         pos = ( 0.2 , 0   ),    color = colorword)
money_feedback  = visual.TextStim(  win, text = "",         pos = ( 0   , 0    ),   color = colorword)
fix             = visual.TextStim(  win, text = "+",        pos = ( 0   ,-0.55),    color = colorword)
picture         = visual.ImageStim( win, size = (1.0,1.2),  pos = ( 0   , 0.4 ),    image = FacesDir + "/" + str(1) + ".jpg")
face_encode     = visual.ImageStim( win, size = (0.7,0.5),  pos = (-0.33 , 0   ),    image = FacesDir + "/" + str(1) + ".jpg")
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
    
    message.text = "请集中注意力，测试将在5秒后开始..."
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

# loading the fMRI data set selected in the previous script (i.e. part 1 and 2)
# dataset = pandas.read_csv(learn_fMRI_file_name, sep = ",", header = None, index_col = False)
dataset = pandas.read_csv(learn_fMRI_file_name, sep = ",", index_col = False)

# opening the dataframe
df = pandas.DataFrame()

# adding different types of info 
df["NOptions"]   = [1] * 5 + [2] * 10 + [4] * 20
df["Correct"]    = [1] * 5 + [0] * 5 + [1] * 5 + [0] * 15 + [1] * 5
df["SRPE"]       = [float(df.loc[i,["Correct"]]) - float(1/df.loc[i,["NOptions"]]) for i in range(df.shape[0])]

# adding the Swahili words
df["Swahili1"]   = expone_words.iloc[nexpone*0:nexpone*1].reset_index(drop=True)
df["Swahili2"]   = expone_words.iloc[nexpone*1:nexpone*2].reset_index(drop=True)
df["Swahili3"]   = expone_words.iloc[nexpone*2:nexpone*3].reset_index(drop=True)
df["Swahili4"]   = expone_words.iloc[nexpone*3:nexpone*4].reset_index(drop=True)
print(dataset)
df["Face"]       = dataset.Pictures.iloc[6:nexpone+6].reset_index(drop=True)

# place the same Swahili words in random order for the test trials
df["TestSwahili1"] = ""
df["TestSwahili2"] = ""
df["TestSwahili3"] = ""
df["TestSwahili4"] = ""
four = [0, 1, 2, 3]
for i in range(nexpone):
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
for i in range(nexpone):
    if df.loc[i,"NOptions"] == 1:
        random.shuffle(oneOptions)
        df.loc[i,["Color1","Color2","Color3","Color4"]] = oneOptions
    elif df.loc[i,"NOptions"] == 2:
        random.shuffle(twoOptions)
        df.loc[i,["Color1","Color2","Color3","Color4"]] = twoOptions

# add the jitters
## creating the jitter priorly optimized for our fMRI design using the DesignDiagnostics Script from Martin Monti 
## available @ https://montilab.psych.ucla.edu/designdiagnostics/
## df["JitterPreEncoding"]      = 0
## df["JitterPostEncoding"]     = 0


# shuffle the dataframe
df = df.sample(frac = 1).reset_index(drop = True)

# instructions for the training session 

display_instructions(file = my_directory + "/instructions/TS_6.jpg")


# countdown another 5 seconds to start the learning task
countdown()

# start of the trial loop for the learning task
for j in range(nexpone):
    
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
    Fix1Onset = globalClock.getTime()
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
    
  
    # display the image and names
    picture.draw()
    win.flip()
    # 
    if iEEG == 1:
        s.write(bytes([3]))
        time.sleep(marker_delay)
        s.write(bytes([0]))

    datetime.now()
    logging.info("reading")

    ReadingOnset = globalClock.getTime()
    time.sleep(Reading_time-marker_delay)
    
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
 
    

    # display the stimuli on the screen
    event.clearEvents(eventType = "keyboard")
    win.flip()
    my_clock.reset()

    if iEEG == 1:
        s.write(bytes([3]))
        time.sleep(marker_delay)
        s.write(bytes([0]))

    datetime.now()
    logging.info("box")

    # wait for the response
    if speedy != 1:
        keys = event.waitKeys(keyList = position_wbox)
    else:
        time.sleep(0.1)
        keys = "d"
        
    # add an escape option
    if keys[0] == "escape":
        break
        
    # register the response
    df.loc[[j], 'RT']               = my_clock.getTime()
    df.loc[[j], 'Response']         = keys[0]
    
    #add marker in the anticipation phase
     # Anticipation before the feedback

    Anticipation.draw()
    win.flip()

    if iEEG == 1:
        s.write(bytes([3]))
        time.sleep(marker_delay)
        s.write(bytes([0]))               
    
    datetime.now()
    logging.info("anticipation")

    AnticipationOnset = globalClock.getTime()
    time.sleep(Anticipation_time-marker_delay)
  

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
    df.loc[[j], 'SelectedWord'] = word_selected
    
    # set the feedback properties
    word_encode.text        = ">      " + str(word_selected).capitalize()
    word_encode.color       = fb_color
    box_encode.lineColor    = fb_color
    feedback1.color         = fb_color
    feedback2.color         = fb_color
 
    
   # display  feedback and add a marker in the feedback phase
    
    feedback1.draw()
    feedback2.draw()
    win.flip()
    feedbackOnset = globalClock.getTime()
    if iEEG == 1:
        s.write(bytes([70]))
        time.sleep(marker_delay)
        s.write(bytes([0]))

    datetime.now()
    logging.info("learning_SRPE = " + str(df.loc[j,"SRPE"]))

    time.sleep(feedback_time-marker_delay) 
    
    # provide correct answer
    word_encode.draw()
    face_encode.draw()
    box_encode.draw()
    win.flip()
    if iEEG == 1:
        s.write(bytes([3]))
        time.sleep(marker_delay)
        s.write(bytes([0]))

    datetime.now()
    logging.info("encoding")

    
    EncodeOnset = globalClock.getTime()
    time.sleep(Encoding_time-marker_delay)
    
    
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
    if iEEG == 1:
        s.write(bytes([3]))
        time.sleep(marker_delay)
        s.write(bytes([0]))

    datetime.now()
    logging.info("total_money")


    moneyOnset = globalClock.getTime()
    time.sleep(Money_time-marker_delay)
    
    # implement early exit
    if earlyExit == 1 and j > 2:
        break

# saving the data from the Learning test
df.to_csv(learn_file_name, encoding='utf_8_sig')

# wait for first fMRI pulse (press escape in the behavioral task)
message.text = ("您好，当前任务已结束！ \n\n" +
                "稍事休息后，我们接下来要进行下一个任务...")
message.draw()
win.flip()
time.sleep(5)
if iEEG == 1:
    s.close()

datetime.now()
logging.info("Learning-1: end")

# close the experiment window
win.close()