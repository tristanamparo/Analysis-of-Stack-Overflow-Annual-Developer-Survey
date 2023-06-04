import csv
import re
import matplotlib.pyplot as plt

# returns the way how the respondents learn coding
def learn_code(file):
    ctr = 0
    where_learn_code = []
    freq = {}

    for i in file:
        how_learn_code = i[6]
        if (";" in how_learn_code):                                       # checks if there is more than 1 answer in that question
            tempfile = re.split("[;]", i[6])                              # if yes, separate each of them and append to the where_learn_code
            for j in tempfile:
                where_learn_code.append(j)
        else:                                                             # append to where_learn_code if only one answer
            where_learn_code.append(how_learn_code)
            
    for i in where_learn_code:                                            # counts the number of occurrence of different answers
        if i in freq:                                                     # and put it in dictionary freq
            freq[i] += 1
        else:
            freq[i] = 1

    return freq


def online_resources_2_learn_code(file):
    code_resources = []
    freq = {}

    for i in file:
        if ";" in i[7]:                                                   # checks if there is more than 1 answer in that question
            tempfile = re.split("[;]", i[7])                              # if yes, separate each of them and append to the new_list
            for j in tempfile:
                code_resources.append(j)
        else:                                                             # append to new_list if only one answer
            code_resources.append(i[7])

    for i in code_resources:                                              # counts the number of occurrence of different answers
        if i in freq:                                                     # and put it in dictionary freq
            freq[i] += 1
        else:
            freq[i] = 1

    return freq


# counts the number of respondents
def no_of_respondents(file):
    ctr = 0
    for i in file:
        ctr += 1

    return ctr


# converts the read file into list so I can easily manipulate it
def convert_to_list(file):
    new_list = []
    for i in file:
        new_list.append(i)

    return new_list


# checks to see how many developers have Masteral Degree
def job_with_masters(file):
    have_masters_and_developer = 0
    dont_have_masters_but_developer = 0

    for i in file:
        profession = i[1]
        educ_level = i[5]
        if profession == "I am a developer by profession":
            if (educ_level[0] == "M"):                                    # checks only the first character of their answer since Masteral Degree starts with M
                have_masters_and_developer += 1
            else:
                dont_have_masters_but_developer += 1

    return (have_masters_and_developer, dont_have_masters_but_developer)


# returns a dictionary of jobs, with corresponding average yearly compensation
def compensation(file):
    new_list_job = []
    new_list_comp = []
    averages = {}
    counts = {}

    for i in file:
        yearly_comp = i[78]
        job = i[11]
        if (yearly_comp.isdigit() and job != "NA"):                      # checks if the respondent puts their salary in the survey
            comp = int(i[78])
            if ";" in job:                                               # check if the respondent has 1 or more jobs
                tempfile = re.split("[;]", job)
                average = comp / len(tempfile)
                for j in tempfile:                                       # append each job in the list of jobs
                    new_list_job.append(j)
                    new_list_comp.append(average)
            else:
                new_list_job.append(i[11])
                new_list_comp.append(comp)

    for jobs, comp in zip(new_list_job, new_list_comp):                  # put the list of jobs and their compensation to a dictionary
        if jobs in averages:                                             # and averaging the yearly compensation
            averages[jobs] += comp
            counts[jobs] += 1
        else:
            averages[jobs] = comp
            counts[jobs] = 1

    for jobs in averages:
        averages[jobs] = averages[jobs] / float(counts[jobs])

    return averages


# gets the coding experience of the respondents with corresponding compensations
def coding_exp_and_comp(file):
    list_of_comp = []
    list_of_code_exp = []
    averages = {}
    counts = {}

    for i in file:
        yearly_comp = i[78]                                             # getting the yearly compensation, 
        years_of_coding = i[9]                                          # years of coding experience, 
        years_of_pro_coding = i[10]                                     # and years of professional coding experience from the file
        
        if (yearly_comp.isdigit()):                                     # if they put their yearly compensation, put it in the list of compensation
            list_of_comp.append(int(yearly_comp))
            
            if (years_of_coding == "NA"):                               # if there is no years of coding experience and only have years of professional 
                if (years_of_pro_coding != "NA"):                       # coding experience, append it to the list of years of professional coding
                    list_of_code_exp.append(int(years_of_pro_coding))
            else:
                if (years_of_coding == "More than 50 years"):           # for the respondents who answered "more than 50 years", I used 51 as  
                    list_of_code_exp.append(51)                         # their years of experience to have an int value so I can analyze it
                elif (years_of_coding == "Less than 1 year"):           # for the respondents who answered "less than 1 year", I used 0.1 as 
                    list_of_code_exp.append(0.1)                        # their years of experience to have an int value so I can analyze it
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

    return averages


with open("./survey_results_public.csv", "r") as file:
    csvreader = csv.reader(file)
    next(csvreader)

    file = convert_to_list(csvreader)

    total_respondents = no_of_respondents(file)

    learn_code_dic = learn_code(file)
    most_common_learn_code = max(learn_code_dic)
    most_common_learn_code_number = max(learn_code_dic.values())
    print(
        str(most_common_learn_code)
        + " is the most common way of the respondents to learn coding with "
        + str(most_common_learn_code_number)
        + " out of "
        + str(total_respondents)
        + " respondents"
    )

    developer_has_masteral = job_with_masters(file)[0]
    developer_dont_have_masteral = job_with_masters(file)[1]
    print(
        "there is "
        + str(developer_has_masteral)
        + " developers that has masteral while there are "
        + str(developer_dont_have_masteral)
        + " developers that dont have masteral"
    )

    online_resources = online_resources_2_learn_code(file)
    online_resource = max(online_resources)
    max_value = max(online_resources.values())
    print(str(max_value) + " respondents online resources was " + str(online_resource))

    comp = compensation(file)
    highest_comp_job = max(comp)
    highest_comp = round(max(comp.values()))
    print(
        highest_comp_job
        + " is the highest paying job with $"
        + str(highest_comp)
        + " yearly"
    )

    # print(sorted(coding_exp(file).items(), key=lambda x: x[0]))

    comp_based_exp = coding_exp_and_comp(file)
    print(comp_based_exp)

    plt.scatter(*zip(*comp_based_exp.items()))
    plt.xlabel("Years of Experience")
    plt.ylabel("Average Compensation")
    plt.show()

"""
x = "rer;dsa /d; sasa"
y = "rara"
if re.split("[;]", x) == True:
    print("yes")
else:
    print("false")
print(re.split("[;]", x))
"""