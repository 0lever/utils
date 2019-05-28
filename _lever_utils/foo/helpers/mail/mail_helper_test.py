# -*- coding:utf-8 -*-

from mail_helper import MailServer
import time

# pip install --upgrade 0lever-utils -i https://pypi.org/simple/


def test():
    ms = MailServer('smtp.exmail.qq.com', 'xx@xx.com', '')
    # 获取最新邮件序号
    print ms.get('stat')
    # 获取序号list
    print ms.get('list')
    # 指定序号获取邮件
    print ms.get(1, 2, ms.get('stat')['stat'])

    last_mail_info = ""

    while True:
        # 获取最新一封邮件
        result = ms.get('latest')
        latest_result = result["latest"]

        tmp = latest_result["Date"] + latest_result["Subject"]
        if tmp != last_mail_info:
            print "-----------------" * 10
            print "Subject:\n\t",
            print latest_result["Subject"]
            print "Date:\n\t",
            print latest_result["Date"]
            print "From:\n\t",
            print latest_result["From"]
            print "To:\n\t",
            print latest_result["To"]
            print "Cc:\n\t",
            print latest_result["Cc"]
            print "Files:\n",
            latest_result_files = latest_result["Files"]
            for latest_result_file in latest_result_files:
                print "\t" + latest_result_file["name"]
                # with open("/Users/chaoyang/tmp/"+latest_result_file["name"], 'w') as f:
                #     f.write(latest_result_files[0]["data"])
            print "Bodys:\n",
            latest_result_bodys = latest_result["Bodys"]
            for latest_result_body in latest_result_bodys:
                print "\t", "xxx"
                # print latest_result_body["body"]
        last_mail_info = tmp
        time.sleep(2)

    ms.quit()


if __name__ == '__main__':
    # test()
    pass