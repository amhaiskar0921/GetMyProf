## Project Description

GetMyProf is a web application that determines the best professors for a class the user wants to take for future quarters. The professors that can be chosen are based on whether they taught the course two years ago. 

For example, if the user wants to take I&C SCI 51, the user first picks the department(I&C SCI from the example above), sorted in alphabetical order, and the course number(51 from the model above). After the user inputs the class information, they answer questions based on their desired professor. One factor we use to calculate the best professors is determining the occurrence of tags in the rate my professor reviews that align with the answers to the user's questions. 

## Questionnaire Questions
The first question asks the user the difficulty of the class, which we determine based on the mean GPA of each course the professor has taught in the past two years.

The second question asks the amount of courseload, which is determined by the amount of time spent outside lectures to complete the assignment.

The third question asks if the user cares about the likeability of a professor. In our web application, what we consider likable are professors who display positive professor qualities like being transparent with the grading system, effectively communicating with students, and caring about the students in the class. 

Lastly, the fourth question discusses whether the user prioritizes grades over learning. This means that professors who prioritize grades over learning are people who have clear grading criteria, don’t grade harshly, provide good feedback, etc. 

## Some Functionality of the Web Application
The professor's ranking for determining the best ones for the user is based on the score, which is calculated based on the occurrence of tags that correlate with users' desired qualities and the mean GPA of the class.

After the user answers the questionnaire and the class they want to take, the web application loads a new page containing the top 3 professors that are recommended with their mean GPA, the percentage of people who want to take that professor again, and the rate my professor rating for each professor listed.

## Structure of this Web Application
This project uses the PeterPortal API to fetch the mean GPA and the RateMyProfessor API to fetch the reviews of the professor's attributes like top 5 tags of the professors, rating of the professor, and retake rate. With our Python backend, we call these APIs to fetch the data and determine the scores for each professor to determine the best professors for the user. In the front end, we use HTML to provide the web page structure of the questionnaire and how the user can pick the class and CSS to add more styling to our website. To connect the front end and the back end, we use Flask to achieve this. 

## Why is this Useful?
The project is helpful because it allows users who want to take a class to determine the professor that fits them. This will enable users to spend less time choosing classes as this application takes into account the grade distribution from Zotistics and rates my professor reviews for each professor. 

## Images
### Dropdown Menu for Department:
<img width="1514" alt="Departments" src="https://github.com/amhaiskar0921/ProfRepoFinal/assets/43621944/947c0713-683a-44f8-b84f-7adee12ccc8d">

### Homepage:
<img width="344" alt="Homepage" src="https://github.com/amhaiskar0921/ProfRepoFinal/assets/43621944/a586c086-a024-44d6-a39c-df5d5a93cb24">

### Results (from best match to worst match for user preferences): 
<img width="987" alt="image" src="https://github.com/amhaiskar0921/ProfRepoFinal/assets/43621944/511d410d-d97c-482f-a21b-0ee0aadc1395">


