import pandas as pd
import numpy as np

df = pd.read_csv('./glassdoor_jobs.csv')

#salary parsing
#company name text 
#age of company
#parsing of job desc(python, etc)

# df[pd.to_numeric(df['Salary Estimate'], errors='coerce').notnull()]
df = df[(df['Salary Estimate'] != '-1') & (df['Salary Estimate'].replace(r'^([A-Za-z])', np.NaN, regex=True))]
# df = df['Salary Estimate'].replace(r'^([A-Za-z])', np.NaN, regex=True)