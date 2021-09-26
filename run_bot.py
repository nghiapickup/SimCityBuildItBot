import sys
from bot.click_opinion_bot import ClickOpinionBot
from bot.produce_metal_bot import ProduceMetalBot

bot_map = {
    'click_opinion': ClickOpinionBot,
    'produce_metal': ProduceMetalBot
}

if __name__ == '__main__':
    if len(sys.argv) == 2:
        new_bot = bot_map[sys.argv[1]]()
        new_bot.run()
