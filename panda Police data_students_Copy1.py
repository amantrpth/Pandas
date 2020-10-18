
# coding: utf-8

# In[2]:


import pandas as pd
pd.__version__


# In[3]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# # Dataset: Stanford Open Policing Project
# 

# In[4]:


import pandas as pd


# In[5]:


# ri stands for Rhode Island
ri = pd.read_csv('D:\DATA SCIENCE\python\DataScience\python al docs\Slack_Docs\CSVs Data Set/police.csv') 


# In[6]:


# what does each row represent?
ri.head()


# In[7]:


# what do these numbers mean?
ri.shape 


# In[8]:


# what do these types mean?
ri.dtypes


# - What does NaN mean?
# - Why might a value be missing?
# - Why mark it as NaN? Why not mark it as a 0 or an empty string or a string saying "Unknown"?

# In[9]:


# what are these counts? how does this work?
ri.isnull().sum()


# In[10]:


2 == True


# In[11]:


(True == 1) and (False == 0)


# ## 1. Remove the column that only contains missing values

# In[12]:


# axis=1 also works, inplace is False by default, inplace=True avoids assignment statement
ri.drop('county_name', axis='columns', inplace=True)


# In[13]:


ri.shape


# In[14]:


ri.columns


# In[15]:


# alternative method
ri.dropna(axis='columns', how='all').shape


# Lessons:
# 
# - Pay attention to default arguments
# - Check your work
# - There is more than one way to do everything in pandas

# ## 2. Do men or women speed more often? 

# In[16]:


# when someone is stopped for speeding, how often is it a man or woman?
ri[ri.violation == 'Speeding'].driver_gender.value_counts(normalize=True)*100


# In[17]:


# alternative
ri.loc[ri.violation == 'Speeding', 'driver_gender'].value_counts(normalize=True)


# In[18]:


# when a man is pulled over, how often is it for speeding?
ri[ri.driver_gender == 'M'].violation.value_counts(normalize=True, dropna = False)


# In[19]:


# repeat for women
ri[ri.driver_gender == 'F'].violation.value_counts(normalize=True, dropna = False)


# In[20]:


# combines the two lines above
ri.groupby('driver_gender').    violation.    value_counts(normalize=True).index


# What are some relevant facts that we don't know?
# 
# Lessons:
# 
# - There is more than one way to understand a question

# ## 3. Does gender affect who gets searched during a stop?

# In[21]:


# ignore gender for the moment
ri.search_conducted.value_counts(normalize=True)


# In[22]:


# how does this work?
ri.search_conducted.mean()


# In[23]:


# search rate by gender
ri.groupby('driver_gender').search_conducted.mean()


# Does this prove that gender affects who gets searched?

# In[24]:


# include a second factor
ri.groupby(['violation', 'driver_gender']).search_conducted.mean()


# Does this prove causation?
# 
# Lessons:
# 
# - Causation is difficult to conclude, so focus on relationships
# - Include all relevant factors when studying a relationship

# ## 4. Why is search_type missing so often?

# In[25]:


ri.isnull().sum()


# In[26]:


# maybe search_type is missing any time search_conducted is False?
ri.search_conducted.value_counts()


# In[27]:


# test that theory, why is the Series empty?
ri[ri.search_conducted == False].violation.value_counts()


# In[28]:


# value_counts ignores missing values by default
ri[ri.search_conducted == False].search_type.value_counts(dropna=False)


# In[29]:


# when search_conducted is True, search_type is never missing
ri[ri.search_conducted == True].search_type.value_counts(dropna=False)


# In[30]:


# alternative
ri[ri.search_conducted == True].search_type.isnull().sum()


# Lessons:
# 
# - Verify your assumptions about your data
# - pandas functions ignore missing values by default

# ## 5. During a search, how often is the driver frisked?

# In[31]:


# multiple types are separated by commas
ri.search_type.value_counts(dropna=False)


