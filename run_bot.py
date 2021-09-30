import sys

from bot.click_opinion_bot import ClickOpinionBot
from bot.produce_factory_bot import ProduceFactoryBot
from playsound import playsound

from utils.config import Config

bot_map = {
    'click_opinion': ClickOpinionBot,
    'produce_factory': ProduceFactoryBot
}

if __name__ == '__main__':
    # python -u run_bot.py produce_factory
    try:
        assert len(sys.argv) == 2, '__main__ sys.argv input must be 1'
        new_bot = bot_map[sys.argv[1]]()
        new_bot.run()
    finally:
        while True:
            playsound('./game-over.wav')
