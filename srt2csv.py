import re
import pandas as pd 
from pandas import DataFrame
import sys


# read in the subtitle file
with open(sys.argv[1], 'r') as h:
    sub = h.readlines()

# define regular expression pattern
re_pattern = r'[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} -->'
regex = re.compile(re_pattern)

# Get start times and end_times
start_times = list(filter(regex.search, sub))
start_time = [time.split(' ')[0] for time in start_times]
end_time = [time.split(' ')[-1] for time in start_times]

# Get lines
lines = [[]]
for sentence in sub:
    if re.match(re_pattern, sentence):
        lines[-1].pop()
        lines.append([])
    else:
        lines[-1].append(sentence)
lines = lines[1:]         

# nested list comprehension to remove all the extra '\n'
lines = [[i for i in nested if i != '\n'] for nested in lines]

# Merge results into a dataframe
subs = pd.DataFrame({
    'start_time':start_time,
    'end_time':end_time,
    'line':lines
})

# split lines column to multiple columns
df3 = pd.DataFrame(subs["line"].to_list())

# merge timestamp and all lines
sub_df = pd.merge(left=subs, right=df3, left_index=True, right_index=True)

# drop orginal line column
sub_df = sub_df.drop('line', 1)

#remove all other linebreaker \n
sub_df = sub_df.replace(r'\n',' ', regex=True) 

# export sub_df to csv file
sub_df.to_csv(sys.argv[2], index=False)