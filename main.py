###

import random
import sys
import time

import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

###


def appendNameToDic(studentName: str, i: int, df: dict) -> dict:
    if studentName in df.keys():
        df[studentName].append(i)
    else:
        df[studentName] = [i]
    return df


def main():
    start = time.time()

    if len(sys.argv) != 4:
        print("RUN python3 [piazza_class_URL] \
            [piazza_ID] [piazza_PASSWD]", file=sys.stderr)
        return
    # Config
    df = dict()
    ser = Service("./chromedriver")
    option = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ser, options=option)

    # Login
    url, id, passwd = sys.argv[1], sys.argv[2], sys.argv[3]
    driver.get("{url}?cid={number}".format(url=url, number=1))
    driver.find_element(By.ID, "email_field").send_keys(id)
    driver.find_element(By.ID, "password_field").send_keys(passwd)
    driver.find_element(By.ID, "modal_login_button").click()

    # Page 1 to 600
    for i in range(1, 600):
        try:
            # get HTML
            driver.implicitly_wait(300)
            driver.get("{url}?cid={number}".format(url=url, number=i))
            driver.implicitly_wait(300)
            time.sleep(random.randrange(3, 5))
            html = driver.page_source
            driver.implicitly_wait(300)
            soup = bs(html, 'html.parser')

            # parsing good Question
            endorseQuestion = soup.select("div#question > div#view_quesiton_note > \
            div.post_region_message_wrapper > div#endorse_text > \
            div > span.endorse_message")
            if endorseQuestion:
                endorseStudent = soup.select("div#question > \
                div#view_question_note_bar > \
                div.post_region_actions_meta > div")
                studentName = endorseStudent[0].contents[0].text.strip()
                df = appendNameToDic(studentName, i, df)
            else:
                print("no good question")
            # parsing good Note
            endorseNote = soup.select("div#note > div#view_quesiton_note > \
            div.post_region_message_wrapper > div#endorse_text > \
            div > span.endorse_message")
            if endorseNote:
                endorseStudent = soup.select("div#note > div#view_question_note_bar > \
                div.post_region_actions_meta > div")
                studentName = endorseStudent[0].contents[0].text.strip()
                df = appendNameToDic(studentName, i, df)
            else:
                print("no good Note")

            # parsing good Answer
            endorseAnswer = soup.select("div#member_answer > div > \
            div.post_region_content.view_mode > \
                div.post_region_message_wrapper > \
                    div > div > span.endorse_message")
            if endorseAnswer:
                studentAnswer = soup.select("div#member_answer > div > \
                div.post_region_actions.view_mode > div > div")
                studentName = studentAnswer[0].contents[0].text.strip()
                df = appendNameToDic(studentName, i, df)
            else:
                print("no good answer")
            driver.implicitly_wait(1000)

            # parsing good Discussion
            clarifyingDiscussions = soup.select("div#clarifying_discussion > \
            div[data-pats=followups] > div[data-pats=followup]")
            if clarifyingDiscussions:
                for endorseDiscussion in clarifyingDiscussions:
                    discussionAnswer = \
                        endorseDiscussion.select("\
                            div.post_region_message.endorse.show")
                    if discussionAnswer:
                        studentAnswer = endorseDiscussion.select_one("\
                            div[data-pats=original_post] > div > a > div")
                        studentName = studentAnswer.text.strip()
                        df = appendNameToDic(studentName, i, df)
                    else:
                        print("no good discussion")
            else:
                print("no discussion")
        except Exception:
            continue
        print(df)
    # data to CSV file
    df = {x: df[x] for x in sorted(df.keys())}
    data = pd.DataFrame(list(df.items()), columns=["StudentName", "BonusId"])
    data['Count'] = list(len(x) for x in df.values())
    data.to_csv("output.csv", mode='w', sep='\t')

    # time
    end = time.time()
    print("time", end - start, "seconds")


if __name__ == "__main__":
    main()