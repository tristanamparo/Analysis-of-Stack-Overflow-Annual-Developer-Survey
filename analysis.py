import csv
import re
import matplotlib.pyplot as plt


# returns the way how the respondents learn coding
def learn_code(file):
    where_learn_code = []
    freq = {}

    for i in file:
        how_learn_code = i[6]
        if (";" in how_learn_code):                                         # checks if there is more than 1 answer in that question
            tempfile = re.split("[;]", how_learn_code)                      # if yes, separate each of them and append to the where_learn_code
            for j in tempfile:
                where_learn_code.append(j)
        else:                                                               # append to where_learn_code if only one answer
            where_learn_code.append(how_learn_code)

    for i in where_learn_code:                                              # counts the number of occurrence of different answers
        if i in freq:                                                       # and put it in dictionary freq
            freq[i] += 1
        else:
            freq[i] = 1

    total_respondents = no_of_respondents(file)
    blank_answer = no_answer(file, 6) 

    for source, value in freq.items():
        freq[source] = round(
            (value/(total_respondents - blank_answer)) * 100, 
            2)

    learn_code_dict = sorted(freq.items(), key=lambda x:x[1])

    return dict(learn_code_dict)


def online_resources_2_learn_code(file):
    code_resources = []
    freq = {}

    for i in file:
        if ";" in i[7]:                                                     # checks if there is more than 1 answer in that question
            tempfile = re.split("[;]", i[7])                                # if yes, separate each of them and append to the new_list
            for j in tempfile:
                code_resources.append(j)
        else:                                                               # append to new_list if only one answer
            code_resources.append(i[7])

    for i in code_resources:                                                # counts the number of occurrence of different answers
        if i in freq:                                                       # and put it in dictionary freq
            freq[i] += 1
        else:
            freq[i] = 1

    total_respondents = no_of_respondents(file)
    blank_answer = no_answer(file, 7)

    for source, value in freq.items():
        freq[source] = round(
            (value/(total_respondents - blank_answer)) * 100, 
            2)

    learn_code_online_dict = sorted(freq.items(), key=lambda x:x[1])

    return dict(learn_code_online_dict)


# returns the number of respondents who have no answer in column x
def no_answer(file, x):
    ctr = 0

    for i in file:
        if i[x] == "NA":
            ctr += 1

    return ctr


# counts the number of respondents
def no_of_respondents(file):
    ctr = 0
    for i in file:
        ctr += 1

    return ctr


# converts the read file into list for easy manipulation
def convert_to_list(file):
    new_list = []
    for i in file:
        new_list.append(i)

    return new_list


# reutrns a tuple that checks to see how many developers have Masteral Degree
def job_with_masters(file):
    have_masters_and_developer = 0
    dont_have_masters_but_developer = 0

    for i in file:
        profession = i[1]
        educ_level = i[5]
        if profession == "I am a developer by profession":
            if (educ_level[0] == "M"):                                      # checks only the first character of their answer since Masteral Degree starts with M
                have_masters_and_developer += 1
            else:
                dont_have_masters_but_developer += 1

    return {"Developer with Masters":have_masters_and_developer, "Developers without Masters":dont_have_masters_but_developer}


# returns a dictionary of jobs, with corresponding average yearly compensation
def compensation(file):
    new_list_job = []
    new_list_comp = []
    averages = {}
    counts = {}

    for i in file:
        yearly_comp = i[78]
        job = i[11]

        if (yearly_comp.isdigit() and job != "NA"):                         # checks if the respondent puts their salary in the survey
            comp = int(i[78])

            if ";" in job:                                                  # check if the respondent has 1 or more jobs
                tempfile = re.split("[;]", job)
                average = comp / len(tempfile)

                for j in tempfile:                                          # append each job in the list of jobs
                    new_list_job.append(j)
                    new_list_comp.append(average)
            else:
                new_list_job.append(i[11])
                new_list_comp.append(comp)

    for jobs, comp in zip(new_list_job, new_list_comp):                     # put the list of jobs and their compensation to a dictionary
        if jobs in averages:                                                # and averaging the yearly compensation
            averages[jobs] += comp
            counts[jobs] += 1
        else:
            averages[jobs] = comp
            counts[jobs] = 1

    for jobs in averages:
        averages[jobs] = averages[jobs] / float(counts[jobs])

    comp = sorted(averages.items(), key=lambda x:x[1])

    return dict(comp)


