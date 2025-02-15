# The code below runs on PsychoPy
# and implements the experiment of De Loof and colleagues (2018, PLoS One)
# with the difference that dutch words are replaced by faces

# written by Cristian Buc Calderon and Esther De Loof, spring 2018
# revized by Esther De Loof for PsychoPy3, spring 2019
# some changes by Tom Verguts, spring 2021
# changed by zhaoxiaohui for iEEG experiment , spring 2021

# importing modules
from __future__ import division
from psychopy import visual, event, core, gui, data,logging
import os,sys, math, pandas, numpy, random, time

# import iEEG trigger as s
import logging
from datetime import datetime

# import iEEG trigger as s
# port = parallel.ParallelPort(address=0x0378)

iEEG = 1 # fRMI (set to 1) or pilot (set to something else)
earlyExit = 0 # provide a short test while programming (if set to 1)
speedy = 0 # provide a speeded version of the experiment for debugging (if set to 1)

# set the directory
my_directory = os.getcwd()
data_dir     = os.path.join(my_directory, "data")
FacesDir     = os.path.join(my_directory, "Luminancescaled")
recognitionDir  = os.path.join(data_dir, "recognition")
LogDir     = os.path.join(data_dir, "logfile")

if not os.path.isdir(recognitionDir):
    os.mkdir(recognitionDir)
    
# data file
already_exists              = True
already_exists_train        = True
unknown_participant         = True
unknown_participant_train   = True
while already_exists or already_exists_train or unknown_participant  or unknown_participant_train:
    
    # collect the participant info
    info    = {"Participant number": 99, "Age": 20, "Handedness": [ "right-handed","left-handed"], "Gender": ["female", "male"]}
    myDlg   = gui.DlgFromDict(dictionary = info, title = "Face Swahili fMRI study")
    
    # make the data file names
    rec_file_name       = recognitionDir + "/Recognitiontwo_participant_"           + str(info["Participant number"]) + ".csv"
    rec_train_file_name = recognitionDir + "/Recognitiontwo_training_participant_"  + str(info["Participant number"]) + ".csv"
    exp_file_name       = my_directory + "/data/exp/Learningtwo_participant_"                      + str(info["Participant number"]) + ".csv"
    exp_train_file_name = my_directory + "/data/train/Learning_training_participant_"           + str(info["Participant number"]) + ".csv"
    logging_file_name       = LogDir     + "/Log_participant_"          + str(info["Participant number"]) + ".log"

    # check whether the file names already exists
    if not os.path.isfile(rec_file_name):
        already_exists = False
    else:
        myDlg2 = gui.Dlg(title = "Error")
        myDlg2.addText("This number was already used in the recognition test. Please enter another participant number.")
        myDlg2.show()
    
    if not os.path.isfile(rec_train_file_name):
        already_exists_train = False
    else:
        myDlg2 = gui.Dlg(title = "Error")
        myDlg2.addText("This number was already used in the recognition test training. Please enter another participant number.")
        myDlg2.show()
    
    if os.path.isfile(exp_file_name):
        unknown_participant = False
    else:
        myDlg2 = gui.Dlg(title = "Error")
        myDlg2.addText("This number was not used during the experiment before. Please enter an existing participant number.")
        myDlg2.show()
    
    if os.path.isfile(exp_train_file_name):
        unknown_participant_train = False
    else:
        myDlg2 = gui.Dlg(title = "Error")
        myDlg2.addText("This number was not used during the experiment training before. Please enter an existing participant number.")
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

# set the timing of the experiment
if speedy != 1:
    PreStim_time        = 1
    Anticipation_time   = 3
    Blank_time          = 0.5
    feedback_time       = 3
        
else:
    PreStim_time    = 0.1
    PreStim_time        = 0.1
    Anticipation_time   = 0.1
    Blank_time          = 0.1
    feedback_time       = 0.1
# loading the datasets
data_exp        = pandas.read_csv(exp_file_name,        sep = ",", header = 0, index_col = False)
data_train      = pandas.read_csv(exp_train_file_name,  sep = ",", header = 0, index_col = False)

# load in stimuli and set the stimulus parameters
npractice       = 3
feedback_list   = ["错误", "正确"]
ntrials         = 35
colorword       = (1,1,1)
colorbackground = (-1,-1,-1)
my_clock        = core.Clock()
keyList         = ["d", "c", "n", "j", "escape"]
position_bbox   = []
my_clock        = core.Clock()
globalClock     = core.Clock()

