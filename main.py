import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
name = []
skills = []
ratings = []
level = []

for a in range(1, 83):
    url = f"https://www.coursera.org/courses?language=English&topic=Data%20Science&page={a}&sortBy=BEST_MATCH"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="lxml")

    for course in soup.find_all("li", class_="cds-9 css-0 cds-11 cds-griditem cds-56 cds-64 cds-76 cds-90"):
        name.append(course.find('h3', class_="cds-CommonCard-title css-6ecy9b").text)

        try:
            c = course.find('div', class_="cds-CommonCard-bodyContent")
            skills.append(re.sub("Skills you'll gain:", "", c.text))
        except:
            skills.append("Not Available")

        try:
            ratings.append(course.find('p', class_="css-2xargn").text)
        except:
            ratings.append("Not Available")

        try:
            level.append(course.find('div', class_="cds-CommonCard-metadata").text)
        except:
            level.append("Not Available")

dataset = {"name": name, "skills": skills, "ratings": ratings, "level": level}
df = pd.DataFrame(dataset)
df.to_csv("courseradata.csv", index=False)

data = pd.read_csv("courseradata.csv")

data['ratings'] = pd.to_numeric(data['ratings'], errors='coerce')
mean_rating = data['ratings'].mean()
data['ratings'].fillna(mean_rating, inplace=True)


def assign_class(rating):
    if rating > 4.7:
        return 0
    elif 4.4 <= rating <= 4.7:
        return 1
    else:
        return 2

data['class'] = data['ratings'].apply(assign_class)

X = data[['ratings']] 
y = data['class'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Random Forest Classification Report:")
print(classification_report(y_test, y_pred))


def recommend_course(skill, difficulty):
    relevant_courses = data[(data['level'].str.contains(difficulty, case=False, na=False))]

    if relevant_courses.empty:
        print("No courses found matching the criteria.")
        return pd.DataFrame(columns=['name', 'skills'])

    matching_courses = relevant_courses[relevant_courses['skills'].str.contains(skill, case=False, na=False)]

    if matching_courses.empty:
        print("No courses found matching the provided skill.")
        return pd.DataFrame(columns=['name', 'skills'])

    return matching_courses[['name', 'skills']]


user_skill = input("Enter your desired skill: ")
user_difficulty = input("Enter desired difficulty (Beginner, Intermediate, Advanced, Mixed): ")

recommendations = recommend_course(user_skill, user_difficulty)
print("\nRecommended courses:")
print(recommendations.head())
