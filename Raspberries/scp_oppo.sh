#!/usr/bin/expect -f

set timeout -1
set FILE [lindex $argv 0]
set USER "u0_a277"
set HOST [lindex $argv 1]
set PASS "alumno"

spawn scp -P 8022 $FILE $USER@$HOST:~/storage/music
expect "password:"
send "$PASS\r"
expect eof