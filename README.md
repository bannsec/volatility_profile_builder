# What
This is a python library to help build Linux profiles for volatility.

# Quickstart Use
Support for more distributions are in the works. To run, simply do:

```bash
$ volatility_profile_builder centos

Select a release to build for:
+-------+----------------+
| Index |    Release     |
+-------+----------------+
|   0   |     latest     |
|   1   |       5        |
|   2   |      5.11      |
|   3   |       6        |
|   4   |      6.10      |
|   5   |      6.6       |
|   6   |      6.7       |
|   7   |      6.8       |
|   8   |      6.9       |
|   9   |       7        |
|   10  |    7.0.1406    |
|   11  |    7.1.1503    |
|   12  |    7.2.1511    |
|   13  |    7.3.1611    |
|   14  |    7.4.1708    |
|   15  |    7.5.1804    |
|   16  |    centos5     |
|   17  |   centos5.11   |
|   18  |    centos6     |
|   19  |   centos6.10   |
|   20  |   centos6.6    |
|   21  |   centos6.7    |
|   22  |   centos6.8    |
|   23  |   centos6.9    |
|   24  |    centos7     |
|   25  | centos7.0.1406 |
|   26  | centos7.1.1503 |
|   27  | centos7.2.1511 |
|   28  | centos7.3.1611 |
|   29  | centos7.4.1708 |
|   30  | centos7.5.1804 |
+-------+----------------+
Which release? 23
Building image for centos:centos6.9 ... [ DONE ]
Copying profile out ... [ DONE ]
Your profile should be under: /home/user/opt/volatility/profiles

$ ls -la profiles/
total 680
drwxr-xr-x 2 root root   4096 Nov 19 21:26 .
drwxrwxr-x 6 user user   4096 Nov 19 21:29 ..
-rw-r--r-- 1 root root 686821 Nov 19 21:26 CentOS-6.9-2.6.32-754.6.3.el6.x86_64.zip
```

Follow the prompts to select the version, then wait and your profile will be output to `profiles` directory under your current working directory.

# Installation
This is a python package. Installation via pypi:

```bash
pip install volatility_profile_builder
```

Or locally

```bash
pip install .
```

# Dependencies
This process relies on docker for the build environment. Be sure to have docker installed.
