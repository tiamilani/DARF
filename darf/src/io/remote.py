# © 2025 Nokia
# Licensed under the BSD 3-Clause License
# SPDX-License-Identifier: BSD-3-Clause
#
# Contact: Mattia Milani (Nokia) <mattia.milani@nokia.com>

"""
Remote module
=============

Use this module to manage remote directories.
Supported protocols:
- ssh

The module loads the requested files locally in a path
predefined or a custom path defined by the user.
"""

import os
from pathlib import Path
import paramiko
from scp import SCPClient

from darf.src.io.progress_bar import Pb as pb

from typing import List, Optional

class RemoteHandler:
    """RemoteHandler.
    Class used to manage remote directories
    """

    def __init__(self, path: str,
                 local_path: Optional[str] = None,
                 ssh_config_path: str = "~/.ssh/config"):
        """__init__.
        At the moment the remote connection assumes that the remote is configured in
        the .ssh config file from the user.

        The path passed is the remote path.
        The local path can be none and in that case the darf default path is going
        to be used.

        Parameters
        ----------
        path : str
            path to the remote directory position
        local_path : Optional[str]
            The path where to save possible file transfered from the remote folder
        """
        self.ssh_config_path = ssh_config_path
        self.__path = path
        self.__local_path = local_path if local_path else os.path.join(
            os.path.expanduser("~"), ".darf", "remote"
        )

        self.__host = self.__path.split(":")[0]
        self.__remote_path = self.__path.split(":")[1]

        self.__conn = None

        return
        self.open_connection()
        if not self.test_connection():
            raise Exception("The connection is not active")

        self.close_connection()

    @property
    def path(self) -> str:
        """path of the remote directory managed

        Parameters
        ----------

        Returns
        -------
        str
            the path to the remote directory

        """
        return self.__path

    @property
    def local_path(self) -> str:
        """path of the local directory managed

        Parameters
        ----------

        Returns
        -------
        str
            the path to the local directory

        """
        return self.__local_path

    @property
    def host(self) -> str:
        """host of the remote directory managed

        Parameters
        ----------

        Returns
        -------
        str
            the host to the remote directory

        """
        return self.__host

    @property
    def remote_path(self) -> str:
        """remote_path of the remote directory managed

        Parameters
        ----------

        Returns
        -------
        str
            the remote path to the directory

        """
        return self.__remote_path

    def open_connection(self) -> None:
        """open_connection.
        Open the connection to the remote directory
        """
        # Use paramiko with the ssh config file
        ssh_config = paramiko.SSHConfig()
        with open(os.path.expanduser(self.ssh_config_path)) as f:
            ssh_config.parse(f)

        host_config = ssh_config.lookup(self.__host)
        host = host_config.get("hostname", self.__host)
        user = host_config.get("user", None)
        port = host_config.get("port", 22)
        key_file = host_config.get("identityfile", [None])[0]

        # Create a new SSH client
        self.__conn = paramiko.SSHClient()
        self.__conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # Connect to the remote host
        self.__conn.connect(host, port=port, username=user, key_filename=key_file)

    def test_connection(self) -> None:
        # Run a simple command to test the connection in self.__conn using paramiko
        if self.__conn is None:
            return False
        try:
            stdin, stdout, stderr = self.__conn.exec_command("ls")
            if stdout.channel.recv_exit_status() == 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Connection test failed: {e}")
            raise e

    def close_connection(self) -> None:
        """close_connection.
        Close the connection to the remote directory
        """
        self.__conn.close()
        self.__conn = None

    @classmethod
    def progress(cls, filename, size, sent):
        """Callback function to update the progress bar."""
        bar.update(sent - bar.n)

    def transfer_file(self, remote_file: Optional[str] = None,
                      local_file: Optional[str] = None) -> str:
        """transfer_file.
        Transfer a file from the remote directory to the local directory

        Parameters
        ----------
        remote_file: Optional[str]
            path to the remote file, it might be null in that case
            the configured remote path will be used
        local_file : Optional[str]
            path to the local file

        Returns
        -------
        str
            path to the local file

        """
        global bar
        reset = False
        if not self.test_connection():
            self.open_connection()
            reset = True

        remote_file = os.path.join(self.remote_path, remote_file) if not remote_file is None \
                        else self.remote_path

        if local_file is None:
            local_file = os.path.join(self.local_path, os.path.basename(remote_file))

        # check if local_file already exists and if so return the path
        if os.path.exists(local_file):
            return local_file

        # Create an SCP client
        with SCPClient(self.__conn.get_transport(), progress=RemoteHandler.progress) as scp:
            # Initialize the progress bar
            bar = pb.databar(0, unit="B", unit_scale=True,
                             desc=f"Downloading {remote_file}", leave=False)
            scp.get(remote_file, local_file)
            bar.close()

        if reset:
            self.close_connection()
        return local_file