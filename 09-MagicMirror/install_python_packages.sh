#!/bin/bash

for package in 'pytz' 'feedparser'
do
  sudo pip install $package
done
