#!/bin/sh

pkg=$(dirname "$0")
pip install --user --break-system-packages $pkg || pip install --user $pkg 

