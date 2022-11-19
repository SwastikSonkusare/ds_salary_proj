import pandas as pd
import numpy as np

df = pd.read_csv('./glassdoor_jobs_1.csv')

#salary parsing


#salary parsing and removing those rows whose salary is not present


df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided_salary'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)


df = df[(df['Salary Estimate'] != '-1')]
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_units = salary.apply(lambda x: x.replace("₹", '').replace("L", ''). replace("T", ''))
minus_units = minus_units.apply(lambda x: x.split(':')[1] if ':' in x.lower() else x)


df = df.drop([136,166], axis=0)


minus_units = minus_units.apply(lambda x: x.replace("Per Hour", ''))
df['min_salary'] = minus_units.apply(lambda x: x.split('-')[0])
df['max_salary'] = minus_units.apply(lambda x: x.split('-')[1] if '-' in x.lower() else x)

df['avg_salary'] = (pd.to_numeric(df['min_salary'], errors='raise') + pd.to_numeric(df['max_salary'], errors='raise')) /2

df.drop(columns='Unnamed: 0', axis=1, inplace=True)

df.drop_duplicates(inplace=True)


#company name text 
df['company_text'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis=1)
#age of company
df['Founded'] = pd.to_numeric(df['Founded'].replace(r'^([A-Za-z])', np.NaN, regex=True).fillna(0))
df['company_age'] = pd.to_numeric(df['Founded'], errors='raise').apply(lambda x: x if x < 1 else 2022 - x)

#parsing of job desc(python, etc)

#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
df.python_yn.value_counts()

#r studio
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r' in x.lower() else 0)

#sql
df['sql_yn'] = df['Job Description'].apply(lambda x: 1 if 'sql' in x.lower() else 0)

#excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)


df.drop(['spark_yn', 'hourly'], axis=1, inplace=True)

df.to_csv('salary_clean_data.csv',  index=False)