# initialize the window
win = visual.Window([1000, 700], color = colorbackground, fullscr = True)

# hide mouse cursor
win.mouseVisible = False

# prepare graphical elements
stim1           = visual.TextStim(  win, text = "",         pos = (-0.4,-0.4 ),     color = colorword)
stim2           = visual.TextStim(  win, text = "",         pos = (-0.4,-0.7 ),     color = colorword)
stim3           = visual.TextStim(  win, text = "",         pos = ( 0.4,-0.7 ),     color = colorword)
stim4           = visual.TextStim(  win, text = "",         pos = ( 0.4,-0.4),      color = colorword)
message         = visual.TextStim(  win, text = "",         pos = ( 0  , 0   ),     color = colorword)
Anticipation    = visual.TextStim(  win, text = "…",        pos = ( 0   , 0   ),    color = colorword)
Blank           = visual.TextStim(  win, text = "",        pos = ( 0   , 0   ),    color = colorword)
feedback       = visual.TextStim(  win, text = "",         pos = ( 0   , 0   ),    color = colorword)
fix             = visual.TextStim(  win, text = "+",        pos = ( 0  ,-0.55),     color = colorword)
picture         = visual.ImageStim( win, size = (1.0,1.2),  pos = ( 0  , 0.4 ),     image = my_directory + "/LuminanceScaled/" + str(1) + ".jpg")
instructions    = visual.ImageStim( win, size = (1.5,1.5),  pos = ( 0  , 0   ),     image = my_directory + "/instructions/Welcome.jpg")
certainty       = visual.ImageStim( win, size = (1.5,1.5),  pos = ( 0  , 0   ),     image = my_directory + "/instructions/Recognition_certainty.jpg")

# Cris used a random seed here, but I don't see a reason to use it in this version of the experiment
# set random seed
#random.seed(int(info["Participant number"]))

# make a function to display the instructions via jpg's
def display_instructions(file = "instructions.jpg"):
    
    instructions.image = file
    instructions.draw()
    win.flip()
    event.clearEvents(eventType = "keyboard")
    event.waitKeys(keyList = "space")

# make a function to count down 5 seconds
def countdown():
    
    message.text = "请集中注意力，测试将在5秒后开始..."
    message.draw()
    win.flip()
    time.sleep(4) # left on purpose one more second :)
    
    for i in range(2):
        message.text = str(2-i)
        message.draw()
        win.flip()
        time.sleep(1)

# preping the dataframe for the training and task + loading parameters for both
### extract groups of 5 trials from the data
prop1 = data_exp.iloc[ 0:5]
prop2 = data_exp.iloc[ 5:10]
prop3 = data_exp.iloc[10:15]
prop4 = data_exp.iloc[15:20]
prop5 = data_exp.iloc[20:25]
prop6 = data_exp.iloc[25:30]
prop7 = data_exp.iloc[30:35]

### randomize the order of the trials in these subgroups
pr1 = prop1.sample(frac=1).reset_index(drop=True)
pr2 = prop2.sample(frac=1).reset_index(drop=True)
pr3 = prop3.sample(frac=1).reset_index(drop=True)
pr4 = prop4.sample(frac=1).reset_index(drop=True)
pr5 = prop5.sample(frac=1).reset_index(drop=True)
pr6 = prop6.sample(frac=1).reset_index(drop=True)
pr7 = prop7.sample(frac=1).reset_index(drop=True)

### recombine the shuffled groups
prop_shuffled = [pr1, pr2, pr3, pr4, pr5, pr6, pr7]

### insert the reshuffled data
shuffled_exp = pandas.concat(prop_shuffled).reset_index(drop = True)

### for the training data, we can just directly reshuffle all the data
shuffled_train = data_train.sample(frac = 1)

# instructions
display_instructions(file = my_directory + "/instructions/Recog_1.jpg")

# countdown another 5 seconds to start the recognition test
countdown()


datetime.now()
logging.info("Test2-train: started")

