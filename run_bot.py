import sys
from bot.click_opinion_bot import ClickOpinionBot
from bot.produce_factory_bot import ProduceFactoryBot

bot_map = {
    'click_opinion': ClickOpinionBot,
    'produce_factory': ProduceFactoryBot
}

if __name__ == '__main__':
    # python -u run_bot.py produce_factory
    if len(sys.argv) == 2:
        new_bot = bot_map[sys.argv[1]]()
        new_bot.run()
