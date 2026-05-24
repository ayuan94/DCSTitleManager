"""
命令注册层 - 注册所有 !!title 命令
"""

from mcdreforged.api.types import PluginServerInterface, CommandSource
from mcdreforged.api.command import Literal, Text, Integer

from .title_manager import TitleManager, ADMIN_PERM


def register(server: PluginServerInterface, manager: TitleManager) -> None:
    """注册所有称号管理命令"""

    def is_admin(src: CommandSource) -> bool:
        return src.has_permission(ADMIN_PERM)

    server.register_command(
        Literal('!!title')
        # ---- 帮助 ----
        .runs(lambda src: manager.cmd_help(src))
        .then(Literal('help').runs(lambda src: manager.cmd_help(src)))

        # ---- 玩家命令 ----
        .then(Literal('list')
            .runs(lambda src: manager.cmd_list(src))
            .then(Integer('page').runs(lambda src, ctx: manager.cmd_list(src, ctx['page'])))
        )
        .then(Literal('set')
            .then(Text('titleId').runs(lambda src, ctx: manager.cmd_set(src, ctx['titleId'])))
        )
        .then(Literal('leave').runs(lambda src: manager.cmd_leave(src)))

        # ---- 管理员命令 ----
        .then(Literal('add').requires(is_admin)
            .then(Text('titleId')
                .then(Text('name')
                    .then(Text('color')
                        .then(Text('bold').runs(
                            lambda src, ctx: manager.cmd_add(
                                src, ctx['titleId'], ctx['name'], ctx['color'], ctx['bold']
                            )
                        ))
                    )
                )
            )
        )
        .then(Literal('remove').requires(is_admin)
            .then(Text('titleId').runs(lambda src, ctx: manager.cmd_remove(src, ctx['titleId'])))
        )
        .then(Literal('join').requires(is_admin)
            .then(Text('player')
                .then(Text('titleId').runs(lambda src, ctx: manager.cmd_join(src, ctx['player'], ctx['titleId'])))
            )
        )
        .then(Literal('give').requires(is_admin)
            .then(Text('player')
                .then(Text('titleId').runs(lambda src, ctx: manager.cmd_give(src, ctx['player'], ctx['titleId'])))
            )
        )
        .then(Literal('delete').requires(is_admin)
            .then(Text('player')
                .then(Text('titleId').runs(lambda src, ctx: manager.cmd_delete(src, ctx['player'], ctx['titleId'])))
            )
        )
        .then(Literal('show').requires(is_admin)
            .then(Literal('all').runs(lambda src: manager.cmd_show_all(src)))
            .then(Literal('player')
                .then(Text('playerName').runs(lambda src, ctx: manager.cmd_show_player(src, ctx['playerName'])))
            )
            .then(Literal('title')
                .then(Text('titleId').runs(lambda src, ctx: manager.cmd_show_title(src, ctx['titleId'])))
            )
        )
        .then(Literal('move').requires(is_admin)
            .then(Text('old')
                .then(Text('new').runs(lambda src, ctx: manager.cmd_move(src, ctx['old'], ctx['new'])))
            )
        )
        .then(Literal('export').requires(is_admin)
            .runs(lambda src: manager.cmd_export(src))
        )
        .then(Literal('import').requires(is_admin)
            .runs(lambda src: manager.cmd_import(src))
            .then(Literal('confirm').runs(lambda src: manager.cmd_import_confirm(src)))
        )
    )

    server.register_help_message('!!title', '称号管理')

