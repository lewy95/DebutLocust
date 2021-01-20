from locust import HttpLocust, TaskSet, task

"""
官方案例：

定义 Locust 任务，都是普通的可调用函数，它们只接受一个参数(一个 Locust 类实例)
这些 Locust 任务集中在 TaskSet 类的子类的 tasks 属性中。然后定义了一个 HttpLocust 类的子类，它代表一个用户。
此外，还定义了一个模拟用户在执行任务之间应该等待多长时间，以及哪个TaskSet类定义了用户的行为。
"""


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        self.client.post("/login", {"username": "ellen_key", "password": "education"})

    def logout(self):
        self.client.post("/logout", {"username": "ellen_key", "password": "education"})

    @task(2)
    def index(self):
        self.client.get("/")

    @task(1)
    def profile(self):
        self.client.get("/profile")


# 模拟用户
class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000


"""
Locust 类（以及 HttpLocust，因为它是 Locust 类的子类）还允许指定每个模拟用户在执行任务（min_wait 和 max_wait）
和其他用户行为之间的最小和最大等待时间(以毫秒为单位)。默认情况下，时间是在 min_wait 和 max_wait 之间随机均匀地选择的，
但是可以通过将 wait_function 设置为一个函数来自定义这个等待时间。例如，对于平均为1秒的指数分布等待时间。

import random

class WebsiteUser(HttpLocust):
  task_set = UserBehavior
  wait_function = lambda self: random.expovariate(1) * 1000
"""