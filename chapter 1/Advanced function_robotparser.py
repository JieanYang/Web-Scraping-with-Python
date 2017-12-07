import urllib.robotparser as robotparser

rp = robotparser.RobotFileParser()
rp.set_url('http://www.sephora.fr/robots.txt')
rp.read()
url = 'http://www.sephora.fr/search/search_results.jsp'
user_agent = 'BadCrawler'
print(rp.can_fetch(user_agent, url))

user_agent = 'GoodCrawler'
print(rp.can_fetch(user_agent, url))
#can_fetch()会检测你的访问和身份是否符合robots.txt的要求