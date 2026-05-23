# DCSTitleManager 称号管理插件

####  插件名称：title_manager

 功能概述：方便玩家能自行修改佩戴的称号。

 具体实现： （写在前面：本插件指令识别头用!!title）

1. 基础前置：具备更新能力，比如通过!!title sync从世界存档中调取所有的team名称信息。（只需要名称即可）
2. 基础前置：具备调取识别玩家的功能，如果可行，使用uuid识别玩家，如果不行，退而求其次使用玩家名识别。
3. 基础前置：具备将玩家信息和team关联的功能，比如使用!!title jion team名称 玩家名称，将指定team添加到该玩家的可用team列表下（该指令限制操作权限，需要MCDR的管理员及以上权限），类似的添加!!title leave team名称 玩家名称用于移出。
4. 配置文件：存储team的名称，存储玩家识别信息以及对应玩家的可用team列表。
5. 功能实现：玩家可以使用!!title list调用自己的可用team列表（此处如果能同时显示team前缀的展示效果和team名称更好，如果不能就直接展示team本身的名字），查看列表后如果可以点击对应名称快速切换更好（如果不能实现就利用!!title set team名称切换）
6. 玩家信息自动录入 
7. 快速引导：利用!!title指令调出所有的title可用指令以及简易描述方便上手。
8. 指令汇总：!!title 快速上手 !!title sync 同步team信息 !!title join team名 玩家名 给玩家添加称号 !!title leave team名 玩家名 给玩家移出称号 !!title list 展示拥有的称号 !!title set team名 更换成指定称号 !!title signin 玩家注册
