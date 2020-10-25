#!/bin/bash
echo "Zephyr Installer"
echo "Version 1.0.0"
echo "By Johnny Stene"

echo "Cleaning up any past installations of Zephyr..."
sudo rm -rf /usr/share/zephyr
sudo rm /usr/bin/zephyr

echo "Copying files..."
sudo mkdir /usr/share/zephyr
sudo cp -r zephyr /usr/share/zephyr/
sudo cp zephyr-compile.py /usr/share/zephyr/zephyr-compile

echo "Setting permissions..."
sudo chmod a+rx /usr/share/zephyr/zephyr-compile

echo "Creating symbolic link into /usr/bin..."
sudo ln -s /usr/share/zephyr/zephyr-compile /usr/bin/zephyr
