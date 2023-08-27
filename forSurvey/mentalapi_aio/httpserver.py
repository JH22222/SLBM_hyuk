import tornado
from tornado.ioloop import IOLoop
from config.constants import PORT

from controllers.users import (
    OnlineRegistration,
    VerifyWatchUser,
    RecoverUser
)

from controllers.watch import Upload
from controllers.analytics import QuantifiedSelf

def make_app():
	return tornado.web.Application(
		[
            # (r"/users/onlineregistration", OnlineRegistration),
            (r"/users/recoverUser", RecoverUser),
            (r"/users/verifywatch", VerifyWatchUser),
            (r"/watch/uploadjson", Upload)
            # (r"/analytics/quantifiedSelf", QuantifiedSelf)
		]
	)

if __name__ == "__main__":

    app = make_app()

    print('tornado version:', tornado.version)
    print('Server start up...Listening on PORT:', PORT)
    app.listen(PORT)

    IOLoop.current().start()