bot_pid="$(pgrep bot.py)"

if [ -z $bot_pid ]; then
  echo Not running
else
  kill -9 $bot_pid
  echo Killed
fi
