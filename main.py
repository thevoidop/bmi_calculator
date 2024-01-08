# Import necessary libraries and modules
import customtkinter as ctk
from attributes import *

try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass

# Define the main application class
class App(ctk.CTk):
    def __init__(self):
        # Initialize the main application window
        super().__init__(fg_color=PRIMARY_COLOR)
        self.title("")
        self.iconbitmap("empty.ico")
        self.geometry("400x400")
        self.resizable(False, False)
        self.titlebarcolor()  # Set the title bar color
        
        # Configure the layout
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")
        self.columnconfigure(0, weight=1)
        
        # Initialize variables
        self.heightInt = ctk.IntVar(value=170)
        self.weightFloat = ctk.DoubleVar(value=65)
        self.bmiResult = ctk.StringVar()
        self.metricbool = ctk.BooleanVar(value=True)
        self.updateBMI()  # Update BMI initially
        
        # Create widgets
        Result(self, self.bmiResult)
        self.heightinput = Height(self, self.heightInt, self.metricbool)
        self.weightinput = Weight(self, self.weightFloat, self.metricbool)
        UnitSwitch(self, self.metricbool)
        
        # Set up tracing for variable changes
        self.heightInt.trace("w", self.updateBMI)
        self.weightFloat.trace("w", self.updateBMI)
        self.metricbool.trace("w", self.changeunits)
        
        self.mainloop()
        
    def titlebarcolor(self):
        try:  # This does not work on Mac
            HWND = windll.user32.GetParent(self.winfo_id())
            DWMWA_ATTRIBUTE = 35
            COLOR = TITLE_HEX
            windll.dwmapi.DwmSetWindowAttribute(HWND, DWMWA_ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
        except:
            pass 
        
    def updateBMI(self, *args):
        # Update BMI based on height and weight inputs
        height = self.heightInt.get() / 100
        weight = self.weightFloat.get()
        bmi = round(weight / (height)**2, 2)
        self.bmiResult.set(bmi)
        
    def changeunits(self, *args):
        # Update height and weight inputs based on unit change
        self.heightinput.updateheight(self.heightInt.get())
        self.weightinput.updateweight()
    
# Subclass for the Result widget
class Result(ctk.CTkLabel):
    def __init__(self, parent, bmi):
        # Initialize the Result widget
        super().__init__(master=parent, text="23", text_color=FONT_COLOR,
                         font=ctk.CTkFont(FONT, M_TEXT_SIZE, weight="bold"),
                         textvariable=bmi)
        self.grid(row=0, column=0, rowspan=2, sticky="news")

# Subclass for the Weight widget
class Weight(ctk.CTkFrame):
    def __init__(self, parent, weightfloat, metricbool):
        # Initialize the Weight widget
        super().__init__(master=parent, fg_color=BG_COLOR)
        self.weightfloat = weightfloat
        self.metricbool = metricbool
        self.outputstr = ctk.StringVar()
        self.updateweight()  # Update weight initially
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 4), weight=2, uniform="b")
        self.columnconfigure((1, 3), weight=1, uniform="b")
        self.columnconfigure(2, weight=3, uniform="b")
        self.grid(row=2, column=0, sticky="news", padx=10, pady=10)
        self.widgets()
        
    def widgets(self):
        # Create buttons, label, and configure layout for the Weight widget
        button1 = ctk.CTkButton(self, text="-", font=ctk.CTkFont(FONT, I_TEXT_SIZE, weight="bold"),
                                 fg_color=BUTTON_COLOR, text_color=FONT_COLOR, hover_color=HOVER_COLOR,
                                 command=lambda: self.updateweight(("minus", "large")))
        button2 = ctk.CTkButton(self, text="-", font=ctk.CTkFont(FONT, I_TEXT_SIZE, weight="bold"),
                                 fg_color=BUTTON_COLOR, text_color=FONT_COLOR, hover_color=HOVER_COLOR,
                                 command=lambda: self.updateweight(("minus", "small")))
        button3 = ctk.CTkButton(self, text="+", font=ctk.CTkFont(FONT, I_TEXT_SIZE, weight="bold"),
                                 fg_color=BUTTON_COLOR, text_color=FONT_COLOR, hover_color=HOVER_COLOR,
                                 command=lambda: self.updateweight(("plus", "small")))
        button4 = ctk.CTkButton(self, text="+", font=ctk.CTkFont(FONT, I_TEXT_SIZE, weight="bold"),
                                 fg_color=BUTTON_COLOR, text_color=FONT_COLOR, hover_color=HOVER_COLOR,
                                 command=lambda: self.updateweight(("plus", "large")))
        label = ctk.CTkLabel(self, font=ctk.CTkFont(FONT, I_TEXT_SIZE, weight="bold"),
                             text_color=FONT_COLOR, textvariable=self.outputstr)
        
        button1.grid(column=0, row=0, sticky="news", padx=8, pady=8)
        button2.grid(column=1, row=0, sticky="ns", padx=0, pady=8)
        label.grid(column=2, row=0, sticky="news", padx=5)
        button3.grid(column=3, row=0, sticky="ns", padx=0, pady=8)
        button4.grid(column=4, row=0, sticky="news", padx=8, pady=8)

    def updateweight(self, info=None):
        # Update weight based on button press and unit type
        if info: 
            if self.metricbool.get():
                amount = 1 if info[1] == "large" else 0.1
            else:
                amount = 0.453592 if info[1] == "large" else 0.453592 / 16
            if info[0] == "plus":
                self.weightfloat.set(self.weightfloat.get() + amount)
            else:
                self.weightfloat.set(self.weightfloat.get() - amount)
        if self.metricbool.get():
            self.outputstr.set(f"{round(self.weightfloat.get(), 1)} kg")
        else:
            rawounces = self.weightfloat.get() * 2.20462 * 16
            pounds, ounces = divmod(rawounces, 16)
            self.outputstr.set(f"{int(pounds)}lb {int(ounces)}oz")
                
