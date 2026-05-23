# DCSTitleManager 称号管理插件

####  插件名称：title_manager

#### 功能概述：方便玩家能自行修改佩戴的称号。

- **玩家命令** ```!!title [help|list <page>|set <id>|leave]```
    - ```!!title/!!title help``` 帮助界面，展示所有功能
    - ```!!title list <page>``` 展示当前玩家所拥有的称号
    - ```!!title set <id>``` 给当前玩家设置该称号
    - ```!!title leave``` 解除当前玩家佩戴的称号

- **管理命令** ```!!title [add|remove <id>|join|give|delete|show <all|playerName|id>]```
    - ```!!title add <id> <name> <color> <bold>``` 创建新称号
    - ```!!title remove <id>``` 删除对应id的称号
    - ```!!title join <playerName> <id>``` 手动配置并加入某称号给玩家
    - ```!!title give <playerName> <id>``` 给某玩家新增一个称号但不佩配置
    - ```!!title delete <player> <id>``` 删除某玩家的某称号权限
    - ```!!title show```
        - ```all``` 展示当前服所有称号
        - ```playerName``` 展示该玩家所有称号
        - ```id``` 展示拥有该称号的所有玩家
    - ```!!title move <oldPlayerName> <newPlayerName>``` 将改名前玩家的称号迁移到改名后玩家账户下

    

#### 插件数据文件 /config

##### 1. ```/config/title.json``` 存储称号的详细信息


```json
[
  {
    "id": "1", /* 称号id */
    "name": "[星期六] ", /* 称号显示的名字，名字后加个空格 */
    "color": "red", /* 称号颜色 */
    "bold": "true" /* 是否加粗 */
  }
]
```

​	上面的配置等效于：/team modify 1 prefix {"text":"[星期六] ","color":"red","bold":true} 显示效果为：![titleEG](/title_plugin/img/titleEG.png)

​	```	/team modify 称号id prefix {"text":"称号名字","color":"称号颜色","bold":是否加粗}```

##### 2. ```/config/playerTitleData.json``` 存储玩家的称号所属信息

```json
[
  {
    "playerName":"playerNameA",
    "titleId":"1"
  },
  {
    "playerName":"playerNameA",
    "titleId":"2"
  },
  {
    "playerName":"playerNameB",
    "titleId":"2"
  }
]
```



> [!IMPORTANT]
> ##### 在应用此插件前，最好将该服内所有的team信息清除，以防冲突

> [!IMPORTANT]
> ##### 此插件由于修改了玩家名称格式，所以不能被默认的 ```vanilla_handler``` 处理，需要手动改修改适配

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
        # 去掉第三个[任意字符]（空格） 主要修改了下面这一行
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



