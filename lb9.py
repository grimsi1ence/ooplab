import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class CSV:
    def __init__(self, file: str):
        self.file=file
        self.dataset=None
    def open_csv(self):
        self.dataset=pd.read_csv(self.file)
        return self.dataset
class DataFrame:
    def __init__(self, df):
        self.df=df
    def add_average_salary(self):
        min_s = self.df['Salary Range'].str.extract(r'£(\d+,?\d*) -')[0]
        min_s = min_s.str.replace(',', '').astype(int)
        max_s = self.df['Salary Range'].str.extract(r' £(\d+,?\d*)')[0]
        max_s = max_s.str.replace(',', '').astype(int)
        awg_salary = (max_s + min_s) / 2
        self.df["Average Salary"] = awg_salary
        return self.df
    def add_year_col(self):
        def get_year(date):
            return pd.to_datetime(date, format='%m/%d/%Y').year
        self.df['Year'] = self.df['Date Posted'].apply(get_year)
        return self.df
class Barplot:
    def __init__(self, data: pd.DataFrame, x_param: str, y_param: str):
        self.data=data
        self.x_param=x_param
        self.y_param=y_param
    def plot(self, title ,x_label, y_label):
        try:
            salary_experience=self.data[[self.x_param, self.y_param]]
            plt.figure(figsize=(10, 6))
            sns.barplot(x=self.x_param, y=self.y_param, data=salary_experience, palette='viridis')
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.show()
        except KeyError:
            print("unknown key")

class Boxplot:
    def __init__(self, data: pd.DataFrame, x_param: str, y_param: str):
        self.data=data
        self.x_param=x_param
        self.y_param=y_param
    def plot(self, title ,x_label, y_label):
        try:
            salary_industry = self.data[[self.x_param, self.y_param]]
            plt.figure(figsize=(12, 6))
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            sns.boxplot(x=self.x_param, y=self.y_param, data=salary_industry, palette='viridis')
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.show()
        except KeyError:
            print("unknown key")
        except ValueError:
            print("value error")
class Heatmap:
    def __init__(self, data: pd.DataFrame, x_param: str, y_param: str):
        self.data = data
        self.x_param = x_param
        self.y_param = y_param

    def plot(self, title):
        try:
            plt.figure(figsize=(10,6))
            pivot_table = pd.crosstab(self.data[self.x_param], self.data[self.y_param])
            sns.heatmap(pivot_table)
            plt.title(title)
            plt.show()
        except KeyError:
            print("unknown key")
        except ValueError:
            print("value error")
class Scatterplot:
    def __init__(self, data: pd.DataFrame, x_param: str, y_param: str, hue: str):
        self.data = data
        self.x_param = x_param
        self.y_param = y_param
        self.hue=hue
    def plot(self, title, x_label, y_label):
        try:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x=self.x_param, y=self.y_param, hue=self.hue, data=self.data)
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            plt.show()
        except KeyError:
            print("unknown key")
        except ValueError:
            print("value error")

class Pairplot:
    def __init__(self, data: pd.DataFrame, param_list: list):
        self.data = data
        self.param_list=param_list
    def plot(self, title):
        try:
            sns.pairplot(self.data[self.param_list], diag_kind='kde', palette='bright')
            plt.suptitle(title, y=1.02)
            plt.show()
        except KeyError:
            print("unknown key")
        except ValueError:
            print("value error")

ds=CSV("Job opportunities.csv").open_csv()

dataframe=DataFrame(ds)
df_with_awg_salary=dataframe.add_average_salary()
df=dataframe.add_year_col()

Barplot(df, "Experience Level", "Average Salary").plot("Залежність заробітньої плати від досвіду",
                                                              "Рівень досвіду", "рівень заробітньої плати")
Boxplot(df, "Industry","Average Salary"). plot("Діаграма розмаху для відображення розподілу зарплат за галузями",
                                               "Галузь", "Середня зоробітня плата")
Heatmap(df, "Industry", "Experience Level").plot("Теплова карта для аналізу кількості вакансій за рівнем досвіду та галуззю")
Scatterplot(df, "Year", "Average Salary", "Experience Level").plot("залежність зарплати від року публікації",
                                                                   "Рік публікації", "Середня зарплата")
Pairplot(df, ["Average Salary", "Year", "Experience Level"]).plot("Аналіз взаємозв’язків між зарплатою, роком та рівнем досвіду")
