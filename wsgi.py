from flask import Flask, _app_ctx_stack

import exts


def create_app():
    app = Flask()
    exts.db.init_app(app, scopefunc=_app_ctx_stack.__ident_func__)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run()