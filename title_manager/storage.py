"""
数据持久化层 - 负责称号和玩家数据的加载与保存
"""

import json
import os
from typing import Any, Dict, List, Optional

from mcdreforged.api.types import PluginServerInterface


class Storage:
    """管理称号和玩家数据的持久化存储"""

    def __init__(self, server: PluginServerInterface):
        self.server = server
        self.data_dir = server.get_data_folder()
        os.makedirs(self.data_dir, exist_ok=True)

        self.title_file = os.path.join(self.data_dir, 'title.json')
        self.player_file = os.path.join(self.data_dir, 'playerTitleData.json')
        self.wearing_file = os.path.join(self.data_dir, 'wearingTitle.json')

        self.titles: List[Dict[str, Any]] = self._load(self.title_file, [])
        self.players: List[Dict[str, str]] = self._load(self.player_file, [])
        self.wearing: Dict[str, str] = self._load(self.wearing_file, {})

    # ---- 内部工具方法 ----

    def _load(self, filepath: str, default: Any) -> Any:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                self.server.logger.warning(f'加载数据文件失败 {filepath}: {e}')
        return default

    def _save(self, filepath: str, data: Any) -> None:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except IOError as e:
            self.server.logger.error(f'保存数据文件失败 {filepath}: {e}')

    # ---- 称号数据操作 ----

    def get_title(self, title_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取称号信息"""
        for t in self.titles:
            if t['id'] == title_id:
                return t.copy()
        return None

    def get_all_titles(self) -> List[Dict[str, Any]]:
        """获取所有称号"""
        return [t.copy() for t in self.titles]

    def add_title(self, title_id: str, name: str, color: str, bold: str) -> bool:
        """添加称号，返回是否成功（ID重复则失败）"""
        if self.get_title(title_id) is not None:
            return False
        self.titles.append({'id': title_id, 'name': name, 'color': color, 'bold': bold})
        self._save(self.title_file, self.titles)
        return True

    def remove_title(self, title_id: str) -> bool:
        """删除称号，返回是否成功"""
        for i, t in enumerate(self.titles):
            if t['id'] == title_id:
                self.titles.pop(i)
                self._save(self.title_file, self.titles)
                return True
        return False

    # ---- 玩家称号关联操作 ----

    def get_player_title_ids(self, player_name: str) -> List[str]:
        """获取玩家拥有的所有称号ID"""
        return [p['titleId'] for p in self.players if p['playerName'] == player_name]

    def get_title_players(self, title_id: str) -> List[str]:
        """获取拥有某称号的所有玩家名"""
        return [p['playerName'] for p in self.players if p['titleId'] == title_id]

    def player_has_title(self, player_name: str, title_id: str) -> bool:
        """检查玩家是否拥有某称号"""
        return any(
            p['playerName'] == player_name and p['titleId'] == title_id
            for p in self.players
        )

    def add_player_title(self, player_name: str, title_id: str) -> bool:
        """给玩家添加称号所有权，返回是否成功（已拥有则失败）"""
        if self.player_has_title(player_name, title_id):
            return False
        self.players.append({'playerName': player_name, 'titleId': title_id})
        self._save(self.player_file, self.players)
        return True

    def remove_player_title(self, player_name: str, title_id: str) -> bool:
        """移除玩家的某称号所有权，返回是否成功"""
        for i, p in enumerate(self.players):
            if p['playerName'] == player_name and p['titleId'] == title_id:
                self.players.pop(i)
                self._save(self.player_file, self.players)
                return True
        return False

    def remove_title_all_players(self, title_id: str) -> List[str]:
        """移除某称号的所有玩家关联，返回被移除的玩家列表"""
        removed = [p['playerName'] for p in self.players if p['titleId'] == title_id]
        self.players = [p for p in self.players if p['titleId'] != title_id]
        if removed:
            self._save(self.player_file, self.players)
        return removed

    def move_player(self, old_name: str, new_name: str) -> int:
        """迁移玩家称号数据（改名迁移），返回迁移的称号数量"""
        count = 0
        for p in self.players:
            if p['playerName'] == old_name:
                p['playerName'] = new_name
                count += 1
        if count > 0:
            self._save(self.player_file, self.players)
            if old_name in self.wearing:
                self.wearing[new_name] = self.wearing.pop(old_name)
                self._save(self.wearing_file, self.wearing)
        return count

    # ---- 佩戴状态操作 ----

    def get_wearing(self, player_name: str) -> Optional[str]:
        """获取玩家当前佩戴的称号ID"""
        return self.wearing.get(player_name)

    def set_wearing(self, player_name: str, title_id: str) -> None:
        """设置玩家当前佩戴的称号"""
        self.wearing[player_name] = title_id
        self._save(self.wearing_file, self.wearing)

    def remove_wearing(self, player_name: str) -> bool:
        """移除玩家当前佩戴状态，返回是否成功"""
        if player_name in self.wearing:
            del self.wearing[player_name]
            self._save(self.wearing_file, self.wearing)
            return True
        return False
