import paramiko


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect('hub.local', username="pi", key_filename="/Users/adrien/.ssh/iot_rsa")

    stdin, stdout, stderr = client.exec_command('sleep 5 && touch yaboi', get_pty=True)
    # stdin, stdout, stderr = client.exec_command('rm yaboi')

    for line in stderr:
        print(line.strip("\n"))

    client.close()


main()
