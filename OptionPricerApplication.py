from tkinter import *
import tkinter.font as tkFont
from tkinter import scrolledtext

from BlackScholesOption import BlackScholesOption
from ImpliedVolatility import get_implied_volatility
from AmericanOption import AmericanOption
from GeometricAsianOption import GeometricAsianOption
from ArithmeticAsianOption import ArithmeticAsianOption
from GeometricBasketOption import GeometricBasketOption
from ArithmeticBasketOption import ArithmeticBasketOption
from KikoOption import KikoOption

class OptionPricerApplication:
    def __init__(self):
        self.window = Tk()
        self.window.title("Option Pricer")
        self.window.geometry('%dx%d' % (750, 500))
        self.menubar = Menu(self.window)
        self.window.config(menu=self.menubar)

        self.create_homemenu()
        self.create_modelmenu()

        self.frameHome = Frame(self.window)
        self.frame1 = Frame(self.window)
        self.frame2 = Frame(self.window)
        self.frame3 = Frame(self.window)
        self.frame4 = Frame(self.window)
        self.frame5 = Frame(self.window)
        self.frame6 = Frame(self.window)
        self.frame7 = Frame(self.window)
        self.frame8 = Frame(self.window) 

        self.create_homepage()
        # Display the homepage upon starting program
        self.load_homepage()

        self.window.mainloop()

    # Helper function to create the home menu
    def create_homemenu(self):
        homemenu = Menu(self.menubar, tearoff=0)
        homemenu.add_command(label = "Homepage",command = self.load_homepage)
        homemenu.add_command(label = "Quit", command = self.quit)
        self.menubar.add_cascade(label = "Option Pricer", menu = homemenu)

    # Helper function to create the menu for selecting pricing models
    def create_modelmenu(self):
        modelmenu = Menu(self.menubar, tearoff=0)
        modelmenu.add_command(label = "European Black Scholes", command = self.model_1)
        modelmenu.add_command(label = "Implied Volatility", command = self.model_2)
        modelmenu.add_command(label = "American Binomial Tree", command = self.model_3)
        modelmenu.add_command(label = "Geometric Asian - Closed Form", command = self.model_4)
        modelmenu.add_command(label = "Arithmetic Asian - Monte Carlo", command = self.model_5)
        modelmenu.add_command(label = "Geometric Basket - Closed Form", command = self.model_6)
        modelmenu.add_command(label = "Arithmetic Mean Basket - Monte Carlo", command = self.model_7)
        modelmenu.add_command(label = "KIKO Put - Quasi Monte Carlo", command = self.model_8)
        self.menubar.add_cascade(label = 'Select Pricing Model', menu = modelmenu)

    # Helper function to create the home page
    def create_homepage(self):
        Label(self.frameHome, text= "Option Pricer", font=tkFont.Font(weight='bold',size=50),height=6).pack()

    # Helper function to load Homepage
    def load_homepage(self):
        self.__forgetFrame()
        self.frameHome.pack()

    # Helper function for switching pages - forget the current page
    def __forgetFrame(self):
        self.frameHome.pack_forget()
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack_forget()
        self.frame6.pack_forget()
        self.frame7.pack_forget()
        self.frame8.pack_forget()

    # Helper function for closing the program
    def quit(self):
        self.window.destroy()

    '''
        MODEL 1 - Black Scholes Options Pricing Model (European)
    '''

    def model_1(self):
        # Load frame for model 1
        self.__forgetFrame()
        frame = self.frame1 
        frame.pack()

        # Parameters
        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.q = StringVar()
        self.type = StringVar()

        # Labels of the input widgets
        Label(frame, text = "Black Scholes Options Pricing Model (European)", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price (S)').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price (K)').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Volatility (sigma)').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate (r)').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years) (T)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Repo Rate (q)').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=8,column=1,sticky=W)

        # Widgets for input values for parameters
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.q).grid(row=7,column=2,sticky=W)
        Radiobutton(frame, text="Put",variable=self.type, value='put').grid(row=8, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.type, value='call').grid(row=8, column=2, sticky=W)

        # Reset button to clear input and results log
        Button(frame, width = 15, text = "Reset",command=self.reset_model_1).grid(row = 11, column = 2, columnspan = 1, sticky = E)
        
        # Run button to run the pricing model
        Button(frame, width = 15, text = "Calculate",command=self.run_model_1_pricer).grid(row = 10, column = 2, columnspan = 1, sticky = E)

        # text window to display results
        self.results = scrolledtext.ScrolledText(frame, width = 75, height = 10)
        self.results.grid(row = 13, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_model_1(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.q = 0
        self.model_1()
    
    def run_model_1_pricer(self):
        try:
            model = BlackScholesOption(S=float(self.S.get()),
                                    K=float(self.K.get()),
                                    T=float(self.T.get()),
                                    sigma=float(self.sigma.get()),
                                    r=float(self.r.get()),
                                    q=float(self.q.get()),
                                    cp_flag=self.type.get())
            result = model.get_price_european()
            self.results.insert(END, "[SUCCESS] Price: {}\n".format(result))
        except:       
            self.results.insert(END, "[ERROR] Please input the correct parameters\n")

    '''
        MODEL 2 - Implied Volatility Calculator
    '''

    def model_2(self):
        # Load frame for model 2
        self.__forgetFrame()
        frame = self.frame2
        frame.pack()

        # Parameters
        self.S = StringVar()
        self.K = StringVar()
        self.V = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.q = StringVar()
        self.type = StringVar()

        # Labels of the input widgets
        Label(frame, text = "Implied Volatility Calculator", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price (S)').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price (K)').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Option Premium (V)').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate (r)').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years) (T)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Repo Rate (q)').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=8,column=1,sticky=W)

        # Widgets for input values for parameters
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.V).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.q).grid(row=7,column=2,sticky=W)
        Radiobutton(frame, text="Put",variable=self.type, value='put').grid(row=8, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.type, value='call').grid(row=8, column=2, sticky=W)
        
        # Reset button to clear input and results log
        Button(frame, width = 15, text = "Reset",command=self.reset_model_2).grid(row = 11, column = 2, columnspan = 1, sticky = E)
        
        # Run button to run the pricing model
        Button(frame, width = 15, text = "Calculate",command=self.run_model_2_pricer).grid(row = 10, column = 2, columnspan = 1, sticky = E)

        # text window to display results
        self.results = scrolledtext.ScrolledText(frame, width = 75, height = 10)
        self.results.grid(row = 13, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_model_2(self):
        self.S = 0
        self.K = 0
        self.V = 0
        self.r = 0
        self.T = 0
        self.q = 0
        self.model_2()

    def run_model_2_pricer(self):
        try:
            # TO BE COMPLETED
            result = get_implied_volatility(S=float(self.S.get()),
                                            K=float(self.K.get()),
                                            V=float(self.V.get()),
                                            r=float(self.r.get()),
                                            T=float(self.T.get()),
                                            q=float(self.q.get()),
                                            option_type=self.type.get())
            self.results.insert(END, "[SUCCESS] Implied Volatility: {}\n".format(result))
        except:       
            self.results.insert(END, "[ERROR] Please input the correct parameters\n")
    
    '''
        MODEL 3 - Binomial Tree Options Pricing Model (American)
    '''

    def model_3(self):
        # Load frame for model 3
        self.__forgetFrame()
        frame = self.frame3
        frame.pack()

        # Parameters
        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.N = StringVar()
        self.type = StringVar()

        # Labels of the input widgets
        Label(frame, text = "Binomial Tree Options Pricing Model (American)", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price (S)').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price (K)').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Volatility (sigma)').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate (r)').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years) (T)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Number of Steps (N)').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=8,column=1,sticky=W)

        # Widgets for input values for parameters
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.N).grid(row=7,column=2,sticky=W)
        Radiobutton(frame, text="Put",variable=self.type, value='put').grid(row=8, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.type, value='call').grid(row=8, column=2, sticky=W)
        

        # Reset button to clear input and results log
        Button(frame, width = 15, text = "Reset",command=self.reset_model_3).grid(row = 11, column = 2, columnspan = 1, sticky = E)
        
        # Run button to run the pricing model
        Button(frame, width = 15, text = "Calculate",command=self.run_model_3_pricer).grid(row = 10, column = 2, columnspan = 1, sticky = E)

        # text window to display results
        self.results = scrolledtext.ScrolledText(frame, width = 75, height = 10)
        self.results.grid(row = 13, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_model_3(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.N = 0
        self.model_3()

    def run_model_3_pricer(self):                    
        try:
            model = AmericanOption(S=float(self.S.get()),
                                sigma=float(self.sigma.get()),
                                r=float(self.r.get()),
                                T=float(self.T.get()),
                                K=float(self.K.get()),
                                N=int(self.N.get()),
                                type=self.type.get())
            result = model.get_price_binomial_tree()
            self.results.insert(END, "[SUCCESS] Price: {}\n".format(result))
        except:       
            self.results.insert(END, "[ERROR] Please input the correct parameters\n")

    '''
        MODEL 4 - Geometric Asian Options Pricing Model (Closed Form)
    '''

    def model_4(self):
        # Load frame for model 4
        self.__forgetFrame()
        frame = self.frame4
        frame.pack()

        # Parameters
        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.n = StringVar()
        self.type = StringVar()

        # Labels of the input widgets
        Label(frame, text = "Geometric Asian Options Pricing Model (Closed Form)", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price (S)').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price (K)').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Volatility (sigma)').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate (r)').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years) (T)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Number of Observation Times (n)').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=8,column=1,sticky=W)

        # Widgets for input values for parameters
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.n).grid(row=7,column=2,sticky=W)
        Radiobutton(frame, text="Put",variable=self.type, value='put').grid(row=8, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.type, value='call').grid(row=8, column=2, sticky=W)
        

        # Reset button to clear input and results log
        Button(frame, width = 15, text = "Reset",command=self.reset_model_4).grid(row = 11, column = 2, columnspan = 1, sticky = E)
        
        # Run button to run the pricing model
        Button(frame, width = 15, text = "Calculate",command=self.run_model_4_pricer).grid(row = 10, column = 2, columnspan = 1, sticky = E)

        # text window to display results
        self.results = scrolledtext.ScrolledText(frame, width = 75, height = 10)
        self.results.grid(row = 13, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_model_4(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.n = 0
        self.model_4()

    def run_model_4_pricer(self):                    
        try:

            model = GeometricAsianOption(S=float(self.S.get()),
                                        K=float(self.K.get()),
                                        T=float(self.T.get()),
                                        sigma=float(self.sigma.get()),
                                        r=float(self.r.get()),
                                        n=float(self.n.get()),
                                        cp_flag=self.type.get())
            result = model.get_price_closed_form()
            self.results.insert(END, "[SUCCESS] Price: {}\n".format(result))
        except:       
            self.results.insert(END, "[ERROR] Please input the correct parameters\n")

    '''
        MODEL 5 - Arithmetic Asian Options Pricing Model (Monte Carlo)
    '''

    def model_5(self):
        # Load frame for model 5
        self.__forgetFrame()
        frame = self.frame5
        frame.pack()

        # Parameters
        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.n = StringVar()
        self.M = StringVar()
        self.control_variate = BooleanVar()
        self.type = StringVar()

        # Labels of the input widgets
        Label(frame, text = "Arithmetic Asian Options Pricing Model (Monte Carlo)", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price (S)').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price (K)').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Volatility (sigma)').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate (r)').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years) (T)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Number of Observation Times (n)').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Number of Paths (M)').grid(row=8,column=1,sticky=W)
        Label(frame, text= 'Use Control Variate?').grid(row=9,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=10,column=1,sticky=W)

        # Widgets for input values for parameters
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.n).grid(row=7,column=2,sticky=W)
        Entry(frame, textvariable=self.M).grid(row=8,column=2,sticky=W)
        Checkbutton(frame, text="", variable=self.control_variate).grid(row=9, column=2, sticky=W)
        Radiobutton(frame, text="Put",variable=self.type, value='put').grid(row=10, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.type, value='call').grid(row=10, column=2, sticky=W)

        # Reset button to clear input and results log
        Button(frame, width = 15, text = "Reset",command=self.reset_model_5).grid(row = 13, column = 2, columnspan = 1, sticky = E)
        
        # Run button to run the pricing model
        Button(frame, width = 15, text = "Calculate",command=self.run_model_5_pricer).grid(row = 12, column = 2, columnspan = 1, sticky = E)

        # text window to display results
        self.results = scrolledtext.ScrolledText(frame, width = 75, height = 10)
        self.results.grid(row = 15, column = 1, rowspan = 4, columnspan = 2, sticky = W)
    
    def reset_model_5(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.n = 0
        self.M = 0
        self.model_5()

    def run_model_5_pricer(self):
        try:
            model = ArithmeticAsianOption(S=float(self.S.get()),
                                        K=float(self.K.get()),
                                        T=float(self.T.get()),
                                        sigma=float(self.sigma.get()),
                                        r=float(self.r.get()),
                                        n=int(self.n.get()),
                                        M=int(self.M.get()),
                                        control_variate=self.control_variate.get(),
                                        cp_flag=self.type.get())
            result = model.get_price_monte_carlo()
            self.results.insert(END, "[SUCCESS] Price: {}\n".format(result[0]))
            self.results.insert(END, "[SUCCESS] 95% Confidence Interval: {}\n".format(result[1]))
        except:       
            self.results.insert(END, "[ERROR] Please input the correct parameters\n")


    '''
        MODEL 6 - Geometric Basket Options Pricing Model (Closed Form)
    '''

    def model_6(self):
        # Load frame for model 6
        self.__forgetFrame()
        frame = self.frame6
        frame.pack()

        # Parameters
        self.S1 = StringVar()
        self.S2 = StringVar()
        self.K = StringVar()
        self.sigma1 = StringVar()
        self.sigma2 = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.corr = StringVar()
        self.type = StringVar()

        # Labels of the input widgets
        Label(frame, text = "Geometric Basket Options Pricing Model (Closed Form)", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price of 1st Asset (S1)').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Spot Price of 2nd Asset (S2)').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Strike Price (K)').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Volatility of 1st Asset (sigma1)').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Volatility of 2nd Asset (sigma2)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate (r)').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years) (T)').grid(row=8,column=1,sticky=W)
        Label(frame, text= 'Correlation (corr)').grid(row=9,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=10,column=1,sticky=W)

        # Widgets for input values for parameters
        Entry(frame, textvariable=self.S1).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.S2).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma1).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma2).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=7,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=8,column=2,sticky=W)
        Entry(frame, textvariable=self.corr).grid(row=9,column=2,sticky=W)
        Radiobutton(frame, text="Put",variable=self.type, value='put').grid(row=10, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.type, value='call').grid(row=10, column=2, sticky=W)

        # Reset button to clear input and results log
        Button(frame, width = 15, text = "Reset",command=self.reset_model_6).grid(row = 13, column = 2, columnspan = 1, sticky = E)
        
        # Run button to run the pricing model
        Button(frame, width = 15, text = "Calculate",command=self.run_model_6_pricer).grid(row = 12, column = 2, columnspan = 1, sticky = E)

        # text window to display results
        self.results = scrolledtext.ScrolledText(frame, width = 75, height = 10)
        self.results.grid(row = 15, column = 1, rowspan = 4, columnspan = 2, sticky = W)
    
    def reset_model_6(self):
        self.S1 = 0
        self.S2 = 0
        self.K = 0
        self.sigma1 = 0
        self.sigma2 = 0
        self.r = 0
        self.T = 0
        self.corr = 0
        self.model_6()

    def run_model_6_pricer(self):
        try:
            model = GeometricBasketOption(S=[float(self.S1.get()),float(self.S2.get())],
                                        K=float(self.K.get()),
                                        T=float(self.T.get()),
                                        sigma=[float(self.sigma1.get()),float(self.sigma2.get())],
                                        r=float(self.r.get()),
                                        corr=float(self.corr.get()),
                                        cp_flag=self.type.get())
            result = model.get_price_closed_form()
            self.results.insert(END, "[SUCCESS] Price: {}\n".format(result))
        except:       
            self.results.insert(END, "[ERROR] Please input the correct parameters\n")

    '''
        MODEL 7 - Arithmetic Basket Options Pricing Model (Monte Carlo)
    '''

    def model_7(self):
        # Load frame for model 7
        self.__forgetFrame()
        frame = self.frame7
        frame.pack()

        # Parameters
        self.S1 = StringVar()
        self.S2 = StringVar()
        self.K = StringVar()
        self.sigma1 = StringVar()
        self.sigma2 = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.corr = StringVar()
        self.M = StringVar()
        self.control_variate = BooleanVar()
        self.type = StringVar()

        # Labels of the input widgets
        Label(frame, text = "Arithmetic Basket Options Pricing Model (Monte Carlo)", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price of 1st Asset (S1)').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Spot Price of 2nd Asset (S2)').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Strike Price (K)').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Volatility of 1st Asset (sigma1)').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Volatility of 2nd Asset (sigma2)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate (r)').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years) (T)').grid(row=8,column=1,sticky=W)
        Label(frame, text= 'Correlation (corr)').grid(row=9,column=1,sticky=W)
        Label(frame, text= 'Number of Paths (M)').grid(row=10,column=1,sticky=W)
        Label(frame, text= 'Use Control Variate?').grid(row=11,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=12,column=1,sticky=W)

        # Widgets for input values for parameters
        Entry(frame, textvariable=self.S1).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.S2).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma1).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma2).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=7,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=8,column=2,sticky=W)
        Entry(frame, textvariable=self.corr).grid(row=9,column=2,sticky=W)
        Entry(frame, textvariable=self.M).grid(row=10,column=2,sticky=W)
        Checkbutton(frame, text="", variable=self.control_variate).grid(row=11, column=2, sticky=W)
        Radiobutton(frame, text="Put",variable=self.type, value='put').grid(row=12, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.type, value='call').grid(row=12, column=2, sticky=W)

        # Reset button to clear input and results log
        Button(frame, width = 15, text = "Reset",command=self.reset_model_7).grid(row = 15, column = 2, columnspan = 1, sticky = E)
        
        # Run button to run the pricing model
        Button(frame, width = 15, text = "Calculate",command=self.run_model_7_pricer).grid(row = 14, column = 2, columnspan = 1, sticky = E)

        # text window to display results
        self.results = scrolledtext.ScrolledText(frame, width = 75, height = 10)
        self.results.grid(row = 17, column = 1, rowspan = 4, columnspan = 2, sticky = W)
    
    def reset_model_7(self):
        self.S1 = 0
        self.S2 = 0
        self.K = 0
        self.sigma1 = 0
        self.sigma2 = 0
        self.r = 0
        self.T = 0
        self.corr = 0
        self.M = 0
        self.model_7()

    def run_model_7_pricer(self):
        try:
            model = ArithmeticBasketOption(r=float(self.r.get()),
                                        sigma1=float(self.sigma1.get()),
                                        sigma2=float(self.sigma2.get()),
                                        T=float(self.T.get()),
                                        S10=float(self.S1.get()),
                                        S20=float(self.S2.get()),
                                        K=float(self.K.get()),
                                        rho=float(self.corr.get()),
                                        M=int(self.M.get()),
                                        option_type=self.type.get(),
                                        control_variate=self.control_variate.get())
            result = model.get_price_monte_carlo()
            self.results.insert(END, "[SUCCESS] Price: {}\n".format(result[0]))
            self.results.insert(END, "[SUCCESS] 95% Confidence Interval: {}\n".format(result[1]))
        except:       
            self.results.insert(END, "[ERROR] Please input the correct parameters\n")

    '''
        MODEL 8 - KIKO Put Option Pricing Model (Quasi-Monte Carlo)
    '''

    def model_8(self):
        # Load frame for model 8
        self.__forgetFrame()
        frame = self.frame8
        frame.pack()

        # Parameters
        self.S = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.K = StringVar()
        self.L = StringVar()
        self.U = StringVar()
        self.n = StringVar()
        self.R = StringVar()

        # Labels of the input widgets
        Label(frame, text = "KIKO Put Option Pricing Model (Quasi-Monte Carlo)", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price (S)').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price (K)').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Volatility (sigma)').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate (r)').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years) (T)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Lower Bound (L)').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Upper Bound (U)').grid(row=8,column=1,sticky=W)
        Label(frame, text= 'Number of Observation times (n)').grid(row=9,column=1,sticky=W)
        Label(frame, text= 'Cash Rebate (R)').grid(row=10,column=1,sticky=W)

        # Widgets for input values for parameters
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.L).grid(row=7,column=2,sticky=W)
        Entry(frame, textvariable=self.U).grid(row=8,column=2,sticky=W)
        Entry(frame, textvariable=self.n).grid(row=9,column=2,sticky=W)
        Entry(frame, textvariable=self.R).grid(row=10,column=2,sticky=W)

        # Reset button to clear input and results log
        Button(frame, width = 15, text = "Reset",command=self.reset_model_8).grid(row = 13, column = 2, columnspan = 1, sticky = E)
        
        # Run button to run the pricing model
        Button(frame, width = 15, text = "Calculate",command=self.run_model_8_pricer).grid(row = 12, column = 2, columnspan = 1, sticky = E)

        # text window to display results
        self.results = scrolledtext.ScrolledText(frame, width = 75, height = 10)
        self.results.grid(row = 15, column = 1, rowspan = 4, columnspan = 2, sticky = W)
    
    def reset_model_8(self):
        self.S = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.K = 0
        self.L = 0
        self.U = 0
        self.n = 0
        self.R = 0
        self.model_8()

    def run_model_8_pricer(self):
        try:
            model = KikoOption(S=float(self.S.get()),
                            sigma=float(self.sigma.get()),
                            r=float(self.r.get()),
                            T=float(self.T.get()),
                            K=float(self.K.get()),
                            L=float(self.L.get()),
                            U=float(self.U.get()),
                            n=int(self.n.get()),
                            R=float(self.R.get()))
            result = model.get_price_quasi_monte_carlo()
            self.results.insert(END, "[SUCCESS] Price: {}\n".format(result[0]))
            self.results.insert(END, "[SUCCESS] 95% Confidence Interval: {}\n".format(result[1]))
        except:       
            self.results.insert(END, "[ERROR] Please input the correct parameters\n")

# if __name__ == "main":
#     Application()

OptionPricerApplication()