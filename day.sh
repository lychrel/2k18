#!/usr/bin/expect -f
# updates index file on ncsu www4
# assumes execution from repo folder
set username [lindex $argv 0];
set password [lindex $argv 1];
spawn lftp sftp://$username@ftp.ncsu.edu
expect "Password: "
send "$password\r"
expect "~> "
send "cd www\r"
expect "~/www> "
send "put ./index.html\r"
expect "~/www> "
send "exit\r"
