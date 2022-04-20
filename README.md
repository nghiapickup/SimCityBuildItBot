# SimCityBuildIt Android Bot
Bot script for playing repeatedly tasks in SimcityBuiIt game using Android emulator.

Setup
---
- Install an Andriod emulator. I'm using Genymotion emulator, android 8.1, 1080x1920 screen
- pip install requirements.txt

How to start
---
Simply execute run_bot.py with predefined option. 
> python run_bot.py produce_factory

There are some steps need to be set before execute bot.
- Check config.yaml 

### produce_factory
This is the main bot that produce and collect factory products, 
then sell them on the trade depot. The strategy is that:
- The bot starts at the first factory produce or collect all items
- Loop with all the rest factories and return to the first one
- Click into trade depot and sell all collected item.
- Return to the first factory

At first, we need to put the first factory and trade depot next to each other. 
Then we can switch between 2 windows without move or change the view.
- Clịck into the first factory (the game will center the screen to this factory)
- Find the location of trade depot and set the config.yaml 
    > first_manufacturer_location: [960, 610]



Refs
===
- [Android Debug Bridge: tool for android emulator connection](https://developer.android.com/studio/command-line/adb)
- [Linux kernel's event code book](https://www.kernel.org/doc/Documentation/input/event-codes.txt)
- [Send event short explanation: Using ADB sendevent example](http://ktnr74.blogspot.com/2013/06/emulating-touchscreen-interaction-with.html)
