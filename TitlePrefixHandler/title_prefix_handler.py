import re
from mcdreforged.handler.impl import VanillaHandler

PLUGIN_METADATA = {
    'id': 'title_prefix_handler',
    'version': '1.0.0',
}

class TitlePrefixHandler(VanillaHandler):
    """Handler for trimming title prefixes while keeping the player name intact."""

    def get_name(self) -> str:
        return 'title_prefix_handler'

    def pre_parse_server_stdout(self, text: str):
        text = super().pre_parse_server_stdout(text)
        # Remove the third title prefix segment from the raw console output.
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
    server.register_server_handler(TitlePrefixHandler())
