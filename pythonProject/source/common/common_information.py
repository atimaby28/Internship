import requests
import pass_decrypt
import pandas as pd
import msdatabase as md

# 보안을 위해 특정 번호와 변수를 대치 및 변환하였습니다.
MEMBERS_URL = "https://admin-api.gov-dooray.com/admin/v1/members"
DEPARTMENT_URL = "https://admin-api.gov-dooray.com/admin/v1/departments"
JOBRANK_URL = "https://admin-api.gov-dooray.com/admin/v1/job-ranks"
ORGANIZATIONS_URL = "https://admin-api.gov-dooray.com/admin/v1/organizations/2756171254504278673/departments/organize"

HEADER = {
    "Authorization": "dooray-api {}".format(pass_decrypt.dec_dooray())
}

HEADER_TEST = {
    "Authorization": "dooray-api {}".format(pass_decrypt.dec_dooray_test())
}

def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class CommonInfo:

    def __init__(self):
        self.db_info = pd.DataFrame(md.Database().member_select(), columns=['User_NM', 'Code_NM', 'User_ID', 'User_Dept', 'Emp_No', 'Dept_ID', 'User_State'])
        self.api_info = [[]]
        self.member_api_info = requests.get(MEMBERS_URL + "?page=0&size=400", headers=HEADER, verify=False).json()['result']
        self.dept_api_info = requests.get(DEPARTMENT_URL + "?page=0&size=50", headers=HEADER, verify=False).json()['result']
        self.job_api_info = requests.get(JOBRANK_URL + "?page=0&size=50", headers=HEADER, verify=False).json()['result']
        self.diff_info = []


    def get_db_info(self):
        return self.db_info

    def set_db_info(self, db_info):
        self.db_info = db_info

    def get_api_info(self):
        return self.api_info

    def set_api_info(self, api_info):
        self.api_info = api_info

    def get_member_info(self):
        return self.member_api_info

    def set_member_info(self, member_api_info):
        self.member_api_info = member_api_info

    def get_dept_info(self):
        return self.dept_api_info

    def set_dept_info(self, dept_api_info):
        self.dept_api_info = dept_api_info

    def get_job_info(self):
        return self.job_api_info

    def set_job_info(self, job_api_info):
        self.job_api_info = job_api_info

    def get_diff_info(self):
        return self.diff_info

    def set_diff_info(self, diff_info):
        self.diff_info = diff_info

    def save_info(self):
        dataframe = pd.DataFrame(self.get_db_info())
        dataframe.to_csv("save/INFORMATION_SAVE.csv", encoding="utf-8")



