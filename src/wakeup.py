#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Mon Apr 18 14:13:35 2016
from pprint import pprint as p
import click
import toml
from datetime import datetime, timedelta
import time

@click.command()
@click.option("--config", default="config.toml", type=str)
def main(config):
    with open(config) as tf:
        bot_config = toml.loads(tf.read())
    p(bot_config)
    mainLoop(bot_config)


def mainLoop(conf):
    """
    1分毎に、発言すべきか確認をし、すべきなら適切な発言を投げる
    """

    message = conf["message"]
    sleep_message = conf["sleep_message"]
    # 日曜から土曜までの起きる時間
    weekday_waketimes = [
        tuple(map(int, conf["weekdays"]["sun"].split(":"))),
        tuple(map(int, conf["weekdays"]["mon"].split(":"))),
        tuple(map(int, conf["weekdays"]["tue"].split(":"))),
        tuple(map(int, conf["weekdays"]["wed"].split(":"))),
        tuple(map(int, conf["weekdays"]["thu"].split(":"))),
        tuple(map(int, conf["weekdays"]["fri"].split(":"))),
        tuple(map(int, conf["weekdays"]["sat"].split(":"))),
    ]

    while True:
        now = datetime.now()    # 開始時点での日付が必要
        if now.hour < weekday_waketimes[now.isoweekday()][0]:
            # 今日中に次の通知をする
            waketime = weekday_waketimes[now.isoweekday()]
            next_wake = now.replace(hour=waketime[0], minute=waketime[1])
        else:
            # 翌日に次の通知をする
            waketime = weekday_waketimes[(now.isoweekday()+1)%7]
            next_wake = now.replace(hour=waketime[0], minute=waketime[1]) + timedelta(days=1)

        while True:
            time.sleep(60)
            # countdown_start_time と countdown_end_time
            now = datetime.now()
            delta_hours = (next_wake-now).seconds/(60*60) # 差分の時間

            if int(conf["countdown_start_hours"]) > delta_hours > int(conf["countdown_end_hours"]) and now.minute == 0:
                bot_tweet(message.format(current=now, delta=delta_hours))
            elif int(conf["countdown_end_hours"]) > delta_hours:
                bot_tweet(sleep_message)
                break
            else:
                continue


def botTweet(mes):
    print(datetime.now()+" "+mes)



if __name__ == "__main__":
    main()
