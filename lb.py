import pandas as pd
ds=pd.read_csv("Job opportunities.csv")
first5=ds.head(5)
last5=ds.tail(5)
print(f"перші 5 рядків:\n{first5}")
print(f"останні 5 рядків:\n{last5}")
rows,columns=ds.shape
print(f"====Job opportunities.csv====\n{rows} rows, {columns} columns")
memory=ds.memory_usage(deep="True").sum()
columns_types=ds.dtypes
skip_val=ds.isnull()
sum_skip_val=ds.isnull().sum()
print(f"file memory: {memory/1024:.2f} kBytes")
#------------2-----------
# Переглянути типи даних усіх стовпців.
print(f"типи стовпців:\n {columns_types}")
# Переконатися, чи є пропущені значення.
print(f"пропущені значення \n{sum_skip_val}")
#------------3-----------
# Відібрати вакансії у певній сфері (наприклад,  Cloud Computing).
all_cloud_computing=ds[ds['Industry']=='Cloud Computing']
print(f"----------Вакансії в сфері Cloud Computing:\n{all_cloud_computing}")
# Знайти вакансії з рівнем Senior.
senior_cloud_computing=all_cloud_computing[all_cloud_computing['Experience Level']=='Senior']
print(f"----------Senior вакансії в сфері Cloud Computing:\n{senior_cloud_computing}")
# Відібрати вакансії типу Full-Time у конкретному місті.
senior_cloud_computing_full_Edinburgh=senior_cloud_computing[(senior_cloud_computing['Location']=='Edinburgh') & (senior_cloud_computing['Job Type']=='Full-Time')]
print(f"----------Senior Full-Time вакансії в сфері Cloud Computing в Edinburgh:\n{senior_cloud_computing_full_Edinburgh}")
#------------4-----------
# Відсортувати вакансії за рівнем оплати (Salary Range).
sorted_dataset=ds.sort_values(by='Salary Range', ascending=False)
print(f"----------sorted by salary: \n{sorted_dataset}")
# Вивести 5 вакансій з найвищою зарплатою.
print(f"----------5 вакансій з найвищою зарплатою \n{sorted_dataset.head(5)}")
# Визначити, які посади є найбільш високооплачуваними
top=sorted_dataset[sorted_dataset['Salary Range']==sorted_dataset['Salary Range'].max()]
print(f"----------посади які найбільш високооплачувані \n{top}")
#------------5-----------
#Згрупувати вакансії за галузями (Industry).
groupes_industry=ds.groupby('Industry')
#Для кожної галузі визначити: 
#	кількість вакансій;
count_industry=groupes_industry.size()
print(f"----------Кількість вакансій \n{count_industry}")
#	середню мінімальну зарплату.
min_from_range=ds['Salary Range'].str.extract(r'£(\d+,?\d*) -')[0]
min_from_range=min_from_range.str.replace(',','').astype(int)
max_from_range=ds['Salary Range'].str.extract(r'- £(\d+,?\d*)')[0]
max_from_range=max_from_range.str.replace(',','').astype(int)
ds['avarage salary']=((max_from_range+min_from_range)/2).astype(int)
print(f"----------середня зп \n{ds}")
#Визначити галузь з найвищою середньою зарплатою.
industry_max_zp=ds['Industry'][ds['avarage salary']==ds['avarage salary'].max()].unique()
print(f"===========галузь з найвищою середньою зарплатою \n{industry_max_zp}")
#------------6-----------
#Створити новий стовпець Salary Category:
#	Low - до 40 000;
#	Medium - 40 001 – 70 000;
#	High - понад 70 000.
def categories(zp):
    if zp<40000:
        return 'Low'
    elif zp>40000 and zp<=70000:
        return 'Medium'
    elif zp>70000:
        return 'High'

ds['Salary Category']=ds['avarage salary'].apply(categories)
print(f"----------dataset + новий стовпець Salary Category \n{ds}")
#------------7-----------
#	Перетворити колонку Date Posted у формат datetime.
def to_datetime(date_string):
    return pd.to_datetime(date_string, format='%m/%d/%Y')
ds['Date Posted']=ds['Date Posted'].apply(to_datetime)
print(f"===========\n{ds}")
#	Створити нову колонку Year. 
def get_year(date):
    return pd.to_datetime(date, format='%Y%m/%d').year
ds['Year']=ds['Date Posted'].apply(get_year)
print(f"=============\n{ds}")
#	Проаналізувати кількість вакансій за роками та які роки були найбільш активними.
years_count=ds.groupby('Year').agg(Total_Vacations=('Job Title', 'count'))
print(f"================\n{years_count}")
#	Проаналізуйте отриману таблицю з кількістю вакансій за роками.
active_year=years_count['Total_Vacations'].idxmax()
passive_year=years_count['Total_Vacations'].idxmin()
print(f"================= \n активний рік: {active_year}\n пасивний рік: {passive_year}")
