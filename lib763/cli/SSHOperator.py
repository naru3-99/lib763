import paramiko
from scp import SCPClient

class SSHOperator:
    def __init__(self, username: str, hostname: str, password: str, key_path: str = None, port: int = 22):
        """
        @param:
            username: (str) Username for the SSH connection
            hostname: (str) Hostname for the SSH connection
            password: (str) Password for the SSH connection
            key_path: (str) File path of the SSH private key
            port: (int) Port number for the SSH connection (default is 22)
        """
        self.username = username
        self.hostname = hostname
        self.password = password
        self.key_path = key_path
        self.port = port
        self.state = False
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Automatically add unknown host keys
        self.init_ssh()

    def init_ssh(self):
        """
        Initialize the SSH connection.
        """
        self.client.connect(self.hostname, username=self.username, password=self.password, key_filename=self.key_path, port=self.port)
        self.state = True

    def execute(self, command: str) -> str:
        """
        Execute a command.
        @param:
            command: (str) Command to execute
        @return:
            (str) Output of the command
        """
        if not self.state:
            raise SSHConnectionError("The ssh connection is broken.")
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode('utf-8')

    def send_file(self, local_path: str, remote_path: str):
        """
        Send a file to the remote system.
        @param:
            local_path: (str) Local file path
            remote_path: (str) Remote file path
        """
        with SCPClient(self.client.get_transport()) as scp:
            scp.put(local_path, remote_path)

    def exit(self):
        """
        Close the SSH connection.
        """
        self.client.close()


class SSHConnectionError(Exception):
    pass

