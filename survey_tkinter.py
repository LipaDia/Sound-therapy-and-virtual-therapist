from tkinter import (Tk, Label, Button, Radiobutton, Frame, Menu,
    messagebox, StringVar, Listbox, BROWSE, END, Toplevel, Entry)
from tkinter import ttk
from tkinter import messagebox
import pathlib
import time
import csv
import os.path

# create empty lists used for each set of questions
lifestyle_list = []
#sig_trends_list = []
#future_trends_list = []
#general_answers_list = []

def dialogBox(title, message):
    """
    Basic function to create and display general dialog boxes.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 1280, 720
    positionRight = int(dialog.winfo_screenwidth()/2 - dialogWidth/2)
    positionDown = int(dialog.winfo_screenheight()/2 - dialogHeight/2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    label = Label(dialog, text=message)
    label.pack(side="top", fill="x", pady=10)
    ok_button = ttk.Button(dialog, text="Ok", command=dialog.destroy)
    ok_button.pack(ipady=3, pady=10)
    dialog.mainloop()

def nextSurveyDialog(title, message, cmd):
    """
    Dialog box that appears before moving onto the next set of questions.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 1280, 720
    positionRight = int(dialog.winfo_screenwidth()/2 - dialogWidth/2)
    positionDown = int(dialog.winfo_screenheight()/2 - dialogHeight/2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    dialog.overrideredirect(True)
    label = Label(dialog, text=message)
    label.pack(side="top", fill="x", pady=10)
    ok_button = ttk.Button(dialog, text="QUIT", command=quit)
    ok_button.pack(ipady=3, pady=10)

    dialog.protocol("WM_DELETE_WINDOW", disable_event) # prevent user from clicking ALT + F4 to close
    dialog.mainloop()
    dialog.quit()

def disable_event():
    pass

def finishedDialog(title, message):
    """
    Display the finished dialog box when user reaches the end of the survey.
    """
    dialog = Tk()
    dialog.wm_title(title)
    dialog.grab_set()
    dialogWidth, dialogHeight = 325, 150
    positionRight = int(dialog.winfo_screenwidth()/2 - dialogWidth/2)
    positionDown = int(dialog.winfo_screenheight()/2 - dialogHeight/2)
    dialog.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
    dialog.maxsize(dialogWidth, dialogHeight)
    dialog.overrideredirect(True)
    label = Label(dialog, text=message)
    label.pack(side="top", fill="x", pady=10)
    ok_button = ttk.Button(dialog, text="Quit", command=quit)
    ok_button.pack(ipady=3, pady=10)

    dialog.protocol("WM_DELETE_WINDOW", disable_event) # prevent user from clicking ALT + F4 to close
    dialog.mainloop()

def writeToFile(filename, answer_list):
        """
        Called at end of program when user selects finished button, 
        write all lists to separate files.
        Parameters: filename: name for save file,
                    answer_list: list containing answer from that one of the 
                    four sections in the survey.
        """
        headers = []  
        file_exists = os.path.isfile(filename)

        with open(filename, 'a') as csvfile:
            for i in range(1, len(answer_list) + 1):
                headers.append("Q{}".format(i))
            writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            
            if not file_exists:
                writer.writerow(headers) # file doesn't exist yet, write a header

            writer.writerow(answer_list)

class otherPopUpDialog(object):
    """
    Class for 'other' selections in General Question class.
    When user selects 'other' option, they are able to input 
    their answer into an Entry widget.

    self.value: the value of Entry widget.
    """
    def __init__(self, master, text):
        top=self.top=Toplevel(master)
        self.text = text
        top.wm_title("Other Answers")
        top.grab_set()
        dialogWidth, dialogHeight = 1280, 720
        positionRight = int(top.winfo_screenwidth()/2 - dialogWidth/2)
        positionDown = int(top.winfo_screenheight()/2 - dialogHeight/2)
        top.geometry("{}x{}+{}+{}".format(
        dialogWidth, dialogHeight, positionRight, positionDown))
        self.label = Label(top, text=self.text)
        self.label.pack(ipady=5)
        self.enter = Entry(top)
        self.enter.pack(ipady=5)
        self.ok_button = Button(top, text="Ok", command=self.cleanup) 
        self.ok_button.pack(ipady=5)

    def cleanup(self):
        """
        Get input from Entry widget and close dialog.
        """
        self.value = self.enter.get()
        self.top.destroy()

class Survey(Tk):
    """
    Main class, define the container which will contain all the frames.
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # call closing protocol to create dialog box to ask 
        # if user if they want to quit or not.
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        Tk.wm_title(self, "(PERSONALITY SURVEY)")

        # get position of window with respect to screen
        windowWidth, windowHeight = 1280, 720
        positionRight = int(Tk.winfo_screenwidth(self)/2 - windowWidth/2)
        positionDown = int(Tk.winfo_screenheight(self)/2 - windowHeight/2)
        Tk.geometry(self, newGeometry="{}x{}+{}+{}".format(
            windowWidth, windowHeight, positionRight, positionDown))
        Tk.maxsize(self, windowWidth, windowHeight)

        # Create container Frame to hold all other classes, 
        # which are the different parts of the survey.
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Create menu bar
        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Quit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        
        Tk.config(self, menu=menubar)

        # create empty dictionary for the different frames (the different classes)
        self.frames = {}

        for fr in (StartPage, LifeStyleSurveyPages):
            frame = fr(container, self)
            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()

    def show_frame(self, cont):
        """
        Used to display a frame.
        """
        frame = self.frames[cont]
        frame.tkraise() # bring a frame to the "top"

class StartPage(Frame):
    """
    First page that user will see.
    Explains the rules and any extra information the user may need 
    before beginning the survey.
    User can either click one of the two buttons, Begin Survey or Quit.
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        # set up start page window
        self.configure(bg="#EFF3F6")
        start_label = Label(self, text="Survey", font=("serifed Palatino", 16), 
                            borderwidth=2, relief="ridge")
        start_label.pack(pady=10, padx=10, ipadx=5, ipady=3)

        #play_image = PhotoImage(file='images/Bhoomi.png').subsample(32,32)
        #play_button.config(image=play_image)

        # add labels and buttons to window
        info_text = "WELCOME TO SMV PERSONALITY SURVEY."
        info_label = Label(self, text=info_text, font=("serifed Palatino", 12),
                           borderwidth=2, relief="ridge")
        info_label.pack(pady=10, padx=10, ipadx=20, ipady=3)

        purpose_text = "This survey is used to determine your stress levels.\nYour treatment is given based on the personality survey"
        purpose_text = Label(self, text=purpose_text, font=("serifed Palatino", 12),
                           borderwidth=2, relief="ridge")
        purpose_text.pack(pady=10, padx=10, ipadx=5, ipady=3)

        start_button = ttk.Button(self, text="Begin Survey", 
            command=lambda: controller.show_frame(LifeStyleSurveyPages))
        start_button.pack(ipadx=10, ipady=15, pady=15)

        quit_button = ttk.Button(self, text="Quit", command=self.on_closing)
        quit_button.pack(ipady=3, pady=10)

    def on_closing(self):
        """
        Display dialog box before quitting.
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.controller.destroy()

class LifeStyleSurveyPages(Frame):
    """
    Class that displays the window for the life style survey questions. 
    When the user answers a question, the answer saved to a list.  
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.controller = controller

        global lifestyle_list

        # Create header label
        ttk.Label(self, text="SURVEY", font=('Verdana', 20),
                  borderwidth=2, relief="ridge").pack(padx=10, pady=10)

        self.questions = ["You usually stay calm, even under a lot of pressure.", "Even a small mistake can cause you to doubt your overall abilities and knowledge.", 
                          "You are prone to worrying that things will take a turn for the worse.","You lose patience with people who are not as efficient as you",
                          "You often end up doing things at the last possible moment.","You always second-guess the choices that you have made.","Most of the time, you feel insecure",
                          "Your emotions control you more than you control them","You almost always feel that life is very much not worth living.",
                          "You are so concerned about the future that you do not get as much fun out of the present as you might.",
                          "Disappointment affects you so much that it ruins your day.","I have a greater dependency on alcohol, caffeine, nicotine or drugs",
                          " My self-confidence / self-esteem is lower than I would like it to be","I frequently have guilty feelings if I relax and do nothing",
                          "If something or someone really annoys me I will bottle up my feelings",
                          "I experience mood swings, difficulty making decisions, concentration and memory is impaired",
                          "I feel irritated or angry if the car or traffic in front seems to be going too slowly/ I become very frustrated at having to wait in a queue",
                          "My appetite has changed, have either a desire to binge or have a loss of appetite / may skip meals",
                          "In the last month, often I have felt difficulties were piling up so high that I could not overcome them.",
                          " I have often been upset because of something that happened unexpectedly",
                          "I have often felt nervous and stressed","I have been able to control irritations in my work life.",
                          "I have been angered because of things that happened that were outside of my control",
                          "I have found myself thinking about the things that I want to accomplish.","I find myself thinking about problems even when I am supposed to be relaxing"]

        # set index in questions list 
        self.index = 0
        self.length_of_list = len(self.questions)

        # Set up labels and checkboxes 
        self.question_label = Label(self, text="{}. {}".format(self.index + 1, self.questions[self.index]), font=('serifed Palatino', 10))
        self.question_label.pack(anchor='w', padx=20, pady=10)
        Label(self, text="Choose the answer that best suits you.", font=('serifed Palatino', 10)).pack(padx=50)

        # Not at all, somewhat, average, agree, strongly agree
        scale_text = ["Strongly Disagree", "Disagree","Indifferent","Agree","Strongly agree"]

        scale = [("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5)]

        self.var = StringVar()
        self.var.set(0) # initialize

        # Frame to contain text 
        checkbox_scale_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_scale_frame.pack(pady=2)

        for text in scale_text:
            b = ttk.Label(checkbox_scale_frame, text=text)
            b.pack(side='left', ipadx=7, ipady=5)

        # Frame to contain checkboxes
        checkbox_frame = Frame(self, borderwidth=2, relief="ridge")
        checkbox_frame.pack(pady=10, anchor='center')

        for text, value in scale:
            b = ttk.Radiobutton(checkbox_frame, text=text, 
                variable=self.var, value=value)
            b.pack(side='left', ipadx=17, ipady=2)

        # Create next question button
        enter_button = ttk.Button(self, text="Next Question", command=self.nextQuestion)
        enter_button.pack(ipady=5, pady=20)
        
    def nextQuestion(self):
        '''
        When button is clicked, add user's input to a list
        and display next question.
        '''
        answer = self.var.get()

        if answer == '0':
            dialogBox("No Value Given", 
                "You did not select an answer.\nPlease try again.")
        elif self.index == (self.length_of_list - 1):
            # get the last answer from user
            selected_answer = self.var.get()
            lifestyle_list.append(selected_answer)

            next_survey_text = "End"
            nextSurveyDialog("Next Survey", next_survey_text, lambda: self.controller.show_frame(SignificantConsumptionTrendsSurveyPages))
        else:
            self.index = (self.index + 1) % self.length_of_list

            self.question_label.config(text="{}. {}".format(self.index + 1, self.questions[self.index]))
            selected_answer = self.var.get()
            lifestyle_list.append(selected_answer)

            self.var.set(0) # reset value for next question

            time.sleep(.2) # delay between questions





    def writeToFile(self):
        """
        When user selects finished button, writes each filename with corresponding 
        answer list to separate files.
        """
        # list of names and answer lists
        filenames = ['01_lifestyle_answers.csv']

        answers_lists = [lifestyle_list]

        for filename, answers in zip(filenames, answers_lists):
            writeToFile(filename, answers)

# Run program
if __name__ == "__main__":
    app = Survey()
    app.mainloop()
    app.quit()