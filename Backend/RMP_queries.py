import requests
from bs4 import BeautifulSoup
import ratemyprofessor

UCI_RMP_OBJ = ratemyprofessor.get_school_by_name("UC Irvine")

class UCI_Prof:
    def __init__(self, name: str):
        self._professor = ratemyprofessor.get_professor_by_school_and_name(UCI_RMP_OBJ, name)
    
    def get_avg_difficulty(self):
        if self._professor:
            return self._professor.difficulty
        else:
            return "PROFESSOR DOES NOT EXIST"
    
    def get_retake_percentage(self):
        if self._professor:
            return self._professor.would_take_again
        else:
            return "PROFESSOR DOES NOT EXIST"
    
    def get_tag_freq(self):
        # Available vars: 'id' (num), 'courses' (course obj), 'name' (full name), 'department', 'difficulty'
        # 'rating', 'would_take_again', 'num_ratings', 'school' (school obj)
        if not self._professor:
            return "PROFESSOR DOES NOT EXIST"
        url = 'https://www.ratemyprofessors.com/ShowRatings.jsp?tid={}'.format(self._professor.id)
        page = requests.get(url)
        # Check the HTTP status code
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            proftags = soup.findAll("span", {"class": "Tag-bs9vf4-0 hHOVKF" })
            tag_freq = {}

            numTags = 0
            for mytag in proftags:
                if (numTags >= 5):
                    if mytag.getText().lower() in tag_freq:
                        tag_freq[mytag.getText().lower()] += 1
                    else:
                        tag_freq[mytag.getText().lower()] = 1
                numTags += 1
            
            return tag_freq
        else:
            return "ERROR SCRAPING TAGS"



# Basic testing
if __name__ == '__main__':
    gopi = UCI_Prof("NICOLAU, A")
    print("Avg difficulty: ", gopi.get_avg_difficulty())
    print("Retake rate: ", gopi.get_retake_percentage(), "%")
    print(gopi.get_tag_freq())