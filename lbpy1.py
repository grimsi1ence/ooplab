import json
class User:
    def __init__(self, number, status):
        self.list_status=['outcomming', 'incomming']
        self.status=status
        self.number=number
        self.user_info={}
    def return_status(self):
        if self.status.lower() not in self.list_status or (len(self.number)<10 or len(self.number)>10):
            raise ValueError("unknown status or phone is no correct")
        self.user_info[self.number]=self.status
        return self.user_info
class ProcessingCall:
    def __init__(self, user1, user2):
        self.user1=user1
        self.user2=user2
        self.info={}
    def processing_call(self):
        if self.user1==self.user2:
            return "double status"
        self.info.update(self.user1)
        self.info.update(self.user2)
        return self.info
class CallReport:
    def __init__(self, calling_inform: dict):
        self.calling_inform=calling_inform
    def return_calling_info(self):
        return self.calling_inform
class SaveToJson:
    def __init__(self, f_name):
        self.f_name=f_name
    def save_call(self, report: dict):
        with open(self.f_name, 'r') as f:
            data=f.read().strip()
            di=json.loads(data)
        di.update(report) #старий json + новий report
        with open(self.f_name, 'w') as f:
            json.dump(di, f, indent=4)

u1=User('0967552171', 'outcomming').return_status()
u2=User('0967552172', 'incomming').return_status()
p=ProcessingCall(u1, u2).processing_call()
report=CallReport(p).return_calling_info()
SaveToJson("report.json").save_call(report)