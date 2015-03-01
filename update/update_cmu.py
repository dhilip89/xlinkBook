#!/usr/bin/env python

from spider import *
import time
sys.path.append("..")
from record import CourseRecord

class CMUSpider(Spider):
    dept_dict = {}
    semester_list = []

    def __init__(self):
        Spider.__init__(self)
        self.school = "cmu"
        year = int(time.strftime('%Y',time.localtime(time.time())))
        self.semester_list.append('M' + str(year)[2:])
        self.semester_list.append('S' + str(year)[2:])
        self.semester_list.append('F' + str(year - 1)[2:])

    def getDescription(self, url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text);
        description = ''
        ul = soup.find('ul', class_='list-unstyled instructor')
        if ul != None and ul.li != None:
            description += 'instructors:' + ul.li.text + ' '
        
        for div in soup.find_all('div', class_='col-md-6'):
            if div != None and div.text.find('None') == -1 and div.text.find('Prerequisites') != -1:
                description += 'prereq:' + div.text.replace("\n","").replace('Prerequisites', '').strip() + ' '
                break

        div = soup.find("div", id="course-detail-description")
        if div != None:
            description += 'description:' + div.text.replace("\n","").replace('Description:', '').strip()
        return description

    def processData(self, semester_list, dept):
        file_name = self.get_file_name("eecs/cmu/" + self.dept_dict[dept], self.school)
        file_lines = self.countFileLineNum(file_name)
        f = self.open_db(file_name + ".tmp")
        self.count = 0
        course_dict = {}

        for semester in semester_list:
            print "processing " + self.dept_dict[dept] + " " + semester + " data"
            param = {"SEMESTER" : semester,
                 "MINI" : "NO",
                 "GRAD_UNDER" : "All",
                 "PRG_LOCATION" : "All",
                 "DEPT" : dept,
                 "LAST_NAME" : "",
                 "FIRST_NAME" : "",
                 "BEG_TIME" : "All",
                 "KEYWORD" : "",
                 "TITLE_ONLY" : "NO",
                 "SUBMIT" : ""}
            r = requests.post("https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/search", params=param)
            soup = BeautifulSoup(r.text); 

            for tr in soup.find_all("tr"):
                if tr.td != None and tr.td.a != None:
                    pos = tr.prettify().find("</td>")
                    title = tr.prettify()[tr.prettify().find("<td>", pos) + 4 : tr.prettify().find("</td>", pos + 3)].replace("\n", "").strip()
                    while title.find("<") != -1:
                        title = title[0 : title.find("<")].strip()+ title[title.find(">") + 1:].replace("\n", "").strip()
                    url = "https://enr-apps.as.cmu.edu" + tr.td.a.prettify()[tr.td.a.prettify().find("/open/SOC/SOCServlet"): tr.td.a.prettify().find("'", tr.td.a.prettify().find("/open/SOC/SOCServlet"))].replace("amp;","")
                    course_num = dept + tr.td.a.text 
                    if course_dict.get(course_num, '') != '':
                        continue
                    print course_num + " " + title
                    course_dict[course_num] = CourseRecord(self.get_storage_format(course_num, title, url, self.getDescription(url)))

        for k, record in [(k,course_dict[k]) for k in sorted(course_dict.keys())]:
            self.count += 1
            self.write_db(f, k, record.get_title().strip(), record.get_url().strip(), record.get_describe().strip())

        self.close_db(f)
        if file_lines != self.count and self.count > 0:
            self.do_upgrade_db(file_name)
            print "before lines: " + str(file_lines) + " after update: " + str(self.count) + " \n\n"
        else:
            self.cancel_upgrade(file_name)
            print "no need upgrade\n"

    def getDept(self):
        r = requests.get("https://enr-apps.as.cmu.edu/open/SOC/SOCServlet/search")
        soup = BeautifulSoup(r.text); 
        for child in soup.find("select", id="dept").children:
            if str(child).strip() == "":
                continue
            key = str(child)[str(child).find('"') + 1 : str(child).find('"', str(child).find('"') + 1)]
            value = str(child)[str(child).find(">") + 1 : str(child).find("(")].replace("&amp;", "").replace("\n", "").strip()
            self.dept_dict[key] = value

    def doWork(self):
        self.getDept()
        for dept in self.dept_dict.keys():
            if dept == "CB" or dept == "CS" or dept == "HCI" or dept == "ISR" or dept == "LTI" or dept == "MLG" or dept == "ROB":
                self.processData(self.semester_list, dept)


start = CMUSpider();
start.doWork()
