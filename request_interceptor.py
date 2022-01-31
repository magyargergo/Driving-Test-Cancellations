from incapsula import IncapSession
from seleniumwire.request import Request


def interceptor(request: Request):
    # if request.url.startswith("https://queue.driverpracticaltest.dvsa.gov.uk"):
    #     session = IncapSession(user_agent=request.headers.get('user-agent'))
    #     session.get(request.url)
    #     print(str(session.cookies))
    pass
