from shiny import App, render, ui, reactive
import pandas as pd
import numpy as np
import plotly.express as px
from statsmodels.stats.weightstats import ztest
from scipy import stats
from sklearn.model_selection import train_test_split
import pymongo

client = pymongo.MongoClient("mongodb+srv://dftML:dftML@stano.mez9zwp.mongodb.net/?retryWrites=true&w=majority")
database = client["EDA"]
collection = database["Data_Upload"]


app_ui = ui.page_fluid(
    ui.tags.style(
        """.app1{border: 3px solid black;border-radius: 10px;background-color: #adff2f;padding: 12px;margin-top: 1px;margin-bottom: 5px;}"""
        """.app2{border: 3px solid black;border-radius: 10px;background-color: #b0c4de;padding: 12px;margin-top: 1px;margin-bottom: 5px;}"""
        
        
        """.app3{border: 2px solid black;border-radius: 10px;background-color: #6cda7f;padding: 12px;margin-top: 1px;margin-bottom: 5px;}"""
        """.app4{border: 2px solid black;border-radius: 10px;background-color: #ffcf74;padding: 12px;margin-top: 1px;margin-bottom: 5px;}"""

        """.test1{border: 2px solid black;border-radius: 10px;background-color: #e6e6fa;padding: 12px;margin-top: 0px;margin-bottom: 0px;}"""
        """.test2{border: 2px solid black;border-radius: 10px;background-color: #98fb98;padding: 12px;margin-top: 0px;margin-bottom: 0px;}"""
        """.test3{border: 2px solid black;border-radius: 10px;background-color: #fafad2;padding: 12px;margin-top: 0px;margin-bottom: 0px;}"""
        """.test4{border: 2px solid black;border-radius: 10px;background-color: #fffafa;padding: 12px;margin-top: 0px;margin-bottom: 0px;}"""
        """.test5{border: 2px solid black;border-radius: 10px;background-color: #e0ffff;padding: 12px;margin-top: 0px;margin-bottom: 0px;}"""
        
        """.t1{border: 1px solid black;border-radius: 10px;background-color: #ffa500;padding: 12px;margin-top: 1px;margin-bottom: 10px;}"""
        """.t2{border: 1px solid black;border-radius: 10px;background-color: #ff7f50;padding: 12px;margin-top: 1px;margin-bottom: 10px;}"""
        """.t3{border: 1px solid black;border-radius: 10px;background-color: #FF00FF;padding: 12px;margin-top: 1px;margin-bottom: 10px;}"""
        
        """.g1{border: 2px solid black;border-radius: 10px;background-color: #e6e6fa;padding: 12px;margin-top: 1px;margin-bottom: 5px;}"""
        """.g2{border: 2px solid black;border-radius: 10px;background-color: #e6e6fa;padding: 12px;margin-top: 1px;margin-bottom: 5px;}"""
        """.g3{border: 2px solid black;border-radius: 10px;background-color: #e6e6fa;padding: 12px;margin-top: 1px;margin-bottom: 10px;}"""
        """.g5{border: 2px solid black;border-radius: 10px;background-color: #fafad2;padding: 12px;margin-top: 10px;margin-bottom: 5px;}"""
        """.g6{border: 2px solid black;border-radius: 10px;background-color: #fafad2;padding: 12px;margin-top: 1px;margin-bottom: 10px;}"""
        """.g8{border: 2px solid black;border-radius: 10px;background-color: #fffafa;padding: 12px;margin-top: 10px;margin-bottom: 5px;}"""
        """.g9{border: 2px solid black;border-radius: 10px;background-color: #fffafa;padding: 12px;margin-top: 1px;margin-bottom: 5px;}"""
        """.g10{border: 2px solid black;border-radius: 10px;background-color: #e0ffff;padding: 12px;margin-top: 1px;margin-bottom: 10px;}"""
        """.g11{border: 2px solid black;border-radius: 10px;background-color: #98fb98;padding: 12px;margin-top: 1px;margin-bottom: 5px;}"""
        """.g12{border: 2px solid black;border-radius: 10px;background-color: #98fb98;padding: 12px;margin-top: 1px;margin-bottom: 5px;}"""

    ),
    
    ui.h1({"style": "text-align: center;"}, "Exploratory Data Analysis"),
    
    ui.row(
        ui.column(2),
        
        
        ui.column(4,ui.div({"class": "app1"},
            ui.p(ui.input_select("x0","Select Tools", 
                choices=["None", "Categorical", "Continuous", "Statistics Tests", 
                         "Histogram", "Bar Plot", "Scatter Plot", "Line Plot", "Box Plot"]),
                ui.input_action_button("btn", "Click here")),
            ui.p(ui.input_checkbox("xw","Show Complete Table (if None)")
                ))),
          
        ui.column(4,ui.div({"class": "app2"},
            ui.p(ui.input_file("file1", "Choose a csv file to upload:"),
                 ui.input_text("file2", "Mention the Separator (\" \")", value='","'),
                 ui.input_checkbox("file3","Upload")),
            ui.p("""*Please ensure that the separator is not included in the values."""),
            ui.p("""*Tips : If it occurs, convert it into a different separator and upload it.""")
                          )),
        ui.column(2)),
    
    ui.row(ui.column(12,ui.div({"class": "app-col"},
            ui.p(
                ui.output_ui("different_ui"),
                ui.output_table("All_table")))))
)