# starting the train loop
for j in range(npractice):
    
    # getting the list of words to display
    words = [shuffled_train.TestSwahili1.iloc[j], shuffled_train.TestSwahili2.iloc[j], shuffled_train.TestSwahili3.iloc[j], shuffled_train.TestSwahili4.iloc[j]]
    
    # fixation cross PreStim
    fix.draw()
    win.flip()
    FixOnset = globalClock.getTime()
    time.sleep(PreStim_time)
    
    # load the words on the screen
    stim1.text = str(words[0]).capitalize()
    stim2.text = str(words[1]).capitalize()
    stim3.text = str(words[2]).capitalize()
    stim4.text = str(words[3]).capitalize()
    stim1.draw()
    stim2.draw()
    stim3.draw()
    stim4.draw()
    
    # load the face on the screen
    picture.image = FacesDir + "/" + str(int(shuffled_train.Face.iloc[j])) + ".jpg"
    picture.draw()
    
    # display the stimuli on the screen
    win.flip()
    
    # wait for the response
    my_clock.reset()
    event.clearEvents(eventType = "keyboard")
    if speedy != 1:
        keys = event.waitKeys(keyList = keyList)
    else:
        time.sleep(0.1)
        keys = "d"
    
    # add an escape option
    if keys[0] == "escape":
        break        
        
    # extract the chosen position
    position_response = keyList.index(keys[0])

    # register the response
    shuffled_train.loc[[j], 'RT_recognition']               = my_clock.getTime()
    shuffled_train.loc[[j], 'Response_recognition']         = keys[0]
    shuffled_train.loc[[j], 'Accuracy_recognition']         = int(str(words[position_response]) == str(shuffled_train.SelectedWord.iloc[j]))
    shuffled_train.loc[[j], 'SelectedWord_recognition']     = words[position_response]
    
    # probe the certainty
    certainty.draw()
    win.flip()
    my_clock.reset()
    event.clearEvents(eventType = "keyboard")
    if speedy != 1:
        keys = event.waitKeys(keyList = keyList)
    else:
        time.sleep(0.1)
        keys = "d"
    
    # add an escape option
    if keys[0] == "escape":
        break        
    
    # register the certainty
    shuffled_train.loc[[j], 'RT_certainty']                 = my_clock.getTime()
    shuffled_train.loc[[j], 'Response_certainty']           = keyList.index(keys[0])
    
    # Anticipation before the feedback
    Anticipation.draw()
    win.flip()
    AnticipationOnset = globalClock.getTime()
    time.sleep(Anticipation_time)
    
    # Blank time 
    Blank.draw()
    win.flip()
    BlankOnset = globalClock.getTime()
    time.sleep(Blank_time)
    
        
    # determine the feedback
    if int(str(words[position_response]) == str(shuffled_train.SelectedWord.iloc[j])) == 1:

        fb_color        = "green"
        feedback.text  = feedback_list[1]
        
    elif int(str(words[position_response]) == str(shuffled_train.SelectedWord.iloc[j])) == 0:
        
        fb_color        = "red"
        feedback.text  = feedback_list[0]
    
    # set the feedback properties
    feedback.color         = fb_color
    
    # display  feedback
    feedback.draw()
    win.flip()
    feedbackOnset = globalClock.getTime()
    time.sleep(feedback_time) 
    
    
# removing unecessary dataFileName
shuffled_train = shuffled_train.drop(['Swahili1', 'Swahili2', 'Swahili3', 'Swahili4', 'Color1', 'Color2', 'Color3', 'Color4', 'RT', 'Response', 'SelectedWord'], axis=1)
shuffled_train.to_csv(rec_train_file_name)



datetime.now()
logging.info("Test2-train: end")


if iEEG == 1:
    s.write(bytes([51]))
    time.sleep(0.5)
    s.write(bytes([0]))
datetime.now()
logging.info("Test-2: started")

# announce the actual trials
message.text = "练习已完成，请按空格键开始正式测试..."
message.draw()
win.flip()
event.waitKeys(keyList = "space")

# countdown another 5 seconds to start the recognition test
countdown()

