import pandas as pd
class CSV:
    def __init__(self, file):
        self.file=file

    def open(self):
            ds=pd.read_csv(self.file)
            return ds   
class BaseInf:
    def __init__(self, ds: pd.DataFrame):
        self.dataset=ds
    def memory(self):
        memory=self.dataset.memory_usage(deep="True").sum()
        return f"file memory: {memory/1024:.2f} kBytes"
    def skip_values(self):
        skip_val=self.dataset.isnull()
        return f'==================пропущені значення:\n{skip_val}'
    def types_columns(self):
        types=self.dataset.dtypes
        return types
class Vacation:
    def __init__(self, ds:pd.DataFrame): 
        self.dataset=ds
    def search_on_industry(self, industry:str):
        all_in_industry=self.dataset[self.dataset['Industry']==industry]
        return all_in_industry
    def level(self, level: str):
        industry_level=self.dataset[self.dataset['Experience Level']==level]
        return industry_level
    def city(self, city):
        city_job_type=self.dataset[self.dataset['Location']==city]
        return city_job_type
class Salary:
    def __init__(self, ds:pd.DataFrame):
        self.dataset=ds
    def salary_sorted(self, sort:bool):
        try:
            sorted_dataset=self.dataset.sort_values(by='Salary Range', ascending=sort)
            return sorted_dataset
        except TypeError:
            return None
class Group:
    def __init__(self, ds: pd.DataFrame):
        self.ds=ds
    def group_size(self, by):
        groupes_industry=ds.groupby(by).size()
        return groupes_industry
    def avarage_salary(self): #додає новий 
        min_from_range=self.ds['Salary Range'].str.extract(r'£(\d+,?\d*) -')[0]
        min_from_range=min_from_range.str.replace(',','').astype(int)
        max_from_range=self.ds['Salary Range'].str.extract(r'- £(\d+,?\d*)')[0]
        max_from_range=max_from_range.str.replace(',','').astype(int)
        self.ds['avarage salary']=((max_from_range+min_from_range)/2).astype(int) 
        return self.ds
    def categories(self): #новий стовбець Salary Category
        def categories(zp):
            if zp<=40000:
                return 'Low'
            elif zp>40000 and zp<=70000:
                return 'Medium'
            elif zp>70000:
                return 'High'
        self.ds['Salary Category']=self.ds['avarage salary'].apply(categories)
        return self.ds
class Year:
    def __init__(self, ds: pd.DataFrame):
        self.ds=ds
    def add_col_year(self):
        def to_datetime(date_string):
            return pd.to_datetime(date_string, format='%m/%d/%Y')
        self.ds['Date Posted']=self.ds['Date Posted'].apply(to_datetime)
        def get_year(date):
            return pd.to_datetime(date, format='%Y%m/%d').year
        self.ds['Year']=self.ds['Date Posted'].apply(get_year)
        return self.ds
    def year_activity(self):
        years_count=self.ds.groupby('Year').agg(Total_Vacations=('Job Title', 'count'))
        return years_count
ds=CSV("Job opportunities.csv").open()
memory=BaseInf(ds).memory()
skip_values=BaseInf(ds).skip_values()
types_columns=BaseInf(ds).types_columns()
print(f"пам'ять, яку займає датасет: \n{memory}")
print(f"пропущені значення:\n{skip_values}")
print(f"типи стовпців:\n{types_columns}")

s=Salary(ds).salary_sorted(False)
print(f'----------вакансії відсортовані по зарплаті: \n{s}')
# Вивести 5 вакансій з найвищою зарплатою.
print(f"----------5 вакансій з найвищою зарплатою \n{s.head(5)}")
# Визначити, які посади є найбільш високооплачуваними
top=s[s['Salary Range']==s['Salary Range'].max()]
print(f"----------посади які найбільш високооплачувані \n{top}")

industry=Vacation(ds).search_on_industry('Cloud Computing')
level=Vacation(industry).level('Senior')
city=Vacation(level).city('Manchester')
print(city)

gr=Group(ds).group_size('Industry')
avr=Group(ds).avarage_salary()
categories=Group(avr).categories()
print(f"============новий стовбець по категоріям заробітньої плати:\n{categories[['Industry','avarage salary','Salary Category']]}")
print(f"============кількість вакансій:\n{gr}")
print(f"============середня зарплата за галузями:\n{avr[['Industry','avarage salary']]}")
max_row = avr.loc[avr['avarage salary'].idxmax()]
print(f"============галузь з найвищою зарплатою:\n{max_row[['Industry', 'avarage salary']]}")

year=Year(categories).add_col_year() #фінальний датасет (додані нові стовпці)
year_activity=Year(year).year_activity()
print(year_activity)
year.to_excel('data.xlsx')