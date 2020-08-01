import argparse
import os
import traceback

import tornado.ioloop
import tornado.web

import handlers
import settings


class Application(tornado.web.Application):
    def __init__(self, config, port):
        routes = [
            (r"/", handlers.common.HomePage),
            (r"/homepage", handlers.common.HomePage),
            (r"/create_progress", handlers.common.CreateProgress),
        ]
        super(Application, self).__init__(handlers=routes, **config)
        # For the world to exist peacefully, this application should always listen on localhost.
        http_server = self.listen(port, address='127.0.0.1')
        # Set "xheaders" as true. Currently we are using this so that the over-write behaviour on "remote_ip" can be done
        # using the request headers present "X-Real-Ip" / "X-Forwarded-For". This is important as in our architecture Tornado sits behind a proxy server
        http_server.xheaders = True


async def init():
    config = await settings.get_config()
    return config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8001)
    args = parser.parse_args()

    # Initialize state and static resources
    config = tornado.ioloop.IOLoop.current().run_sync(init)
    # Start application
    application = Application(config, args.port)
    # Start eventloop
    try:
        tornado.ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc()
    finally:
        tornado.ioloop.IOLoop.current().stop()
