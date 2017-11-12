from handlers.rewards_handler import RewardsHandler
from handlers.users_handler import UsersHandler

# Email regex adapted from http://www.regular-expressions.info/email.html
# Not perfect but 99% good. Could be revisited.

url_patterns = [
    (r'/rewards', RewardsHandler),
    (r'/users', UsersHandler),
    (r'/users\/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]', UsersHandler),
]
