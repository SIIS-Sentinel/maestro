import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
client.connect('hub.local', username="pi", key_filename="/Users/adrien/.ssh/iot_rsa")

stdin, stdout, stderr = client.exec_command('ls -l')

for line in stdout:
    print(line)

client.close()
