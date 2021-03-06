import sys
import time

from bot.click_opinion_bot import ClickOpinionBot
from bot.produce_factory_bot import ProduceFactoryBot
from bot.search_special_item import SearchSpecialItem
from playsound import playsound

from bot.setup_bot import SetupBot

bot_map = {
    'click_opinion': ClickOpinionBot,
    'produce_factory': ProduceFactoryBot,
    'setup': SetupBot,
    'trade_hq': SearchSpecialItem,
}

if __name__ == '__main__':
    # python -u run_bot.py produce_factory
    try:
        assert len(sys.argv) == 2, '__main__ sys.argv input must be 1'
        new_bot = bot_map[sys.argv[1]]()
        new_bot.run()

        exit(0)
    except BaseException as e :
        print(e)
        while True:
            playsound('./game-over.wav')
            playsound('./game-over.wav')
            time.sleep(30)
