#!/bin/bash
localPATH='/home/vladimir/parse-mail'                                        # path of current directory
sep='---------------'                                   
  echo $sep"Processing" $d$sep
  remoteRepo="https://github.com/13excite/parse-mail.git"   
  lastLocalCommit=`git -C $localPATH rev-list HEAD | head -n 1`  # identify the last commit in master
  echo $lastLocalCommit
  lastRemoteCommit=`git -C $localPATH rev-list remotes/origin/HEAD | head -n 1`
  echo $lastRemoteCommit
  #load update info 
  git fetch --all 
 
  if [[ "$lastLocalCommit" != "$lastRemoteCommit" ]]
     then
      echo "try pulling remote repo"
      git pull
  else
      echo "local branch equally remote branch"
  fi

echo -e "\n"
