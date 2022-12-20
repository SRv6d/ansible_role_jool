from dataclasses import dataclass
from typing import Literal

import pytest


@dataclass
class JoolInstance:
    """A Jool instance.

    Attributes:
        name: The name of the instance.
        framework: The framework used by the instance.
    """

    name: str
    framework: Literal["netfilter", "iptables"]

    @classmethod
    def from_instance_display_csv(cls, csv: str):
        """Create a JoolInstance from a CSV line from the instance display command."""
        _, name, framework = csv.strip().split(",")
        return cls(name, framework)


@pytest.fixture
def jool_instances(host):
    return host.ansible.get_variables().get("jool_instances")


@pytest.mark.parametrize("package_name", ["jool-dkms", "jool-tools"])
def test_jool_packages(host, package_name):
    """Jool packages are installed."""
    package = host.package(package_name)
    assert package.is_installed


def test_jool_configuration_directory(host):
    """Jool configuration directory exists with correct permissions."""
    directory = host.file("/etc/jool")
    assert directory.is_directory
    assert directory.user == "root"
    assert directory.group == "root"
    assert directory.mode == 0o755


def test_jool_main_systemd_service(host):
    """Jool main Systemd service is running and enabled."""
    main_service = host.service("jool.service")
    assert main_service.is_running
    assert main_service.is_enabled


def test_jool_siit_systemd_service_masked(host):
    """Jool SIIT Systemd service included with package is not running and masked."""
    package_siit_service = host.service("jool_siit.service")
    assert not package_siit_service.is_running
    assert package_siit_service.is_masked


def test_jool_systemd_instance_services(host, jool_instances):
    """Jool instance Systemd services are running."""
    service_names = ["jool." + i.get("instance") + ".service" for i in jool_instances]
    for service in service_names:
        instance_service = host.service(service)
        assert instance_service.is_running


def test_jool_instances(host, jool_instances):
    """Jool instances match configured instances."""

    if result_nat64 := host.run("jool instance display --csv --no-headers").stdout:
        instances_nat64 = [
            sorted(
                JoolInstance.from_instance_display_csv(i)
                for i in result_nat64.splitlines()
            )
        ]
        expected_instances_nat64 = [
            sorted(
                JoolInstance(i["instance"], i["framework"])
                for i in jool_instances
                if i["type"] == "nat64"
            )
        ]

        assert instances_nat64 == expected_instances_nat64

    if result_siit := host.run("jool_siit instance display --csv --no-headers").stdout:
        instances_siit = [
            sorted(
                JoolInstance.from_instance_display_csv(i)
                for i in result_siit.splitlines()
            )
        ]
        expected_instances_siit = [
            sorted(
                JoolInstance(i["instance"], i["framework"])
                for i in jool_instances
                if i["type"] == "siit"
            )
        ]

        assert instances_siit == expected_instances_siit