def server(input, output, session):
    @reactive.Effect
    @reactive.event(input.btn)
    def _():
        print(f"You have click the button and choose data type")

    def uploads():
        file_obj = input.file1()                  # 
        if not file_obj:
            return
        # Multiple files file_obj is a list of dicts; 
        # each dict represents one file. Example:
        # [{'name': 'data.csv','size': 2601,'type': 'text/csv','datapath': '/tmp/fileupload-1wnx_7c2/tmpga4x9mps/0.csv'}]
        out_str = ""
        with open(file_obj[0]["datapath"], "r") as f1:
            out_str = out_str + (f1.read())
            out_str = out_str.split("\n")
        lists1 = []
        for rows in out_str:
            lists1.append(rows.split(eval(input.file2())))
        
        lists3 = []
        for row in lists1:
            lists2 = []
            for element in row:                                 
                try:                                                               # evaluate of string comes as a variable undefined
                    if isinstance(eval(element), float):
                        lists2.append(float(element))
                        
                    if isinstance(eval(element), int):
                        lists2.append(int(element))
                except:                                                            # program crashes due to which incude in except block
                    lists2.append(str(element))
            
            lists3.append(lists2)

        lists4 = []
        for rows in range(len(lists3)-2):                                           #last row is empty strings -1    
            lists4.append(dict(zip(lists3[0],lists3[rows+1])))                      #1st row is columns -1 
        
        collection.drop()
        collection.insert_many(lists4)
    
    
    
    @output
    @render.table()
    def All_table():
        d1 = uploads()
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]   # 1st columns gives _id
        if input.x0() == "None" and input.file3() == True:
            if input.xw() == True:
                if "Index" == df.columns[0]:                  
                     return df                                  # Repeatedly Show Table insert many times index columns
                df.insert(0,"Index",range(len(df)))
                return df                                       # Show Table insert index columns
            return df.head(50)


    
    @output
    @render.ui()
    @reactive.event(input.btn)
    def different_ui():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        
        #Table Visualization Kits
        t1 = ui.row(
                    ui.column(2),
                    ui.column(3,ui.div({"class": "t1"},
                            ui.p(
                                ui.input_checkbox("unit8a", "Continuous Columns Visualization")))),
                    ui.column(3,ui.div({"class": "t2"},
                            ui.p(
                                ui.input_checkbox("unit8b", "Categorical Columns Visualization")))),
                    ui.column(3,ui.div({"class": "t3"},
                                   ui.p(
                                ui.input_checkbox("unit8c", "Complete Columns Visualization")))),
                    ui.column(1)),
        t2 = ui.row(ui.column(2),
                    ui.column(3,ui.panel_well(
                                ui.input_radio_buttons("unit9", "Row Indexing", choices={"Head":"Head (starting)","Tail" : "Tail (ending)"}),
                                ui.input_numeric("unit10","Number of rows",value=5, min=-len(df), max=len(df)))))
        t3 = ui.row(ui.column(1),
                    ui.column(11,ui.div({"class": "app-col"},
                                   ui.p(ui.output_table("Table")))))
        #Graph Visualization Schema
        g1 = ui.row(
                    ui.column(2),
                    ui.column(4,ui.div({"class": "g1"},
                            ui.p(ui.input_select("h1", "Select the x-axis",choices=["None"]+l0)))),
                    ui.column(4,ui.div({"class": "g1"},
                            ui.p(ui.input_select("h2", "Select the y-axis",choices=["None"]+l0)))),
                   ui.column(2)),
        
        g2 = ui.row(
                    ui.column(2),
                    ui.column(4,ui.div({"class": "g2"},
                            ui.p(
                                ui.input_checkbox("h5rx","Range of x-axis (float values)"),
                                ui.input_text("h5ax", "Lowest value", value="None"),
                                ui.input_text("h5bx", "Highest Value", value="None"),
                                ui.input_checkbox("h6lx","Log Scaling"),
                                ui.input_radio_buttons("h6x", "x-axis",choices=["False","True"])))),
                    ui.column(4,ui.div({"class": "g2"},
                            ui.p(
                                ui.input_checkbox("h5ry","Range of y-axis (float values)"),
                                ui.input_text("h5ay", "Lowest Value", value="None"),
                                ui.input_text("h5by", "Highest Value", value="None"),
                                ui.input_checkbox("h6ly","Log Scaling"),
                                ui.input_radio_buttons("h6y", "y-axis",choices=["False","True"])))),
                    ui.column(2)),
        g3 = ui.row(
                    ui.column(2),
                    ui.column(4,ui.div({"class": "g3"},
                            ui.p(ui.input_numeric("h7x","Width (in pixels)",step=25,value=1000)))),
                    ui.column(4,ui.div({"class": "g3"},
                            ui.p(ui.input_numeric("h7y","Height (in pixels)",step=25,value=500)))),
                    ui.column(2)),
        
        g4 = ui.row(ui.column(2),
                    ui.column(8,ui.panel_well(
            ui.h6({"style": "text-align: left;"}, 
                  """For single group, choose a colour, and for multiple groups or third columns, choose None (by default:Colour distribution)"""
                 ))),
                   ui.column(2)),
        
        g5 = ui.row(ui.column(2),
                    ui.column(4,ui.div({"class": "g5"},
                            ui.p(ui.input_select("h11","Colour of Plot",choices=["None"]+l5)))),
                    ui.column(4,ui.div({"class": "g5"},
                            ui.p(ui.input_select("h8", "Select the 3rd-Columns(Color)", choices=["None"]+l0)))),
                   ui.column(2)),
        
        g6 = ui.row(
                    ui.column(2),
                    ui.column(4,ui.div({"class": "g6"},
                            ui.p(
                                """Orientations""",
                                ui.input_radio_buttons("h10","when x & y both provided", choices={"v": "Vertical (y : continuous)","h": "Horizontal (y : categorical)"})
                            ))),
                    ui.column(4,ui.div({"class": "g6"},
                            ui.p(ui.input_select("h3b","Plotting Pattern", choices=['', 'x','/', '\\','-', '|', '+', '.'])))),
                    ui.column(2)),
        
        g7 = ui.row(
                    ui.column(2),
                    ui.column(8,ui.panel_well(
            ui.h6({"style": "text-align: left;"},
                  """Multiple Plotting based on different unique categories of groups"""
                 ))),
                    ui.column(2)),
        
        #opacity with no. of columns
        g8 = ui.row(
                ui.column(2),
                ui.column(4,ui.div({"class": "g8"},
                            ui.p(ui.input_select("h3","Multiple Rows",choices=["None"]+l0),
                                ui.input_slider("h3a","Rows Plot Spacing",min=0.0,max=1.0,step=0.01,value=0.04),
                                ui.input_slider("h9","Opacity",min=0,max=1.0,step=0.01,value=1.0,)))),
                       
                ui.column(4,ui.div({"class": "g8"},
                            ui.p(ui.input_select("h4","Multiple Columns",choices=["None"]+l0),
                                ui.input_slider("h4a","Columns Plot Spacing",min=0.0,max=1.0,step=0.01,value=0.04),
                                ui.input_numeric("h4b","Number of columns in a row (default:0)",min=0,value=0,step=1)))),
                ui.column(2)),
        
        
        g9 = ui.row(
                    ui.column(2),
                    ui.column(4,ui.div({"class": "g9"},
                            ui.p(ui.input_select("h3c","Animation Frame",choices=["None"]+l0)))),
                    ui.column(4,ui.div({"class": "g9"},
                            ui.p(ui.input_select("h4c","Animation Group",choices=["None"]+l0)))),
                    ui.column(2)),
        
        g10 = ui.row(
                    ui.column(2),
                    ui.column(4,ui.div({"class": "g10"},
                            ui.p(ui.input_text("h3d","Title",value="None")))),
                    ui.column(4,ui.div({"class": "g10"},
                            ui.p(ui.input_text("h4d","Labels { 'Previous' : 'New' }",value="None")))),
                    ui.column(2))
        
        g11 = ui.row(
                    ui.column(2),
                    ui.column(4,ui.div({"class": "g11"},
                            ui.p(ui.input_select("h3e","Select the 4th-Columns (Symbol)",choices=["None"]+l0)))),
                    ui.column(4,ui.div({"class": "g11"},
                            ui.p(ui.input_numeric("h4e","Point Pattern (Symbol)",value=0)))),
                    ui.column(2))
        
        g12 = ui.row(ui.column(2),
                    ui.column(4,ui.div({"class": "g12"},
                            ui.p(ui.input_select("h3f","Select the 5th-Columns (Size)",choices=["None"]+l0)))),
                    ui.column(4,ui.div({"class": "g12"},
                            ui.p(ui.input_numeric("h4f","Point Size (Size)",value=20)))),
                    ui.column(2))
        
        
        # Categorical
        if input.x0() == "Categorical":
            return ui.page_fluid(
                ui.h2({"style": "text-align: center;"}, "Feature Analysis Tools"),
                ui.row(
                    ui.column(2),
                    ui.column(6,ui.div({"class": "app3"},
                            ui.p(ui.TagList(
                                ui.input_select("col1", "Select Object Columns", choices=l2),
                                ui.input_checkbox("unit1", "Column Value Analysis"),
                                ui.input_radio_buttons("unit2", "", 
                                choices=["Missing Values %", "Mode", "No. Unique Values", "Distinct Value", "Length", "Rows", "Columns"]),
                                ui.output_text_verbatim("Categ_Info"),)))),
                    ui.column(2,ui.div({"class": "app-col"},
                            ui.p(ui.TagList(
                                # Values Counts
                                ui.input_checkbox("unit7", "Frequency of Value"),
                                ui.output_table("Conti_freq"))))),
                    ui.column(2),
                ),t1,t2,t3)
            
        # Continuous
        if input.x0() == "Continuous":
            return ui.page_fluid(
                ui.h2({"style": "text-align: center;"}, "Feature Analysis Tools"),
                ui.row(
                    ui.column(2),
                    ui.column(6,ui.div({"class": "app4"},
                            ui.p(ui.TagList(
                                ui.input_select("col1", "Select Numeric Columns", choices=l1),
                                ui.input_checkbox("unit1", "Statistical Analysis"),
                                ui.input_radio_buttons("unit2", "", 
                                choices=["Minimum","Maximum","Range","Mean","Mode","Median","Variance","Standard Deviation",]),
                                ui.output_text_verbatim("Conti_Info"),
                                # percentile
                                ui.input_checkbox("unit3", "Percentile"),
                                ui.input_slider("unit4", "Select Percentage", min=0, max=100, value=50, step=1),
                                ui.output_text_verbatim("Conti_Perc"),
                                ui.input_checkbox("unit5", "Column Value Analysis"),
                                ui.input_radio_buttons("unit6", "", choices=["Missing Values %", "No. Unique Values", "Distinct Value","Length", "Rows", "Columns"]),
                                ui.output_text_verbatim("Conti_Ana"))))),
                    ui.column(2,ui.div({"class": "app-col"},
                            ui.p(ui.TagList(
                                # Values Counts
                                ui.input_checkbox("unit7", "Frequency of Value"),
                                ui.output_table("Conti_freq"))))),
                    ui.column(2)),t1,t2,t3)
        #Histogram
        if input.x0() == "Histogram":
            return ui.page_fluid(ui.h2({"style": "text-align: center;"}, "Histogram Features Selection"),
                                 
                                 ui.row(ui.column(9),
                                     ui.column(3,ui.div({"class": "app-col"},
                                                           ui.p(
                                                               ui.input_action_button("btnhist","Click Plot"))))),
                                 g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,
                                 t1,t2,t3,ui.output_plot("hist")
                                )

        #Bar Plot
        if input.x0() == "Bar Plot":
            return ui.page_fluid(ui.h2({"style": "text-align: center;"}, "Bar-Plot Features Selection"),
                                 
                                 ui.row(ui.column(9),
                                     ui.column(3,ui.div({"class": "app-col"},
                                                           ui.p(
                                                               ui.input_action_button("btnbar","Click Plot"))))),
                                 g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,
                                 t1,t2,t3,ui.output_plot("barplot")
                                )
      
        #Scatter Plot
        if input.x0() == "Scatter Plot":
            return ui.page_fluid(ui.h2({"style": "text-align: center;"}, "Scatter-Plot Features Selection"),
                                
                                 ui.row(ui.column(9),
                                     ui.column(3,ui.div({"class": "app-col"},
                                                           ui.p(
                                                               ui.input_action_button("btnscatter","Click Plot"))))),
                                  g1,g2,g3,g4,g5,g11,g12,g7,g8,g9,g10,
                                 t1,t2,t3,ui.output_plot("scatterplot")
                                )
        #Line Plot
        if input.x0() == "Line Plot":
            return ui.page_fluid(ui.h2({"style": "text-align: center;"}, "Line-Plot Features Selection"),
                                            
                                 ui.row(ui.column(9),
                                     ui.column(3,ui.div({"class": "app-col"},
                                                           ui.p(
                                                               ui.input_action_button("btnline","Click Plot"))))),
                                 g1,g2,g3,g4,g5,g6,g11,g7,g8,g9,g10,  
                                 t1,t2,t3,ui.output_plot("lineplot")
                                )
      
        #Box Plot
        if input.x0() == "Box Plot":
            return ui.page_fluid(ui.h2({"style": "text-align: center;"}, "Box-Plot Features Selection"),
                                           
                                 ui.row(ui.column(9),
                                     ui.column(3,ui.div({"class": "app-col"},
                                                           ui.p(
                                                               ui.input_action_button("btnbox","Click Plot"))))),
                                 g1,g2,g3,g4,g5,g6,g7,g8,g9,g10,   
                                 t1,t2,t3,ui.output_plot("boxplot")
                                )
       
            
        #Statistics test
        if input.x0() == "Statistics Tests":
            return ui.page_fluid(
                ui.h2({"style": "text-align: center;"}, "Tests Tools"),
                ui.row(
                    ui.column(2),
                    ui.column(4,ui.div({"class": "test1"},
                            ui.p(
                                ui.input_checkbox("test2", "Correlation"),
                                ui.input_radio_buttons("test3","Methods",choices=['pearson', 'kendall', 'spearman'],inline=True)
                            ))),
                    ui.column(4,ui.div({"class": "test1"},
                            ui.p(
                                ui.input_checkbox("test1", "Covariance")))),
                    ui.column(2)),
                
                ui.row(
                    ui.column(9),
                    ui.column(3,ui.div({"class": "app-col"},
                            ui.p(ui.input_action_button("test4","Click Test"))))),
                
                ui.row(
                    ui.column(1),
                    ui.column(11,ui.div({"class": "app-col"},
                            ui.p(ui.output_table("Stat_Test"))))),

                ui.row(
                    ui.column(2),
                    ui.column(4,ui.div({"class": "test2"},
                            ui.p(ui.input_checkbox("test1a", "Numeric Columns Summarize")))),
                    ui.column(4,ui.div({"class": "test2"},
                            ui.p(""" """),
                            ui.p(ui.input_checkbox("test2a", "Object Columns Summarize")))),
                    ui.column(2)),
                
                ui.row(
                    ui.column(9),
                    ui.column(3,ui.div({"class": "app-col"},
                            ui.p(ui.input_action_button("test3a","Click Test"))))),
                
                ui.row(
                    ui.column(1),
                    ui.column(11,ui.div({"class": "app-col"},
                            ui.p(ui.output_table("Summary"))))),
                
                
                #### Z-test ####
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "test3"},
                            ui.p(
                                ui.input_checkbox("test5", "Z-test"),
                                ui.input_radio_buttons("test5a","Select Array 1D or 2D",choices={"1":"One Column","2":"Two Columns"}),
                                ui.output_ui("Choice1a")),
                            ui.p("Null Hypothesis H0"),
                            ui.p("Single 1D: Sample mean & Population mean of feature are equal & same"),
                            ui.p("Double 2D : 1st feature mean & 2nd feature mean are equal & same"))),
                    ui.column(2)),
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "test3"},
                            ui.p("""Z-test can only be used if the population standard deviation is known and the sample size is 30 data points or larger.""",
                                ui.input_radio_buttons("test5b","Sample Selection",choices=["Random","Train-Test","Starting","Ending","Range"],inline=True),
                                ui.output_ui("Choice2a")))),
                ui.column(2)),

                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "test3"},
                            ui.p(
                            ui.input_radio_buttons("test5c","Alternate Hypthesis H1",choices=["two-sided","larger","smaller"],inline=True),
                            ui.p("* 'two-sided' : H1: 1D (Sample mean not equal to Population mean) & 2D(1st feature not equal to 2nd feature)")),
                            ui.p("* 'larger'    : H1: 1D (Sample mean larger than Population mean) & 2D(1st feature larger than 2nd feature)"),
                            ui.p("* 'smaller'   : H1: 1D (Sample mean smaller than Population mean) & 2D(1st feature larger than 2nd feature)"),
                            ui.p("* Z-test gives P-value on the basis of Null Hypothesis H0 (which is opposite statements of Alternate Hypothesis H1) "),
                            ui.p(" if P-value < significant value(alpha) Reject Null Hypothesis (H0) accepts Alternate Hypothesis (H1)"),
                            ui.p(" if P-value >= significant value(alpha) Fail to Reject Null Hypothesis (H0) accepts Null Hypothesis (H0)"),
                            ui.p(" Don't select the missing columns(NAN) and Z-test performs only in numeric columns"))),
                    ui.column(2)),
                
                ui.row(
                    ui.column(9),
                    ui.column(3,ui.div({"class": "app-col"},
                            ui.p(ui.input_action_button("btn5","Click Z-test")))),
                    ),
                
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "app-col"},
                            ui.p(ui.output_table("ztest_table")))),
                    ui.column(2)),
                
                #### T-test ####
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "test4"},
                            ui.p(
                                ui.input_checkbox("test6", "T-test"),
                                ui.input_radio_buttons("test6a","Select Array 1D or 2D",choices={"1":"One Column","2":"Two Columns"}),
                                ui.output_ui("Choice1b")),
                            ui.p("Null Hypothesis H0"),
                            ui.p("Single 1D: Sample mean & Population mean of feature are equal & same"),
                            ui.p("Double 2D : 1st feature mean & 2nd feature mean are equal & same"))),
                    ui.column(2)),
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "test4"},
                            ui.p("T-test can only be used if the population standard deviation is unknown and the sample size is less than 30."),
                            ui.p("If the size of the sample is more than 30, then the distribution of the t-test and the normal distribution will not be distinguishable."),
                            ui.p(
                                ui.input_radio_buttons("test6b","Sample Selection",choices=["Random","Train-Test","Starting","Ending","Range"],inline=True),
                                ui.output_ui("Choice2b")))),
                    ui.column(2)),

                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "test4"},
                            ui.p(
                            ui.input_radio_buttons("test6c","Alternate Hypthesis H1",choices=["two-sided", "greater","less"],inline=True),
                            ui.p("* 'two-sided' : H1: 1D (Sample mean not equal to Population mean) & 2D(1st feature not equal to 2nd feature)")),
                            ui.p("* 'greater'   : H1: 1D (Sample mean greater than Population mean) & 2D(1st feature greater than 2nd feature)"),
                            ui.p("* 'less'     : H1: 1D (Sample mean less than Population mean) & 2D(1st feature less than 2nd feature)"),
                            ui.p("* T-test gives P-value on the basis of Null Hypothesis H0 (which is opposite statements of Alternate Hypothesis H1) "),
                            ui.p(" if P-value < significant value(alpha) Reject Null Hypothesis (H0) accepts Alternate Hypothesis (H1)"),
                            ui.p(" if P-value >= significant value(alpha) Fail to Reject Null Hypothesis (H0) accepts Null Hypothesis (H0)"),
                            ui.p(" Don't select the missing columns(NAN) and T-test performs only in numeric columns"))),
                ui.column(2)),
                
                ui.row(
                    ui.column(9),
                    ui.column(3,ui.div({"class": "app-col"},
                            ui.p(ui.input_action_button("btn6","Click T-test"))))),
                
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "app-col"},
                            ui.p(ui.output_table("ttest_table")))),
                    ui.column(2)),

                #### chi2-test ####
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "test5"},
                            ui.p(
                                ui.input_checkbox("test7", "Chi Squared (chi2) -test"),
                                ui.input_radio_buttons("test7a","Select Array 1D or 2D",choices={"1":"One Column","2":"Two Columns"}),
                                ui.output_ui("Choice1c")),
                            
                            ui.p("Null Hypothesis H0"),
                            ui.p("""Single 1D: Observed frequency & Expected frequency of feature are equal it means
                            there is a relationships between feature counts"""),
                            ui.p("""Double 2D : Observed frequency & Expected frequency of 1st feature & 2nd feature are equal 
                            it means there is a relationships between two features"""))),
                    ui.column(2)),
                
                ui.row(
                    ui.column(9),
                    ui.column(3,ui.div({"class": "app-col"},
                            ui.p(ui.input_action_button("btn7","Click Z-test"))))),
                
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "app-col"},
                            ui.p(ui.output_table("chi2test1_table")))),
                    ui.column(2)),
                
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "app-col"},
                            ui.p(ui.h5({"style": "text-align: left;"}, ui.output_text("chi2test2_text"))),
                            ui.p(ui.output_table("chi2test2_table")))),
                    ui.column(2)),
                
                ui.row(
                    ui.column(2),
                    ui.column(8,ui.div({"class": "app-col"},
                            ui.p(ui.h5({"style": "text-align: left;"}, ui.output_text("chi2test3_text"))),
                            ui.p(ui.output_table("chi2test3_table")))),
                    ui.column(2)),
             t1,t2,t3
            )

    # Select Features for z-test
    @output
    @render.ui()
    def Choice1a():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.test5() == True:
            if input.test5a() == "1":
                return ui.TagList(
                    ui.input_selectize("test5a1","Select Features",choices=[None]+l1))
            if input.test5a() == "2":
                return ui.row(ui.column(6,ui.div({"class": "app-col"},
                                       ui.p(ui.input_selectize("test5a2","Select 1st Feature",choices=[None]+l1)))),
                    ui.column(6,ui.div({"class": "app-col"},
                                       ui.p(ui.input_selectize("test5a3","Select 2nd Feature",choices=[None]+l1)))))

    # Select Features for t-test
    @output
    @render.ui()
    def Choice1b():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.test6() == True:
            if input.test6a() == "1":
                return ui.TagList(
                    ui.input_selectize("test6a1","Select Features",choices=[None]+l1))
            if input.test6a() == "2":
                return ui.row(ui.column(6,ui.div({"class": "app-col"},
                                       ui.p(ui.input_selectize("test6a2","Select 1st Feature",choices=[None]+l1)))),
                    ui.column(6,ui.div({"class": "app-col"},
                                       ui.p(ui.input_selectize("test6a3","Select 2nd Feature",choices=[None]+l1)))))

    # Select Features for chi2-test
    @output
    @render.ui()
    def Choice1c():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.test7() == True:
            if input.test7a() == "1":
                return ui.TagList(
                    ui.input_selectize("test7a1","Select Features",choices=[None]+l0))
            if input.test7a() == "2":
                return ui.row(ui.column(6,ui.div({"class": "app-col"},
                                       ui.p(ui.input_selectize("test7a2","Select 1st Feature (Rows Groupby)",choices=[None]+l0)))),
                    ui.column(6,ui.div({"class": "app-col"},
                                       ui.p(ui.input_selectize("test7a3","Select 2nd Feature (Columns Groupby)",choices=[None]+l0)))))
    
    #Sample Selection
    @output
    @render.ui()
    def Choice2a():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.test5() == True:
            if input.test5b() == "Random":
                return ui.TagList(
                    ui.input_numeric("test5b1","No. of Sample Size",min=2,max=len(df),value=45))
            if input.test5b() == "Train-Test":
                return ui.TagList(
                    ui.input_slider("test5b2","Proportion of Sample Size respect Population Size",min=0.00,max=1.00,value=0.30,step=0.02))
            if input.test5b() == "Starting":
                return ui.TagList(
                    ui.input_numeric("test5b3","Sample Size from top ",min=2,max=len(df),value=45))
            if input.test5b() == "Ending":
                return ui.TagList(
                    ui.input_numeric("test5b4","Sample Size from bottom",min=2,max=len(df),value=45))
            if input.test5b() == "Range":
                return ui.row(
                    ui.column(4,ui.div({"class": "app-col"},
                                       ui.p(ui.input_numeric("test5b5","Initial Index",min=2,max=len(df),value=0)))),
                    ui.column(4,ui.div({"class": "app-col"},
                                       ui.p(ui.input_numeric("test5b6","End Index",min=2,max=len(df),value=45)))),
                    ui.column(4,ui.div({"class": "app-col"},
                                       ui.p(ui.input_numeric("test5b7","Jump Index",min=2,max=len(df),value=1)))))
    
                
    #Sample Selection
    @output
    @render.ui()
    def Choice2b():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.test6() == True:
            if input.test6b() == "Random":
                return ui.TagList(
                    ui.input_numeric("test6b1","No. of Sample Size",min=2,max=len(df),value=25))
            if input.test6b() == "Train-Test":
                return ui.TagList(
                    ui.input_slider("test6b2","Proportion of Sample Size respect Population Size",min=0.00,max=1.00,value=0.30,step=0.02))
            if input.test6b() == "Starting":
                return ui.TagList(
                    ui.input_numeric("test6b3","Sample Size from top ",min=2,max=len(df),value=25))
            if input.test6b() == "Ending":
                return ui.TagList(
                    ui.input_numeric("test6b4","Sample Size from bottom",min=2,max=len(df),value=25))
            if input.test6b() == "Range":
                return ui.row(
                    ui.column(4,ui.div({"class": "app-col"},
                                       ui.p(ui.input_numeric("test6b5","Initial Index",min=2,max=len(df),value=0)))),
                    ui.column(4,ui.div({"class": "app-col"},
                                       ui.p(ui.input_numeric("test6b6","End Index",min=2,max=len(df),value=25)))),
                    ui.column(4,ui.div({"class": "app-col"},
                                       ui.p(ui.input_numeric("test6b7","Jump Index",min=2,max=len(df),value=1)))))
        
        

    # Stastical Analysis
    @output
    @render.text()
    def Conti_Info():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.unit1() == True:

            if input.unit2() == "Minimum":
                return df[input.col1()].min()

            elif input.unit2() == "Maximum":
                return df[input.col1()].max()

            elif input.unit2() == "Range":
                return df[input.col1()].max() - df[input.col1()].min()

            elif input.unit2() == "Mean":
                return round(df[input.col1()].mean(), 5)

            elif input.unit2() == "Mode":
                return df[input.col1()].mode()[0]

            elif input.unit2() == "Median":
                return df[input.col1()].median()

            elif input.unit2() == "Variance":
                return round(df[input.col1()].var(), 5)

            elif input.unit2() == "Standard Deviation":
                return round(df[input.col1()].std(), 5)

    # Percentile Function
    @output
    @render.text()
    def Conti_Perc():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.unit3() == True:
            return df[input.col1()].quantile(input.unit4() / 100)

    # Column Value Analysis
    @output
    @render.text()
    def Conti_Ana():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.unit5() == True:
            if input.unit6() == "Missing Values %":
                s = df[input.col1()].isna().sum()
                z = round((s / len(df[input.col1()])) * 100, 3)
                return f"Sum {s} & Percentage {z} %"

            elif input.unit6() == "No. Unique Values":
                return len(df[input.col1()].unique())

            elif input.unit6() == "Distinct Value":
                return sorted(list(df[input.col1()].unique()))

            elif input.unit6() == "Length":
                return f"Size of {input.col1()} : {df[input.col1()].size}"

            elif input.unit6() == "Rows":
                return f"Total no.of Rows : {df.shape[0]}"

            elif input.unit6() == "Columns":
                return f"Total no.of Columns : {df.shape[1]}"

            
    #Frequency Table
    @output
    @render.table
    def Conti_freq():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.unit7() == True:
            return (
                df[input.col1()]
                .value_counts()
                .reset_index()
                .rename(columns={"index": input.col1(), input.col1(): "Counts"})
            )

    # Table Visualizations
    @output
    @render.table
    def Table():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.unit9() == "Tail":
            if input.unit8a()==True and input.unit8b()==False and input.unit8c()==False:
                return df[l1].tail(input.unit10())
                
            if input.unit8a()==False and input.unit8b()==True and input.unit8c()==False:
                return df[l2].tail(input.unit10())

            if input.unit8a()==False and input.unit8b()==False and input.unit8c()==True:
                return df[l0].tail(input.unit10())

        else:
            if input.unit8a()==True and input.unit8b()==False and input.unit8c()==False:
                return df[l1].head(input.unit10())
                
            if input.unit8a()==False and input.unit8b()==True and input.unit8c()==False:
                return df[l2].head(input.unit10())

            if input.unit8a()==False and input.unit8b()==False and input.unit8c()==True:
                return df[l0].head(input.unit10())


    # Categorical Columns
    @output
    @render.text()
    def Categ_Info():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.unit1() == True:

            if input.unit2() == "Missing Values %":
                s = df[input.col1()].isna().sum()
                z = round((s / len(df[input.col1()])) * 100, 3)
                return f"Sum {s} & Percentage {z} %"

            elif input.unit2() == "Mode":
                return df[input.col1()].mode()[0]

            elif input.unit2() == "No. Unique Values":
                return len(df[input.col1()].unique())

            elif input.unit2() == "Distinct Value":
                return sorted(list(df[input.col1()].unique()), key = len)

            elif input.unit2() == "Length":
                return f"Size of {input.col1()} : {df[input.col1()].size}"

            elif input.unit2() == "Rows":
                return f"Total no.of Rows : {df.shape[0]}"

            elif input.unit2() == "Columns":
                return f"Total no.of Columns : {df.shape[1]}"


    #Covariance and Correlations
    @output
    @render.table()
    @reactive.event(input.test4)
    def Stat_Test():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.test1() == True and input.test2() == False:
            df1 = df.cov()
            df1.insert(0,"Columns",df1.columns)          # insert columns front
            df1.insert(df1.shape[1],"Columns",df1.columns[1:],allow_duplicates=True)  # insert columns back
            return df1

        if input.test1() == False and input.test2() == True:
            df1 = df.corr(method=input.test3())
            df1.insert(0,"Columns",df1.columns)          # insert columns front
            df1.insert(df1.shape[1],"Columns",df1.columns[1:],allow_duplicates=True)  # insert columns back
            return df1
        

    #Summarize Colums
    @output
    @render.table()
    @reactive.event(input.test3a)
    def Summary():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.test1a() == True and input.test2a() == False:
            df1 = df[l1].describe()
            df1.insert(0,"Quantity",df1.index)          # insert columns front
            df1.insert(df1.shape[1],"Quantity",df1.index,allow_duplicates=True)  # insert columns back
            return df1

        if input.test1a() == False and input.test2a() == True:
            df1 = df[l2].describe()
            df1.insert(0,"Quantity",df1.index)          # insert columns front
            df1.insert(df1.shape[1],"Quantity",df1.index,allow_duplicates=True)  # insert columns back
            return df1
            
    #z-test
    @output
    @render.table()
    @reactive.event(input.btn5)
    def ztest_table():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.test5() == True:
            if input.test5a() == "1":
                if input.test5b() == "Random":
                    dfz = np.random.choice(df[input.test5a1()],input.test5b1())
                elif input.test5b() == "Train-Test":
                    dfztrain,dfz = train_test_split(df[input.test5a1()],test_size=input.test5b2())
                elif input.test5b() == "Starting":
                    dfz = df[input.test5a1()].iloc[:input.test5b3()]
                elif input.test5b() == "Ending":
                    dfz = df[input.test5a1()].iloc[len(df[input.test5a1()])-input.test5b4():]
                elif input.test5b() == "Range":
                    dfz = df[input.test5a1()].iloc[input.test5b5():input.test5b6():input.test5b7()]

                dfz_test = pd.DataFrame(ztest(dfz,value=df[input.test5a1()].mean(),alternative=input.test5c()), columns=["Value"])
                dfz_test.insert(0,"Index",["Z-Score","p-value"])
                dfz_test.loc[len(dfz_test.index)] = ['Sample Size',len(dfz)] 
            
                return dfz_test


            if input.test5a() == "2":
                if input.test5b() == "Random":
                    dfz1 = np.random.choice(df[input.test5a2()],input.test5b1())
                    dfz2 = np.random.choice(df[input.test5a3()],input.test5b1())
                elif input.test5b() == "Train-Test":
                    dfztrain,dfz1 = train_test_split(df[input.test5a2()],test_size=input.test5b2())
                    dfztrain,dfz2 = train_test_split(df[input.test5a3()],test_size=input.test5b2())
                elif input.test5b() == "Starting":
                    dfz1 = df[input.test5a2()].iloc[:input.test5b3()]
                    dfz2 = df[input.test5a3()].iloc[:input.test5b3()]
                elif input.test5b() == "Ending":
                    dfz1 = df[input.test5a2()].iloc[len(df[input.test5a2()])-input.test5b4():]
                    dfz2 = df[input.test5a3()].iloc[len(df[input.test5a3()])-input.test5b4():]
                    
                elif input.test5b() == "Range":
                    dfz1 = df[input.test5a2()].iloc[input.test5b5():input.test5b6():input.test5b7()]
                    dfz2 = df[input.test5a3()].iloc[input.test5b5():input.test5b6():input.test5b7()]

                dfz_test = pd.DataFrame(ztest(dfz1,dfz2,value=df[input.test5a2()].mean()-df[input.test5a3()].mean()
                                              ,alternative=input.test5c()), columns=["Value"])
                dfz_test.insert(0,"Index",["Z-Score","p-value"])
                dfz_test.loc[len(dfz_test.index)] = ['Sample Size',len(dfz1)] 
            
                return dfz_test


    #t-test
    @output
    @render.table()
    @reactive.event(input.btn6)
    def ttest_table():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        if input.test6() == True:
            if input.test6a() == "1":
                if input.test6b() == "Random":
                    dfz = np.random.choice(df[input.test6a1()],input.test6b1())
                elif input.test6b() == "Train-Test":
                    dfztrain,dfz = train_test_split(df[input.test6a1()],test_size=input.test6b2())
                elif input.test6b() == "Starting":
                    dfz = df[input.test6a1()].iloc[:input.test6b3()]
                elif input.test6b() == "Ending":
                    dfz = df[input.test6a1()].iloc[len(df[input.test6a1()])-input.test6b4():]
                elif input.test6b() == "Range":
                    dfz = df[input.test6a1()].iloc[input.test6b5():input.test6b6():input.test6b7()]

                dfz_test = pd.DataFrame(stats.ttest_1samp(dfz,popmean=df[input.test6a1()].mean(),
                                                          alternative=input.test6c()),columns=["Value"])
                dfz_test.insert(0,"Index",["t-statistic","p-value"])
                dfz_test.loc[len(dfz_test.index)] = ['Sample Size',len(dfz)] 
            
                return dfz_test


            if input.test6a() == "2":
                if input.test6b() == "Random":
                    dfz1 = np.random.choice(df[input.test6a2()],input.test6b1())
                    dfz2 = np.random.choice(df[input.test6a3()],input.test6b1())
                elif input.test6b() == "Train-Test":
                    dfztrain,dfz1 = train_test_split(df[input.test6a2()],test_size=input.test6b2())
                    dfztrain,dfz2 = train_test_split(df[input.test6a3()],test_size=input.test6b2())
                elif input.test6b() == "Starting":
                    dfz1 = df[input.test6a2()].iloc[:input.test6b3()]
                    dfz2 = df[input.test6a3()].iloc[:input.test6b3()]
                elif input.test6b() == "Ending":
                    dfz1 = df[input.test6a2()].iloc[len(df[input.test6a2()])-input.test6b4():]
                    dfz2 = df[input.test6a3()].iloc[len(df[input.test6a3()])-input.test6b4():]
                    
                elif input.test6b() == "Range":
                    dfz1 = df[input.test6a2()].iloc[input.test6b5():input.test6b6():input.test6b7()]
                    dfz2 = df[input.test6a3()].iloc[input.test6b5():input.test6b6():input.test6b7()]

                dfz_test = pd.DataFrame(stats.ttest_ind( dfz1, dfz2, alternative=input.test6c()),columns=["Value"])
                dfz_test.insert(0,"Index",["t-statistic","p-value"])
                dfz_test.loc[len(dfz_test.index)] = ['Sample Size',len(dfz1)] 
            
                return dfz_test



    #chi2-test -- Index
    @output
    @render.table()
    @reactive.event(input.btn7)
    def chi2test1_table():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]

        if input.test7() == True:
            if input.test7a() == "1":
                ch1 = stats.chi2_contingency(df[input.test7a1()].value_counts())
                dfch = pd.DataFrame([{"chi2-statistic": ch1[0], "p-value" : ch1[1], "Degrees of freedom" : ch1[2]}], index=["Value"]).T
                dfch.insert(0,"Index", dfch.index)
                return dfch

            if input.test7a() == "2":
                df2 = pd.crosstab(df[input.test7a2()], df[input.test7a3()], margins=False)
                ch1 = stats.chi2_contingency(df2)
                dfch = pd.DataFrame([{"chi2-statistic": ch1[0], "p-value" : ch1[1], "Degrees of freedom" : ch1[2]}], index=["Value"]).T
                dfch.insert(0,"Index", dfch.index)
                return dfch
                
    #chi2-test -- Predicted Text
    @output
    @render.text()
    @reactive.event(input.btn7)
    def chi2test2_text():
        if input.test7() == True:
            if input.test7a() == "1":
                return f"Predicted Table of {input.test7a1()} :"

            if input.test7a() == "2":
                return f"Predicte Table of {input.test7a2()} vs {input.test7a3()} :"
                
    #chi2-test -- Predicted Table
    @output
    @render.table()
    @reactive.event(input.btn7)
    def chi2test2_table():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]

        if input.test7() == True:
            if input.test7a() == "1":
                dfchp = pd.DataFrame(df[input.test7a1()].value_counts())
                dfchp.rename(columns={input.test7a1() : "Counts"}, inplace=True)
                dfchp.insert(0, input.test7a1(), dfchp.index)
                return dfchp

            if input.test7a() == "2":
                dfchp = pd.crosstab(df[input.test7a2()], df[input.test7a3()], margins=True, colnames=[f"{input.test7a3()} →→ "])
                dfchp.insert(0, f"{input.test7a2()} ↓↓", dfchp.index)
                return dfchp

    #chi2-test -- Expected Text
    @output
    @render.text()
    @reactive.event(input.btn7)
    def chi2test3_text():
        if input.test7() == True:
            if input.test7a() == "1":
                return f"Expected Table of {input.test7a1()} :"
            if input.test7a() == "2":
                return f"Expected Table of {input.test7a2()} vs {input.test7a3()} :"

    #chi2-test -- Expected Table
    @output
    @render.table()
    @reactive.event(input.btn7)
    def chi2test3_table():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]

        if input.test7() == True:
            if input.test7a() == "1":
                ch1 = stats.chi2_contingency(df[input.test7a1()].value_counts())
                dfche = pd.DataFrame(ch1[3], columns=["Counts"])
                dfche.insert(0, input.test7a1(), df[input.test7a1()].value_counts().index )
                return dfche
            if input.test7a() == "2":
                df2 = pd.crosstab(df[input.test7a2()], df[input.test7a3()], margins=False, colnames=[f"{input.test7a3()} →→ "])
                ch1 = stats.chi2_contingency(df2)
                dfche = pd.DataFrame(ch1[3], columns=[df2.columns], index = [df2.index])
                dfche.insert(0, f"{input.test7a2()} ↓↓", df2.index)
                return dfche
                
                
    #Histogram
    @output
    @render.plot()
    @reactive.event(input.btnhist)
    def hist():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        
        if input.h6lx() == True or input.h6ly() == True:           #log scaling uses by default range
        
            fig = px.histogram(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               log_x=eval(input.h6x()),log_y=eval(input.h6y()),
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               orientation= input.h10(), opacity = input.h9(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               pattern_shape_sequence=input.h3b(), facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                              )

        else:                                                         #range of axis of x and y 
            fig = px.histogram(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               range_x=[eval(input.h5ax()),eval(input.h5bx())], range_y=[eval(input.h5ay()),eval(input.h5by())],
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               orientation= input.h10(), opacity = input.h9(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               pattern_shape_sequence=input.h3b(), facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                              )
                           
        return fig.show()


    # Bar Plot
    @output
    @render.plot()
    @reactive.event(input.btnbar)
    def barplot():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        
        if input.h6lx() == True or input.h6ly() == True:           #log scaling uses by default range
        
            fig = px.bar(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               log_x=eval(input.h6x()),log_y=eval(input.h6y()),
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               orientation= input.h10(), opacity = input.h9(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               pattern_shape_sequence=input.h3b(), facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                              )

        else:                                                         #range of axis of x and y 
            fig = px.bar(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               range_x=[eval(input.h5ax()),eval(input.h5bx())], range_y=[eval(input.h5ay()),eval(input.h5by())],
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               orientation= input.h10(), opacity = input.h9(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               pattern_shape_sequence=input.h3b(), facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                              )
                           
        return fig.show()

    # Scatter Plot
    @output
    @render.plot()
    @reactive.event(input.btnscatter)
    def scatterplot():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        
        if input.h6lx() == True or input.h6ly() == True:           #log scaling uses by default range

            
            
            
            fig = px.scatter(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               log_x=eval(input.h6x()),log_y=eval(input.h6y()),
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               symbol = None if input.h3e()=="None" else input.h3e(), symbol_sequence=str(input.h4e()),
                               size = None if input.h3f() =="None" else input.h3f(), size_max=input.h4f(), 
                               opacity = input.h9(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                            )

        else:                                                         #range of axis of x and y 
            fig = px.scatter(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               range_x=[eval(input.h5ax()),eval(input.h5bx())], range_y=[eval(input.h5ay()),eval(input.h5by())],
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               symbol = None if input.h3e()=="None" else input.h3e(), symbol_sequence=str(input.h4e()),
                               size = None if input.h3f()=="None" else input.h3f(), size_max=input.h4f(),
                               opacity = input.h9(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                              )

                           
        return fig.show()


    # Line Plot
    @output
    @render.plot()
    @reactive.event(input.btnline)
    def lineplot():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        
        if input.h6lx() == True or input.h6ly() == True:           #log scaling uses by default range
        
            fig = px.line(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               log_x=eval(input.h6x()),log_y=eval(input.h6y()),
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               symbol = None if input.h3e()=="None" else input.h3e(), symbol_sequence=str(input.h4e()),
                               orientation = input.h10(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                              )

        else:                                                         #range of axis of x and y 
            fig = px.line(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               range_x=[eval(input.h5ax()),eval(input.h5bx())], range_y=[eval(input.h5ay()),eval(input.h5by())],
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               symbol = None if input.h3e()=="None" else input.h3e(), symbol_sequence=str(input.h4e()),
                               orientation = input.h10(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                              )
                           
        return fig.show()

    # Box Plot
    @output
    @render.plot()
    @reactive.event(input.btnbox)
    def boxplot():
        df = pd.DataFrame(list(collection.find())).iloc[:,1:]
        l0 = [i for i in df.columns]
        l1 = [i for i in df.columns if df[i].dtypes != "O"]
        l2 = [i for i in df.columns if df[i].dtypes == "O"]
        
        if input.h6lx() == True or input.h6ly() == True:           #log scaling uses by default range
        
            fig = px.box(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               log_x=eval(input.h6x()),log_y=eval(input.h6y()),
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               orientation = input.h10(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                              )

        else:                                                         #range of axis of x and y 
            fig = px.box(df, x=None if input.h1()=="None" else input.h1(),y=None if input.h2()=="None" else input.h2(),
                               range_x=[eval(input.h5ax()),eval(input.h5bx())], range_y=[eval(input.h5ay()),eval(input.h5by())],
                               width = input.h7x(),height = input.h7y(),
                               color_discrete_sequence=[None if input.h11()=="None" else input.h11()],
                               color=None if input.h8()=="None" else input.h8(),
                               orientation = input.h10(),
                               facet_row=None if input.h3()=="None" else input.h3(), facet_row_spacing= input.h3a(),
                               facet_col=None if input.h4()=="None" else input.h4(), facet_col_spacing= input.h4a(),
                               facet_col_wrap= input.h4b(),
                               animation_frame=None if input.h3c()=="None" else input.h3c(),animation_group=None if input.h4c()=="None" else input.h4c(),
                               title = None if input.h3d()=="None" else input.h3d(),labels = None if input.h4d()=="None" else eval(input.h4d())
                              )
                           
        return fig.show()
    
        
    
l5 = ['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure', 'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet', 'brown','burlywood', 'cadetblue', 'chartreuse', 'chocolate', 'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange', 'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue', 'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue', 'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro', 'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green', 'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow', 'lightgray', 'lightgrey', 'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey', 'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen', 'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid', 'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen', 'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive', 'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple', 'red', 'rosybrown', 'royalblue', 'rebeccapurple','saddlebrown', 'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver', 'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow', 'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow', 'yellowgreen']
app = App(app_ui, server)

