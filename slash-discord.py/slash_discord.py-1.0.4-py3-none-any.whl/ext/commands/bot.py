# -*- coding: utf-8 -*-

"""
The MIT License (MIT)

Copyright (c) 2021-present Grifonice99

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import asyncio
import collections
import copy
import inspect
import logging
import importlib.util
import sys
import traceback
import types
import typing 

import discord

from inspect import getdoc, iscoroutinefunction
from .core import GroupMixin, slash
from .view import StringView
from .utils import manage_commands, manage_components
from .errors import DuplicateCommand, IncorrectGuildIDType, DuplicateCallback, IncorrectFormat
from .context import Context, SlashContext, ComponentContext
from . import errors , model
from .help import HelpCommand, DefaultHelpCommand
from .cog import Cog
from contextlib import suppress

def _get_val(d: dict, key):  # util function to get value from dict with fallback to None key
    try:
        value = d[key]
    except KeyError:  # if there is no specific key set, we fallback to "global/any"
        value = d[None]
    return value

def when_mentioned(bot, msg):
    """A callable that implements a command prefix equivalent to being mentioned.

    These are meant to be passed into the :attr:`.Bot.command_prefix` attribute.
    """
    return [bot.user.mention + ' ', '<@!%s> ' % bot.user.id]

def when_mentioned_or(*prefixes):
    """A callable that implements when mentioned or other prefixes provided.

    These are meant to be passed into the :attr:`.Bot.command_prefix` attribute.

    Example
    --------

    .. code-block:: python3

        bot = commands.Bot(command_prefix=commands.when_mentioned_or('!'))


    .. note::

        This callable returns another callable, so if this is done inside a custom
        callable, you must call the returned callable, for example:

        .. code-block:: python3

            async def get_prefix(bot, message):
                extras = await prefixes_for(message.guild) # returns a list
                return commands.when_mentioned_or(*extras)(bot, message)


    See Also
    ----------
    :func:`.when_mentioned`
    """
    def inner(bot, msg):
        r = list(prefixes)
        r = when_mentioned(bot, msg) + r
        return r

    return inner

def _is_submodule(parent, child):
    return parent == child or child.startswith(parent + ".")

class _DefaultRepr:
    def __repr__(self):
        return '<default-help-command>'

_default = _DefaultRepr()

class BotBase(GroupMixin):
    def __init__(self, 
        command_prefix, 
        help_command=_default, 
        description=None, 
        sync_commands: bool = False,
        delete_from_unused_guilds: bool = False,
        sync_on_cog_reload: bool = False,
        override_type: bool = False,
        **options
    ):
        super().__init__(**options)
        self.command_prefix = command_prefix
        self.loop=asyncio.get_event_loop()
        self._sync_commands=sync_commands
        self._delete_from_unused_guilds=delete_from_unused_guilds
        self._sync_on_cog_reload=sync_on_cog_reload
        self._override_type=override_type
        self.extra_events = {}
        self.__cogs = {}
        self.__extensions = {}
        self._checks = []
        self._check_once = []
        self.commandslash = {}
        self.subcommands = {}
        self._before_invoke = None
        self._after_invoke = None
        self._help_command = None
        self.logger = logging.getLogger("discord")
        self.description = inspect.cleandoc(description) if description else ''
        self.owner_id = options.get('owner_id')
        self.owner_ids = options.get('owner_ids', set())
        self.strip_after_prefix = options.get('strip_after_prefix', False)

        if self.owner_id and self.owner_ids:
            raise TypeError('Both owner_id and owner_ids are set.')

        if self.owner_ids and not isinstance(self.owner_ids, collections.abc.Collection):
            raise TypeError('owner_ids must be a collection not {0.__class__!r}'.format(self.owner_ids))

        if options.pop('self_bot', False):
            self._skip_check = lambda x, y: x != y
        else:
            self._skip_check = lambda x, y: x == y

        if help_command is _default:
            self.help_command = DefaultHelpCommand()
        else:
            self.help_command = help_command

        if self._sync_commands:
            self.loop.create_task(self.sync_all_commands(self._delete_from_unused_guilds))
    

    # internal helpers
    
    def dispatch(self, event_name, *args, **kwargs):
        super().dispatch(event_name, *args, **kwargs)
        ev = 'on_' + event_name
        for event in self.extra_events.get(ev, []):
            self._schedule_event(event, ev, *args, **kwargs)

    async def close(self):
        for extension in tuple(self.__extensions):
            try:
                self.unload_extension(extension)
            except Exception:
                pass

        for cog in tuple(self.__cogs):
            try:
                self.remove_cog(cog)
            except Exception:
                pass

        await super().close()


    async def on_command_error(self, context, exception):
        """|coro|

        The default command error handler provided by the bot.

        By default this prints to :data:`sys.stderr` however it could be
        overridden to have a different implementation.

        This only fires if you do not specify any listeners for command error.
        """
        if self.extra_events.get('on_command_error', None):
            return

        if hasattr(context.command, 'on_error'):
            return

        cog = context.cog
        if cog and Cog._get_overridden_method(cog.cog_command_error) is not None:
            return

        print('Ignoring exception in command {}:'.format(context.command), file=sys.stderr)
        traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    # global check registration

    def check(self, func):
        r"""A decorator that adds a global check to the bot.

        A global check is similar to a :func:`.check` that is applied
        on a per command basis except it is run before any command checks
        have been verified and applies to every command the bot has.

        .. note::

            This function can either be a regular function or a coroutine.

        Similar to a command :func:`.check`\, this takes a single parameter
        of type :class:`.Context` and can only raise exceptions inherited from
        :exc:`.CommandError`.

        Example
        ---------

        .. code-block:: python3

            @bot.check
            def check_commands(ctx):
                return ctx.command.qualified_name in allowed_commands

        """
        self.add_check(func)
        return func

    def add_check(self, func, *, call_once=False):
        """Adds a global check to the bot.

        This is the non-decorator interface to :meth:`.check`
        and :meth:`.check_once`.

        Parameters
        -----------
        func
            The function that was used as a global check.
        call_once: :class:`bool`
            If the function should only be called once per
            :meth:`.Command.invoke` call.
        """

        if call_once:
            self._check_once.append(func)
        else:
            self._checks.append(func)

    def remove_check(self, func, *, call_once=False):
        """Removes a global check from the bot.

        This function is idempotent and will not raise an exception
        if the function is not in the global checks.

        Parameters
        -----------
        func
            The function to remove from the global checks.
        call_once: :class:`bool`
            If the function was added with ``call_once=True`` in
            the :meth:`.Bot.add_check` call or using :meth:`.check_once`.
        """
        l = self._check_once if call_once else self._checks

        try:
            l.remove(func)
        except ValueError:
            pass

    def check_once(self, func):
        r"""A decorator that adds a "call once" global check to the bot.

        Unlike regular global checks, this one is called only once
        per :meth:`.Command.invoke` call.

        Regular global checks are called whenever a command is called
        or :meth:`.Command.can_run` is called. This type of check
        bypasses that and ensures that it's called only once, even inside
        the default help command.

        .. note::

            When using this function the :class:`.Context` sent to a group subcommand
            may only parse the parent command and not the subcommands due to it
            being invoked once per :meth:`.Bot.invoke` call.

        .. note::

            This function can either be a regular function or a coroutine.

        Similar to a command :func:`.check`\, this takes a single parameter
        of type :class:`.Context` and can only raise exceptions inherited from
        :exc:`.CommandError`.

        Example
        ---------

        .. code-block:: python3

            @bot.check_once
            def whitelist(ctx):
                return ctx.message.author.id in my_whitelist

        """
        self.add_check(func, call_once=True)
        return func

    async def can_run(self, ctx, *, call_once=False):
        data = self._check_once if call_once else self._checks

        if len(data) == 0:
            return True

        return await discord.utils.async_all(f(ctx) for f in data)

    async def is_owner(self, user):
        """|coro|

        Checks if a :class:`~discord.User` or :class:`~discord.Member` is the owner of
        this bot.

        If an :attr:`owner_id` is not set, it is fetched automatically
        through the use of :meth:`~.Bot.application_info`.

        .. versionchanged:: 1.3
            The function also checks if the application is team-owned if
            :attr:`owner_ids` is not set.

        Parameters
        -----------
        user: :class:`.abc.User`
            The user to check for.

        Returns
        --------
        :class:`bool`
            Whether the user is the owner.
        """

        if self.owner_id:
            return user.id == self.owner_id
        elif self.owner_ids:
            return user.id in self.owner_ids
        else:
            app = await self.application_info()
            if app.team:
                self.owner_ids = ids = {m.id for m in app.team.members}
                return user.id in ids
            else:
                self.owner_id = owner_id = app.owner.id
                return user.id == owner_id

    def before_invoke(self, coro):
        """A decorator that registers a coroutine as a pre-invoke hook.

        A pre-invoke hook is called directly before the command is
        called. This makes it a useful function to set up database
        connections or any type of set up required.

        This pre-invoke hook takes a sole parameter, a :class:`.Context`.

        .. note::

            The :meth:`~.Bot.before_invoke` and :meth:`~.Bot.after_invoke` hooks are
            only called if all checks and argument parsing procedures pass
            without error. If any check or argument parsing procedures fail
            then the hooks are not called.

        Parameters
        -----------
        coro: :ref:`coroutine <coroutine>`
            The coroutine to register as the pre-invoke hook.

        Raises
        -------
        TypeError
            The coroutine passed is not actually a coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('The pre-invoke hook must be a coroutine.')

        self._before_invoke = coro
        return coro

    def after_invoke(self, coro):
        r"""A decorator that registers a coroutine as a post-invoke hook.

        A post-invoke hook is called directly after the command is
        called. This makes it a useful function to clean-up database
        connections or any type of clean up required.

        This post-invoke hook takes a sole parameter, a :class:`.Context`.

        .. note::

            Similar to :meth:`~.Bot.before_invoke`\, this is not called unless
            checks and argument parsing procedures succeed. This hook is,
            however, **always** called regardless of the internal command
            callback raising an error (i.e. :exc:`.CommandInvokeError`\).
            This makes it ideal for clean-up scenarios.

        Parameters
        -----------
        coro: :ref:`coroutine <coroutine>`
            The coroutine to register as the post-invoke hook.

        Raises
        -------
        TypeError
            The coroutine passed is not actually a coroutine.
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('The post-invoke hook must be a coroutine.')

        self._after_invoke = coro
        return coro

    # listener registration

    def add_listener(self, func, name=None):
        """The non decorator alternative to :meth:`.listen`.

        Parameters
        -----------
        func: :ref:`coroutine <coroutine>`
            The function to call.
        name: Optional[:class:`str`]
            The name of the event to listen for. Defaults to ``func.__name__``.

        Example
        --------

        .. code-block:: python3

            async def on_ready(): pass
            async def my_message(message): pass

            bot.add_listener(on_ready)
            bot.add_listener(my_message, 'on_message')

        """
        name = func.__name__ if name is None else name

        if not asyncio.iscoroutinefunction(func):
            raise TypeError('Listeners must be coroutines')

        if name in self.extra_events:
            self.extra_events[name].append(func)
        else:
            self.extra_events[name] = [func]

    def remove_listener(self, func, name=None):
        """Removes a listener from the pool of listeners.

        Parameters
        -----------
        func
            The function that was used as a listener to remove.
        name: :class:`str`
            The name of the event we want to remove. Defaults to
            ``func.__name__``.
        """

        name = func.__name__ if name is None else name

        if name in self.extra_events:
            try:
                self.extra_events[name].remove(func)
            except ValueError:
                pass

    def listen(self, name=None):
        """A decorator that registers another function as an external
        event listener. Basically this allows you to listen to multiple
        events from different places e.g. such as :func:`.on_ready`

        The functions being listened to must be a :ref:`coroutine <coroutine>`.

        Example
        --------

        .. code-block:: python3

            @bot.listen()
            async def on_message(message):
                print('one')

            # in some other file...

            @bot.listen('on_message')
            async def my_message(message):
                print('two')

        Would print one and two in an unspecified order.

        Raises
        -------
        TypeError
            The function being listened to is not a coroutine.
        """

        def decorator(func):
            self.add_listener(func, name)
            return func

        return decorator

    # cogs

    def add_cog(self, cog):
        """Adds a "cog" to the bot.

        A cog is a class that has its own event listeners and commands.

        Parameters
        -----------
        cog: :class:`.Cog`
            The cog to register to the bot.

        Raises
        -------
        TypeError
            The cog does not inherit from :class:`.Cog`.
        CommandError
            An error happened during loading.
        """

        if not isinstance(cog, Cog):
            raise TypeError('cogs must derive from Cog')

        cog = cog._inject(self)
        self.__cogs[cog.__cog_name__] = cog

    def get_cog(self, name):
        """Gets the cog instance requested.

        If the cog is not found, ``None`` is returned instead.

        Parameters
        -----------
        name: :class:`str`
            The name of the cog you are requesting.
            This is equivalent to the name passed via keyword
            argument in class creation or the class name if unspecified.

        Returns
        --------
        Optional[:class:`Cog`]
            The cog that was requested. If not found, returns ``None``.
        """
        return self.__cogs.get(name)

    def remove_cog(self, name):
        """Removes a cog from the bot.

        All registered commands and event listeners that the
        cog has registered will be removed as well.

        If no cog is found then this method has no effect.

        Parameters
        -----------
        name: :class:`str`
            The name of the cog to remove.
        """

        cog = self.__cogs.pop(name, None)
        if cog is None:
            return

        help_command = self._help_command
        if help_command and help_command.cog is cog:
            help_command.cog = None
        cog._eject(self)

    @property
    def cogs(self):
        """Mapping[:class:`str`, :class:`Cog`]: A read-only mapping of cog name to cog."""
        return types.MappingProxyType(self.__cogs)

    # extensions

    def _remove_module_references(self, name):
        # find all references to the module
        # remove the cogs registered from the module
        for cogname, cog in self.__cogs.copy().items():
            if _is_submodule(name, cog.__module__):
                self.remove_cog(cogname)

        # remove all the commands from the module
        for cmd in self.all_commands.copy().values():
            if cmd.module is not None and _is_submodule(name, cmd.module):
                if isinstance(cmd, GroupMixin):
                    cmd.recursively_remove_all_commands()
                self.remove_command(cmd.name)

        # remove all the listeners from the module
        for event_list in self.extra_events.copy().values():
            remove = []
            for index, event in enumerate(event_list):
                if event.__module__ is not None and _is_submodule(name, event.__module__):
                    remove.append(index)

            for index in reversed(remove):
                del event_list[index]

    def _call_module_finalizers(self, lib, key):
        try:
            func = getattr(lib, 'teardown')
        except AttributeError:
            pass
        else:
            try:
                func(self)
            except Exception:
                pass
        finally:
            self.__extensions.pop(key, None)
            sys.modules.pop(key, None)
            name = lib.__name__
            for module in list(sys.modules.keys()):
                if _is_submodule(name, module):
                    del sys.modules[module]

    def _load_from_module_spec(self, spec, key):
        # precondition: key not in self.__extensions
        lib = importlib.util.module_from_spec(spec)
        sys.modules[key] = lib
        try:
            spec.loader.exec_module(lib)
        except Exception as e:
            del sys.modules[key]
            raise errors.ExtensionFailed(key, e) from e

        try:
            setup = getattr(lib, 'setup')
        except AttributeError:
            del sys.modules[key]
            raise errors.NoEntryPointError(key)

        try:
            setup(self)
        except Exception as e:
            del sys.modules[key]
            self._remove_module_references(lib.__name__)
            self._call_module_finalizers(lib, key)
            raise errors.ExtensionFailed(key, e) from e
        else:
            self.__extensions[key] = lib

    def _resolve_name(self, name, package):
        try:
            return importlib.util.resolve_name(name, package)
        except ImportError:
            raise errors.ExtensionNotFound(name)

    def load_extension(self, name, *, package=None):
        """Loads an extension.

        An extension is a python module that contains commands, cogs, or
        listeners.

        An extension must have a global function, ``setup`` defined as
        the entry point on what to do when the extension is loaded. This entry
        point must have a single argument, the ``bot``.

        Parameters
        ------------
        name: :class:`str`
            The extension name to load. It must be dot separated like
            regular Python imports if accessing a sub-module. e.g.
            ``foo.test`` if you want to import ``foo/test.py``.
        package: Optional[:class:`str`]
            The package name to resolve relative imports with.
            This is required when loading an extension using a relative path, e.g ``.foo.test``.
            Defaults to ``None``.

            .. versionadded:: 1.7

        Raises
        --------
        ExtensionNotFound
            The extension could not be imported.
            This is also raised if the name of the extension could not
            be resolved using the provided ``package`` parameter.
        ExtensionAlreadyLoaded
            The extension is already loaded.
        NoEntryPointError
            The extension does not have a setup function.
        ExtensionFailed
            The extension or its setup function had an execution error.
        """

        name = self._resolve_name(name, package)
        if name in self.__extensions:
            raise errors.ExtensionAlreadyLoaded(name)

        spec = importlib.util.find_spec(name)
        if spec is None:
            raise errors.ExtensionNotFound(name)        
        self._load_from_module_spec(spec, name)
        self.load_commandslash()

    def unload_extension(self, name, *, package=None):
        """Unloads an extension.

        When the extension is unloaded, all commands, listeners, and cogs are
        removed from the bot and the module is un-imported.

        The extension can provide an optional global function, ``teardown``,
        to do miscellaneous clean-up if necessary. This function takes a single
        parameter, the ``bot``, similar to ``setup`` from
        :meth:`~.Bot.load_extension`.

        Parameters
        ------------
        name: :class:`str`
            The extension name to unload. It must be dot separated like
            regular Python imports if accessing a sub-module. e.g.
            ``foo.test`` if you want to import ``foo/test.py``.
        package: Optional[:class:`str`]
            The package name to resolve relative imports with.
            This is required when unloading an extension using a relative path, e.g ``.foo.test``.
            Defaults to ``None``.

            .. versionadded:: 1.7

        Raises
        -------
        ExtensionNotFound
            The name of the extension could not
            be resolved using the provided ``package`` parameter.
        ExtensionNotLoaded
            The extension was not loaded.
        """

        name = self._resolve_name(name, package)
        lib = self.__extensions.get(name)
        if lib is None:
            raise errors.ExtensionNotLoaded(name)

        self._remove_module_references(lib.__name__)
        self._call_module_finalizers(lib, name)
        self.load_commandslash()

    def reload_extension(self, name, *, package=None):
        """Atomically reloads an extension.

        This replaces the extension with the same extension, only refreshed. This is
        equivalent to a :meth:`unload_extension` followed by a :meth:`load_extension`
        except done in an atomic way. That is, if an operation fails mid-reload then
        the bot will roll-back to the prior working state.

        Parameters
        ------------
        name: :class:`str`
            The extension name to reload. It must be dot separated like
            regular Python imports if accessing a sub-module. e.g.
            ``foo.test`` if you want to import ``foo/test.py``.
        package: Optional[:class:`str`]
            The package name to resolve relative imports with.
            This is required when reloading an extension using a relative path, e.g ``.foo.test``.
            Defaults to ``None``.

            .. versionadded:: 1.7

        Raises
        -------
        ExtensionNotLoaded
            The extension was not loaded.
        ExtensionNotFound
            The extension could not be imported.
            This is also raised if the name of the extension could not
            be resolved using the provided ``package`` parameter.
        NoEntryPointError
            The extension does not have a setup function.
        ExtensionFailed
            The extension setup function had an execution error.
        """

        name = self._resolve_name(name, package)
        lib = self.__extensions.get(name)
        if lib is None:
            raise errors.ExtensionNotLoaded(name)

        # get the previous module states from sys modules
        modules = {
            name: module
            for name, module in sys.modules.items()
            if _is_submodule(lib.__name__, name)
        }

        try:
            # Unload and then load the module...
            self._remove_module_references(lib.__name__)
            self._call_module_finalizers(lib, name)
            self.load_extension(name)
        except Exception:
            # if the load failed, the remnants should have been
            # cleaned from the load_extension function call
            # so let's load it from our old compiled library.
            lib.setup(self)
            self.__extensions[name] = lib

            # revert sys.modules back to normal and raise back to caller
            sys.modules.update(modules)
            raise
        self.load_commandslash()

    @property
    def extensions(self):
        """Mapping[:class:`str`, :class:`py:types.ModuleType`]: A read-only mapping of extension name to extension."""
        return types.MappingProxyType(self.__extensions)

    # help command stuff

    @property
    def help_command(self):
        return self._help_command

    @help_command.setter
    def help_command(self, value):
        if value is not None:
            if not isinstance(value, HelpCommand):
                raise TypeError('help_command must be a subclass of HelpCommand')
            if self._help_command is not None:
                self._help_command._remove_from_bot(self)
            self._help_command = value
            value._add_to_bot(self)
        elif self._help_command is not None:
            self._help_command._remove_from_bot(self)
            self._help_command = None
        else:
            self._help_command = None

    # command processing

    async def get_prefix(self, message):
        """|coro|

        Retrieves the prefix the bot is listening to
        with the message as a context.

        Parameters
        -----------
        message: :class:`discord.Message`
            The message context to get the prefix of.

        Returns
        --------
        Union[List[:class:`str`], :class:`str`]
            A list of prefixes or a single prefix that the bot is
            listening for.
        """
        prefix = ret = self.command_prefix
        if callable(prefix):
            ret = await discord.utils.maybe_coroutine(prefix, self, message)

        if not isinstance(ret, str):
            try:
                ret = list(ret)
            except TypeError:
                # It's possible that a generator raised this exception.  Don't
                # replace it with our own error if that's the case.
                if isinstance(ret, collections.abc.Iterable):
                    raise

                raise TypeError("command_prefix must be plain string, iterable of strings, or callable "
                                "returning either of these, not {}".format(ret.__class__.__name__))

            if not ret:
                raise ValueError("Iterable command_prefix must contain at least one prefix")

        return ret

    async def get_context(self, message, *, cls=Context):
        r"""|coro|

        Returns the invocation context from the message.

        This is a more low-level counter-part for :meth:`.process_commands`
        to allow users more fine grained control over the processing.

        The returned context is not guaranteed to be a valid invocation
        context, :attr:`.Context.valid` must be checked to make sure it is.
        If the context is not valid then it is not a valid candidate to be
        invoked under :meth:`~.Bot.invoke`.

        Parameters
        -----------
        message: :class:`discord.Message`
            The message to get the invocation context from.
        cls
            The factory class that will be used to create the context.
            By default, this is :class:`.Context`. Should a custom
            class be provided, it must be similar enough to :class:`.Context`\'s
            interface.

        Returns
        --------
        :class:`.Context`
            The invocation context. The type of this can change via the
            ``cls`` parameter.
        """

        view = StringView(message.content)
        ctx = cls(prefix=None, view=view, bot=self, message=message)

        if self._skip_check(message.author.id, self.user.id):
            return ctx

        prefix = await self.get_prefix(message)
        invoked_prefix = prefix

        if isinstance(prefix, str):
            if not view.skip_string(prefix):
                return ctx
        else:
            try:
                # if the context class' __init__ consumes something from the view this
                # will be wrong.  That seems unreasonable though.
                if message.content.startswith(tuple(prefix)):
                    invoked_prefix = discord.utils.find(view.skip_string, prefix)
                else:
                    return ctx

            except TypeError:
                if not isinstance(prefix, list):
                    raise TypeError("get_prefix must return either a string or a list of string, "
                                    "not {}".format(prefix.__class__.__name__))

                # It's possible a bad command_prefix got us here.
                for value in prefix:
                    if not isinstance(value, str):
                        raise TypeError("Iterable command_prefix or list returned from get_prefix must "
                                        "contain only strings, not {}".format(value.__class__.__name__))

                # Getting here shouldn't happen
                raise

        if self.strip_after_prefix:
            view.skip_ws()

        invoker = view.get_word()
        ctx.invoked_with = invoker
        ctx.prefix = invoked_prefix
        ctx.command = self.all_commands.get(invoker)
        return ctx

    async def invoke(self, ctx):
        """|coro|

        Invokes the command given under the invocation context and
        handles all the internal event dispatch mechanisms.

        Parameters
        -----------
        ctx: :class:`.Context`
            The invocation context to invoke.
        """
        if ctx.command is not None:
            self.dispatch('command', ctx)
            try:
                if await self.can_run(ctx, call_once=True):
                    await ctx.command.invoke(ctx)
                else:
                    raise errors.CheckFailure('The global check once functions failed.')
            except errors.CommandError as exc:
                await ctx.command.dispatch_error(ctx, exc)
            else:
                self.dispatch('command_completion', ctx)
        elif ctx.invoked_with:
            exc = errors.CommandNotFound('Command "{}" is not found'.format(ctx.invoked_with))
            self.dispatch('command_error', ctx, exc)

    async def process_commands(self, message):
        """|coro|

        This function processes the commands that have been registered
        to the bot and other groups. Without this coroutine, none of the
        commands will be triggered.

        By default, this coroutine is called inside the :func:`.on_message`
        event. If you choose to override the :func:`.on_message` event, then
        you should invoke this coroutine as well.

        This is built using other low level tools, and is equivalent to a
        call to :meth:`~.Bot.get_context` followed by a call to :meth:`~.Bot.invoke`.

        This also checks if the message's author is a bot and doesn't
        call :meth:`~.Bot.get_context` or :meth:`~.Bot.invoke` if so.

        Parameters
        -----------
        message: :class:`discord.Message`
            The message to process commands for.
        """
        if message.author.bot:
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)
    
    async def on_message(self, message):
        await self.process_commands(message)

    def get_cog_commands(self, cog: Cog):
        
        """
        Gets slash command from :class:`discord.ext.commands.Cog`.

        .. note::
            Since version ``1.0.9``, this gets called automatically during cog initialization.

        :param cog: Cog that has slash commands.
        :type cog: discord.ext.commands.Cog
        """
        if hasattr(cog, "_slash_registered"):  # Temporary warning
            return self.logger.warning(
                "Calling get_cog_commands is no longer required "
                "to add cog slash commands. Make sure to remove all calls to this function."
            )
        try:cog._slash_registered = True  # Assuming all went well
        except:pass
        func_list = [getattr(cog, x) for x in dir(cog)]

        self._get_cog_slash_commands(cog, func_list)
        self._get_cog_component_callbacks(cog, func_list)

    def _get_cog_slash_commands(self, cog, func_list):
        res = [
            x
            for x in func_list
            if isinstance(x, (model.CogBaseCommandObject, model.CogSubcommandObject))
        ]

        for x in res:
            x.cog = cog
            if isinstance(x, model.CogBaseCommandObject):
                if x.name in self.commandslash:
                    raise DuplicateCommand(x.name)
                self.commandslash[x.name] = x
            else:
                if x.base in self.commandslash:
                    base_command = self.commandslash[x.base]
                    for i in x.allowed_guild_ids:
                        if i not in base_command.allowed_guild_ids:
                            base_command.allowed_guild_ids.append(i)

                    base_permissions = x.base_command_data["api_permissions"]
                    if base_permissions:
                        for applicable_guild in base_permissions:
                            if applicable_guild not in base_command.permissions:
                                base_command.permissions[applicable_guild] = []
                            base_command.permissions[applicable_guild].extend(
                                base_permissions[applicable_guild]
                            )

                    self.commandslash[x.base].has_subcommands = True

                else:
                    self.commandslash[x.base] = model.BaseCommandObject(x.base, x.base_command_data)
                if x.base not in self.subcommands:
                    self.subcommands[x.base] = {}
                if x.subcommand_group:
                    if x.subcommand_group not in self.subcommands[x.base]:
                        self.subcommands[x.base][x.subcommand_group] = {}
                    if x.name in self.subcommands[x.base][x.subcommand_group]:
                        raise DuplicateCommand(f"{x.base} {x.subcommand_group} {x.name}")
                    self.subcommands[x.base][x.subcommand_group][x.name] = x
                else:
                    if x.name in self.subcommands[x.base]:
                        raise DuplicateCommand(f"{x.base} {x.name}")
                    self.subcommands[x.base][x.name] = x

    def _get_cog_component_callbacks(self, cog, func_list):
        res = [x for x in func_list if isinstance(x, model.CogComponentCallbackObject)]

        for x in res:
            x.cog = cog
            self._add_comp_callback_obj(x)

    def remove_cog_commands(self, cog):
        """
        Removes slash command from :class:`discord.ext.commands.Cog`.

        .. note::
            Since version ``1.0.9``, this gets called automatically during cog de-initialization.

        :param cog: Cog that has slash commands.
        :type cog: discord.ext.commands.Cog
        """
        if hasattr(cog, "_slash_registered"):
            del cog._slash_registered
        func_list = [getattr(cog, x) for x in dir(cog)]
        self._remove_cog_slash_commands(func_list)
        self._remove_cog_component_callbacks(func_list)

    def _remove_cog_slash_commands(self, func_list):
        res = [
            x
            for x in func_list
            if isinstance(x, (model.CogBaseCommandObject, model.CogSubcommandObject))
        ]
        for x in res:
            if isinstance(x, model.CogBaseCommandObject):
                if x.name not in self.commandslash:
                    continue  # Just in case it is removed due to subcommand.
                if x.name in self.subcommands:
                    self.commandslash[x.name].func = None
                    continue  # Let's remove completely when every subcommand is removed.
                del self.commandslash[x.name]
            else:
                if x.base not in self.subcommands:
                    continue  # Just in case...
                if x.subcommand_group:
                    del self.subcommands[x.base][x.subcommand_group][x.name]
                    if not self.subcommands[x.base][x.subcommand_group]:
                        del self.subcommands[x.base][x.subcommand_group]
                else:
                    del self.subcommands[x.base][x.name]
                if not self.subcommands[x.base]:
                    del self.subcommands[x.base]
                    if x.base in self.commandslash:
                        if self.commandslash[x.base].func:
                            self.commandslash[x.base].has_subcommands = False
                        else:
                            del self.commandslash[x.base]

    def _remove_cog_component_callbacks(self, func_list):
        res = [x for x in func_list if isinstance(x, model.CogComponentCallbackObject)]

        for x in res:
            self.remove_component_callback_obj(x)

    async def to_dict(self):
        """
        Converts all commands currently registered to :class:`SlashCommand` to a dictionary.
        Returns a dictionary in the format:

        .. code-block:: python

            {
                "global" : [], # list of global commands
                "guild" : {
                    0000: [] # list of commands in the guild 0000
                }
            }

        Commands are in the format specified by discord `here <https://discord.com/developers/docs/interactions/slash-commands#applicationcommand>`_
        """
        await self.wait_until_ready()  # In case commands are still not registered to SlashCommand.
        all_guild_ids = []
        for x in self.commandslash:
            for i in self.commandslash[x].allowed_guild_ids:
                if i not in all_guild_ids:
                    all_guild_ids.append(i)
        cmds = {"global": [], "guild": {x: [] for x in all_guild_ids}}
        wait = {}  # Before merging to return dict, let's first put commands to temporary dict.
        for x in self.commandslash:
            selected = self.commandslash[x]
            if selected.allowed_guild_ids:
                for y in selected.allowed_guild_ids:
                    if y not in wait:
                        wait[y] = {}
                    command_dict = {
                        "name": x,
                        "description": selected.description or "No Description.",
                        "options": selected.options or [],
                        "default_permission": selected.default_permission,
                        "permissions": {},
                    }
                    if y in selected.permissions:
                        command_dict["permissions"][y] = selected.permissions[y]
                    wait[y][x] = copy.deepcopy(command_dict)
            else:
                if "global" not in wait:
                    wait["global"] = {}
                command_dict = {
                    "name": x,
                    "description": selected.description or "No Description.",
                    "options": selected.options or [],
                    "default_permission": selected.default_permission,
                    "permissions": selected.permissions or {},
                }
                wait["global"][x] = copy.deepcopy(command_dict)

        # Separated normal command add and subcommand add not to
        # merge subcommands to one. More info at Issue #88
        # https://github.com/eunwoo1104/discord-py-slash-command/issues/88

        for x in self.commandslash:
            if not self.commandslash[x].has_subcommands:
                continue
            tgt = self.subcommands[x]
            for y in tgt:
                sub = tgt[y]
                if isinstance(sub, model.SubcommandObject):
                    _dict = {
                        "name": sub.name,
                        "description": sub.description or "No Description.",
                        "type": model.SlashCommandOptionType.SUB_COMMAND,
                        "options": sub.options or [],
                    }
                    if sub.allowed_guild_ids:
                        for z in sub.allowed_guild_ids:
                            wait[z][x]["options"].append(_dict)
                    else:
                        wait["global"][x]["options"].append(_dict)
                else:
                    queue = {}
                    base_dict = {
                        "name": y,
                        "description": "No Description.",
                        "type": model.SlashCommandOptionType.SUB_COMMAND_GROUP,
                        "options": [],
                    }
                    for z in sub:
                        sub_sub = sub[z]
                        _dict = {
                            "name": sub_sub.name,
                            "description": sub_sub.description or "No Description.",
                            "type": model.SlashCommandOptionType.SUB_COMMAND,
                            "options": sub_sub.options or [],
                        }
                        if sub_sub.allowed_guild_ids:
                            for i in sub_sub.allowed_guild_ids:
                                if i not in queue:
                                    queue[i] = copy.deepcopy(base_dict)
                                queue[i]["options"].append(_dict)
                        else:
                            if "global" not in queue:
                                queue["global"] = copy.deepcopy(base_dict)
                            queue["global"]["options"].append(_dict)
                    for i in queue:
                        wait[i][x]["options"].append(queue[i])

        for x in wait:
            if x == "global":
                [cmds["global"].append(n) for n in wait["global"].values()]
            else:
                [cmds["guild"][x].append(n) for n in wait[x].values()]

        return cmds

    def load_commandslash(self):
        for x in self.cogs:
            try:
                self.remove_cog_commands(self.get_cog(x))
            except:
                pass            
            self.get_cog_commands(self.get_cog(x))

    async def sync_all_commands(
        self, delete_from_unused_guilds=False, delete_perms_from_unused_guilds=False
     ):
        self.load_commandslash()
        """
        Matches commands registered on Discord to commands registered here.
        Deletes any commands on Discord but not here, and registers any not on Discord.
        This is done with a `put` request.
        A PUT request will only be made if there are changes detected.
        If ``sync_commands`` is ``True``, then this will be automatically called.

        :param delete_from_unused_guilds: If the bot should make a request to set no commands for guilds that haven't got any commands registered in :class:``SlashCommand``
        :param delete_perms_from_unused_guilds: If the bot should make a request to clear permissions for guilds that haven't got any permissions registered in :class:``SlashCommand``
        """
        permissions_map = {}
        
        cmds = await self.to_dict()
        
        #print("Syncing commands...")
        cmds_formatted = {None: cmds["global"]}
        for guild in cmds["guild"]:
            cmds_formatted[guild] = cmds["guild"][guild]
        
        for scope in cmds_formatted:
            permissions = {}
            new_cmds = cmds_formatted[scope]
            existing_cmds = await self.http.get_all_commands(guild_id=scope)
            existing_by_name = {}
            to_send = []
            changed = False
            
            for cmd in existing_cmds:
                existing_by_name[cmd["name"]] = model.CommandData(**cmd)

            if len(new_cmds) != len(existing_cmds):
                changed = True

            for command in new_cmds:
                cmd_name = command["name"]
                permissions[cmd_name] = command.pop("permissions")
                if cmd_name in existing_by_name:
                    cmd_data = model.CommandData(**command)
                    existing_cmd = existing_by_name[cmd_name]
                    
                    if cmd_data != existing_cmd:
                        changed = True
                        to_send.append(command)
                    else:
                        command_with_id = command
                        command_with_id["id"] = existing_cmd.id
                        to_send.append(command_with_id)
                else:
                    changed = True
                    to_send.append(command)
            
            if changed:
                #print(
                #    f"Detected changes on {scope if scope is not None else 'global'}, updating them"
                #)
                existing_cmds = await self.http.put_slash_commands(
                    slash_commands=to_send, guild_id=scope
                )
           # else:
                #print(
                #    f"Detected no changes on {scope if scope is not None else 'global'}, skipping"
               # )

            id_name_map = {}
            for cmd in existing_cmds:
                id_name_map[cmd["name"]] = cmd["id"]

            for cmd_name in permissions:
                cmd_permissions = permissions[cmd_name]
                cmd_id = id_name_map[cmd_name]
                for applicable_guild in cmd_permissions:
                    if applicable_guild not in permissions_map:
                        permissions_map[applicable_guild] = []
                    permission = {
                        "id": cmd_id,
                        "guild_id": applicable_guild,
                        "permissions": cmd_permissions[applicable_guild],
                    }
                    permissions_map[applicable_guild].append(permission)

        #print("Syncing permissions...")
        #print(f"Commands permission data are {permissions_map}")
        for scope in permissions_map:
            existing_perms = await self.http.get_all_guild_commands_permissions(scope)
            new_perms = permissions_map[scope]

            changed = False
            if len(existing_perms) != len(new_perms):
                changed = True
            else:
                existing_perms_model = {}
                for existing_perm in existing_perms:
                    existing_perms_model[existing_perm["id"]] = model.GuildPermissionsData(
                        **existing_perm
                    )
                for new_perm in new_perms:
                    if new_perm["id"] not in existing_perms_model:
                        changed = True
                        break
                    if existing_perms_model[new_perm["id"]] != model.GuildPermissionsData(
                        **new_perm
                    ):
                        changed = True
                        break

            if changed:
                #print(f"Detected permissions changes on {scope}, updating them")
                await self.http.update_guild_commands_permissions(scope, new_perms)
            else:
                return
                #print(f"Detected no permissions changes on {scope}, skipping")

        if delete_from_unused_guilds:
            #print("Deleting unused guild commands...")
            other_guilds = [
                guild.id for guild in self.guilds if guild.id not in cmds["guild"]
            ]
            # This is an extremly bad way to do this, because slash cmds can be in guilds the bot isn't in
            # But it's the only way until discord makes an endpoint to request all the guild with cmds registered.

            for guild in other_guilds:
                with suppress(discord.Forbidden):
                    existing = await self.http.get_all_commands(guild_id=guild)
                    if len(existing) != 0:
                        #print(f"Deleting commands from {guild}")
                        await self.http.put_slash_commands(slash_commands=[], guild_id=guild)

        if delete_perms_from_unused_guilds:
            self.logger.info("Deleting unused guild permissions...")
            other_guilds = [
                guild.id for guild in self.guilds if guild.id not in permissions_map.keys()
            ]
            for guild in other_guilds:
                with suppress(discord.Forbidden):
                    print(f"Deleting permissions from {guild}")
                    existing_perms = await self.http.get_all_guild_commands_permissions(guild)
                    if len(existing_perms) != 0:
                        await self.http.update_guild_commands_permissions(guild, [])

        #print("Completed syncing all commands!")

    def add_slash_command(
        self,
        cmd,
        name: str = None,
        description: str = None,
        guild_ids: typing.List[int] = None,
        options: list = None,
        default_permission: bool = True,
        permissions: typing.Dict[int, list] = None,
        connector: dict = None,
        has_subcommands: bool = False,
    ):
        """
        Registers slash command to SlashCommand.

        .. warning::
            Just using this won't register slash command to Discord API.
            To register it, check :meth:`.utils.manage_commands.add_slash_command` or simply enable `sync_commands`.

        :param cmd: Command Coroutine.
        :type cmd: Coroutine
        :param name: Name of the slash command. Default name of the coroutine.
        :type name: str
        :param description: Description of the slash command. Defaults to command docstring or ``None``.
        :type description: str
        :param guild_ids: List of Guild ID of where the command will be used. Default ``None``, which will be global command.
        :type guild_ids: List[int]
        :param options: Options of the slash command. This will affect ``auto_convert`` and command data at Discord API. Default ``None``.
        :type options: list
        :param default_permission: Sets if users have permission to run slash command by default, when no permissions are set. Default ``True``.
        :type default_permission: bool
        :param permissions: Dictionary of permissions of the slash command. Key being target guild_id and value being a list of permissions to apply. Default ``None``.
        :type permissions: dict
        :param connector: Kwargs connector for the command. Default ``None``.
        :type connector: dict
        :param has_subcommands: Whether it has subcommand. Default ``False``.
        :type has_subcommands: bool
        """
        name = name or cmd.__name__
        name = name.lower()
        guild_ids = guild_ids if guild_ids else []
        if not all(isinstance(item, int) for item in guild_ids):
            raise IncorrectGuildIDType(
                f"The snowflake IDs {guild_ids} given are not a list of integers. Because of discord.py convention, please use integer IDs instead. Furthermore, the command '{name}' will be deactivated and broken until fixed."
            )
        if name in self.commandslash:
            tgt = self.commandslash[name]
            if not tgt.has_subcommands:
                raise DuplicateCommand(name)
            has_subcommands = tgt.has_subcommands
            for x in tgt.allowed_guild_ids:
                if x not in guild_ids:
                    guild_ids.append(x)

        description = description or getdoc(cmd)

        if options is None:
            options = manage_commands.generate_options(cmd, description, connector)

        _cmd = {
            "func": cmd,
            "description": description,
            "guild_ids": guild_ids,
            "api_options": options,
            "default_permission": default_permission,
            "api_permissions": permissions,
            "connector": connector or {},
            "has_subcommands": has_subcommands,
        }
        obj = model.BaseCommandObject(name, _cmd)
        self.commandslash[name] = obj
        #print(f"Added command `{name}`")
        return obj

    def add_subcommand(
        self,
        cmd,
        base,
        subcommand_group=None,
        name=None,
        description: str = None,
        base_description: str = None,
        base_default_permission: bool = True,
        base_permissions: typing.Dict[int, list] = None,
        subcommand_group_description: str = None,
        guild_ids: typing.List[int] = None,
        options: list = None,
        connector: dict = None,
    ):
        """
        Registers subcommand to SlashCommand.

        :param cmd: Subcommand Coroutine.
        :type cmd: Coroutine
        :param base: Name of the base command.
        :type base: str
        :param subcommand_group: Name of the subcommand group, if any. Default ``None`` which represents there is no sub group.
        :type subcommand_group: str
        :param name: Name of the subcommand. Default name of the coroutine.
        :type name: str
        :param description: Description of the subcommand. Defaults to command docstring or ``None``.
        :type description: str
        :param base_description: Description of the base command. Default ``None``.
        :type base_description: str
        :param default_permission: Sets if users have permission to run base command by default, when no permissions are set. Default ``True``.
        :type default_permission: bool
        :param base_permissions: Dictionary of permissions of the slash command. Key being target guild_id and value being a list of permissions to apply. Default ``None``.
        :type base_permissions: dict
        :param subcommand_group_description: Description of the subcommand_group. Default ``None``.
        :type subcommand_group_description: str
        :param guild_ids: List of guild ID of where the command will be used. Default ``None``, which will be global command.
        :type guild_ids: List[int]
        :param options: Options of the subcommand. This will affect ``auto_convert`` and command data at Discord API. Default ``None``.
        :type options: list
        :param connector: Kwargs connector for the command. Default ``None``.
        :type connector: dict
        """
        base = base.lower()
        subcommand_group = subcommand_group.lower() if subcommand_group else subcommand_group
        name = name or cmd.__name__
        name = name.lower()
        description = description or getdoc(cmd)
        guild_ids = guild_ids if guild_ids else []
        if not all(isinstance(item, int) for item in guild_ids):
            raise IncorrectGuildIDType(
                f"The snowflake IDs {guild_ids} given are not a list of integers. Because of discord.py convention, please use integer IDs instead. Furthermore, the command '{name}' will be deactivated and broken until fixed."
            )

        if base in self.commandslash:
            for x in guild_ids:
                if x not in self.commandslash[base].allowed_guild_ids:
                    self.commandslash[base].allowed_guild_ids.append(x)

        if options is None:
            options = manage_commands.generate_options(cmd, description, connector)

        _cmd = {
            "func": None,
            "description": base_description,
            "guild_ids": guild_ids.copy(),
            "api_options": [],
            "default_permission": base_default_permission,
            "api_permissions": base_permissions,
            "connector": {},
            "has_subcommands": True,
        }
        _sub = {
            "func": cmd,
            "name": name,
            "description": description,
            "base_desc": base_description,
            "sub_group_desc": subcommand_group_description,
            "guild_ids": guild_ids,
            "api_options": options,
            "connector": connector or {},
        }
        if base not in self.commandslash:
            self.commandslash[base] = model.BaseCommandObject(base, _cmd)
        else:
            base_command = self.commandslash[base]
            base_command.has_subcommands = True
            if base_permissions:
                for applicable_guild in base_permissions:
                    if applicable_guild not in base_command.permissions:
                        base_command.permissions[applicable_guild] = []
                    base_command.permissions[applicable_guild].extend(
                        base_permissions[applicable_guild]
                    )
            if base_command.description:
                _cmd["description"] = base_command.description
        if base not in self.subcommands:
            self.subcommands[base] = {}
        if subcommand_group:
            if subcommand_group not in self.subcommands[base]:
                self.subcommands[base][subcommand_group] = {}
            if name in self.subcommands[base][subcommand_group]:
                raise DuplicateCommand(f"{base} {subcommand_group} {name}")
            obj = model.SubcommandObject(_sub, base, name, subcommand_group)
            self.subcommands[base][subcommand_group][name] = obj
        else:
            if name in self.subcommands[base]:
                raise DuplicateCommand(f"{base} {name}")
            obj = model.SubcommandObject(_sub, base, name)
            self.subcommands[base][name] = obj
        self.logger.debug(
            f"Added subcommand `{base} {subcommand_group or ''} {name or cmd.__name__}`"
        )
        return obj

    def slash(
        self,
        *,
        name: str = None,
        description: str = None,
        guild_ids: typing.List[int] = None,
        options: typing.List[dict] = None,
        default_permission: bool = True,
        permissions: dict = None,
        connector: dict = None,
    ):
        """
        Decorator that registers coroutine as a slash command.\n
        All decorator args must be passed as keyword-only args.\n
        1 arg for command coroutine is required for ctx(:class:`.model.SlashContext`),
        and if your slash command has some args, then those args are also required.\n
        All args must be passed as keyword-args.

        .. note::
            If you don't pass `options` but has extra args, then it will automatically generate options.
            However, it is not recommended to use it since descriptions will be "No Description." or the command's description.

        .. warning::
            Unlike discord.py's command, ``*args``, keyword-only args, converters, etc. are not supported or behave differently.

        Example:

        .. code-block:: python

            @slash.slash(name="ping")
            async def _slash(ctx): # Normal usage.
                await ctx.send(content=f"Pong! (`{round(bot.latency*1000)}`ms)")


            @slash.slash(name="pick")
            async def _pick(ctx, choice1, choice2): # Command with 1 or more args.
                await ctx.send(content=str(random.choice([choice1, choice2])))

        To format the connector, follow this example.

        .. code-block:: python

            {
                "example-arg": "example_arg",
                "시간": "hour"
                # Formatting connector is required for
                # using other than english for option parameter name
                # for in case.
            }

        Set discord UI's parameter name as key, and set command coroutine's arg name as value.

        :param name: Name of the slash command. Default name of the coroutine.
        :type name: str
        :param description: Description of the slash command. Default ``None``.
        :type description: str
        :param guild_ids: List of Guild ID of where the command will be used. Default ``None``, which will be global command.
        :type guild_ids: List[int]
        :param options: Options of the slash command. This will affect ``auto_convert`` and command data at Discord API. Default ``None``.
        :type options: List[dict]
        :param default_permission: Sets if users have permission to run slash command by default, when no permissions are set. Default ``True``.
        :type default_permission: bool
        :param permissions: Permission requirements of the slash command. Default ``None``.
        :type permissions: dict
        :param connector: Kwargs connector for the command. Default ``None``.
        :type connector: dict
        """
        if not permissions:
            permissions = {}

        def wrapper(cmd):
            decorator_permissions = getattr(cmd, "__permissions__", None)
            if decorator_permissions:
                permissions.update(decorator_permissions)

            obj = self.add_slash_command(
                cmd,
                name,
                description,
                guild_ids,
                options,
                default_permission,
                permissions,
                connector,
            )

            return obj

        return wrapper

    def subcommand(
        self,
        *,
        base,
        subcommand_group=None,
        name=None,
        description: str = None,
        base_description: str = None,
        base_desc: str = None,
        base_default_permission: bool = True,
        base_permissions: dict = None,
        subcommand_group_description: str = None,
        sub_group_desc: str = None,
        guild_ids: typing.List[int] = None,
        options: typing.List[dict] = None,
        connector: dict = None,
    ):
        """
        Decorator that registers subcommand.\n
        Unlike discord.py, you don't need base command.\n
        All args must be passed as keyword-args.

        .. note::
            If you don't pass `options` but has extra args, then it will automatically generate options.
            However, it is not recommended to use it since descriptions will be "No Description." or the command's description.

        .. warning::
            Unlike discord.py's command, ``*args``, keyword-only args, converters, etc. are not supported or behave differently.

        Example:

        .. code-block:: python

            # /group say <str>
            @slash.subcommand(base="group", name="say")
            async def _group_say(ctx, _str):
                await ctx.send(content=_str)

            # /group kick user <user>
            @slash.subcommand(base="group",
                              subcommand_group="kick",
                              name="user")
            async def _group_kick_user(ctx, user):
                ...

        :param base: Name of the base command.
        :type base: str
        :param subcommand_group: Name of the subcommand group, if any. Default ``None`` which represents there is no sub group.
        :type subcommand_group: str
        :param name: Name of the subcommand. Default name of the coroutine.
        :type name: str
        :param description: Description of the subcommand. Default ``None``.
        :type description: str
        :param base_description: Description of the base command. Default ``None``.
        :type base_description: str
        :param base_desc: Alias of ``base_description``.
        :param default_permission: Sets if users have permission to run slash command by default, when no permissions are set. Default ``True``.
        :type default_permission: bool
        :param permissions: Permission requirements of the slash command. Default ``None``.
        :type permissions: dict
        :param subcommand_group_description: Description of the subcommand_group. Default ``None``.
        :type subcommand_group_description: str
        :param sub_group_desc: Alias of ``subcommand_group_description``.
        :param guild_ids: List of guild ID of where the command will be used. Default ``None``, which will be global command.
        :type guild_ids: List[int]
        :param options: Options of the subcommand. This will affect ``auto_convert`` and command data at Discord API. Default ``None``.
        :type options: List[dict]
        :param connector: Kwargs connector for the command. Default ``None``.
        :type connector: dict
        """
        base_description = base_description or base_desc
        subcommand_group_description = subcommand_group_description or sub_group_desc
        if not base_permissions:
            base_permissions = {}

        def wrapper(cmd):
            decorator_permissions = getattr(cmd, "__permissions__", None)
            if decorator_permissions:
                base_permissions.update(decorator_permissions)

            obj = self.add_subcommand(
                cmd,
                base,
                subcommand_group,
                name,
                description,
                base_description,
                base_default_permission,
                base_permissions,
                subcommand_group_description,
                guild_ids,
                options,
                connector,
            )

            return obj

        return wrapper

    def permission(self, guild_id: int, permissions: list):
        """
        Decorator that add permissions. This will set the permissions for a single guild, you can use it more than once for each command.

        :param guild_id: ID of the guild for the permissions.
        :type guild_id: int
        :param permissions: List of permissions to be set for the specified guild.
        :type permissions: list
        """

        def wrapper(cmd):
            if not getattr(cmd, "__permissions__", None):
                cmd.__permissions__ = {}
            cmd.__permissions__[guild_id] = permissions
            return cmd

        return wrapper

    def add_component_callback(
        self,
        callback: typing.Coroutine,
        *,
        messages: typing.Union[int, discord.Message, list] = None,
        components: typing.Union[str, dict, list] = None,
        use_callback_name=True,
        component_type: int = None,
    ):
        """
        Adds a coroutine callback to a component.
        Callback can be made to only accept component interactions from a specific messages
        and/or custom_ids of components.

        :param Coroutine callback: The coroutine to be called when the component is interacted with. Must accept a single argument with the type :class:`.context.ComponentContext`.
        :param messages: If specified, only interactions from the message given will be accepted. Can be a message object to check for, or the message ID or list of previous two. Empty list will mean that no interactions are accepted.
        :type messages: Union[discord.Message, int, list]
        :param components: If specified, only interactions with ``custom_id`` of given components will be accepted. Defaults to the name of ``callback`` if ``use_callback_name=True``. Can be a custom ID (str) or component dict (actionrow or button) or list of previous two.
        :type components: Union[str, dict, list]
        :param use_callback_name: Whether the ``custom_id`` defaults to the name of ``callback`` if unspecified. If ``False``, either ``messages`` or ``components`` must be specified.
        :type use_callback_name: bool
        :param component_type: The type of the component to avoid collisions with other component types. See :class:`.model.ComponentType`.
        :type component_type: Optional[int]
        :raises: .error.DuplicateCustomID, .error.IncorrectFormat
        """

        message_ids = list(manage_components.get_messages_ids(messages)) if messages is not None else [None]
        custom_ids = list(manage_components.get_components_ids(components)) if components is not None else [None]

        if use_callback_name and custom_ids == [None]:
            custom_ids = [callback.__name__]

        if message_ids == [None] and custom_ids == [None]:
            raise IncorrectFormat("You must specify messages or components (or both)")

        callback_obj = model.ComponentCallbackObject(
            callback, message_ids, custom_ids, component_type
        )
        self._add_comp_callback_obj(callback_obj)
        return callback_obj

    def _add_comp_callback_obj(self, callback_obj):
        component_type = callback_obj.component_type

        for message_id, custom_id in callback_obj.keys:
            self._register_comp_callback_obj(callback_obj, message_id, custom_id, component_type)

    def _register_comp_callback_obj(self, callback_obj, message_id, custom_id, component_type):
        message_id_dict = self.components
        custom_id_dict = message_id_dict.setdefault(message_id, {})
        component_type_dict = custom_id_dict.setdefault(custom_id, {})

        if component_type in component_type_dict:
            raise DuplicateCallback(message_id, custom_id, component_type)

        component_type_dict[component_type] = callback_obj
        self.logger.debug(
            f"Added component callback for "
            f"message ID {message_id or '<any>'}, "
            f"custom_id `{custom_id or '<any>'}`, "
            f"component_type `{component_type or '<any>'}`"
        )

    def extend_component_callback(
        self,
        callback_obj: model.ComponentCallbackObject,
        message_id: int = None,
        custom_id: str = None,
    ):
        """
        Registers existing callback object (:class:`.model.ComponentCallbackObject`)
        for specific combination of message_id, custom_id, component_type.

        :param callback_obj: callback object.
        :type callback_obj: model.ComponentCallbackObject
        :param message_id: If specified, only removes the callback for the specific message ID.
        :type message_id: Optional[.model]
        :param custom_id: The ``custom_id`` of the component.
        :type custom_id: Optional[str]
        :raises: .error.DuplicateCustomID, .error.IncorrectFormat
        """

        component_type = callback_obj.component_type
        self._register_comp_callback_obj(callback_obj, message_id, custom_id, component_type)
        callback_obj.keys.add((message_id, custom_id))

    def get_component_callback(
        self,
        message_id: int = None,
        custom_id: str = None,
        component_type: int = None,
    ):
        """
        Returns component callback (or None if not found) for specific combination of message_id, custom_id, component_type.

        :param message_id: If specified, only removes the callback for the specific message ID.
        :type message_id: Optional[.model]
        :param custom_id: The ``custom_id`` of the component.
        :type custom_id: Optional[str]
        :param component_type: The type of the component. See :class:`.model.ComponentType`.
        :type component_type: Optional[int]

        :return: Optional[model.ComponentCallbackObject]
        """
        message_id_dict = self.components
        try:
            custom_id_dict = _get_val(message_id_dict, message_id)
            component_type_dict = _get_val(custom_id_dict, custom_id)
            callback = _get_val(component_type_dict, component_type)

        except KeyError:  # there was no key in dict and no global fallback
            pass
        else:
            return callback

    def remove_component_callback(
        self, message_id: int = None, custom_id: str = None, component_type: int = None
    ):
        """
        Removes a component callback from specific combination of message_id, custom_id, component_type.

        :param message_id: If specified, only removes the callback for the specific message ID.
        :type message_id: Optional[int]
        :param custom_id: The ``custom_id`` of the component.
        :type custom_id: Optional[str]
        :param component_type: The type of the component. See :class:`.model.ComponentType`.
        :type component_type: Optional[int]
        :raises: .error.IncorrectFormat
        """
        try:
            callback = self.components[message_id][custom_id].pop(component_type)
            if not self.components[message_id][custom_id]:  # delete dict nesting levels if empty
                self.components[message_id].pop(custom_id)
                if not self.components[message_id]:
                    self.components.pop(message_id)
        except KeyError:
            raise IncorrectFormat(
                f"Callback for "
                f"message ID `{message_id or '<any>'}`, "
                f"custom_id `{custom_id or '<any>'}`, "
                f"component_type `{component_type or '<any>'}` is not registered!"
            )
        else:
            callback.keys.remove((message_id, custom_id))

    def remove_component_callback_obj(self, callback_obj: model.ComponentCallbackObject):
        """
        Removes a component callback from all related message_id, custom_id listeners.

        :param callback_obj: callback object.
        :type callback_obj: model.ComponentCallbackObject
        :raises: .error.IncorrectFormat
        """
        if not callback_obj.keys:
            raise IncorrectFormat("Callback already removed from any listeners")

        component_type = callback_obj.component_type
        for message_id, custom_id in callback_obj.keys.copy():
            self.remove_component_callback(message_id, custom_id, component_type)

    def component_callback(
        self,
        *,
        messages: typing.Union[int, discord.Message, list] = None,
        components: typing.Union[str, dict, list] = None,
        use_callback_name=True,
        component_type: int = None,
    ):
        """
        Decorator that registers a coroutine as a component callback.
        Adds a coroutine callback to a component.
        Callback can be made to only accept component interactions from a specific messages
        and/or custom_ids of components.

        :param messages: If specified, only interactions from the message given will be accepted. Can be a message object to check for, or the message ID or list of previous two. Empty list will mean that no interactions are accepted.
        :type messages: Union[discord.Message, int, list]
        :param components: If specified, only interactions with ``custom_id`` of given components will be accepted. Defaults to the name of ``callback`` if ``use_callback_name=True``. Can be a custom ID (str) or component dict (actionrow or button) or list of previous two.
        :type components: Union[str, dict, list]
        :param use_callback_name: Whether the ``custom_id`` defaults to the name of ``callback`` if unspecified. If ``False``, either ``messages`` or ``components`` must be specified.
        :type use_callback_name: bool
        :param component_type: The type of the component to avoid collisions with other component types. See :class:`.model.ComponentType`.
        :type component_type: Optional[int]
        :raises: .error.DuplicateCustomID, .error.IncorrectFormat
        """

        def wrapper(callback):
            return self.add_component_callback(
                callback,
                messages=messages,
                components=components,
                use_callback_name=use_callback_name,
                component_type=component_type,
            )

        return wrapper

    async def process_options(
        self,
        guild: discord.Guild,
        options: list,
        connector: dict,
        temporary_auto_convert: dict = None,
    ) -> dict:
        """
        Processes Role, User, and Channel option types to discord.py's models.

        :param guild: Guild of the command message.
        :type guild: discord.Guild
        :param options: Dict of options.
        :type options: list
        :param connector: Kwarg connector.
        :param temporary_auto_convert: Temporary parameter, use this if options doesn't have ``type`` keyword.
        :return: Union[list, dict]
        """

        if not guild or not isinstance(guild, discord.Guild):
            return {connector.get(x["name"]) or x["name"]: x["value"] for x in options}

        converters = [
            # If extra converters are added and some needs to fetch it,
            # you should pass as a list with 1st item as a cache get method
            # and 2nd as a actual fetching method.
            [guild.get_member, guild.fetch_member],
            guild.get_channel,
            guild.get_role,
        ]

        types = {
            "user": 0,
            "USER": 0,
            model.SlashCommandOptionType.USER: 0,
            "6": 0,
            6: 0,
            "channel": 1,
            "CHANNEL": 1,
            model.SlashCommandOptionType.CHANNEL: 1,
            "7": 1,
            7: 1,
            "role": 2,
            "ROLE": 2,
            model.SlashCommandOptionType.ROLE: 2,
            8: 2,
            "8": 2,
        }

        to_return = {}

        for x in options:
            processed = None  # This isn't the best way, but we should to reduce duplicate lines.

            # This is to temporarily fix Issue #97, that on Android device
            # does not give option type from API.
            if "type" not in x:
                x["type"] = temporary_auto_convert[x["name"]]

            if x["type"] not in types:
                processed = x["value"]
            else:
                loaded_converter = converters[types[x["type"]]]
                if isinstance(loaded_converter, list):  # For user type.
                    cache_first = loaded_converter[0](int(x["value"]))
                    if cache_first:
                        processed = cache_first
                    else:
                        loaded_converter = loaded_converter[1]
                if not processed:
                    try:
                        processed = (
                            await loaded_converter(int(x["value"]))
                            if iscoroutinefunction(loaded_converter)
                            else loaded_converter(int(x["value"]))
                        )
                    except (
                        discord.Forbidden,
                        discord.HTTPException,
                        discord.NotFound,
                    ):  # Just in case.
                        self.logger.warning("Failed fetching discord object! Passing ID instead.")
                        processed = int(x["value"])
            to_return[connector.get(x["name"]) or x["name"]] = processed
        return to_return

    async def invoke_command(self, func, ctx, args):
        """
        Invokes command.

        :param func: Command coroutine.
        :param ctx: Context.
        :param args: Args. Can be list or dict.
        """
        try:
            await func.invoke(ctx, **args)
        except Exception as ex:
            if not await self._handle_invoke_error(func, ctx, ex):
                await self.on_slash_command_error(ctx, ex)

    async def invoke_component_callback(self, func, ctx):
        """
        Invokes component callback.

        :param func: Component callback object.
        :param ctx: Context.
        """
        try:
            await func.invoke(ctx)
        except Exception as ex:
            if not await self._handle_invoke_error(func, ctx, ex):
                await self.on_component_callback_error(ctx, ex)

    async def _handle_invoke_error(self, func, ctx, ex):
        if hasattr(func, "on_error"):
            if func.on_error is not None:
                try:
                    if hasattr(func, "cog"):
                        await func.on_error(func.cog, ctx, ex)
                    else:
                        await func.on_error(ctx, ex)
                    return True
                except Exception as e:
                    self.logger.error(f"{ctx.command}:: Error using error decorator: {e}")
        return False

    async def on_socket_response(self, msg):
        """
        This event listener is automatically registered at initialization of this class.

        .. warning::
            DO NOT MANUALLY REGISTER, OVERRIDE, OR WHATEVER ACTION TO THIS COROUTINE UNLESS YOU KNOW WHAT YOU ARE DOING.

        :param msg: Gateway message.
        """
        if msg["t"] != "INTERACTION_CREATE":
            return

        to_use = msg["d"]
        interaction_type = to_use["type"]
        if interaction_type in (1, 2):
            return await self._on_slash(to_use)
        if interaction_type == 3:
            return await self._on_component(to_use)

        raise NotImplementedError

    async def _on_component(self, to_use):
        ctx = ComponentContext(self.http, to_use, self, self.logger)
        self.dispatch("component", ctx)

        callback = self.get_component_callback(
            ctx.origin_message_id, ctx.custom_id, ctx.component_type
        )
        if callback is not None:
            self.dispatch("component_callback", ctx, callback)
            await self.invoke_component_callback(callback, ctx)

    async def _on_slash(self, to_use):
        if to_use["data"]["name"] in self.commandslash:

            ctx = SlashContext(self.http, to_use, self, self.logger)
            cmd_name = to_use["data"]["name"]

            if cmd_name not in self.commandslash and cmd_name in self.subcommands:
                return await self.handle_subcommand(ctx, to_use)

            selected_cmd = self.commandslash[to_use["data"]["name"]]

            if (
                selected_cmd.allowed_guild_ids
                and ctx.guild_id not in selected_cmd.allowed_guild_ids
            ):
                return

            if selected_cmd.has_subcommands and not selected_cmd.func:
                return await self.handle_subcommand(ctx, to_use)

            if "options" in to_use["data"]:
                for x in to_use["data"]["options"]:
                    if "value" not in x:
                        return await self.handle_subcommand(ctx, to_use)

            # This is to temporarily fix Issue #97, that on Android device
            # does not give option type from API.
            temporary_auto_convert = {}
            for x in selected_cmd.options:
                temporary_auto_convert[x["name"].lower()] = x["type"]

            args = (
                await self.process_options(
                    ctx.guild,
                    to_use["data"]["options"],
                    selected_cmd.connector,
                    temporary_auto_convert,
                )
                if "options" in to_use["data"]
                else {}
            )

            self.dispatch("slash_command", ctx)

            await self.invoke_command(selected_cmd, ctx, args)

    
    async def handle_subcommand(self, ctx: SlashContext, data: dict):
        """
        Coroutine for handling subcommand.

        .. warning::
            Do not manually call this.

        :param ctx: :class:`.model.SlashContext` instance.
        :param data: Gateway message.
        """
        if data["data"]["name"] not in self.subcommands:
            return
        base = self.subcommands[data["data"]["name"]]
        sub = data["data"]["options"][0]
        sub_name = sub["name"]
        if sub_name not in base:
            return
        ctx.subcommand_name = sub_name
        sub_opts = sub["options"] if "options" in sub else []
        for x in sub_opts:
            if "options" in x or "value" not in x:
                sub_group = x["name"]
                if sub_group not in base[sub_name]:
                    return
                ctx.subcommand_group = sub_group
                selected = base[sub_name][sub_group]

                # This is to temporarily fix Issue #97, that on Android device
                # does not give option type from API.
                temporary_auto_convert = {}
                for n in selected.options:
                    temporary_auto_convert[n["name"].lower()] = n["type"]

                args = (
                    await self.process_options(
                        ctx.guild, x["options"], selected.connector, temporary_auto_convert
                    )
                    if "options" in x
                    else {}
                )
                self.dispatch("slash_command", ctx)
                await self.invoke_command(selected, ctx, args)
                return
        selected = base[sub_name]

        # This is to temporarily fix Issue #97, that on Android device
        # does not give option type from API.
        temporary_auto_convert = {}
        for n in selected.options:
            temporary_auto_convert[n["name"].lower()] = n["type"]

        args = (
            await self.process_options(
                ctx.guild, sub_opts, selected.connector, temporary_auto_convert
            )
            if "options" in sub
            else {}
        )
        self.dispatch("slash_command", ctx)
        await self.invoke_command(selected, ctx, args)

    def _on_error(self, ctx, ex, event_name):
        on_event = "on_" + event_name
        if self.has_listener:
            if self.extra_events.get(on_event):
                self.dispatch(event_name, ctx, ex)
                return True
        if hasattr(self, on_event):
            self.dispatch(event_name, ctx, ex)
            return True
        return False

    async def on_slash_command_error(self, ctx, ex):
        """
        Handles Exception occurred from invoking command.

        Example of adding event:

        .. code-block:: python

            @client.event
            async def on_slash_command_error(ctx, ex):
                ...

        Example of adding listener:

        .. code-block:: python

            @bot.listen()
            async def on_slash_command_error(ctx, ex):
                ...

        :param ctx: Context of the command.
        :type ctx: :class:`.model.SlashContext`
        :param ex: Exception from the command invoke.
        :type ex: Exception
        :return:
        """
        if not self._on_error(ctx, ex, "slash_command_error"):
            # Prints exception if not overridden or has no listener for error.
            self.logger.exception(
                f"An exception has occurred while executing command `{ctx.name}`:"
            )

    async def on_component_callback_error(self, ctx, ex):
        """
        Handles Exception occurred from invoking component callback.

        Example of adding event:

        .. code-block:: python

            @client.event
            async def on_component_callback_error(ctx, ex):
                ...

        Example of adding listener:

        .. code-block:: python

            @bot.listen()
            async def on_component_callback_error(ctx, ex):
                ...

        :param ctx: Context of the callback.
        :type ctx: :class:`.model.ComponentContext`
        :param ex: Exception from the command invoke.
        :type ex: Exception
        :return:
        """
        if not self._on_error(ctx, ex, "component_callback_error"):
            # Prints exception if not overridden or has no listener for error.
            self.logger.exception(
                f"An exception has occurred while executing component callback custom ID `{ctx.custom_id}`:"
            )


class Bot(BotBase, discord.Client):
    """Represents a discord bot.

    This class is a subclass of :class:`discord.Client` and as a result
    anything that you can do with a :class:`discord.Client` you can do with
    this bot.

    This class also subclasses :class:`.GroupMixin` to provide the functionality
    to manage commands.

    Attributes
    -----------
    command_prefix
        The command prefix is what the message content must contain initially
        to have a command invoked. This prefix could either be a string to
        indicate what the prefix should be, or a callable that takes in the bot
        as its first parameter and :class:`discord.Message` as its second
        parameter and returns the prefix. This is to facilitate "dynamic"
        command prefixes. This callable can be either a regular function or
        a coroutine.

        An empty string as the prefix always matches, enabling prefix-less
        command invocation. While this may be useful in DMs it should be avoided
        in servers, as it's likely to cause performance issues and unintended
        command invocations.

        The command prefix could also be an iterable of strings indicating that
        multiple checks for the prefix should be used and the first one to
        match will be the invocation prefix. You can get this prefix via
        :attr:`.Context.prefix`. To avoid confusion empty iterables are not
        allowed.

        .. note::

            When passing multiple prefixes be careful to not pass a prefix
            that matches a longer prefix occurring later in the sequence.  For
            example, if the command prefix is ``('!', '!?')``  the ``'!?'``
            prefix will never be matched to any message as the previous one
            matches messages starting with ``!?``. This is especially important
            when passing an empty string, it should always be last as no prefix
            after it will be matched.
    case_insensitive: :class:`bool`
        Whether the commands should be case insensitive. Defaults to ``False``. This
        attribute does not carry over to groups. You must set it to every group if
        you require group commands to be case insensitive as well.
    description: :class:`str`
        The content prefixed into the default help message.
    self_bot: :class:`bool`
        If ``True``, the bot will only listen to commands invoked by itself rather
        than ignoring itself. If ``False`` (the default) then the bot will ignore
        itself. This cannot be changed once initialised.
    help_command: Optional[:class:`.HelpCommand`]
        The help command implementation to use. This can be dynamically
        set at runtime. To remove the help command pass ``None``. For more
        information on implementing a help command, see :ref:`ext_commands_help_command`.
    owner_id: Optional[:class:`int`]
        The user ID that owns the bot. If this is not set and is then queried via
        :meth:`.is_owner` then it is fetched automatically using
        :meth:`~.Bot.application_info`.
    owner_ids: Optional[Collection[:class:`int`]]
        The user IDs that owns the bot. This is similar to :attr:`owner_id`.
        If this is not set and the application is team based, then it is
        fetched automatically using :meth:`~.Bot.application_info`.
        For performance reasons it is recommended to use a :class:`set`
        for the collection. You cannot set both ``owner_id`` and ``owner_ids``.

        .. versionadded:: 1.3
    strip_after_prefix: :class:`bool`
        Whether to strip whitespace characters after encountering the command
        prefix. This allows for ``!   hello`` and ``!hello`` to both work if
        the ``command_prefix`` is set to ``!``. Defaults to ``False``.

        .. versionadded:: 1.7
    """
    pass

class AutoShardedBot(BotBase, discord.AutoShardedClient):
    """This is similar to :class:`.Bot` except that it is inherited from
    :class:`discord.AutoShardedClient` instead.
    """
    pass
