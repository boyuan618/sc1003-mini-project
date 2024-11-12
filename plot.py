# IMPORTING ALL LIBRARIES

#%pip install matplotlib
#%pip install seaborn
#%pip install plotly.express

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import plotly.express as px



# FUNCTION TO RECIEVE USER INPUT + CORRESPONDING DATA

def plotter(filestr):

    # checks for invalid group number entered
    while True:
        try:
            group = int(input("Input tutorial group (if you want to enter G-1, enter 1): "))
            break
        except ValueError:
            print("Invalid group number entered. Try again.")


    # reading new CSV file + all data in dic
    dic_data = r_file(filestr)

    # returns dic of the chosen group
    data_group_chosen = [student for student in dic_data if student["Tutorial_Group"] == f"G-{group}"]
    return data_group_chosen, group

# for generating dot plot

def dot(data_group_chosen, group):
    all_cgpas = [float(student["CGPA"]) for student in data_group_chosen]
    all_student_teams = [student["Team Assigned"] for student in data_group_chosen]

    # combining both data into a new dictionary
    data = [{"CGPA": cgpa, "Team": team} for team, cgpa in zip(all_student_teams, all_cgpas)]

    # create the plot
    fig = px.strip(data, x = "CGPA", y = "Team", title = f"CGPA distribution in each team in Tutorial Group {group}", stripmode = "overlay")

    fig.show()

# function for plotting bar chart for schools
# data only contains that group's member details

def bar_school(data, group):
    #generate the total no. of unique schools
    different_schools_with_repetition = (student["School"] for student in data)
    different_schools = []
    for element in different_schools_with_repetition:
      if element not in different_schools:
        different_schools.append(element)

    #create a dictionary to hold values for each school and put it in a list (should be updated after every team)
    list_of_school_dict = []

    teams_tally_with_repetitions = sorted(

      (student["Team Assigned"] for student in data),
      key=lambda x: int(x[1:])  # Sort based on the numeric part after 'T'
    )

    teams_tally = []

  #retrieve only the unique elements within teams_tally_with_repetitions
    for element in teams_tally_with_repetitions:
      if element not in teams_tally:
        teams_tally.append(element)

      #iterate through all the teams in a tutorial group
    for team in teams_tally:

          #iterate through all different schools in a team of a tutorial group
          dict_school = {school: 0 for school in different_schools}

          # Iterate over each student record
          for student in data:
              # Check if the student is in the current team
              if student["Team Assigned"] == team and student["School"] in dict_school:
                  dict_school[student["School"]] +=1       # Count number of student from each school

          list_of_school_dict.append(dict_school)


      # Step 1: create dic with key with the value being initialised to an empty list initially
    school_counts = {school: [] for school in list_of_school_dict[0]}

      # Step 2: Iterate through each team's dictionary in list_of_school_dict
    for team_dic in list_of_school_dict:
          # Step 3: Append the count for each school to its list
        for school in school_counts:
              school_counts[school].append(team_dic[school])


      # put keys and values from dictionary into lists
    schools = list(school_counts.keys())
    values = [school_counts[school] for school in schools] #list of values corresponding to no. of students in a school in different teams in a bigger list

      #make a list of colors which each school can be assigned to
    colors_to_pick_from = [
          "Red", "Green", "Blue", "Cyan", "Magenta",
          "Yellow", "Black", "Gold", "Orange",
          "Purple", "Pink", "Brown", "Grey",
          "lightblue", "darkred", "darkgreen",
          "navy", "lavender"
      ]

    xpos = list(range(len(teams_tally)))
    barWidth = 0.4
    bottom = [0] * len(teams_tally)  # create a list ten '0's for bottom which will be updated with new value of bottom after iterating through no. of students in each school

    plt.figure(figsize=(20, 7))

    for no_of_students_from_each_school, color, school_name in zip(values, colors_to_pick_from, schools):
        plt.bar(xpos, no_of_students_from_each_school, bottom=bottom, color=color, width=barWidth, label=school_name)
          # update bottom with current value of each school
        bottom = [a + b for a, b in zip(bottom, no_of_students_from_each_school)]  # current no. of students in a school + increase in no. of students for each team

      # adding all labels
    plt.xlabel("Teams Distribution", fontsize = "20")
    plt.ylabel("Number of students", fontsize = "20")
    plt.title(f"School distribution of teams in Tutorial group {group}", fontsize = "30")
    plt.xticks(xpos, teams_tally, fontsize = "15")

      # bbox: x moves legend away by 0.1 away from the edge; y = keeps legend aligned at the top
    plt.legend(bbox_to_anchor = (1.1, 1), loc = "upper left", fontsize = "15")

      # automatically adjust all elements such that they don't overlap
    plt.tight_layout()

    plt.show()