# starting the exp loop
for j in range(ntrials):
    
    # getting the list of words to display
    words = [shuffled_exp.TestSwahili1.iloc[j], shuffled_exp.TestSwahili2.iloc[j], shuffled_exp.TestSwahili3.iloc[j], shuffled_exp.TestSwahili4.iloc[j]]
    
    # fixation cross PreStim
    fix.draw()
    win.flip()
    FixOnset = globalClock.getTime()
    time.sleep(PreStim_time)
    
    # load the words on the screen
    stim1.text = str(words[0]).capitalize()
    stim2.text = str(words[1]).capitalize()
    stim3.text = str(words[2]).capitalize()
    stim4.text = str(words[3]).capitalize()
    stim1.draw()
    stim2.draw()
    stim3.draw()
    stim4.draw()
    
    # load the face on the screen
    picture.image = FacesDir + "/" + str(int(shuffled_exp.Face.iloc[j])) + ".jpg"
    picture.draw()
    
    # display the stimuli on the screen
    win.flip()
    my_clock.reset()
   
    if iEEG == 1:
        s.write([71])
        time.sleep(marker_delay)
        s.write(bytes([0]))
    datetime.now()
    logging.info("test_SRPE = " + str(shuffled_exp.loc[j,"SRPE"]))
    
    
    # wait for the response
    event.clearEvents(eventType = "keyboard")
    if speedy != 1:
        keys = event.waitKeys(keyList = keyList)
    else:
        time.sleep(0.1)
        keys = "d"
    
    #add a marker in the recognition certainty phase onset

       
    # add an escape option
   
    # extract the chosen position
     
    # register the response
    shuffled_exp.loc[[j], 'RT_recognition']                 = my_clock.getTime()
    if keys[0] == "escape":
        break

    position_response = keyList.index(keys[0])
    shuffled_exp.loc[[j], 'Response_recognition']           = keys[0]
    shuffled_exp.loc[[j], 'Accuracy_recognition']           = int(str(words[position_response]) == str(shuffled_exp.SelectedWord.iloc[j]))
    shuffled_exp.loc[[j], 'SelectedWord_recognition']       = words[position_response]
    
    # probe the certainty
    certainty.draw()
    win.flip()
    my_clock.reset()    

    if iEEG == 1:
        s.write(bytes([3]))
        time.sleep(marker_delay)
        s.write(bytes([0]))

    datetime.now()
    logging.info("Uncertainty")

    event.clearEvents(eventType = "keyboard")
    if speedy != 1:
        keys = event.waitKeys(keyList = keyList)
    else:
        time.sleep(0.1)
        keys = "d"

    # register the certainty
    shuffled_exp.loc[[j], 'RT_certainty']                   = my_clock.getTime()
    shuffled_exp.loc[[j], 'Response_certainty']             = keyList.index(keys[0])
    
    # Anticipation before the feedback
    Anticipation.draw()
    win.flip()

    if iEEG == 1:
        s.write(bytes([3]))
        time.sleep(marker_delay)
        s.write(bytes([0]))
    datetime.now()
    logging.info("test_anticipation")


    AnticipationOnset = globalClock.getTime()
    time.sleep(Anticipation_time-marker_delay)
    
    # Blank time 
    Blank.draw()
    win.flip()
     # ieeg
    if iEEG == 1:
        s.write(bytes([3]))
        time.sleep(marker_delay)
        s.write(bytes([0]))
    datetime.now()
    logging.info("blank:0.5s")

    BlankOnset = globalClock.getTime()
    time.sleep(Blank_time-marker_delay)
     
    
    # determine the feedback
    if int(str(words[position_response]) == str(shuffled_exp.SelectedWord.iloc[j])) == 1:
        fb_color        = "green"
        feedback.text  = feedback_list[1]
        
    elif int(str(words[position_response]) == str(shuffled_exp.SelectedWord.iloc[j])) == 0:
        fb_color        = "red"
        feedback.text  = feedback_list[0]
     
    # set the feedback properties
    feedback.color         = fb_color 
    
    # display  feedback
    feedback.draw()
    win.flip()
    feedbackOnset = globalClock.getTime()
    # 
    if iEEG == 1:
        s.write(bytes([3]))
        time.sleep(marker_delay)
        s.write(bytes([0]))
    datetime.now()

    logging.info("acc_feedback")
    time.sleep(feedback_time-marker_delay) 

#removing unecessary dataFileName

shuffled_exp.to_csv(rec_file_name)

# wait for first fMRI pulse (press escape in the behavioral task)
message.text = ("恭喜您，当前测试已完成！")
message.draw()
win.flip()
time.sleep(5)


if iEEG == 1:
    s.close()
datetime.now()
logging.info("Test-2: end")
# close the experiment window
win.close()
