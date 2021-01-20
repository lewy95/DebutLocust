from locust import HttpLocust, TaskSet, task, between


# UserBehavior类继承TaskSet类，用于描述用户行为
class UserBehavior(TaskSet):

    # baidu_index() 方法表示一个用户为行，访问百度首页
    # 使用@task装饰该方法为一个事务
    # client.get()用于指请求的路径"/"，因为是百度首页，所以指定为根路径
    @task
    def baidu_index(self):
        self.client.get("/")


# 模拟用户
class WebsiteUser(HttpLocust):
    task_set = UserBehavior  # 指向一个定义的用户行为类
    wait_time = between(5, 9)  # 执行事务之间用户等待时间的下界和上界（单位：秒）


if __name__ == "__main__":
    import os

    os.system("locust -f baidu_locustfile.py --host=https://www.baidu.com")
