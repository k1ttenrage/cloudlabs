import boto3
import pandas as pd
import matplotlib.pyplot as plt

def getdata(start='1/1/2021', end='12/31/2021'):
    df = pd.DataFrame({"date":[], 'USD':[], 'EUR':[]})
    dates = pd.Series(pd.date_range(start='1/1/2021', end='12/31/2021', freq='d'))
    dates = dates.dt.strftime('%Y%m%d')
    for date in dates:
        df_t = pd.read_json(f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={date}&json')
        df_t = pd.DataFrame({"date":df_t[df_t['cc']=="USD"]['exchangedate'].values, 'USD':df_t[df_t['cc']=="USD"]['rate'].values, 'EUR':df_t[df_t['cc']=="EUR"]['rate'].values})
        df = pd.concat([df,df_t], axis=0)
    df = df.reset_index(drop=True)
    df.to_csv("data.csv", index=False)
    df.plot(x='date', y=['USD', 'EUR'], figsize=(15, 7), title="UAH currency", fontsize=12)
    plt.savefig('plot.png')

def s3_upload(filename, backetname):
    s3 = boto3.client('s3')
    with open(filename, "rb") as f:
        s3.upload_fileobj(f, backetname, filename)

def s3_download(filename, backetname):
    s3 = boto3.client('s3')
    s3.download_file(backetname, filename, filename)

s3 = boto3.client('s3')
results = s3.list_objects(Bucket='kittenragelab2', Prefix='data.csv')

try:
    s3_download('data.csv', 'kittenragelab2')
    s3_download('plot.png', 'kittenragelab2')
except:
    getdata()
    s3_upload('data.csv', 'kittenragelab2')
    s3_upload('plot.png', 'kittenragelab2')