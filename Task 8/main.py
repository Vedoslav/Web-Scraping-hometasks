import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3


def parse():
    driver = webdriver.Chrome()
    max_page = 3

    wait = WebDriverWait(driver, 10)

    result = []

    for page in range(1, max_page):
        driver.get(f'https://jobs.marksandspencer.com/job-search?page={page}')
        wait.until(EC.presence_of_element_located((By.XPATH, "//h3[contains(@class,'text-2xl bold mb-16')]")))
        titles = driver.find_elements(By.XPATH, "//h3[contains(@class,'text-2xl bold mb-16')]")
        jobs = driver.find_elements(By.XPATH, "//a[contains(@class,'c-btn c-btn--primary')]")
        for job, elem in zip(jobs,titles):
            url = job.get_attribute('href')
            title = elem.text
            result.append({
                'title': title,
                'url': url,                
            })
    result1 = [list(tup) for tup in zip([i["title"] for i in result],([j["url"] for j in result]))]
    driver.quit()
    with open('result.json', 'w') as f:
        json.dump(result, f, indent=4)
    return result1

def write_sql(result1: list) -> None:
    filename = 'parse_Sel.db'
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()
    sql = """
        create table if not exists vacancies (
            id integer primary key,
            titles text,
            urls text            
        )
    """
    cursor.execute(sql)

    for item in result1:
        cursor.execute("""
            insert into vacancies(titles, urls)
            values (?, ?)
        """, (item[0], item[1]))

    conn.commit()
    conn.close()
    

if __name__ == '__main__':
    parse()
    
    # write_sql(result1)
