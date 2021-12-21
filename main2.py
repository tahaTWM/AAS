from pyzbar.pyzbar import decode
import cv2
import time

from datetime import datetime
import pandas as pd
import xlsxwriter


def AAS():
    video = cv2.VideoCapture(0)
    studentName = []
    studentTime = []
    studentAll = []

    now = datetime.now()
    today = now.strftime("%d_%m_%Y-%H_%M")

    print("Today's date: {}".format(today))

    def readData():
        data = pd.read_excel("stuent.xlsx", "Sheet1")
        names = data["Names"].values.tolist()
        dept = data["Department"].values.tolist()
        return names, dept

    def writeData():
        workbook = xlsxwriter.Workbook("{}.xlsx".format(today))
        worksheet = workbook.add_worksheet()

        row = 1
        worksheet.write_column(0, 0, ["Names"])
        worksheet.write_column(0, 1, ["Times"])
        for col, data in enumerate(studentAll):
            worksheet.write_column(row, col, data)

        workbook.close()

    names, dept = readData()
    while True:
        check, frame = video.read()
        dcode = decode(frame)

        try:
            for obj in dcode:
                name = dcode[0].data.decode()
                if name not in names:
                    print("Not found, this Student is from this Department")
                if name in names:
                    studentName.append(name)
                    studentTime.append(today)
                    print("add is done")
                    time.sleep(1)

        except:
            print("error")

        cv2.imshow("Attendance", frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            print("Stopped")
            studentAll.append(studentName)
            studentAll.append(studentTime)
            if len(studentAll) > 2:
                writeData()
            break

    video.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    AAS()