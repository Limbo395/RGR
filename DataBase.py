import pandas as pd
from tkinter import messagebox

class OrdinaryWorker:
    def __init__(self):
        self.data = pd.read_excel('data.xlsx')

    def getName(self, workers_id):
        return self.data.iloc[workers_id, self.data.columns.get_loc("Name")]

    def getSurname(self, workers_id):
        return self.data.iloc[workers_id, self.data.columns.get_loc("Surname")]

    def getAge(self, workers_id):
        return self.data.iloc[workers_id, self.data.columns.get_loc("Age")]

    def getPosition(self, workers_id):
        return self.data.iloc[workers_id, self.data.columns.get_loc("Position")]

    def getRating(self, workers_id):
        return self.data.iloc[workers_id, self.data.columns.get_loc("Rating")]

    def getSalary(self, workers_id):
        return self.data.iloc[workers_id, self.data.columns.get_loc("Salary")]

    def setName(self, surname, new_name):
        self.data.at[self.data.loc[self.data['Surname'] == surname].index[0], "Name"] = new_name
        self.data.to_excel('data.xlsx', index=False)

    def setSalary(self, surname, new_salary):
        self.data.at[self.data.loc[self.data['Surname'] == surname].index[0], "Salary"] = new_salary
        self.data.to_excel('data.xlsx', index=False)

    def setRating(self, surname, new_rating):
        self.data.at[self.data.loc[self.data['Surname'] == surname].index[0], "Rating"] = new_rating
        self.data.to_excel('data.xlsx', index=False)


class DepartmentManager(OrdinaryWorker):
    def findByName(self, name):
        try:
            return self.data.loc[self.data['Name'] == name].index[0]
        except ValueError:
            messagebox.showinfo(message="There is no one " + name + " in data.")

    def findBySurname(self, surname):
        try:
            return self.data.loc[self.data['Name'] == surname].index[0]
        except ValueError:
            messagebox.showinfo(message="There is no one " + surname + " in data.")

    def findByAge(self, age):
        try:
            return self.data.loc[self.data['Age'] == age].index[0]
        except ValueError:
            messagebox.showinfo(message="There is no one with this age in data.")

    def findBySalary(self, salary):
        try:
            return self.data.loc[self.data['Salary'] == salary].index[0]
        except ValueError:
            messagebox.showinfo(message="There is no one with this salary in data.")

    def findByUsername(self, username):
        try:
            return self.data.loc[self.data['Salary'] == username].index[0]
        except ValueError:
            messagebox.showinfo(message="There is no one with this username in data.")