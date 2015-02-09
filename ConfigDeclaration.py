import ConfigParser
import optparse
import os

from utils import merge_dicts


def unimplemented(fun):
    "Decorator for virtual methods"
    def ret(self, *_args, **_kwargs):
        assert False, "Unimplemented %s in %s" % (
            fun.__func__.__name__,
            self.__class__.__name__)
    return ret


def fluent(fun):
    "Decorator for creating fluent methods"
    def ret(self, *args, **kwargs):
        fun(self, *args, **kwargs)
        return self
    return ret


def verify(config, schema, strict=True):
    """Verify that config conforms to "schema".
    This is to prevent user from using nonexitent
    sections/items in config"""
    for section in config.sections():
        assert section in schema, "Bad section: %s" % section
        warnings = 0
        for key, _ in config.items(section):
            if key not in schema[section]:
                warnings += 1
                print "Unused config item: [%s] %s" % (section, key)
        assert not strict or warnings == 0, "Bad config"


class ConfigOption(object):
    # pylint: disable=R0903,R0902,R0913
    def __init__(
            self,
            dest, x_type, default, cmd_options, cfg_item_name,
            help_text, doc_text):

        assert isinstance(x_type, BaseType), "Bad class of x_type"
        self.dest = dest
        self.x_type = x_type
        self.default = default
        self.cmd_options = cmd_options
        self.cfg_item_name = cfg_item_name
        self.help_text = help_text
        self.doc_text = help_text.capitalize() + '.'
        if doc_text:
            self.doc_text += ' ' + doc_text

        self.value = None


class MetavarMixin(object):
    # pylint: disable=R0903
    @fluent
    def with_metavar(self, metavar):
        self.kwargs['metavar'] = metavar


class BaseType(object):
    def __init__(self):
        self.value = None
        self.help_note = None
        self.kwargs = {
            'action': 'callback',
            'callback': self._callback,
        }

    @unimplemented
    @staticmethod
    def from_string(_string):
        "To be called with value from config"
        pass

    @unimplemented
    def _value_callback(self, _value):
        pass

    def _callback(self, option, _opt_str, value, parser, *_args, **_kwargs):
        self._value_callback(value)
        setattr(parser.values, option.dest, self.value)

    def optparse_option_kwargs(self):
        "Prepare Option for optparse OptionParser"
        return self.kwargs


class Const(BaseType):
    def __init__(self):
        super(Const, self).__init__()
        self.kwargs.update({
            'type': None,
            'nargs': 0
        })
        self._callback_value = None

    def _value_callback(self, _):
        self.value = self._callback_value

    @fluent
    def with_value(self, value):
        self._callback_value = value


class String(BaseType, MetavarMixin):
    def __init__(self):
        super(String, self).__init__()
        self.kwargs.update({
            'type': 'string',
            'nargs': 1
        })

    @staticmethod
    def from_string(string):
        return string

    def _value_callback(self, value):
        self.value = value


class BaseTypeMultiCall(BaseType):
    def __init__(self):
        super(BaseTypeMultiCall, self).__init__()
        self.help_note = 'repeatable'


class Counter(BaseTypeMultiCall):
    def __init__(self):
        super(Counter, self).__init__()
        self.value = 0
        self.kwargs.update({
            'type': None,
            'nargs': 0
        })

    @staticmethod
    def from_string(string):
        return int(string)

    def _value_callback(self, _):
        self.value += 1
        return self.value


class StringList(BaseTypeMultiCall, MetavarMixin):
    def __init__(self):
        super(StringList, self).__init__()
        self.value = []
        self.kwargs.update({
            'nargs': 1,
            'type': 'string',
            'metavar': 'STRING'
        })

    @staticmethod
    def from_string(string):
        if string == '':
            return []
        else:
            return string.split(",")

    def _value_callback(self, value):
        self.value.append(value)


class DirList(StringList):
    def __init__(self):
        super(DirList, self).__init__()
        self.kwargs['metavar'] = 'DIR'

    def _value_callback(self, value):
        directory = value
        if not os.path.exists(directory):
            raise optparse.OptionValueError(
                "%s does not exit" % directory)
        if not os.path.isdir(directory):
            raise optparse.OptionValueError(
                "%s is not a directory" % directory)
        if not os.access(directory, os.R_OK | os.X_OK):
            raise optparse.OptionValueError(
                "%s has wron permissions" % directory)
        return super(DirList, self)._value_callback(value)


class AppConfig(object):

    def __init__(self, declaration):
        assert isinstance(declaration, dict)
        self._declaration = declaration

    def _get_config_schema(self):
        return {
            self._declaration.get('config_section'): [
                element.cfg_item_name
                for element in self._declaration.get('config_description')
                if element.cfg_item_name
            ]
        }

    def process_configs(self):
        schema = self._get_config_schema()
        config = ConfigParser.ConfigParser()
        config.read(self._declaration.get('config_files'))
        verify(config, schema, strict=False)

    def _get_option_parser(self):
        parser = optparse.OptionParser(
            conflict_handler='error',
            usage=self._declaration.get('app_usage')
        )
        for element in self._declaration.get('config_description'):
            if not element.cmd_options:  # ...is non-empty list.
                continue

            x_type = element.x_type

            help_text = element.help_text
            if x_type.help_note:
                help_text = '%s; %s' % (help_text, x_type.help_note)
            default = element.default
            if default is not None:
                help_text = '%s; default: %s' % (help_text, repr(default))

            parser.add_option(*element.cmd_options, **merge_dicts(
                element.x_type.optparse_option_kwargs(),
                {
                    'dest': element.dest,
                    'default': default,
                    'help': help_text
                }
            ))
        return parser

    def parse_args(self, argv):
        return self._get_option_parser().parse_args(argv)
