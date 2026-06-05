import pandas as pd
import sqlite3
#------------------1-----------------
ds=pd.read_csv('Job opportunities.csv')
conn = sqlite3.connect('my_database.db') 
cursor = conn.cursor()  
ds.to_sql('jobs', conn, if_exists='replace', index=False)  
#------------------2-----------------
#1.	Виведіть перші 10 вакансій із таблиці.
pershi_10_vakansiy="SELECT * FROM jobs LIMIT 10"
pershi_10_vakansiy_res=pd.read_sql(pershi_10_vakansiy, conn)
#2.	Виберіть усі вакансії з вимогою SQL у полі Required Skills.
sql='''SELECT * 
    FROM jobs
    WHERE "Required Skills" LIKE "%SQL%"
    '''
sql_res=pd.read_sql(sql, conn)
#3.	Виведіть усі унікальні Location та Company.
unikalni_from_location_i_company="SELECT DISTINCT Location, Company FROM jobs"
unikalni_from_location_i_company_res=pd.read_sql(unikalni_from_location_i_company, conn)
#------------------3-----------------
#1.	Обчисліть середню зарплату для кожного рівня досвіду 
min=ds['Salary Range'].str.extract(r'£(\d+,?\d*) -')[0]
min=min.str.replace(',','').astype(int)
max=ds['Salary Range'].str.extract(r' £(\d+,?\d*)')[0]
max=max.str.replace(',','').astype(int)
ds['Average Salary']=((min+max)/2).astype(int)
ds.to_sql('jobs', conn, if_exists='replace', index=False)
avr_salary='''SELECT "Experience Level", AVG('Average Salary') 
            FROM jobs
            GROUP BY "Experience Level"'''
#2.	Підрахуйте кількість вакансій для кожного рівня досвіду 
count_vacations='''SELECT "Experience Level", COUNT(*)
                FROM jobs
                GROUP BY "Experience Level"'''
count_vacations_res=pd.read_sql(count_vacations, conn)
#3.	Знайдіть мінімальну та максимальну зарплату серед усіх вакансій.
min_s=ds['Salary Range'].str.extract(r'£(\d+,?\d*) -')[0]
min_s=min_s.str.replace(',','').astype(int)
max_s=ds['Salary Range'].str.extract(r' £(\d+,?\d*)')[0]
max_s=max_s.str.replace(',','').astype(int)
ds['min']=min_s
ds['max']=max_s
ds.to_sql('jobs', conn, if_exists='replace', index=False)
min_max_salary='''SELECT MIN(min), MAX(max)
            FROM jobs
            '''
min_max_salary_res=pd.read_sql(min_max_salary, conn)
#------------------4-----------------
#1.	Виберіть кількість вакансій у кожній індустрії (Industry) для вакансій із зарплатою більше £50,000.
salary_up_50000='''SELECT "Industry",COUNT(*)
                FROM jobs
                WHERE min>50000
                GROUP BY "Industry"'''
salary_up_50000_res=pd.read_sql(salary_up_50000, conn)
#2.	Обчисліть середню зарплату для кожної індустрії.
industry_salary_avr='''SELECT "Industry", AVG("Average Salary")
                    FROM jobs
                    GROUP BY "Industry"'''
industry_salary_avr_res=pd.read_sql(industry_salary_avr, conn)
#------------------5-----------------
#1.	Підрахуйте кількість вакансій за Location та Experience Level.
location_counter='''SELECT "Location", "Experience Level" ,COUNT(*) as quantity
                FROM jobs
                GROUP BY "Location", "Experience Level"'''
location_counter_res=pd.read_sql(location_counter, conn)
#2.	Обчисліть загальну кількість вакансій у кожній індустрії (Industry) 
# та для кожного типу роботи (Job Type).
industry_job_counter='''SELECT "Industry", "Job Type" ,COUNT(*) as quantity
                FROM jobs
                GROUP BY "Industry", "Job Type"'''
industry_job_counter_res=pd.read_sql(industry_job_counter, conn)
#3.	Визначте середню зарплату для вакансій за Location та Experience Level
location_Experience_avr_counter='''SELECT "Location", "Experience Level" ,AVG("Average Salary") as average_salary
                FROM jobs
                GROUP BY "Location", "Experience Level"'''
location_Experience_avr_counter_res=pd.read_sql(location_Experience_avr_counter, conn)
#------------------6-----------------
#1.	Виведіть 5 вакансій з найвищою верхньою межою зарплати.
top5='''SELECT *
        FROM jobs 
        WHERE "max"=(SELECT MAX(max)
                FROM jobs)
        LIMIT 5;
        '''
top5_res=pd.read_sql(top5, conn)
#2.	Підрахуйте кількість вакансій для кожного Required Skills 
# (окремо для кожного ключового слова, якщо в колонці кілька навичок через коми).
vacation_for_every_skill='''SELECT "Required Skills", COUNT(*) as quantity
                        FROM jobs
                        WHERE "Required Skills" LIKE "%,%"
                        GROUP BY "Required Skills"
                        '''
vacation_for_every_skill_res=pd.read_sql(vacation_for_every_skill, conn)
#3.	Визначте, які компанії розміщують найбільшу кількість вакансій у 2023 році.
ds['Year'] = pd.to_datetime(ds['Date Posted'], format='%m/%d/%Y').dt.year
ds.to_sql('jobs', conn, if_exists='replace', index=False)
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
max_vacations_2023_res=pd.read_sql(max_vacations_2023, conn)
print(max_vacations_2023_res)
conn.close()