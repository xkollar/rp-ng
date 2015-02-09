import ConfigDeclaration as C

from utils import usual_config_files

APP_CONFIG_DECLARATION = {
    'doc': 'This is a cool application',
    'config_files': usual_config_files('rhnpush', sysdir='/etc/sysconfig/rhn'),
    'config_section': 'rhnpush',
    'app_usage': '%prog [option] [package]',
    'config_description': [
        C.ConfigOption(
            dest='verbose',
            x_type=C.Counter(),
            default=0,
            cmd_options=['-v', '--verbose'],
            cfg_item_name="verbose",
            help_text='increase verbosity',
            doc_text=None
        ),
        C.ConfigOption(
            dest='dirs',
            x_type=C.DirList(),
            default=[],
            cmd_options=['-d', '--dir'],
            cfg_item_name="dir",
            help_text='process packages from directory',
            doc_text=None
        ),
        C.ConfigOption(
            dest='channel',
            x_type=C.StringList().with_metavar('CHANNEL'),
            default=[],
            cmd_options=['-c', '--channel'],
            cfg_item_name="dir",
            help_text='process packages from directory',
            doc_text=None
        ),
        C.ConfigOption(
            dest='username',
            x_type=C.String().with_metavar('USERNAME'),
            default=None,
            cmd_options=['-u', '--username'],
            cfg_item_name=None,
            help_text='username for connecting to server',
            doc_text=None
        ),
        C.ConfigOption(
            dest='password',
            x_type=C.String().with_metavar('PASSWORD'),
            default=None,
            cmd_options=['-p', '--password'],
            cfg_item_name=None,
            help_text='password for connecting to server',
            doc_text=None
        ),
        C.ConfigOption(
            dest='nosig',
            x_type=C.Const().with_value(True),
            default=False,
            cmd_options=['--nosig'],
            cfg_item_name='nosig',
            help_text='push unsigned packages',
            doc_text=None
        ),
        C.ConfigOption(
            dest='force',
            x_type=C.Const().with_value(True),
            default=False,
            cmd_options=['--force'],
            cfg_item_name='force',
            help_text='force the package upload '
                '(overwrites if already uploaded)',
            doc_text=None
        )
    ]
}
