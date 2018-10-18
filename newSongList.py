#coding:utf-8
import csv
import datetime
from collections import OrderedDict
from getMonth import getMonth

throwBack = 10 #type: int
end = datetime.date.today() #type: datetime.date
begin = end - datetime.timedelta(days = throwBack) #type: datetime.date

f = open("./rowdata/latest.csv", "r", encoding = "utf-8")
dataReader = csv.reader(f)

archive = [] #type: List[artist: str, song: str, album: str]
time = [] #type: List[datetime.date]
songDate = OrderedDict() #type: OrderedDict{name:str, time:datetime.date}
songArtist = {} #type: dict{name: str, List[artist: str, album: str]}
newSongList = [] #type: List[artist: str, song: str]

for row in dataReader:
    t = row[3].split(" ")
    try:
        date = datetime.date(int(t[2]), getMonth(t[1]), int(t[0]))
        time.append(date)
        archive.append([str(row[0]), str(row[2]), str(row[1])])
    except (IndexError, TypeError): #稀に時刻が取得されていない時がある
        pass

archive.reverse(); time.reverse();
sub = 0 #type: int

for data in archive:
    if (not data[1] in songDate):
        songDate[data[1]] = time[sub]
    if (not data[1] in songArtist):
        songArtist[data[1]] = [data[0], data[2]]
    sub += 1

while True:
    s, t = songDate.popitem(last = True)
    if t > begin:
        newSongList.append([songArtist[s][0], songArtist[s][1], s])
    else:
        break

f = open("./output/output.csv", "w", encoding = "utf-8")
writer = csv.writer(f, lineterminator = "\n")
for row in newSongList:
    writer.writerow(row)
f.close()
