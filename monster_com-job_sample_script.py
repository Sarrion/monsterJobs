#%% DATA IMPORT
import pandas as pd
data = pd.read_csv('monster_com-job_sample.csv')
data = data[['job_description', 'job_title', 'job_type', 'location',
 'organization', 'page_url', 'salary', 'sector']]

#%% DATA FILTER BY SALARY
import re

# Filtering only numerics in salary column
numerics = lambda x: pd.notnull(x) and bool(re.search('[0-9]', x))
nums=data.salary.apply(numerics)
salaries = data[nums]

#%% DATA FILTER BY YEAR BASED SALARIES
# Filtering year salaries 
yearize = lambda x: bool(re.search('year', x))
ySalaries = salaries[salaries.salary.apply(yearize)]

#%% COMPUTATION OF MEAN SALARIES
def meanSalary(dat):
    numbers = re.findall('[0-9]+\.', 
                         re.sub(',', '', dat)
                         )
    numbers = pd.Series(numbers).apply(lambda x: float(x))
    return(numbers.mean())
# Mean Salary column addition to ySalaries
ySalaries = ySalaries.assign(MeanSalary = ySalaries.salary.apply(meanSalary))
#ySalaries = ySalaries.sort_values('MeanSalary', ascending = False)

#%% DICTIONARY CONSTRUCTION
dic = ySalaries.job_description.str.cat(sep = ' ')
dic = re.split('[ | \xa0]', dic)
dic = pd.Series(dic).drop_duplicates()

