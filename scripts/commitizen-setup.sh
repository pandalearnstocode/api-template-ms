cd .git/hooks
touch commit-msg
chmod +x commit-msg
echo -e "#!/bin/bash \nMSG_FILE=$1 \ncz check --commit-msg-file $MSG_FILE \n" >> commit-msg