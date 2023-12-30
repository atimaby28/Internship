# coding=utf-8

exception = {}

# 비교를 통해 변화값을 알아내는 부분
class Difference:

    def __init__(self, common_info):
        self.common_info = common_info

    def dept_diff(self):

        old_data = self.common_info.get_api_info()
        new_data = self.common_info.get_db_info()

        old_dict = {}
        for i in range(len(old_data['EmpNo'])):
            old_dict[old_data['EmpNo'][i]] = [old_data['EmpNo'][i], old_data['UserNM'][i], old_data['UserID'][i],
                                              old_data['Member_ID'][i], old_data['JOB_ID'][i], old_data['Dept_ID'][i]]

        new_dict = {}
        for i in range(len(new_data['EmpNo'])):
            new_dict[new_data['EmpNo'][i]] = [new_data['EmpNo'][i], new_data['UserNM'][i], new_data['UserID'][i],
                                              new_data['Member_ID'][i], new_data['JOB_ID'][i], new_data['Dept_ID'][i]]

        changed = []

        changed_job = []
        changed_dept = []
        new_member = []

        for key, value in new_dict.items():
            if new_dict[key][0] in exception:
                continue

            try:
                if old_dict[key][4] != value[4] and old_dict[key][5] != value[5]:
                    changed_job.append(value)
                    changed_dept.append(value)
                elif old_dict[key][4] != value[4]:
                    changed_job.append(value)
                elif old_dict[key][5] != value[5]:
                    changed_dept.append(value)
                else:
                    continue

            except Exception as e:
                if key is u'':
                    continue

                # <사번 + *> 를 통해 예외처리 해야 할 인원이 있는지 확인하는 부분
                try:
                    if old_dict[key + '*'][2] == new_dict[key][2]:
                        continue
                except Exception as e:
                    new_member.append(value)

        changed.append(changed_job)
        changed.append(changed_dept)
        changed.append(new_member)

        self.common_info.set_diff_info(changed)

        return changed




