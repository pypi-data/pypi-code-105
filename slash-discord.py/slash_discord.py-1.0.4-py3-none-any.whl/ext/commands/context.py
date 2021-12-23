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

import datetime
import discord.abc
import discord.utils
import typing
from .model import *
from .errors import *
from .errors import IncorrectFormat, AlreadyResponded
from warnings import warn
from ...http import HTTPClient
from ...utils import snowflake_time


class Context(discord.abc.Messageable):
    r"""Represents the context in which a command is being invoked under.

    This class contains a lot of meta data to help you understand more about
    the invocation context. This class is not created manually and is instead
    passed around to commands as the first parameter.

    This class implements the :class:`~discord.abc.Messageable` ABC.

    Attributes
    -----------
    message: :class:`.Message`
        The message that triggered the command being executed.
    bot: :class:`.Bot`
        The bot that contains the command being executed.
    args: :class:`list`
        The list of transformed arguments that were passed into the command.
        If this is accessed during the :func:`on_command_error` event
        then this list could be incomplete.
    kwargs: :class:`dict`
        A dictionary of transformed arguments that were passed into the command.
        Similar to :attr:`args`\, if this is accessed in the
        :func:`on_command_error` event then this dict could be incomplete.
    prefix: :class:`str`
        The prefix that was used to invoke the command.
    command: :class:`Command`
        The command that is being invoked currently.
    invoked_with: :class:`str`
        The command name that triggered this invocation. Useful for finding out
        which alias called the command.
    invoked_parents: List[:class:`str`]
        The command names of the parents that triggered this invocation. Useful for
        finding out which aliases called the command.

        For example in commands ``?a b c test``, the invoked parents are ``['a', 'b', 'c']``.

        .. versionadded:: 1.7

    invoked_subcommand: :class:`Command`
        The subcommand that was invoked.
        If no valid subcommand was invoked then this is equal to ``None``.
    subcommand_passed: Optional[:class:`str`]
        The string that was attempted to call a subcommand. This does not have
        to point to a valid registered subcommand and could just point to a
        nonsense string. If nothing was passed to attempt a call to a
        subcommand then this is set to ``None``.
    command_failed: :class:`bool`
        A boolean that indicates if the command failed to be parsed, checked,
        or invoked.
    """

    def __init__(self, **attrs):
        self.message = attrs.pop('message', None)
        self.bot = attrs.pop('bot', None)
        self.args = attrs.pop('args', [])
        self.kwargs = attrs.pop('kwargs', {})
        self.prefix = attrs.pop('prefix')
        self.command = attrs.pop('command', None)
        self.view = attrs.pop('view', None)
        self.invoked_with = attrs.pop('invoked_with', None)
        self.invoked_parents = attrs.pop('invoked_parents', [])
        self.invoked_subcommand = attrs.pop('invoked_subcommand', None)
        self.subcommand_passed = attrs.pop('subcommand_passed', None)
        self.command_failed = attrs.pop('command_failed', False)
        self._state = self.message._state

    async def invoke(self, *args, **kwargs):
        r"""|coro|

        Calls a command with the arguments given.

        This is useful if you want to just call the callback that a
        :class:`.Command` holds internally.

        .. note::

            This does not handle converters, checks, cooldowns, pre-invoke,
            or after-invoke hooks in any matter. It calls the internal callback
            directly as-if it was a regular function.

            You must take care in passing the proper arguments when
            using this function.

        .. warning::

            The first parameter passed **must** be the command being invoked.

        Parameters
        -----------
        command: :class:`.Command`
            The command that is going to be called.
        \*args
            The arguments to to use.
        \*\*kwargs
            The keyword arguments to use.

        Raises
        -------
        TypeError
            The command argument to invoke is missing.
        """

        try:
            command = args[0]
        except IndexError:
            raise TypeError('Missing command to invoke.') from None

        arguments = []
        if command.cog is not None:
            arguments.append(command.cog)

        arguments.append(self)
        arguments.extend(args[1:])

        ret = await command.callback(*arguments, **kwargs)
        return ret

    async def reinvoke(self, *, call_hooks=False, restart=True):
        """|coro|

        Calls the command again.

        This is similar to :meth:`~.Context.invoke` except that it bypasses
        checks, cooldowns, and error handlers.

        .. note::

            If you want to bypass :exc:`.UserInputError` derived exceptions,
            it is recommended to use the regular :meth:`~.Context.invoke`
            as it will work more naturally. After all, this will end up
            using the old arguments the user has used and will thus just
            fail again.

        Parameters
        ------------
        call_hooks: :class:`bool`
            Whether to call the before and after invoke hooks.
        restart: :class:`bool`
            Whether to start the call chain from the very beginning
            or where we left off (i.e. the command that caused the error).
            The default is to start where we left off.

        Raises
        -------
        ValueError
            The context to reinvoke is not valid.
        """
        cmd = self.command
        view = self.view
        if cmd is None:
            raise ValueError('This context is not valid.')

        # some state to revert to when we're done
        index, previous = view.index, view.previous
        invoked_with = self.invoked_with
        invoked_subcommand = self.invoked_subcommand
        invoked_parents = self.invoked_parents
        subcommand_passed = self.subcommand_passed

        if restart:
            to_call = cmd.root_parent or cmd
            view.index = len(self.prefix)
            view.previous = 0
            self.invoked_parents = []
            self.invoked_with = view.get_word() # advance to get the root command
        else:
            to_call = cmd

        try:
            await to_call.reinvoke(self, call_hooks=call_hooks)
        finally:
            self.command = cmd
            view.index = index
            view.previous = previous
            self.invoked_with = invoked_with
            self.invoked_subcommand = invoked_subcommand
            self.invoked_parents = invoked_parents
            self.subcommand_passed = subcommand_passed

    @property
    def valid(self):
        """:class:`bool`: Checks if the invocation context is valid to be invoked with."""
        return self.prefix is not None and self.command is not None

    async def _get_channel(self):
        return self.channel

    @property
    def cog(self):
        """Optional[:class:`.Cog`]: Returns the cog associated with this context's command. None if it does not exist."""

        if self.command is None:
            return None
        return self.command.cog

    @discord.utils.cached_property
    def guild(self):
        """Optional[:class:`.Guild`]: Returns the guild associated with this context's command. None if not available."""
        return self.message.guild

    @discord.utils.cached_property
    def channel(self):
        """Union[:class:`.abc.Messageable`]: Returns the channel associated with this context's command.
        Shorthand for :attr:`.Message.channel`.
        """
        return self.message.channel

    @discord.utils.cached_property
    def author(self):
        """Union[:class:`~discord.User`, :class:`.Member`]:
        Returns the author associated with this context's command. Shorthand for :attr:`.Message.author`
        """
        return self.message.author

    @discord.utils.cached_property
    def me(self):
        """Union[:class:`.Member`, :class:`.ClientUser`]:
        Similar to :attr:`.Guild.me` except it may return the :class:`.ClientUser` in private message contexts.
        """
        return self.guild.me if self.guild is not None else self.bot.user

    @property
    def voice_client(self):
        r"""Optional[:class:`.VoiceProtocol`]: A shortcut to :attr:`.Guild.voice_client`\, if applicable."""
        g = self.guild
        return g.voice_client if g else None

    async def send_help(self, *args):
        """send_help(entity=<bot>)

        |coro|

        Shows the help command for the specified entity if given.
        The entity can be a command or a cog.

        If no entity is given, then it'll show help for the
        entire bot.

        If the entity is a string, then it looks up whether it's a
        :class:`Cog` or a :class:`Command`.

        .. note::

            Due to the way this function works, instead of returning
            something similar to :meth:`~.commands.HelpCommand.command_not_found`
            this returns :class:`None` on bad input or no help command.

        Parameters
        ------------
        entity: Optional[Union[:class:`Command`, :class:`Cog`, :class:`str`]]
            The entity to show help for.

        Returns
        --------
        Any
            The result of the help command, if any.
        """
        from .core import Group, Command, wrap_callback
        from .errors import CommandError

        bot = self.bot
        cmd = bot.help_command

        if cmd is None:
            return None

        cmd = cmd.copy()
        cmd.context = self
        if len(args) == 0:
            await cmd.prepare_help_command(self, None)
            mapping = cmd.get_bot_mapping()
            injected = wrap_callback(cmd.send_bot_help)
            try:
                return await injected(mapping)
            except CommandError as e:
                await cmd.on_help_command_error(self, e)
                return None

        entity = args[0]
        if entity is None:
            return None

        if isinstance(entity, str):
            entity = bot.get_cog(entity) or bot.get_command(entity)

        try:
            entity.qualified_name
        except AttributeError:
            # if we're here then it's not a cog, group, or command.
            return None

        await cmd.prepare_help_command(self, entity.qualified_name)

        try:
            if hasattr(entity, '__cog_commands__'):
                injected = wrap_callback(cmd.send_cog_help)
                return await injected(entity)
            elif isinstance(entity, Group):
                injected = wrap_callback(cmd.send_group_help)
                return await injected(entity)
            elif isinstance(entity, Command):
                injected = wrap_callback(cmd.send_command_help)
                return await injected(entity)
            else:
                return None
        except CommandError as e:
            await cmd.on_help_command_error(self, e)

    @discord.utils.copy_doc(discord.Message.reply)
    async def reply(self, content=None, **kwargs):
        return await self.message.reply(content, **kwargs)