# In[33]:


# use bracket notation when creating a column
ri['frisk'] = ri.search_type == 'Protective Frisk'


# In[34]:


ri.frisk.dtype


# In[35]:


# includes exact matches only
ri.frisk.sum()


# In[36]:


# is this the answer?
ri.frisk.mean()


# In[37]:


# uses the wrong denominator (includes stops that didn't involve a search)
ri.frisk.value_counts()


# In[38]:


161 / (91580 + 161)


# In[39]:


# includes partial matches
ri['frisk'] = ri.search_type.str.contains('Protective Frisk')


# In[40]:


# seems about right
ri.frisk.sum()


# In[41]:


# frisk rate during a search
ri.frisk.mean()


# In[42]:


# str.contains preserved missing values from search_type
ri.frisk.value_counts(dropna=False)


# In[43]:


# excludes stops that didn't involve a search
274 / (2922 + 274)


# Lessons:
# 
# - Use string methods to find partial matches
# - Use the correct denominator when calculating rates
# - pandas calculations ignore missing values
# - Apply the "smell test" to your results

# ## 6. Which year had the least number of stops? 

# In[44]:


# this works, but there's a better way
ri.stop_date.str.slice(0, 4).value_counts()


# In[45]:


# make sure you create this column
combined = ri.stop_date.str.cat(ri.stop_time, sep=' ')
ri['stop_datetime'] = pd.to_datetime(combined)


# In[46]:


ri.dtypes


# In[47]:


# why is 2005 so much smaller?
ri.stop_datetime.dt.year.value_counts()


# Lessons:
# 
# - Consider removing chunks of data that may be biased
# - Use the datetime data type for dates and times

# ## 7. How does drug activity change by time of day?

# In[48]:


ri.drugs_related_stop.dtype


# In[49]:


# baseline rate
ri.drugs_related_stop.mean()


# In[50]:


# can't groupby 'hour' unless you create it as a column
ri.groupby(ri.stop_datetime.dt.hour).drugs_related_stop.mean()


# In[51]:


# line plot by default (for a Series)
ri.groupby(ri.stop_datetime.dt.hour).    drugs_related_stop.    mean().plot()


# In[52]:


# alternative: count drug-related stops by hour
ri.groupby(ri.stop_datetime.dt.hour).drugs_related_stop.sum().
\plot()


# Lessons:
# 
# - Use plots to help you understand trends
# - Create exploratory plots using pandas one-liners

# ## 8. Do most stops occur at night? 

# In[53]:


ri.stop_datetime.dt.hour.value_counts()


# In[54]:


ri.stop_datetime.dt.hour.value_counts().plot()


# In[55]:


ri.stop_datetime.dt.hour.value_counts().sort_index().plot()


# In[56]:


# alternative method
ri.groupby(ri.stop_datetime.dt.hour).stop_date.count().plot()


# Lessons:
# 
# - Be conscious of sorting when plotting

# ## 9. Find the bad data in the stop_duration column and fix it

# In[57]:


# mark bad data as missing
ri.stop_duration.value_counts()


# In[58]:


# what four things are wrong with this code?
# ri[ri.stop_duration == 1 | ri.stop_duration == 2].stop_duration = 'NaN'


# In[59]:


# what two things are still wrong with this code?
ri[(ri.stop_duration == '1') | (ri.stop_duration == '2')].stop_duration = 'NaN'


# In[60]:


# assignment statement did not work
ri.stop_duration.value_counts()


# In[61]:


# solves SettingWithCopyWarning
ri.loc[(ri.stop_duration == '1') | (ri.stop_duration == '2'), 'stop_duration'] = 'NaN'


# In[62]:


# confusing!
ri.stop_duration.value_counts(dropna=False)


# In[63]:


# replace 'NaN' string with actual NaN value
import numpy as np
ri.loc[ri.stop_duration == 'NaN', 'stop_duration'] = np.nan


