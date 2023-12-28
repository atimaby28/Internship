# coding=utf-8
import pymssql
import pass_decrypt

# 보안을 위해 임의의 값으로 대치 및 치환 그리고 변환하였습니다.
HOST = "173.15.15.1"
PORT = 1443
USER = "dooray_user"
PASSWORD = pass_decrypt.dec_conn()
DB = "HWFVer01"
CHARSET = "UTF8"


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance

@singleton
class Database:
    def __init__(self):
        self.conn = pymssql.connect(
            server=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DB,
            charset=CHARSET
        )

    def dept_select(self):
        try:
            cursor = self.conn.cursor()
            query = "SELECT Org_CD, ParOrg_CD, Org_NM, View_Order FROM FIS_Org WHERE state = 50"

            cursor.execute(query)
            result = cursor.fetchall()

            return result

        except Exception as e:
            print(e)

    def member_select(self):
        try:
            cursor = self.conn.cursor()
            query = "SELECT u.User_NM, g.Code_NM, u.Login_ID, o.Org_NM, uo.Emp_No, uo.Org_CD, tuo.State FROM (((HWFVer01.dbo.FIS_User as u JOIN HWFVer01.dbo.FIS_User_Org as uo ON u.User_CD = uo.User_CD) JOIN HWFVer01.dbo.FIS_Org as o ON uo.Org_CD = o.Org_CD) JOIN HWFVer01.dbo.FIS_Grade_Duty as g ON uo.Duty = g.Code) JOIN HWFVer01.dbo.KPFIS_User_Org as tuo ON tuo.Emp_No = uo.Emp_No WHERE uo.Emp_No != '' AND tuo.Major_Flag = 'M' AND uo.Major_Flag = 'M' AND tuo.State != 50 AND g.Group_CD = 'Duty'"
            cursor.execute(query)
            result = cursor.fetchall()

            return result

        except Exception as e:
            print(e)

    def close(self):
        self.conn.close()
