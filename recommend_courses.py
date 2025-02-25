import numpy as np

course = data["course"].tolist()
des = data["description"].tolist()
level = data["level"].tolist()
rate = data["rating"].tolist()
doc = []

for i in range(len(des)):
    doc.append(course[i] + des[i])

sim = get_similarity(doc, lemmatized=True, no_stopword=True)
sim_sort = np.argsort(sim)[:, ::-1]

def rec_sim(course_name, current_level):
    equal = ""
    higher = ""
    
    if current_level == "Beginner":
        equal = "Beginner"
        higher = "Intermediate"
    elif current_level == "Intermediate":
        equal = "Intermediate"
        higher = "Advanced"
    elif current_level == "Advanced":
        equal = "Advanced"
        higher = "Advanced"
    
    index = course.index(course_name)
    sim_list = sim_sort[index]
    equal_count = 0
    higher_count = 0
    mix_count = 0
    sim_index = 0
    result = []

    while equal_count < 5 or higher_count < 5 or mix_count < 5:
        sim_index += 1
        if sim_index < len(course):  
            course_index = sim_list[sim_index]
            if level[course_index] == equal and equal_count < 5:
                equal_count += 1
                result.append((course[course_index], level[course_index], rate[course_index]))
            elif level[course_index] == higher and higher_count < 5:
                higher_count += 1
                result.append((course[course_index], level[course_index], rate[course_index]))
            elif "Mixed" in level[course_index] and mix_count < 5:
                mix_count += 1
                result.append((course[course_index], level[course_index], rate[course_index]))
        else:
            return result
    return result

def rec_docvec(course_name, current_level):
    equal = ""
    higher = ""

    if current_level == "Beginner":
        equal = "Beginner"
        higher = "Intermediate"
    elif current_level == "Intermediate":
        equal = "Intermediate"
        higher = "Advanced"
    elif current_level == "Advanced":
        equal = "Advanced"
        higher = "Advanced"

    index = course.index(course_name)
    sim_list = get_docvec_sim(index)
    equal_count = 0
    higher_count = 0
    mix_count = 0
    sim_index = 0
    result = []

    while equal_count < 5 or higher_count < 5 or mix_count < 5:
        sim_index += 1
        if sim_index < len(course):  
            course_index = sim_list[sim_index]
            if level[course_index] == equal and equal_count < 5:
                equal_count += 1
                result.append((course[course_index], level[course_index], rate[course_index]))
            elif level[course_index] == higher and higher_count < 5:
                higher_count += 1
                result.append((course[course_index], level[course_index], rate[course_index]))
            elif "Mixed" in level[course_index] and mix_count < 5:
                mix_count += 1
                result.append((course[course_index], level[course_index], rate[course_index]))
        else:
            return result
    return result