# In[64]:


ri.stop_duration.value_counts(dropna=False)


# In[65]:


# alternative method
ri.stop_duration.replace(['1', '2'], value=np.nan, inplace=True)


# Lessons:
# 
# - Ambiguous data should be marked as missing
# - Don't ignore the SettingWithCopyWarning
# - NaN is not a string

# ## 10. What is the mean stop_duration for each violation_raw?

# In[66]:


# make sure you create this column
mapping = {'0-15 Min':8, '16-30 Min':23, '30+ Min':45}
ri['stop_minutes'] = ri.stop_duration.map(mapping)


# In[67]:


# matches value_counts for stop_duration
ri.stop_minutes.value_counts()


# In[68]:


ri.groupby('violation_raw').stop_minutes.mean()


# In[69]:


ri.groupby('violation_raw').stop_minutes.agg(['mean', 'count'])


# Lessons:
# 
# - Convert strings to numbers for analysis
# - Approximate when necessary
# - Use count with mean to looking for meaningless means

# ## 11. Plot the results of the first groupby from the previous exercise

# In[70]:


# what's wrong with this?
ri.groupby('violation_raw').stop_minutes.mean().plot()


# In[71]:


# how could this be made better?
ri.groupby('violation_raw').stop_minutes.mean().plot(kind='bar')


# In[72]:


ri.groupby('violation_raw').stop_minutes.mean().sort_values().plot(kind='barh')


# Lessons:
# 
# - Don't use a line plot to compare categories
# - Be conscious of sorting and orientation when plotting

# ## 12. Compare the age distributions for each violation

# In[73]:


# good first step
ri.groupby('violation').driver_age.describe()


# In[74]:


# histograms are excellent for displaying distributions
ri.driver_age.plot(kind='hist')


# In[75]:


# similar to a histogram
ri.driver_age.value_counts().sort_index().plot()


# In[76]:


# can't use the plot method
ri.hist('driver_age', by='violation')


# In[77]:


# what changed? how is this better or worse?
ri.hist('driver_age', by='violation', sharex=True)


# In[78]:


# what changed? how is this better or worse?
ri.hist('driver_age', by='violation', sharex=True, sharey=True)


# Lessons:
# 
# - Use histograms to show distributions
# - Be conscious of axes when using grouped plots

# ## 13. Pretend you don't have the driver_age column, and create it from driver_age_raw (and call it new_age)

# In[79]:


ri.head()


# In[80]:


# appears to be year of stop_date minus driver_age_raw
ri.tail()


# In[81]:


ri['new_age'] = ri.stop_datetime.dt.year - ri.driver_age_raw


# In[82]:


# compare the distributions
ri[['driver_age', 'new_age']].hist()


# In[83]:


# compare the summary statistics (focus on min and max)
ri[['driver_age', 'new_age']].describe()


# In[84]:


# calculate how many ages are outside that range
ri[(ri.new_age < 15) | (ri.new_age > 99)].shape


# In[85]:


# raw data given to the researchers
ri.driver_age_raw.isnull().sum()


# In[86]:


# age computed by the researchers (has more missing values)
ri.driver_age.isnull().sum()


# In[87]:


# what does this tell us? researchers set driver_age as missing if less than 15 or more than 99
5621-5327


# In[88]:


# driver_age_raw NOT MISSING, driver_age MISSING
ri[(ri.driver_age_raw.notnull()) & (ri.driver_age.isnull())].head()


# In[89]:


# set the ages outside that range as missing
ri.loc[(ri.new_age < 15) | (ri.new_age > 99), 'new_age'] = np.nan


# In[90]:


ri.new_age.equals(ri.driver_age)


# Lessons:
# 
# - Don't assume that the head and tail are representative of the data
# - Columns with missing values may still have bad data (driver_age_raw)
# - Data cleaning sometimes involves guessing (driver_age)
# - Use histograms for a sanity check
