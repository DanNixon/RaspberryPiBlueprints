#!/bin/bash

for package in 'pytz' 'feedparser' 'TwitterSearch'
do
  sudo pip install $package
done
