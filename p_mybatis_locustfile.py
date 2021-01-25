from locust import HttpLocust, TaskSet, task, between, TaskSequence, seq_task

"""
定义 Locust 任务，都是普通的可调用函数，它们只接受一个参数(一个 Locust 类实例)
这些 Locust 任务集中在 TaskSet 类的子类的 tasks 属性中。然后定义了一个 HttpLocust 类的子类，它代表一个用户。
此外，还定义了一个模拟用户在执行任务之间应该等待多长时间，以及哪个TaskSet类定义了用户的行为。
"""

# locustfile 惟一的要求在这个文件中必须至少定义一个继承自 Locust 类

# Locust 类：
# 表示一个用户（或者一个 locust 的集群），如 class WebsiteUser(HttpLocust):
# Locust 类将为每个被模拟的用户生成（孵化）一个 locust 类的实例。
# 一个 locust 类通常应该定义如下一些属性：
# task_set 属性：指向一个定义了用户行为的 TaskSet 类
# wait_time 属性：指定执行每个任务之间等待的最小时间和最大时间（单位：秒）
# weight 属性：当一个文件中定义了两个 Locust 类，用于指定哪个执行更频繁，weight=3是weight=1的三陪执行效率
# host 属性：请求地址（ip+port）

# TaskSet 类：
# 如果 Locust 代表一个 locust 的集群，那么 TaskSet 类则代表 locust 的大脑。
# 每个 Locust 类必须有一个指向 TaskSet 类的 task_set 属性集。
# 如果 Locust 代表一个 locust 的集群，那么 TaskSet 类则代表 locust 的大脑。每个 Locust 类必须有一个指向TaskSet 类的 task_set 属性集。
# TaskSet 就像它的名字一样，是一组任务，这些任务都是普通的Python可调用对象。
# 比如对一个拍卖的网站进行负载测试，那么可以执行诸如“搜索某些产品”和“出价”等操作。
# 当启动负载测试时，派生的 Locust 类的每个实例将开始执行它们的 TaskSet，然后每个 TaskSet 将选择一个任务并执行。
# 之后等待若干毫秒，这个等待时间是均匀分布在 Locust 类的 wait_time 属性值之间的一个随机数。然后它将再次选择要执行的任务，再次等待。以此类推。
# TaskSet 也可以设置自己的 wait_time 属性，并且这个优先级高于派生的 Locust 类中的。

# TaskSequence 类
# TaskSequence 类本质也是一个 TaskSet，但是它的任务将按顺序执行。

# HttpLocust 的每个实例都有一个值为 HttpSession 实例的 client 属性，可用于发起HTTP请求。
# HttpSession 类实际上是 requests.Session 类的子类，这个类的实例可以使用 get，post，head，put，delete 等方法发出 HTTP 请求并报告给 Locust的统计数据。


class CountryBehavior(TaskSet):
    # @task(n) 中 n 接受一个可选参数 weight，用来指定任务的执行比率，比如 @task(2) 执行频率是 @task(1) 的两倍
    @task(1)
    def query_detail_1(self):
        self.client.post("/detail", {"countryId": "11"})

    @task(2)
    def query_detail_2(self):
        self.client.post("/detail", {"countryId": "22"})


# 测试有序执行
class CountrySeqBehavior(TaskSequence):
    # @seq_task(n) 指定执行顺序，越小优先级越高
    # 此处的执行顺序为：执行一次 query_detail_1 → 执行两次 query_detail_2
    @seq_task(1)
    def query_detail_1(self):
        self.client.post("/detail", {"countryId": "11"})

    @seq_task(2)
    @task(2)
    def query_detail_2(self):
        self.client.post("/detail", {"countryId": "22"})


# 模拟用户
class WebsiteUser(HttpLocust):
    task_set = CountryBehavior
    wait_time = between(5, 9)


if __name__ == "__main__":
    import os

    os.system("locust -f p_mybatis_locustfile.py --host=localhost:8081")

"""
Locust 类（以及 HttpLocust，因为它是 Locust 类的子类）还允许指定每个模拟用户在执行任务（min_wait 和 max_wait）
和其他用户行为之间的最小和最大等待时间(以毫秒为单位)。默认情况下，时间是在 min_wait 和 max_wait 之间随机均匀地选择的，
但是可以通过将 wait_function 设置为一个函数来自定义这个等待时间。例如，对于平均为1秒的指数分布等待时间。

import random

class WebsiteUser(HttpLocust):
  task_set = UserBehavior
  wait_function = lambda self: random.expovariate(1) * 1000
"""
