# DCSTitleManager

Minecraft 服务器称号管理 MCDR 插件，基于 Team 机制实现称号的前缀显示，玩家可自行切换佩戴。

## 依赖

| 依赖 | 版本 | 说明 |
|---|---|---|
| MCDReforged | >=2.14.0 | 核心框架 |
| openpyxl | >=3.0.0 | 可选，导入导出功能需要 |

## 命令

### 玩家命令

| 命令 | 说明 |
|---|---|
| `!!title` | 显示帮助 |
| `!!title help` | 显示帮助 |
| `!!title list [页码]` | 查看拥有的称号 |
| `!!title set <titleId>` | 佩戴称号 |
| `!!title leave` | 解除佩戴 |

### 管理员命令

| 命令 | 说明 |
|---|---|
| `!!title add <titleId> <名称> <颜色> <加粗>` | 创建称号（无需输入中括号） |
| `!!title remove <titleId>` | 删除称号 |
| `!!title join <玩家> <titleId>` | 赋予并佩戴 |
| `!!title give <玩家> <titleId>` | 赋予（不佩戴） |
| `!!title delete <玩家> <titleId>` | 移除玩家称号 |
| `!!title show all` | 查看所有称号 |
| `!!title show player <玩家>` | 查看玩家称号 |
| `!!title show title <titleId>` | 查看称号拥有者 |
| `!!title move <旧玩家> <新玩家>` | 迁移称号（改名） |
| `!!title export` | 导出数据到 Excel |
| `!!title import` | 从 Excel 导入（预览） |
| `!!title import confirm` | 确认导入 |

## 游戏内交互

- 称号列表以**实际颜色和加粗**效果预览，所见即所得
- 称号名可**点击**直接佩戴，佩戴中的称号显示 `[解除]` 按钮
- 鼠标**悬停**显示操作提示
- 管理员 `show all` 中点击称号名可跳转查看拥有者

## 数据文件

数据存储在 `/config/title_manager/` 目录下。

### `title.json` — 称号定义

```json
[
  {
    "id": "1",
    "name": "[星期六]",
    "color": "red",
    "bold": "true"
  }
]
```

> 创建称号时无需输入中括号，插件会自动补齐 `[名称]`，Team 前缀中自动追加空格与玩家名分隔。

等效命令：

```
/team modify 1 prefix {"text":"[星期六] ","color":"red","bold":true}
```

效果：![titleEG](/img/titleEG.png)

### `playerTitleData.json` — 玩家与称号的关联

```json
[
  { "playerName": "Steve", "titleId": "1" },
  { "playerName": "Steve", "titleId": "2" },
  { "playerName": "Alex",  "titleId": "2" }
]
```

### `wearingTitle.json` — 当前佩戴状态

```json
{
  "Steve": "1",
  "Alex": "2"
}
```

## Excel 导入导出

`!!title export` 导出数据到插件目录下的 `title_data_export.xlsx`，包含三个 Sheet：

| Sheet | 列 | 说明 |
|---|---|---|
| 称号 | 称号ID / 名称 / 颜色 / 加粗 | 所有称号定义 |
| 玩家称号 | 玩家名 / 称号ID | 玩家与称号关联 |
| 佩戴状态 | 玩家名 / 佩戴称号ID | 当前佩戴状态 |

**导入流程：**

1. 将 Excel 文件放到插件数据目录，命名为 `title_data_export.xlsx`
2. 执行 `!!title import` 预览数据量
3. 确认后执行 `!!title import confirm` 完成导入

> [!WARNING]
> 导入会**覆盖**当前所有数据，请先 `!!title export` 备份。

## Name Handler 适配

> [!IMPORTANT]
> 本插件通过修改 Team 前缀改变玩家名显示格式，默认的 `vanilla_handler` 无法正确解析，需配合以下 Handler 使用：

```python
import re
from mcdreforged.handler.impl import VanillaHandler

PLUGIN_METADATA = {
    'id': 'name_handler',
    'version': '0.0.0',
}

class MyHandler(VanillaHandler):
    def get_name(self) -> str:
        return 'name_handler'

    def pre_parse_server_stdout(self, text: str):
        text = super().pre_parse_server_stdout(text)
        # 去掉第三个 [xxx]（称号前缀），保留前两个
        text = re.sub(
            r'^(.*?\[[^]]+\].*?\[[^]]+\].*?)\[[^]]+\]\s+',
            r'\1',
            text
        )
        return text

    def parse_server_stdout(self, text: str):
        info = super().parse_server_stdout(text)
        if info.player is None:
            m = re.fullmatch(r'<\[[^]]+](?P<name>[^>]+)> (?P<message>.*)', info.content)
            if m is not None:
                name = m['name'].strip()
                if self._verify_player_name(name):
                    info.player, info.content = name, m['message']
        return info

def on_load(server, prev_module):
    server.register_server_handler(MyHandler())
```

> [!IMPORTANT]
> 启用本插件前，建议清除服务器内所有已有 Team，避免冲突。