# Subclass for the Height widget
class Height(ctk.CTkFrame):
    def __init__(self, parent, heightint, metricbool):
        # Initialize the Height widget
        super().__init__(master=parent, fg_color=BG_COLOR)
        self.metricbool = metricbool
        slider = ctk.CTkSlider(self, button_color=BUTTON_COLOR, button_hover_color=HOVER_COLOR,
                               progress_color=BUTTON_COLOR, fg_color=FONT_COLOR, variable=heightint,
                               from_=100, to=250, command=self.updateheight)
        self.outputstr = ctk.StringVar()
        self.updateheight(heightint.get())
        slidertext = ctk.CTkLabel(self, text_color=FONT_COLOR, font=ctk.CTkFont(FONT, I_TEXT_SIZE, weight="bold"),
                                  textvariable=self.outputstr)
        slider.pack(side="left", expand=True, fill="x", padx=10)
        slidertext.pack(side="top", expand=True, fill="both", padx=10)
        self.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        
    def updateheight(self, heightint):
        # Update height display based on unit type
        if self.metricbool.get():
            meter = str(int(heightint))[0]
            centimeter  = str(int(heightint))[1:]
            self.outputstr.set(f"{meter}.{centimeter} m")
        else:
            feet, inches = divmod(heightint/2.54, 12)
            self.outputstr.set(f"{int(feet)}\'{int(inches)}\" ")
            
# Subclass for the UnitSwitch widget
class UnitSwitch(ctk.CTkLabel):
    def __init__(self, parent, metricbool):
        # Initialize the UnitSwitch widget
        super().__init__(master=parent, text="(metric)", text_color=HOVER_COLOR,
                         font=ctk.CTkFont(FONT, 15, weight="bold")) 
        self.place(relx=0.98, rely=0.01, anchor="ne")
        self.metricbool = metricbool
        self.bind("<Button>", self.changeunits)
        
    def changeunits(self, event):
        # Change the unit type based on button press
        self.metricbool.set(not self.metricbool.get())
        if self.metricbool.get():
            self.configure(text="(metric)")
        else:
            self.configure(text="(imperial)")

# Run the application if the script is executed directly
if __name__ == "__main__":
    App()
