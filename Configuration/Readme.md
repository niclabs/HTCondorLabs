# Configuration files

Configuration files used for multi machine pool with firewall condor environment.

You need to open port 9618 on your firewall to use the shared port described in 41shared_port.config.

'condor_config_doc' is the "master" file. It contains all configurations available for condor.
You will not need to touch most of them, but in case you need, copy that line and paste it in a local file.

# How to use

Place 00*.config, 40*.config and 41*.config in your local condor configuration path. It should be /etc/condor/config.d.
Overwrite files if needed. If you have condor already running, reconfig and restart condor by the following commands:
condor_restart and condor_reconfig.