# gets the coding experience of the respondents with corresponding compensations
def coding_exp_and_comp(file):
    list_of_comp = []
    list_of_code_exp = []
    averages = {}
    counts = {}

    for i in file:
        yearly_comp = i[78]                                                 # getting the yearly compensation,
        years_of_coding = i[9]                                              # years of coding experience,
        years_of_pro_coding = i[10]                                         # and years of professional coding experience from the file
        if (yearly_comp.isdigit()):                                         # if they put their yearly compensation, put it in the list of compensation
            list_of_comp.append(int(yearly_comp))
            if (years_of_coding == "NA"):                                   # if there is no years of coding experience and only have years of professional
                if (years_of_pro_coding != "NA"):                           # coding experience, append it to the list of years of professional coding
                    list_of_code_exp.append(int(years_of_pro_coding))
            else:
                if ( years_of_coding == "More than 50 years"):              # for the respondents who answered "more than 50 years", I used 51 as
                    list_of_code_exp.append(51)                             # their years of experience to have an int value so I can analyze it
                elif (years_of_coding == "Less than 1 year"):               # for the respondents who answered "less than 1 year", I used 0.1 as
                    list_of_code_exp.append(0.5)                            # their years of experience to have an int value so I can analyze it
                else:
                    list_of_code_exp.append(int(years_of_coding))

    for exp, comp in zip(list_of_code_exp, list_of_comp):
        if exp in averages:
            averages[exp] += comp
            counts[exp] += 1
        else:
            averages[exp] = comp
            counts[exp] = 1

    for exp in averages:
        averages[exp] = averages[exp] / float(counts[exp])

    coding_exp = sorted(averages.items(), key=lambda x:x[0])
    
    return dict(coding_exp)

# create graph function
def create_graph(dict_, graph_title, x_label, y_label, label_font_size, string_ext = ""):
    keys = list(dict_.keys())                                                # putting the keys and values of dict into a list      
    values = list(dict_.values())

    fig, ax = plt.subplots(figsize = (17, 8))                               # size of figure

    ax.barh(keys, values)                                                   # horizontal bar plot

    for s in ['top', 'bottom', 'left', 'right']:                            # remove axes spines
        ax.spines[s].set_visible(False)

    ax.xaxis.set_ticks_position('none')                                     # remove axes spines
    ax.yaxis.set_ticks_position('none')

    for i in ax.patches:                                                    # adds annotation to the bars
        plt.text(i.get_width()+0.2, i.get_y()+0.5,
            str(round((i.get_width()), 2)) + string_ext,
            fontsize = label_font_size, fontweight ='bold',
            color ='grey')

    plt.yticks(fontsize=5.5)                                                # font size of each y ticks
    plt.title(graph_title)                                                  # adds title and label of x and y
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()
    


if __name__ == "__main__":
    with open("../survey_results_public.csv", "r") as file:
        csvreader = csv.reader(file)
        next(csvreader)

        file = convert_to_list(csvreader)

        total_respondents = no_of_respondents(file)

        # prints the most common way of learning code
        learn_code_dic = learn_code(file)
        create_graph(learn_code_dic, "Most common way of developers to learn code", "percentage", "Ways of Learning Code", 11, "%")

        # prints the most common online source of learning to code
        learn_code_online_dic = online_resources_2_learn_code(file)
        create_graph(learn_code_online_dic, "Most common online source to learn code", "percentage", "Online Resources", 11, "%")

        # prints the average yearly compensation of each Developer Job
        comp = compensation(file)
        create_graph(comp, "Developer Job Compensation",  "Average yearly compensation(in $)", "Developer job", 8)

        # prints the relationship of developers with masteral and developers without masteral
        dev_masters = job_with_masters(file)
        create_graph(dev_masters, "Number of Developers with and without Masteral", "No. of Respondents", "", 15)

        # prints the relationship of average yearly compensation to the coding experience of developers
        coding_exp_comp = coding_exp_and_comp(file)
        create_graph(coding_exp_comp, "Coding Experience of Developer and their Yearly Compensation", "Average yearly compensation(in $)", "Coding Experience", 6)
        plt.scatter(*zip(*coding_exp_comp.items()))
        plt.title("Coding Experience of Developer and their Yearly Compensation")
        plt.xlabel("Years of Experience")
        plt.ylabel("Average Compensation")
        plt.show()
