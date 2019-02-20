import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import codecademylib3_seaborn
import glob

files_glob = glob.glob('states*.csv')
dfs_files = [pd.read_csv(file) for file in files_glob]
us_census = pd.concat(dfs_files)
print(us_census.head())
print(us_census.columns)


us_census.Income = us_census.Income.replace('[\$,]','',regex=True)
us_census.Income = pd.to_numeric(us_census.Income)
#print(us_census.dtypes)

gender_adjust = us_census.GenderPop.str.split('_')
us_census['Men'] = gender_adjust.str.get(0)
us_census['Women'] = gender_adjust.str.get(1)
#print(us_census.head(2))
us_census.Men = pd.to_numeric(us_census.Men.replace('M','', regex=True))

us_census.Women = pd.to_numeric(us_census.Women.replace('F', '', regex=True))
#print(us_census.head(2))
#print(us_census.Men.dtype)

us_census = us_census.fillna(value = {'Women': us_census.TotalPop - us_census.Men})
#print(us_census.Women)

cen_dups = us_census.duplicated()
print(cen_dups.value_counts())
us_census.drop_duplicates(inplace=True)

#Scatter Plot
plt.scatter(us_census.Women, us_census.Income)
plt.xlabel('Women Population')
plt.ylabel("Income")
plt.show()

#Removal of % signs
race_lst = us_census.columns[3:9]
for race in race_lst:
  us_census[race] = pd.to_numeric(us_census[race].replace('[\%,]','', regex=True))
  
us_census = us_census.fillna(value = {'Hispanic': us_census.Hispanic.mean(),'White':us_census.White.mean(),'Native': us_census.Native.mean(), 'Asian': us_census.Asian.mean(), 'Pacific':us_census.Pacific.mean()})

#Histogram
#plt.close('all')
for race in race_lst:
  plt.figure()
  plt.xlabel(race)
  plt.hist(us_census[race], bins = 20)
  plt.show()
