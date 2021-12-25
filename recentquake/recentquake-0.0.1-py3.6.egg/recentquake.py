import pandas as pd
import subprocess as sp
from IPython.display import display
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
from datetime import timedelta
import webbrowser
import os
import folium

class main:

  def main(self,ecountry="India",magp=1.0,magl=7.0):
      sp.call('wget https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv',shell=True)
      df = pd.read_csv('all_month.csv')

      for i in range(len(df)):
        if not  ', ' in df.loc[i,'place']:
          df.loc[i,'country']=df.loc[i,'place']
        else:
          target = ', '
          s=df.loc[i,'place']
          idx = s.find(target)
          r = s[idx+2:]
          df.loc[i,'country']=r

      list_dt=[]
      for i in range(len(df)):
          dt=datetime.datetime(int(str(df['time'][i])[0:4]),int(str(df['time'][i])[5:7]),int(str(df['time'][i])[8:10]))
          list_dt.append(dt)
      df['today']=list_dt
      df['year'] = df['today'].dt.year
      df['month'] = df['today'].dt.month
      df['day'] = df['today'].dt.day

      dfd=df[~df.duplicated(subset='country')]
      print('country_list')
      country_list = list(dfd.country)
      print(country_list)

      df=df[df.country==ecountry]
      df=df[(df['mag']  >  magp) & (df['mag'] < magl)]
      
      last_month_min = df[(df['month']==df['month'].min())].day.min()
      last_month_max = df[(df['month']==df['month'].min())].day.max()
      pre_month_min = df[(df['month']==df['month'].max())].day.min()
      pre_month_max = df[(df['month']==df['month'].max())].day.max()

      try:
        par_today = []
        for i in range(last_month_min, last_month_max+1):
            par_today.append(len(df.query("month=={} & day=={}".format(df.month.min(),i))))
        for i in range(pre_month_min, pre_month_max+1):
            par_today.append(len(df.query("month=={} & day=={}".format(df.month.max(),i))))
      except:
        print('データがありませんでした')
      
      # 日付のリスト生成()
      date_list = [df['today'].min() + timedelta(days=i) for i in range(len(par_today))]
      # 文字列に変換
      date_str_list = [d.strftime("%Y-%m-%d") for d in date_list]

      print('データ数 : ', len(df))
      #display(df)

      df=df.reset_index(drop=True)

      center_lat=df.latitude.median()
      center_lon=df.longitude.median()
      map = folium.Map(location=[center_lat, center_lon], zoom_start=5)
      for i in range(0,len(df)):
        folium.Marker(location=[df["latitude"][i],df["longitude"][i]]).add_to(map)
      map.save("output.html")

      pa=os.getcwd()
      url = "file:{}/output.html".format(pa)
      webbrowser.open_new_tab(url) 

      fig, axes = plt.subplots(2, 2, figsize=(20, 8))
      left = date_str_list
      height = par_today
      sns.boxplot(data=df, x='mag',ax=axes[0,0])
      sns.histplot(data=df, x='mag',ax=axes[0,1])
      sns.scatterplot(data=df, x='mag', y='depth',ax=axes[1,0])
      plt.xticks(rotation=90)
      axes[1,1].bar(left, height)
      plt.show()

      #def earthquake_map(self, dfm):
      
      sp.call("rm all_month.csv output.html",shell=True)
      

ecountry=str(sys.argv[1])
magp=float(sys.argv[2])
magl=float(sys.argv[3])

m=main()  
m.main(ecountry,magp,magl)
