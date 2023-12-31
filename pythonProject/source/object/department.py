# coding=utf-8

import sys
import requests
import pandas as pd
import common_information as info
import logger_factory as log

class Department:

    def __init__(self, common_info):
        self.common_info = common_info

    # 부서를 업데이트 하는 부분
    @staticmethod
    def make_dept(level_df):

        departments = []

        for i in range(1, len(level_df)):
            if int(level_df['Level'][i]) == 1:

                element = {
                    "externalKey": "{}".format(level_df['Dept'][i]),
                    "name": "{}".format(level_df['DeptName'][i].encode('utf-8'))
                }

            elif int(level_df['Level'][i]) == 2:
                if level_df['Dept'][i] == "Dept_1826" or level_df['Dept'][i] == "Dept_2912":
                    continue

                element = {
                    "externalKey": "{}".format(level_df['Dept'][i]),
                    "name": "{}".format(level_df['DeptName'][i].encode('utf-8')),
                    "parentDepartmentExternalKey": "{}".format(level_df['ParDept'][i]),
                    "displayOrder": "{}".format(level_df['ViewOrder'][i]),
                }

            else:
                element = {
                    "externalKey": "{}".format(level_df['Dept'][i]),
                    "name": "{}".format(level_df['DeptName'][i].encode('utf-8')),
                    "parentDepartmentExternalKey": "{}".format(level_df['ParDept'][i]),
                    "displayOrder": "{}".format(level_df['ViewOrder'][i]),
                }

            departments.append(element)

        json_body = {
            "departments": departments
        }

        post_response = requests.post(info.ORGANIZATIONS_URL, json=json_body, headers=info.HEADER_TEST, verify=False)

        sys.stdout.write("Function : Make Dept Result, Status Code : {} \n".format(post_response.status_code))

    # Dooray 측에서 보내는 개별 ID를 기존의 정보에 덧붙이는 부분
    def add_dept_id(self):

        db_dataframe = self.common_info.get_db_info()
        api_dataframe = self.common_info.get_api_info()

        dept = self.common_info.get_dept_info()

        db_dataframe.loc[db_dataframe['UserState'] == "0050", 'UserDept'] = u'휴직'
        db_dataframe.loc[db_dataframe['UserState'] == "0060", 'UserDept'] = u'파견'

        db_dept_id = [0] * len(db_dataframe)
        api_dept_id = [0] * len(api_dataframe)

        for i in range(len(db_dataframe)):
            for j in range(len(dept)):
                if db_dataframe['User_Dept'][i] == dept[j]['name']:
                    db_dept_id[i] = dept[j]['id']
                    break

        for i in range(len(api_dept_id)):
            for j in range(len(dept)):
                if api_dataframe['User_Dept'][i] == dept[j]['name']:
                    api_dept_id[i] = dept[j]['id']
                    break

        db_se = pd.Series(db_dept_id)
        db_dataframe['Dept_ID'] = db_se

        api_se = pd.Series(api_dept_id)
        api_dataframe['Dept_ID'] = api_se

        self.common_info.set_db_info(db_dataframe)
        self.common_info.set_api_info(api_dataframe)

    # 부서를 업데이트하는 부분
    def put_dept_to_member(self):

        # No. [0] -> Changed job.
        # No. [1] -> Changed dept.
        # No. [2] -> Add new member.

        changed = self.common_info.get_diff_info()[1]

        for change in changed:
            try:
                data = [{
                    "departmentId": "{}".format(change[5]),
                }]

                put_dept = requests.put(
                    info.MEMBERS_URL + "/{}/departments".format(change[3]), json=data,
                    headers=info.HEADER, verify=False)

                if put_dept.status_code == 200 :
                    log.LoggerFactory._LOGGER.info(u'[Success] : {}\'s department has been changed.'.format(change[1]))
                else:
                    log.LoggerFactory._LOGGER.info(u'[Fail - {} ] : {} department failed to update.'.format(put_dept.status_code, change[1]))

                sys.stdout.write("{} {} \n".format(change[1].encode('utf-8'), put_dept.status_code))

            except Exception as e:
                log.LoggerFactory._LOGGER.info(u'{}'.format(e))
                sys.stdout.write("{}".format(e))

    def add_update(self):
        self.add_dept_id()

    def put_update(self):
        self.put_dept_to_member()

