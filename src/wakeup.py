#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: kakakaya, Date: Mon Apr 18 14:13:35 2016
from pprint import pprint as p
import click
import toml
import datetime


@click.command()
@click.option("--config", default="config.toml", type=str)
def main(config):
    with open(config) as tf:
        bot_config = toml.loads(tf.read())
    p(bot_config)
    now = datetime.datetime.now()
    print(bot_config["message"].format(current=now, delta=3))

if __name__ == "__main__":
    main()
