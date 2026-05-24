"""
DCSTitleManager 称号管理插件
"""

from mcdreforged.api.types import PluginServerInterface, Info

from .storage import Storage
from .title_manager import TitleManager
from .command import register as register_commands

_manager: TitleManager = None


def on_load(server: PluginServerInterface, old):
    global _manager
    storage = Storage(server)
    _manager = TitleManager(server, storage)
    register_commands(server, _manager)
    server.logger.info('DCSTitleManager 已加载')


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    if _manager is not None:
        _manager.on_player_join(player)


def on_unload(server: PluginServerInterface):
    server.logger.info('DCSTitleManager 已卸载')
