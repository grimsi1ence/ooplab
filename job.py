import pandas as pd
import sqlite3
#------------------1-----------------
class SQLBase:
    def __init__(self, csv:str, database: str):
        self.open_csv_sheet=pd.read_csv(csv)
        self.conn=sqlite3.connect(database) 
        self.cursor=self.conn.cursor()
    def connection_to_db(self):
        return self.conn
    def cursor(self):
        return self.cursor
    def ds(self):
        return self.open_csv_sheet
    def close_db(self):
        self.conn.close()
#------------------2-----------------
class FIRST10:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def first_10(self):
        pershi_10_vakansiy="SELECT * FROM jobs LIMIT 10"
        pershi_10_vakansiy_res=pd.read_sql(pershi_10_vakansiy, self.conn)
        return pershi_10_vakansiy_res
class SQLSkill:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def sql_skill_vacations(self):
        sql='''SELECT * 
            FROM jobs
            WHERE "Required Skills" LIKE "%SQL%"
            '''
        sql_res=pd.read_sql(sql, self.conn)
        return sql_res
class DISTINCTLocations:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def distinct_locations(self):
        unikalni_from_locations="SELECT DISTINCT Location FROM jobs"
        unikalni_from_locations_res=pd.read_sql(unikalni_from_locations, self.conn)
        return unikalni_from_locations_res
class DISTINCTCompanies:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def distinct_companies(self):
        unikalni_from_locations="SELECT DISTINCT Company FROM jobs"
        unikalni_from_location_i_company_res=pd.read_sql(unikalni_from_locations, self.conn)
        return unikalni_from_location_i_company_res
#------------------3-----------------
class AVG:
    def __init__(self, db: sqlite3.Connection, ds: pd.DataFrame):
        self.conn=db
        self.ds=ds
    def avg_salary_skills(self): # + додаються в датасет нові стовпці 'min', 'max'
        min_from_salary=self.ds['Salary Range'].str.extract(r'£(\d+,?\d*) -')[0]
        min_from_salary=min_from_salary.str.replace(',','').astype(int)
        max_from_salary=self.ds['Salary Range'].str.extract(r' £(\d+,?\d*)')[0]
        max_from_salary=max_from_salary.str.replace(',','').astype(int)
        self.ds['min']=min_from_salary
        self.ds['max']=max_from_salary
        self.ds['Average Salary']=((min_from_salary+max_from_salary)/2).astype(int)
        self.ds.to_sql('jobs', self.conn, if_exists='replace', index=False)
        avr_salary='''SELECT "Experience Level", AVG("Average Salary") 
                    FROM jobs
                    GROUP BY "Experience Level"'''
        avr_salary_res=pd.read_sql(avr_salary, self.conn)
        return avr_salary_res
class CounterVacationSkills:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def counter_skills_vacations(self):
        count_vacations='''SELECT "Experience Level", COUNT(*) as quantity
                FROM jobs
                GROUP BY "Experience Level"'''
        count_vacations_res=pd.read_sql(count_vacations, self.conn)
        return count_vacations_res
class MinMaxSalary:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def min_max_salary(self):
        min_max_salary='''SELECT MIN(min), MAX(max)
                FROM jobs
                '''
        min_max_salary_res=pd.read_sql(min_max_salary, self.conn)
        return min_max_salary_res
#------------------4-----------------
class SalaryUp50000:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def salary_up_50000(self):
        salary_up_50000='''SELECT "Industry",COUNT(*) as quantity
                FROM jobs
                WHERE min>50000
                GROUP BY "Industry"'''
        salary_up_50000_res=pd.read_sql(salary_up_50000, self.conn)
        return salary_up_50000_res
class IndustryAVGSalary:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def industry_avg_salary(self):
        industry_salary_avr='''SELECT "Industry", AVG("Average Salary")
                    FROM jobs
                    GROUP BY "Industry"'''
        industry_salary_avr_res=pd.read_sql(industry_salary_avr, self.conn)
        return industry_salary_avr_res
