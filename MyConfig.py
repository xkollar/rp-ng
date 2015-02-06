
# def unimplemented(fun):
#     def ret(self, *args, **kwargs):
#         assert False, "Unimplemented %s in %s" % (
#             fun.func_name,
#             slef.__class__.__name__)
#     return ret
#
# class ConfigType(object):
#     @unimplemented
#     @staticmethod
#     def from_string(_in_string):
#         pass
#
#     @unimplemented
#     @staticmethod
#     def check():
#         pass
#
#     @unimplemented
#     @staticmethod
#     def callback():
#         pass

# class ConfigTypeString(ConfigType):
#     @staticmethod
#     def from_string(in_string):
#         return in_string
#
#     @staticmethod
#     def check(value):
#         return isinstance(value, str)
#
#     @staticmethod
#     def callback():
#         pass
#
# class ConfigTypeCounter(ConfigType):
#     def __init__(self):
#         self._count = 0
#
#     @staticmethod
#     def from_string(in_string):
#
#
#     def callback(self,*args,**kwargs):
#         self._count += 1
#
# from optparse import Option, OptionParser
#
# x = ConfigTypeCounter()
#
# def main():
#     optlist = [
#         Option('-v', action='callback', callback=x.callback, nargs=0)]
#
#     parser = OptionParser(option_list=optlist)
#     opts, args = parser.parse_args([
#         "-v", "-v", "-vvv"])
#
# main()

# type=config.String
# type=config.List(config.String)
# type=config.Maybe(config.String)

# BASE_TYPES = {
#     'string': (str, isinstance),
#     'int': (int, isinstance),
#     'bool': bool}
#
# ALL_TYPES = BASE_TYPES
#
# def str_to_class(s):
#     assert s in ALL_TYPES, "Wrong class"
#
# class ConfigSpec(object):
#     def __init__(
#             self,
#             dest=None
#             x_type=None
#             default=None
#             check=None
#             cmd_options=[]
#             cfg_name=None
#             action=None
#             x_help=None
#             doc=None)
#         assert dest is not None, "Destination has to be specified"
#         assert x_type in ALL_TYPES, "Type has to be specified"
#         assert isinstance(default, str_to_class(x_type)), "Default has to be of appropriate type"
#         if check is not None:
#             assert check(default)
#
#
# configSpecs = [
#     ConfigSpec(
#         dest='verbose',
#         type='int',
#         default=0,
#
#         cmd_options=['-v', '--verbose'],
#         cfg_name="""Increase verbosity (can use multiple times).""",
#         action='count',
#
#         help='Increase verbosity',
#         doc='Tralala')]
#
#     Option('-v', '--verbose', action='count', help='Increase verbosity',
#            default=0),
#     Option('-d', '--dir', action='store',
#            help='Process packages from this directory'),
#     Option('-c', '--channel', action='append',
#            help='Manage this channel (specified by label)'),
#     Option('-n', '--count', action='store',
#            help='Process this number of headers per call', type='int'),
#     Option('-l', '--list', action='store_true',
#            help='Only list the specified channels'),
#     Option('-r', '--reldir', action='store',
#            help='Relative dir to associate with the file'),
#     Option('-o', '--orgid', action='store',
#            help='Org ID', type='int'),
#     Option('-u', '--username', action='store',
#            help='Use this username to connect to RHN/Satellite'),
#     Option('-p', '--password', action='store',
#            help='Use this password to connect to RHN/Satellite'),
#     Option('-s', '--stdin', action='store_true',
#            help='Read the package names from stdin'),
#     Option('-X', '--exclude', action='append',
#            help='Exclude packages that match this glob expression'),
#     Option('--force', action='store_true',
#            help='Force the package upload (overwrites if already uploaded)'),
#     Option('--nosig', action='store_true', help='Push unsigned packages'),
#     Option('--newest', action='store_true',
#            help='Only push the packages that are newer than the server ones'),
#     Option('--nullorg', action='store_true', help='Use the null org id'),
#     Option('--header', action='store_true',
#            help='Upload only the header(s)'),
#     Option('--source', action='store_true',
#            help='Upload source package information'),
#     Option('--server', action='store',
#            help='Push to this server (http[s]://<hostname>/APP)'),
#     Option('--proxy', action='store',
#            help='Use proxy server (<server>:<port>)'),
#     Option('--test', action='store_true',
#            help='Only print the packages to be pushed'),
#     Option('-?', '--usage', action='store_true',
#            help='Briefly describe the options'),
#     Option('-N', '--new-cache', action='store_true',
#            help='Create a new username/password cache'),
#     Option('--extended-test', action='store_true',
#            help='Perform a more verbose test'),
#     Option('--no-session-caching', action='store_true',
#            help='Disables session-token authentication.'),
#     Option('--tolerant', action='store_true',
#            help='If rhnpush errors while uploading a package, continue uploading the rest of the packages.'),
#     Option('--ca-chain', action='store', help='alternative SSL CA Cert')
# ]

import ConfigParser
import os

def get_home_dir():
    return '.'


def usual_config_files(base_name):
    sysdir = '/etc/sysconfig/rhn'
    homedir = get_home_dir()

    hidden = '.' + base_name

    system_file = os.path.join(sysdir, base_name)
    user_file = os.path.join('~', hidden)
    local_file = os.path.join('.', hidden)
    return (system_file, user_file, local_file)

class ConfigOption(object):
    def __init__(
            self,
            dest=None, default=None, cmd_options=None, cfg_item_name=None,
            help_text=None, doc_text=None):
        self.dest = dest
        self.default = default
        self.cmd_options = cmd_options
        self.cfg_item_name = cfg_item_name
        self.help_text = help_text
        self.doc_text = doc_text

        self.value = None

class CCounter(ConfigOption):
    def set_from_string(self, string):
        self.value = int(string)

    def check(self):
        assert self.value >= 0

    def option_callback(self, option, opt_str, value, parser, *args, **kwargs):
        print "tralala"

class AppConfig(object):
    def __init__(self, declaration, argv):
        pass

app_config_declaration = {
    'doc': 'This is a cool application',
    'config_files': usual_config_files("rhnpush"),
    'config_section': 'rhnpush',
    'config': [
        CCounter(
            dest='verbose',
            default='0',
            cmd_options=['-v', '--verbose'],
            cfg_item_name="verbose",
            help_text='Increase verbosity',
            doc_text='Increase verbosity (can use multiple times).'
            )
        ]
    }

import sys
app_config = AppConfig(app_config_declaration, argv=sys.argv)

# config = {
#     'config_files':
#     'config_schema': { 'rhnpush': [
#         'newest',
#         'usage',
#         'header',
#         'test',
#         'nullorg',
#         'source',
#         'stdin',
#         'verbose',
#         'force',
#         'nosig',
#         'list',
#         'exclude',
#         'files',
#         'orgid',
#         'reldir',
#         'count',
#         'dir',
#         'server',
#         'channel',
#         'cache_lifetime',
#         'new_cache',
#         'extended_test',
#         'no_session_caching',
#         'tolerant',
#         'ca_chain'] }}
#
# print config
#
# x = ConfigParser.ConfigParser()
# x.read('rhnpushrc')
# schema = config.get('config_schema')

def verify(config, schema, strict=True):
    for section in config.sections():
        assert section in schema, "Bad section: %s" % section
        warnings = 0
        for key, _ in x.items(section):
            if key not in schema[section]:
                warnings += 1
                print "Unused config item: [%s] %s" % (section, key)
        assert not strict or warnings == 0, "Bad config"

# verify(x, schema, strict=True)
#
# with file("/dev/stdout", "w") as f:
#     x.write(f)
