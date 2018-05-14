# requests for fetching html of website
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Make the GET request to a url
url = "http://www.cleveland.com/metro/index.ssf/2017/12/case_western_reserve_university_president_barbara_snyders_base_salary_and_bonus_pay_tops_among_private_colleges_in_ohio.html?platform=hootsuite"
r = requests.get(url)

# Extract the content
c = r.content


# Create a soup object
soup = BeautifulSoup(c, "lxml")

# print(soup)

# Find the element on the webpage
main_content = soup.find('div', attrs={'class': 'entry-content'})

#print (main_content)


# Extract the relevant information as text
content = main_content.find('ul').text

#print (content)

# Create a pattern to match names
name_pattern = re.compile(r'^([A-Z]{1}.+?)(?:,)', flags=re.M)

# Find all occurrences of the pattern
names = name_pattern.findall(content)


#print (names)

# Make school patttern and extract schools
school_pattern = re.compile(r'(?:,|,\s)([A-Z]{1}.*?)(?:\s\(|:|,)')
schools = school_pattern.findall(content)

# Pattern to match the salaries
salary_pattern = re.compile(r'\$.+')
salaries = salary_pattern.findall(content)

# Convert salaries to numbers in a list comprehension
salaries = [int(''.join(s[1:].split(','))) for s in salaries]

#print (salaries)

# df = pd.DataFrame(
# {'College': schools,
# 'President': names,
# 'salary': salaries
# })

df = pd.DataFrame(np.column_stack([schools, names, salaries]),
                  columns=['College', 'President', 'salary'])


# manually adding in my President's information to the dataframe
# Append information
df.loc[17, :] = ['CWRU', 'Barbara Synder', 1154000]

df['salary'] = df['salary'].astype(int)


# Sanity check to make sure everything is correct!
y = len(names) == len(schools) == len(salaries)


# Sort the values by highest to lowest salary
df = df.sort_values('salary', ascending=False).reset_index(drop=True)

#plt(kind='barh', x='President', y='salary').show()


# Pick a style
plt.style.use('fivethirtyeight')
plt.rcParams['font.size'] = 16

# Sort the values by highest to lowest salary
# df = df.sort_values('salary', ascending=False).reset_index()

# Shorten this one name for plotting
df.ix[df['College'] == 'University of Mount Union', 'College'] = 'Mount Union'

# Create the basic figure
plt.figure(figsize=(10, 8))
sns.barplot(x='salary', y='President', data=df,
            color='tomato', edgecolor='k', linewidth=2)

# Add text showing values and colleges
for i, row in df.iterrows():
    plt.text(x=row['salary'] + 6000, y=i + 0.15, s='$%d' % (round(row['salary'] / 1000) * 1000))
    plt.text(x=5000, y=i + 0.15, s=row['College'], size=14)

# Labels are a must!
plt.xticks(size=16)
plt.yticks(size=18)
plt.xlabel('Total Compensation ($)')
plt.ylabel('President')
plt.title('2015 Compensation of Private Ohio College Presidents')

#plt.show()
#print(df)
#print('#####')

# Calculate value of 5 minutes of your presidents time
five_minutes_fraction = 5 / (2000 * 60)
total_df = pd.DataFrame(df.groupby('College')['salary'].sum()) #adds the salaries of the same college
total_df['five_minutes_cost'] = round(total_df['salary'] * five_minutes_fraction)
total_df = total_df.sort_values('five_minutes_cost', ascending=False).reset_index()

#print(total_df)

# Text for caption
txt = 'Calculated from 2015 Total Compensation assuming 2000 hrs worked/year. Source: Chronical of Higher Education'

# Create the basic barplot
plt.figure(figsize=(10, 8))
sns.barplot(x = 'five_minutes_cost', y = 'College', data = total_df, 
            color = 'red', edgecolor = 'k', linewidth = 2)

# Add the text with the value
for i, row in total_df.iterrows():
  plt.text(x = row['five_minutes_cost'] + 0.5, y = i + 0.15, 
           s = '$%d' % (row['five_minutes_cost']), size = 18)

# Add the caption
plt.text(x = -5, y = 20, s = txt, size = 14)

# Add the labels
plt.xticks(size = 16); plt.yticks(size = 18)
plt.xlabel('Value ($)')
plt.ylabel('') 
plt.title("Value of Five Minutes of Your President's Time")
plt.show()
