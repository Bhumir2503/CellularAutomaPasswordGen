import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Randomized Length and Using All Chars Dataset
results_files_1 = ['Rule30_Results.csv', 
                   'Rule54_Results.csv', 
                   'Rule90_Results.csv', 
                   'Rule110_Results.csv' ]

#Randomized Length and Not Using All Chars Dataset
results_files_2 = ['Rule30_Results_randl_not_using_all_chars.csv',
                   'Rule54_Results_randl_not_using_all_chars.csv',
                   'Rule90_Results_randl_not_using_all_chars.csv',
                   'Rule110_Results_randl_not_using_all_chars.csv' ]

#Fixed Length and Using All Chars Dataset
results_files_3 = ['Rule30_Results_fixedlength_usingallchars.csv',
                   'Rule54_Results_fixedlength_usingallchars.csv',
                   'Rule90_Results_fixedlength_usingallchars.csv',
                   'Rule110_Results_fixedlength_usingallchars.csv' ]

#Fixed Length and Not Using All Chars Dataset
results_files_4 = ['Rule30_Results_fixedlength_notusingallchars.csv',
                   'Rule54_Results_fixedlength_notusingallchars.csv',
                   'Rule90_Results_fixedlength_notusingallchars.csv',
                   'Rule110_Results_fixedlength_notusingallchars.csv' ]

xAxis = ['Rule 30', 'Rule 54', 'Rule 90', 'Rule 110'] #Rule used

def generate_bar_plot (result_list, title_str):
    yAxis = [] #column being tested
    for file in result_list:
        data = pd.read_csv(file)
        yAxis.append(np.round(np.mean(data['Strength']), 3))

    strongest_bar = np.max(yAxis)
    colors = ['#fa8d20' if val == strongest_bar else '#3480eb' for val in yAxis]

    plt.bar(xAxis, yAxis, color = colors)
    plt.ylim(0,100)
    plt.xlabel("Rule Used")
    plt.ylabel("Cryptographic Strength")
    plt.title(title_str)
    # Show y-values above each bar
    for i, value in enumerate(yAxis):
        plt.text(i, value + 1, str(value), ha='center', va='bottom')
    plt.show()

def generate_table_plot (my_df):
    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.axis('off')  # Hide axes

    # Create table
    table = ax.table(cellText=my_df.values, colLabels=my_df.columns, loc='center')
    table.scale(1, 2)  # Optional: Adjust size
    #plt.title("Data Table")
    plt.show()

""" for file in results_files:
    data = pd.read_csv(file)
    yAxis.append(np.round(np.mean(data['Strength']), 3))
    #print("Strength: ", np.mean(data['Strength']))
    #print("Length: ",np.mean(data['Length']) )
    strongest_val = np.max(data['Strength'].values)
    row = data[data['Strength'] == strongest_val]
    print (row)
    print("Strongest score: ", strongest_val) """


### Randomized Length and Using All Chars Plot
generate_bar_plot(results_files_1, "Rule vs. Strength w/ Random Lengths, Using All Chars")


### Randomized Length and Not Using All Chars Plot
generate_bar_plot(results_files_2, "Rule vs. Strength w/ Random Lengths, Not Using All Chars")


### Fixed Length and Using All Chars Plot
generate_bar_plot(results_files_3, "Rule vs. Strength w/ Fixed Lengths, Using All Chars")


### Fixed Length and Not Using All Chars Plot
generate_bar_plot(results_files_4, "Rule vs. Strength w/ Fixed Lengths, Not Using All Chars")

