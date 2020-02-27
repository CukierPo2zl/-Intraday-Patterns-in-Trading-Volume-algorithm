import pandas as pd
import settings
headers = ["company", "zero1", "date", "hour", "value1", "value2", "value3", "value4", "volume", "zero"]
data = pd.read_csv('assets/PKOBP/PKOBP.prn', sep=",", names=headers)

data.pop("company")
data.pop("zero1")
data.pop("value1")
data.pop("value2")
data.pop("value3")
data.pop("value4")
data.pop("zero")

start = data['date'] >= settings.STARTDATE
end = data['date'] <= settings.ENDDATE
data = data[start & end]
data = data.reset_index(drop=True)

DATA_LEN = len(data)
f = open(settings.OUTDIR+'info.txt', "a")
f.write("liczba transakcji w okresie: "+str(DATA_LEN))
f.close()

def get_table(curr_date, curr_hour):
    start = data['date'] == curr_date
    tmp = data[start]
    if (str(curr_hour)[0:1] == '9'):
        _filter = tmp['hour'].astype(str).str.startswith(str(curr_hour)[0:1])
    else:
        _filter = tmp['hour'].astype(str).str.startswith(str(curr_hour)[0:2])
    tmp = tmp[_filter]
    return tmp

def get_volume(curr_date, curr_hour):
    final = 0
    tmp = get_table(curr_date, curr_hour)
    tmp = tmp.reset_index(drop=True)
    for i in range(len(tmp)):
        final +=tmp.loc[i,'volume']
    return final

def mainv():
    index = 0
    dates = []
    hours = []
    volumes = []

    while(index != len(data)):
        print(index)
        _date = data.loc[index, 'date']
        _hour = data.loc[index, 'hour']

        dates.append(_date)

        if (str(_hour)[0:1] == '9'):
            hours.append(str(_hour)[0:1])
        else:
            hours.append(str(_hour)[0:2])
        
        volumes.append(get_volume(_date, _hour))

        index = (get_table(_date, _hour).index[-1]) + 1
    
    d = {'date':dates, 'hour': hours, 'volume': volumes}
    frame = pd.DataFrame(data=d)

    frame.to_excel('assets/result.xlsx') 

def test():
    pass

if __name__ == '__main__':
    mainv()
    

