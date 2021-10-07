import requests
import lxml.html as html
import pandas as pd
import datetime

# get url content

url = 'https://www.myfitness.ee/liitumine-ja-hinnad/myfitness-klubide-taituvus/'

page = requests.get(url)
content = html.fromstring(page.content)

tr_elements = content.xpath('/html/body/div[3]/section[1]/div[2]/div/div/div/div/table')

# parse content

raw_data = tr_elements[0].text_content().splitlines()
parsed_data = []

for i in raw_data:
    if '   ' in i:
        item = i.strip()
        if len(item) > 0:
            parsed_data.append(item)

data_dict = {
    'Venue:' : [],
    'Capacity:' : [],
    'Timestamp:': []
}

for i in parsed_data[1::2]:
    data_dict['Venue:'].append(i)
    data_dict['Timestamp:'].append(datetime.datetime.utcnow())

for i in parsed_data[0::2]:
    data_dict['Capacity:'].append(i)

# union output

data_table = pd.DataFrame(data_dict)

prev_output = pd.read_csv('output.csv')

prev_output[['Venue:','Capacity:','Timestamp:']]

output = pd.concat([prev_output,data_table],ignore_index=True)

#data_table.to_csv('output.csv',index=False)

output.to_csv('output.csv',index=False)

# transform output

datetime_raw = output
datetime_raw['tz_hour'] = datetime_raw['Timestamp:'].apply(lambda x: pd.to_datetime(x).tz_localize('UTC').tz_convert('Asia/Tel_Aviv').hour)
datetime_raw['tz_wkd'] = datetime_raw['Timestamp:'].apply(lambda x: pd.to_datetime(x).tz_localize('UTC').tz_convert('Asia/Tel_Aviv').weekday())
datetime_raw['Capacity:'] = datetime_raw['Capacity:'].apply(lambda x: float(x.strip('%'))/100)
datetime_raw.head()

datetime_raw.rename(columns={
    'Venue:' : 'venue',
    'Capacity:': 'cap'},
    inplace=True)

datetime_raw = datetime_raw[['venue','tz_wkd','tz_hour','cap']]
datetime_gp = datetime_raw.groupby(['venue','tz_wkd','tz_hour'], as_index=False).mean()
datetime_gp_hour = datetime_raw.groupby(['venue','tz_hour'], as_index=False).mean()

datetime_gp_hour.to_csv('/home/rainermesi/Documents/myfitness_capacity/group_by_hour.csv',index=False)

def chunks(L,n):
    return_list = []
    for i in range(0,len(L),n):
        return_list.append(L[i:i+n])
    return return_list

venues_list = chunks(datetime_gp_hour.venue.unique(),3)
pd.DataFrame(venues_list).to_csv('venues_list.csv',index=False)