class InteractionContext:
    """
    Base context for interactions.\n
    In some ways similar with discord.ext.commands.Context.

    .. warning::
        Do not manually init this model.

    :ivar message: Message that invoked the slash command.
    :ivar interaction_id: Interaction ID of the command message.
    :ivar bot: discord.py client.
    :ivar _http: :class:`.http.SlashCommandRequest` of the client.
    :ivar _logger: Logger instance.
    :ivar data: The raw data of the interaction.
    :ivar values: The values sent with the interaction. Currently for selects.
    :ivar deferred: Whether the command is current deferred (loading state)
    :ivar _deferred_hidden: Internal var to check that state stays the same
    :ivar responded: Whether you have responded with a message to the interaction.
    :ivar guild_id: Guild ID of the command message. If the command was invoked in DM, then it is ``None``
    :ivar author_id: User ID representing author of the command message.
    :ivar channel_id: Channel ID representing channel of the command message.
    :ivar author: User or Member instance of the command invoke.

    """

    def __init__(
        self,
        _http: HTTPClient,
        _json: dict,
        _discord: discord.Client,
        logger,
    ):
        self._token = _json["token"]
        self.message = None  # Should be set later.
        self.interaction_id = _json["id"]
        self._http = _http
        self.bot = _discord
        self._logger = logger
        self.deferred = False
        self.responded = False
        self.data = _json["data"]
        self.values = _json["data"]["values"] if "values" in _json["data"] else None
        self._deferred_hidden = False  # To check if the patch to the deferred response matches
        self.guild_id = int(_json["guild_id"]) if "guild_id" in _json.keys() else None
        self.author_id = int(
            _json["member"]["user"]["id"] if "member" in _json.keys() else _json["user"]["id"]
        )
        self.channel_id = int(_json["channel_id"])
        if self.guild:
            self.author = discord.Member(
                data=_json["member"], state=self.bot._connection, guild=self.guild
            )
        elif self.guild_id:
            self.author = discord.User(data=_json["member"]["user"], state=self.bot._connection)
        else:
            self.author = discord.User(data=_json["user"], state=self.bot._connection)
        self.created_at: datetime.datetime = snowflake_time(int(self.interaction_id))

    @property
    def _deffered_hidden(self):
        warn(
            "`_deffered_hidden` as been renamed to `_deferred_hidden`.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._deferred_hidden

    @_deffered_hidden.setter
    def _deffered_hidden(self, value):
        warn(
            "`_deffered_hidden` as been renamed to `_deferred_hidden`.",
            DeprecationWarning,
            stacklevel=2,
        )
        self._deferred_hidden = value

    @property
    def deffered(self):
        warn("`deffered` as been renamed to `deferred`.", DeprecationWarning, stacklevel=2)
        return self.deferred

    @deffered.setter
    def deffered(self, value):
        warn("`deffered` as been renamed to `deferred`.", DeprecationWarning, stacklevel=2)
        self.deferred = value

    @property
    def guild(self) -> typing.Optional[discord.Guild]:
        """
        Guild instance of the command invoke. If the command was invoked in DM, then it is ``None``

        :return: Optional[discord.Guild]
        """
        return self.bot.get_guild(self.guild_id) if self.guild_id else None

    @property
    def channel(self) -> typing.Optional[typing.Union[discord.TextChannel, discord.DMChannel]]:
        """
        Channel instance of the command invoke.

        :return: Optional[Union[discord.abc.GuildChannel, discord.abc.PrivateChannel]]
        """
        return self.bot.get_channel(self.channel_id)

    async def defer(self, hidden: bool = False):
        """
        'Defers' the response, showing a loading state to the user

        :param hidden: Whether the deferred response should be ephemeral . Default ``False``.
        """
        if self.deferred or self.responded:
            raise AlreadyResponded("You have already responded to this command!")
        base = {"type": 5}
        if hidden:
            base["data"] = {"flags": 64}
            self._deferred_hidden = True
        await self._http.post_initial_response(base, self.interaction_id, self._token)
        self.deferred = True

    async def send(
        self,
        content: str = "",
        *,
        embed: discord.Embed = None,
        embeds: typing.List[discord.Embed] = None,
        tts: bool = False,
        file: discord.File = None,
        files: typing.List[discord.File] = None,
        allowed_mentions: discord.AllowedMentions = None,
        hidden: bool = False,
        delete_after: float = None,
        components: typing.List[dict] = None,
    ) -> SlashMessage:
        """
        Sends response of the interaction.

        .. warning::
            - Since Release 1.0.9, this is completely changed. If you are migrating from older version, please make sure to fix the usage.
            - You can't use both ``embed`` and ``embeds`` at the same time, also applies to ``file`` and ``files``.
            - If you send files in the initial response, this will defer if it's not been deferred, and then PATCH with the message

        :param content:  Content of the response.
        :type content: str
        :param embed: Embed of the response.
        :type embed: discord.Embed
        :param embeds: Embeds of the response. Maximum 10.
        :type embeds: List[discord.Embed]
        :param tts: Whether to speak message using tts. Default ``False``.
        :type tts: bool
        :param file: File to send.
        :type file: discord.File
        :param files: Files to send.
        :type files: List[discord.File]
        :param allowed_mentions: AllowedMentions of the message.
        :type allowed_mentions: discord.AllowedMentions
        :param hidden: Whether the message is hidden, which means message content will only be seen to the author.
        :type hidden: bool
        :param delete_after: If provided, the number of seconds to wait in the background before deleting the message we just sent. If the deletion fails, then it is silently ignored.
        :type delete_after: float
        :param components: Message components in the response. The top level must be made of ActionRows.
        :type components: List[dict]
        :return: Union[discord.Message, dict]
        """
        if embed and embeds:
            raise IncorrectFormat("You can't use both `embed` and `embeds`!")
        if embed:
            embeds = [embed]
        if embeds:
            if not isinstance(embeds, list):
                raise IncorrectFormat("Provide a list of embeds.")
            elif len(embeds) > 10:
                raise IncorrectFormat("Do not provide more than 10 embeds.")
        if file and files:
            raise IncorrectFormat("You can't use both `file` and `files`!")
        if file:
            files = [file]
        if delete_after and hidden:
            raise IncorrectFormat("You can't delete a hidden message!")
        if components and not all(comp.get("type") == 1 for comp in components):
            raise IncorrectFormat(
                "The top level of the components list must be made of ActionRows!"
            )

        if allowed_mentions is not None:
            if self.bot.allowed_mentions is not None:
                allowed_mentions = self.bot.allowed_mentions.merge(allowed_mentions).to_dict()
            else:
                allowed_mentions = allowed_mentions.to_dict()
        else:
            if self.bot.allowed_mentions is not None:
                allowed_mentions = self.bot.allowed_mentions.to_dict()
            else:
                allowed_mentions = {}

        base = {
            "content": content,
            "tts": tts,
            "embeds": [x.to_dict() for x in embeds] if embeds else [],
            "allowed_mentions": allowed_mentions,
            "components": components or [],
        }
        if hidden:
            base["flags"] = 64

        initial_message = False
        if not self.responded:
            initial_message = True
            if files and not self.deferred:
                await self.defer(hidden=hidden)
            if self.deferred:
                if self._deferred_hidden != hidden:
                    self._logger.warning(
                        "Deferred response might not be what you set it to! (hidden / visible) "
                        "This is because it was deferred in a different state."
                    )
                resp = await self._http.edit(base, self._token, files=files)
                self.deferred = False
            else:
                json_data = {"type": 4, "data": base}
                await self._http.post_initial_response(json_data, self.interaction_id, self._token)
                if not hidden:
                    resp = await self._http.edit({}, self._token)
                else:
                    resp = {}
            self.responded = True
        else:
            resp = await self._http.post_followup(base, self._token, files=files)
        if files:
            for file in files:
                file.close()
        if not hidden:
            smsg = SlashMessage(
                state=self.bot._connection,
                data=resp,
                channel=self.channel or discord.Object(id=self.channel_id),
                _http=self._http,
                interaction_token=self._token,
            )
            if delete_after:
                self.bot.loop.create_task(smsg.delete(delay=delete_after))
            if initial_message:
                self.message = smsg
            return smsg
        else:
            return resp

class SlashContext(InteractionContext):
    """
    Context of a slash command. Has all attributes from :class:`InteractionContext`, plus the slash-command-specific ones below.

    :ivar name: Name of the command.
    :ivar args: List of processed arguments invoked with the command.
    :ivar kwargs: Dictionary of processed arguments invoked with the command.
    :ivar subcommand_name: Subcommand of the command.
    :ivar subcommand_group: Subcommand group of the command.
    :ivar command_id: ID of the command.
    """

    def __init__(
        self,
        _http: HTTPClient,
        _json: dict,
        _discord: discord.Client,
        logger,
    ):
        self.name = self.command = self.invoked_with = _json["data"]["name"]
        self.args = []
        self.kwargs = {}
        self.subcommand_name = self.invoked_subcommand = self.subcommand_passed = None
        self.subcommand_group = self.invoked_subcommand_group = self.subcommand_group_passed = None
        self.command_id = _json["data"]["id"]

        super().__init__(_http=_http, _json=_json, _discord=_discord, logger=logger)

class ComponentContext(InteractionContext):
    """
    Context of a component interaction. Has all attributes from :class:`InteractionContext`, plus the component-specific ones below.

    :ivar custom_id: The custom ID of the component (has alias component_id).
    :ivar component_type: The type of the component.
    :ivar component: Component data retrieved from the message. Not available if the origin message was ephemeral.
    :ivar origin_message: The origin message of the component. Not available if the origin message was ephemeral.
    :ivar origin_message_id: The ID of the origin message.
    :ivar selected_options: The options selected (only for selects)
    """

    def __init__(
        self,
        _http: HTTPClient,
        _json: dict,
        _discord: discord.Client,
        logger,
    ):
        self.custom_id = self.component_id = _json["data"]["custom_id"]
        self.component_type = _json["data"]["component_type"]
        super().__init__(_http=_http, _json=_json, _discord=_discord, logger=logger)
        self.origin_message = None
        self.origin_message_id = int(_json["message"]["id"]) if "message" in _json.keys() else None

        self.component = None

        self._deferred_edit_origin = False

        if self.origin_message_id and (_json["message"]["flags"] & 64) != 64:
            self.origin_message = ComponentMessage(
                state=self.bot._connection, channel=self.channel, data=_json["message"]
            )
            self.component = self.origin_message.get_component(self.custom_id)

        self.selected_options = None

        if self.component_type == 3:
            self.selected_options = _json["data"].get("values", [])

    async def defer(self, hidden: bool = False, edit_origin: bool = False):
        """
        'Defers' the response, showing a loading state to the user

        :param hidden: Whether the deferred response should be ephemeral . Default ``False``.
        :param edit_origin: Whether the type is editing the origin message. If ``False``, the deferred response will be for a follow up message. Defaults ``False``.
        """
        if self.deferred or self.responded:
            raise errors.AlreadyResponded("You have already responded to this command!")

        base = {"type": 6 if edit_origin else 5}

        if hidden:
            if edit_origin:
                raise errors.IncorrectFormat(
                    "'hidden' and 'edit_origin' flags are mutually exclusive"
                )
            base["data"] = {"flags": 64}
            self._deferred_hidden = True

        self._deferred_edit_origin = edit_origin

        await self._http.post_initial_response(base, self.interaction_id, self._token)
        self.deferred = True

    async def send(
        self,
        content: str = "",
        *,
        embed = None,
        embeds = None,
        tts: bool = False,
        file: discord.File = None,
        files = None,
        allowed_mentions: discord.AllowedMentions = None,
        hidden: bool = False,
        delete_after: float = None,
        components: dict = None,
    ) -> SlashMessage:
        if self.deferred and self._deferred_edit_origin:
            self._logger.warning(
                "Deferred response might not be what you set it to! (edit origin / send response message) "
                "This is because it was deferred with different response type."
            )
        return await super().send(
            content,
            embed=embed,
            embeds=embeds,
            tts=tts,
            file=file,
            files=files,
            allowed_mentions=allowed_mentions,
            hidden=hidden,
            delete_after=delete_after,
            components=components,
        )

    async def edit_origin(self, **fields):
        """
        Edits the origin message of the component.
        Refer to :meth:`discord.Message.edit` and :meth:`InteractionContext.send` for fields.
        """
        _resp = {}

        try:
            content = fields["content"]
        except KeyError:
            pass
        else:
            if content is not None:
                content = str(content)
            _resp["content"] = content

        try:
            components = fields["components"]
        except KeyError:
            pass
        else:
            if components is None:
                _resp["components"] = []
            else:
                _resp["components"] = components

        try:
            embeds = fields["embeds"]
        except KeyError:
            # Nope
            pass
        else:
            if not isinstance(embeds, list):
                raise errors.IncorrectFormat("Provide a list of embeds.")
            if len(embeds) > 10:
                raise errors.IncorrectFormat("Do not provide more than 10 embeds.")
            _resp["embeds"] = [e.to_dict() for e in embeds]

        try:
            embed = fields["embed"]
        except KeyError:
            pass
        else:
            if "embeds" in _resp:
                raise errors.IncorrectFormat("You can't use both `embed` and `embeds`!")

            if embed is None:
                _resp["embeds"] = []
            else:
                _resp["embeds"] = [embed.to_dict()]

        file = fields.get("file")
        files = fields.get("files")

        if files is not None and file is not None:
            raise errors.IncorrectFormat("You can't use both `file` and `files`!")
        if file:
            files = [file]

        allowed_mentions = fields.get("allowed_mentions")
        if allowed_mentions is not None:
            if self.bot.allowed_mentions is not None:
                _resp["allowed_mentions"] = self.bot.allowed_mentions.merge(
                    allowed_mentions
                ).to_dict()
            else:
                _resp["allowed_mentions"] = allowed_mentions.to_dict()
        else:
            if self.bot.allowed_mentions is not None:
                _resp["allowed_mentions"] = self.bot.allowed_mentions.to_dict()
            else:
                _resp["allowed_mentions"] = {}

        if not self.responded:
            if files and not self.deferred:
                await self.defer(edit_origin=True)
            if self.deferred:
                if not self._deferred_edit_origin:
                    self._logger.warning(
                        "Deferred response might not be what you set it to! (edit origin / send response message) "
                        "This is because it was deferred with different response type."
                    )
                _json = await self._http.edit(_resp, self._token, files=files)
                self.deferred = False
            else:  # noqa: F841
                json_data = {"type": 7, "data": _resp}
                _json = await self._http.post_initial_response(  # noqa: F841
                    json_data, self.interaction_id, self._token
                )
            self.responded = True
        else:
            raise errors.IncorrectFormat("Already responded")

        if files:
            for file in files:
                file.close()

        # Commented out for now as sometimes (or at least, when not deferred) _json is an empty string?
        # self.origin_message = ComponentMessage(state=self.bot._connection, channel=self.channel,
        #                                        data=_json)
