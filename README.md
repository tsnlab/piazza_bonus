# Piazza bonus web crawler
Piazza is a free online gathering place where students can ask, answer, and explore 24/7, under the guidance of their instructors. https://piazza.com/

This is a crawler for piazza to extract students who are endorsed for good questions, notes, and discussions. It also extracts the number of times endorsed and the total.

### environment
- Ubuntu 20.04.3 LTS 
- Python 3.8.10
- Recommanded chrome version
    -  Version 96.0.4664.110 (Official Build) (64-bit)
- Chromedriver
    - you have to download chromedriver which matches your chrome version and place it in the working directory where `main.py` is located. https://sites.google.com/chromium.org/driver/
### launch
- `python3 main.py [piazza_class_URL] [start_page_number] [end_page_number] [piazza_ID] [piazza_PASSWD]`
    <br>
    **piazza_class_URL** means like `https://piazza.com/class/[class_string]`.<br>
    you have to remove **?** character at the end of the string.<br>
    When you click on each posts, there is a number after ***cid=*** in the url.<br>
    So, **start_page_number** means the first post of the class,<br>
    and **end_page_number** means the last post of the class.<br>
    **piazza_ID** and **piazza_PASSWD** is your piazza login id and password.
- mesurement time 1~600 posts : 3183 seconds, 53 minutes
### output
- csv file
    - StudentName, Count, BonusId

### future upgrade
- ...