#------------------5-----------------
class CountVacLocationsLevel:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def count_vac_locations_level(self):
        location_counter='''SELECT "Location", "Experience Level" ,COUNT(*) as quantity
                FROM jobs
                GROUP BY "Location", "Experience Level"'''
        location_counter_res=pd.read_sql(location_counter, self.conn)
        return location_counter_res
class IndustryJobCounter:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def industry_job_counter(self):
        industry_job_counter='''SELECT "Industry", "Job Type" ,COUNT(*) as quantity
                FROM jobs
                GROUP BY "Industry", "Job Type"'''
        industry_job_counter_res=pd.read_sql(industry_job_counter, self.conn)
        return industry_job_counter_res
class AVGSalaryLocationExperience:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def avg_salary_location_experience(self):
        location_experience_avr_counter='''SELECT "Location", "Experience Level" ,AVG("Average Salary") as average_salary
                FROM jobs
                GROUP BY "Location", "Experience Level"'''
        location_experience_avr_counter_res=pd.read_sql(location_experience_avr_counter, self.conn)
        return location_experience_avr_counter_res
#------------------6-----------------
class Top5Vacations:
    def __init__(self, db: pd.DataFrame):
        self.conn=db
    def top5_salary_vac(self):
        top5='''SELECT *
        FROM jobs 
        WHERE "max"=(SELECT MAX(max)
                FROM jobs)
        LIMIT 5;
        '''
        top5_res=pd.read_sql(top5, self.conn)
        return top5_res
class MaxVacations2023:
    def __init__(self, db: sqlite3.Connection, ds: pd.DataFrame):
        self.conn=db
        self.ds=ds
    def max_vacations_2023(self):
        self.ds['Year'] = pd.to_datetime(self.ds['Date Posted'], format='%m/%d/%Y').dt.year
        self.ds.to_sql('jobs', self.conn, if_exists='replace', index=False)
        max_vacations_2023='''SELECT Company, COUNT(*) AS "vacancy count(2023)"
                            FROM jobs
                            WHERE Year = 2023
                            GROUP BY Company
                            HAVING "vacancy count(2023)" = (
                                SELECT MAX(cnt)
                                FROM (
                                    SELECT COUNT(*) AS cnt
                                    FROM jobs
                                    WHERE Year = 2023
                                    GROUP BY Company
                                )
                            );
                            '''
        max_vacations_2023_res=pd.read_sql(max_vacations_2023, self.conn)
        return max_vacations_2023_res

#================1================
sql_db=SQLBase('Job opportunities.csv', 'my_database.db')
ds=sql_db.ds()
conn=sql_db.connection_to_db()
cursor=ds.to_sql('jobs', conn, if_exists='replace', index=False) 
#================2================
first10=FIRST10(conn).first_10()
print(first10)
vacations_with_sql_skill=SQLSkill(conn).sql_skill_vacations()
print(vacations_with_sql_skill)
distinct_locations=DISTINCTLocations(conn).distinct_locations()
print(distinct_locations)
distinct_companies=DISTINCTCompanies(conn).distinct_companies()
print(distinct_companies)
#================3================
avg_salary_experience=AVG(conn, ds).avg_salary_skills()
print(avg_salary_experience)
counter_vacation_experience=CounterVacationSkills(conn).counter_skills_vacations()
print(counter_vacation_experience)
min_max_salary=MinMaxSalary(conn).min_max_salary()
print(min_max_salary)
#================4================
industry_where_salary_up_50000=SalaryUp50000(conn).salary_up_50000()
print(industry_where_salary_up_50000)
industry_average_salary=IndustryAVGSalary(conn).industry_avg_salary()
print(industry_average_salary)
#================5================
counter_vacations_location_level=CountVacLocationsLevel(conn).count_vac_locations_level()
print(counter_vacations_location_level)
counter_vacations_industry_job=IndustryJobCounter(conn).industry_job_counter()
print(counter_vacations_industry_job)
average_salary_location_experience=AVGSalaryLocationExperience(conn).avg_salary_location_experience()
print(average_salary_location_experience)
#================6================
top5_vacations_by_salary=Top5Vacations(conn).top5_salary_vac()
print(top5_vacations_by_salary)
max_vacations_2023=MaxVacations2023(conn, ds).max_vacations_2023()
print(max_vacations_2023)
sql_db.close_db()