# function for plotting bar chart for gender distribution

def bar_gender(data, group):

    #create a list to hold numbers of girls/guys in each team
    girls_in_tutorial_group =[]
    guys_in_tutorial_group =[]

    #creates list of all possible unique teams in the tutorial group we are checking
    teams_tally = set(student["Team Assigned"] for student in data) #set ensures that all the elements generated are unique
    teams_tally = sorted(teams_tally, key=lambda x: int(x[1:])) #cite stackoverflow

    for team in teams_tally:
        female_count = 0  # Resets to 0 for each team
        male_count = 0    # Resets to 0 for each team

        # Iterate over each student record
        for student in data:
            # Check if the student is in the specified tutorial group and the current team
            if student["Team Assigned"] == team:
                # Count female and male students
                if student["Gender"]== "Female":
                    female_count += 1
                elif student["Gender"]== "Male":
                    male_count += 1

        # Append the counts for this team to the respective lists
        girls_in_tutorial_group.append(female_count)
        guys_in_tutorial_group.append(male_count)

    #plot data for girls
    xpos = list(range(len(girls_in_tutorial_group)))
    plt.figure(figsize=(10, 7))
    barWidth = 0.3
    plt.bar (xpos,girls_in_tutorial_group,color='red',width = barWidth,label = 'Females')

    #plot data for guys
    plt.bar([x + barWidth for x in xpos], guys_in_tutorial_group, color='blue', width=barWidth, label="Males")

    # x-axis label, y-axis label, and legend respectively
    plt.xlabel('Teams')
    plt.ylabel('Number of Each Gender')
    plt.legend()

    # Labeling for each team in the tutorial group
    plt.xticks([x + barWidth / 2 for x in xpos], teams_tally)


    #naming our graph
    plt.title(f"Gender distribution per team in Tutorial Group {group}")


def main_graph():
    write_filstr = "dataset 1 (5 per team).csv"
    data_group_chosen, group = plotter(write_filstr)

    # generating dot plots
    dot(data_group_chosen, group)

    # generating bar charts
    bar_school(data_group_chosen, group)
    bar_gender(data_group_chosen, group)
    
def r_file(filestr):
    # Parse CSV File
    infile = open(filestr)

    column_names = infile.readline()                          # Save 1st row (column names) in a string
    keys = column_names[0:-1]                                 # Removes /n from string
    keys = keys.split(",")                                    # Save column names as individual elements in list

    number_of_columns = len(keys)                             # Total number of columns in dataset
    data = infile.readlines()                                 # Pull the rest of the csv file

    list_of_rows = list()                                     # Initialise buffer list that temporarily stores all data
    for row in data:                                          # Saves each row as a list inside a list
        row = row[0:-1]                                       # Removes /n from end of string
        list_of_rows.append(row.split(","))                   # Append entire row into list

    infile.close()                                            # Closes CSV file, allows saving of file

    list_of_dictionaries = []                                 # Initialise List that will contain Dictionaries
    for item in list_of_rows:
        row_as_a_dictionary = {}                              # Dictionary Data Type
        for i in range(number_of_columns):
            row_as_a_dictionary[keys[i]] = item[i]            # Key number increments from 0
        list_of_dictionaries.append(row_as_a_dictionary)      # Stores Dictionary into a List

    return(list_of_dictionaries)
main_graph()

# Import CSV file
# RETURNS ENTIRE CSV AS A LIST OF DICTIONARIES

