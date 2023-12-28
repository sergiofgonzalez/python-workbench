#!/bin/bash -e


echo -e "About to remove \e[1m\e[92m.venv\e[0m recursively from the CWD"
echo -e "Scanning size of the current dir \e[1m\e[92mbefore\e[0m the operation: " $(du -sh .)
echo -e "This action is \e[1m\e[31m\e[4mdestructive\e[0m"
read -p "Are you sure you want to continue (y/n)? " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
  for FILE_IN_NODE_MODULES in `find . -name .venv`
  do
    rm -rf $FILE_IN_NODE_MODULES
  done
  echo -e "done! -- Size of the current dir \e[1m\e[92mafter\e[0m the operation: " $(du -sh .)
fi
