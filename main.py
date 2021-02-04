from bs4 import BeautifulSoup

from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def login(driver, user):
    url = 'https://auth.dtu.dk/dtu'
    driver.get(url)
    w = WebDriverWait(driver, 10)

    username_element = w.until(lambda x: x.find_element_by_id('userNameInput'))
    username_element.send_keys(user['username'])

    password_element = w.until(lambda x: x.find_element_by_id('passwordInput'))
    password_element.send_keys(user['password'])

    element = w.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submitButton"]')))
    element.click()

def extract(source):
    soup = BeautifulSoup(source, 'html5lib')
    soup = soup.find('table', {'class':'gradesList'})
    soup = soup.find_all('tr')

    grades = []
    for x in soup:
        x = x.find_all('td')
        try:
            grade = {
                    'no':       x[0].text,
                    'title':    x[1].text,
                    'grade':    int(x[2].text.split()[0]),
                    'ects':     float(x[3].text),
                    }
        except:
            continue
        grades.append(grade)
    return grades

def browse(user):
    fireFoxOptions = FirefoxOptions()
    fireFoxOptions.set_headless()
    browser = Firefox(firefox_options=fireFoxOptions)

    login(browser, user)

    browser.get('https://cn.inside.dtu.dk/cnnet/Grades/Grades.aspx')
    grades = extract(browser.page_source)

    browser.close()

    return grades

def run(user):
    grades  = browse(data)
    gradez  = sum([x['grade']*x['ects'] for x in grades])
    credits = sum([x['ects'] for x in grades])
    return gradez/credits

data = {
        'username':'sXXXXXX',
        'password':'XxXxXxXxXxXxXxXxX'
        }

print(run(data))

