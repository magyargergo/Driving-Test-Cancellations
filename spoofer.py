# from fake_useragent import UserAgent
#
#
# class Spoofer(object):
#     def __init__(self, country_id=["US"], rand=True, anonym=True):
#         self.country_id = country_id
#         self.rand = rand
#         self.anonym = anonym
#         self.userAgent, self.ip = self.get()
#
#     def get(self):
#
#         proxy = FreeProxy(
#             country_id=self.country_id, rand=self.rand, anonym=self.anonym
#         ).get()
#         ip = proxy.split("://")[1]
#         return ua.random, ip
