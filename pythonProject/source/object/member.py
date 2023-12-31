# coding=utf-8

import sys
import requests
import json

import pandas as pd
import common_information as info
import logger_factory as log

class Member:

    def __init__(self, common_info):
        self.common_info = common_info

    # Dooray에서 제공하는 고유정보를 DB Member정보에 붙이는 부분
    def db_add_member_info(self):

        dataframe = self.common_info.get_db_info()
        member = self.common_info.get_member_info()

        member_id = [0] * len(dataframe)

        for i in range(len(dataframe)):
            for j in range(len(member)):
                if dataframe['Emp_No'][i] == member[j]['displayMemberId']:
                    member_id[i] = member[j]['id']
                    break
                else:
                    continue

        se = pd.Series(member_id)
        dataframe['Member_ID'] = se

        self.common_info.set_db_info(dataframe)

        return dataframe

    # Dooray에서 제공하는 고유정보를 DB Job정보에 붙이는 부분
    def db_add_job_info(self):

        dataframe = self.common_info.get_db_info()

        job = self.common_info.get_job_info()

        job_id = [0] * len(dataframe)

        for i in range(len(dataframe)):
            for j in range(len(job)):
                if dataframe['Code_NM'][i] == job[j]['name']:
                    job_id[i] = job[j]['id']
                    break
                else:
                    continue

        se = pd.Series(job_id)
        dataframe['JOB_ID'] = se

        self.common_info.set_db_info(dataframe)

    # Dooray에서 제공하는 고유정보를 API Job정보에 붙이는 부분
    def api_add_job_info(self):
        api_member = pd.DataFrame(self.common_info.get_member_info())

        job_id = []
        for add in api_member['additional']:
            job_id.append(add['jobRankId'])

        #api_member['additional'] = api_member['additional']

        api_member = api_member[['name', 'user_Code', 'department', 'displayMemberId', 'id']].rename(columns={'name': 'User_NM', 'userCode': 'User_ID', 'department': 'User_Dept',
                                    'displayMemberId': 'Emp_No', 'id': 'Member_ID'})

        api_member['JOB_ID'] = job_id

        self.common_info.set_api_info(api_member)

    # 직급을 업데이트하는 부분
    def put_job_rank(self):

        # No. [0] -> Changed job.
        # No. [1] -> Changed dept.
        # No. [2] -> Add new member.

        changed = self.common_info.get_diff_info()[0]

        for change in changed:
            try:
                data = {
                    "additional": {
                        "jobRankId": "{}".format(change[4])
                    }
                }

                put_job_pos = requests.put(
                    info.MEMBERS_URL + "/{}".format(change[3]), json=data,
                    headers=info.HEADER, verify=False)

                if put_job_pos.status_code == 200 :
                    log.LoggerFactory._LOGGER.info(u'[Success] : {}\'s job-position has been changed.'.format(change[1]))
                else:
                    log.LoggerFactory._LOGGER.info(u'[Fail - {} ] : {} job-position failed to update.'.format(put_job_pos.status_code, change[1]))

                sys.stdout.write("{} {} \n".format(change[1].encode('utf-8'), put_job_pos.status_code))

            except Exception as e:
                log.LoggerFactory._LOGGER.info(u'{}'.format(e))
                sys.stdout.write("{}".format(e))

    # 새로운 Member를 업데이트하는 부분
    def post_additional_member(self):

        # No. [0] -> Changed job.
        # No. [1] -> Changed dept.
        # No. [2] -> Add new member.

        changed = self.common_info.get_diff_info()[2]

        for change in changed:
            print(change)
            try:
                data = {
                    "idProviderType": "service",
                    "name": "{}".format(change[1].encode('utf-8')),
                    "userCode": "{}".format(change[2]),
                    "displayMemberId": "{}".format(change[0]),
                    "password": "1234"
                }

                post_member = requests.post(
                    info.MEMBERS_URL, json=data,
                    headers=info.HEADER, verify=False)


                if post_member.status_code == 200 :
                    change[3] = "{}".format(post_member.json()['result']['id'])
                    log.LoggerFactory._LOGGER.info(u'[Success] : {} has been newly added.'.format(change[1]))
                else:
                    log.LoggerFactory._LOGGER.info(u'[Fail - {} ] : {} member failed to add.'.format(post_member.status_code, change[1]))

                sys.stdout.write("{} {} POST MEMBER\n".format(change[1].encode('utf-8'), post_member.status_code))

            except Exception as e:
                log.LoggerFactory._LOGGER.info(u'Error Code : {}'.format(e))
                sys.stdout.write("{}".format(e))

            try:
                data = {
                    "additional": {
                        "jobRankId": "{}".format(change[4])
                    }
                }

                put_job_pos = requests.put(
                    info.MEMBERS_URL + "/{}".format(change[3]), json=data,
                    headers=info.HEADER, verify=False)

                if put_job_pos.status_code == 200 :
                    log.LoggerFactory._LOGGER.info(u'[Success] : {}\'s job-position has been changed.'.format(change[1]))
                else:
                    log.LoggerFactory._LOGGER.info(u'[Fail - {} ] : {} job-position failed to update.'.format(put_job_pos.status_code, change[1]))

                sys.stdout.write("{} {} PUT JOB_POS\n".format(change[1].encode('utf-8'), put_job_pos.status_code))

            except Exception as e:
                log.LoggerFactory._LOGGER.info(u'Error Code : {}'.format(e))
                sys.stdout.write("{}".format(e))

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

                sys.stdout.write("{} {} PUT DEPT\n".format(change[1].encode('utf-8'), put_dept.status_code))

            except Exception as e:
                log.LoggerFactory._LOGGER.info(u'Error Code : {}'.format(e))
                sys.stdout.write("{}".format(e))

    def add_update(self):
        self.db_add_member_info()
        self.db_add_job_info()
        self.api_add_job_info()

    def put_update(self):
        self.put_job_rank()
