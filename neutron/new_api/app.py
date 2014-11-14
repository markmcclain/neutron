from keystonemiddleware import auth_token
import pecan
from oslo.config import cfg
from oslo.middleware import request_id

from neutron.new_api import hooks

CONF = cfg.CONF
CONF.import_opt('bind_host', 'neutron.common.config')
CONF.import_opt('bind_port', 'neutron.common.config')


def setup_app():
    config = {
        'server': {
            'port': CONF.bind_port,
            'host': CONF.bind_host
        },
        'app': {
            'root': 'neutron.new_api.controllers.root.RootController',
            'modules': ['neutron.new_api'],
        }
    }
    pecan_config = pecan.configuration.conf_from_dict(config)

    app_hooks = [
        hooks.TranslationHook(),
        hooks.ContextHook()
    ]

    app = pecan.make_app(
        pecan_config.app.root,
        debug=cfg.CONF.debug,
        wrap_app=_wrap_app,
        force_canonical=False,
        hooks=app_hooks,
        guess_content_type_from_ext=True
    )

    return app


def _wrap_app(app):
    app = request_id.RequestId(app)
    app = auth_token.AuthProtocol(app, {})
    return app
