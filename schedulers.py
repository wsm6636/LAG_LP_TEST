 #1
class gEDFca():
    def __init__(self, tasks=[], cpu=None) -> None:
        self.tasks = tasks
        self.cpu = cpu

    def set(self, tasks, cpu):
        self.tasks = tasks
        self.cpu = cpu

    def schedulable(self, func):
        return func(self.tasks, self.cpu)