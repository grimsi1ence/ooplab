class MathTools:
    def __init__(self, a, b):
        self.a=a
        self.b=b
    def add_nums(self):
        return self.a+self.b
    def minus(self):
        return self.a-self.b
    def multiplication(self):
        return self.a*self.b
    def division(self):
        return self.a/self.b

class LibraryItem:
    def __init__(self, title, author, year):
        self.title=title
        self.author=author
        self.year=year
    def details(self):
        return f"{self.title}: {self.author} ({self.year})"
class NotificationService:
    def send(self, user, msg):
        return user, msg
class UserManager(NotificationService):
    def __init__(self,user, service: NotificationService):
        self.user=user
        self.service=service
    def notify_user(self, msg):
        return self.service.send(self.user, msg)
def check_even(num):
    if num%2==0:
        return True
    else:
        return False