from pyzbar.pyzbar import decode  # decode QrCode in each Frame

import cv2  # Use this package to use camera that connect to system

import time  # buildIn class to make application sleep (delay)

from datetime import datetime  # buildIn class to get current system time

import pandas as pd  # use this package to deal with files (open and manipulate)

import xlsxwriter  # use this package to write data exel sheet


def AAS():  # main function of the application

    video = cv2.VideoCapture(0)  # 0 for selecting the build web camera
    
    studentName = []  # list of student signIn time
    studentTime = []  # list of student that signIn
    studentAll = []  # mix students names withe time to store it.

    now = datetime.now()  # get current system time
    today = now.strftime("%d_%m_%Y-%H_%M")  # format system time to (24_12_2021-11_14)

    print("Today's date: {}".format(today))

    def readData():  # read students data form exel sheet
        data = pd.read_excel("students.xlsx", "Sheet1")
        names = data["Names"].values.tolist()
        dept = data["Department"].values.tolist()
        return names, dept

    def writeData():  # write or storing data to exel sheet
        if len(studentName) > 0:
            workbook = xlsxwriter.Workbook("{}.xlsx".format(today))
            worksheet = workbook.add_worksheet()

            # adding header or first row of exel sheet like ---  Names   Times --- in next 2 line
            worksheet.write_column(0, 0, ["Names"])
            worksheet.write_column(0, 1, ["Times"])

            studentAll.append(studentName)
            studentAll.append(studentTime)
            print(studentAll)

            row = 1  # starting in second row in exel sheet
            for col, data in enumerate(studentAll):
                worksheet.write_column(row, col, data)

            workbook.close()

    names, dept = readData()
    while True:
        check, frame = video.read()
        dcode = decode(frame)
        try:
            for items in dcode:
                name = items[0].decode()
                # jsonLoad = json.loads(name)
                # print(jsonLoad['name'])

                if name not in names:
                    print(
                        f"{name}{', Is Not found in this Students of this Department'}"
                    )
                    time.sleep(3)
                if name in names:
                    studentName.append(name)
                    studentTime.append(today)
                    print("add is done")
                    print(studentName)
                    time.sleep(3)

        except:
            print("error")

        cv2.imshow("Attendance", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            print("Stopped")
            writeData()
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    AAS()
