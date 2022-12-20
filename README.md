# Jool Ansible Role

Ansible role to install [Jool](https://nicmx.github.io/Jool), an open source IPv4/IPv6 translator.

[![Tests](https://img.shields.io/github/actions/workflow/status/srv6d/ansible_role_jool/molecule.yml?branch=main&label=Tests)](https://github.com/SRv6d/ansible_role_jool/actions/workflows/molecule.yml)
[![Ansible Galaxy](https://img.shields.io/badge/Ansible%20Galaxy-srv6d.jool-blue)](https://galaxy.ansible.com/srv6d/jool)

## Example Playbook

```yaml
- hosts: aftrs
  roles:
    - srv6d.jool
  vars:
    jool_instances:
      - instance: nat64-minimal
        type: nat64
        framework: netfilter
        global:
          pool6: 64:ff9b::/96
```

## Role Variables

| Variable       | Required | Default | Input        | Comments                                                                                                                                                                                                               |
| -------------- | -------- | ------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| jool_instances | **yes**  | _null_  | `list[dict]` | A list of dictionaries containing [Jool instance configuration](https://nicmx.github.io/Jool/en/config-atomic.html) in YAML format, with an additionally required `type` key that can be set to `"nat64"` or `"siit"`. |

## Usage

For each Jool instance, a Systemd service will be created that can be managed with the service name `"jool.<instance-name>.service"`.
To manage all Jool instances at once, the master service `"jool.service"` can be used.

## Requirements

- Rsync

## Supported distributions

The role is tested on the following, but may also work with other debian based distributions:

- Ubuntu
  - 20.04 LTS (Focal Fossa)
  - 22.04 LTS (Jammy Jellyfish)

## Known Issues

- The `pool6` argument of an existing NAT64 instance cannot be changed while it is active and doing so will result in an error.

## License

[GNU General Public License v3.0](./LICENSE)

## Author Information

Marvin Vogt (git@srv6d.space)
