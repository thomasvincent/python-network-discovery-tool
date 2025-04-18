"""Tests for the Device class."""

from network_discovery.domain.device import Device


class TestDevice:
    """Tests for the Device class."""

    def test_init(self):
        """Test that a Device can be initialized with the required parameters."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        assert device.id == 1
        assert device.host == "example.com"
        assert device.ip == "192.168.1.1"
        assert device.snmp_group == "public"
        assert not device.alive
        assert not device.snmp
        assert not device.ssh
        assert not device.mysql
        assert device.mysql_user == ""
        assert device.mysql_password == ""
        assert device.uname == ""
        assert device.errors == []
        assert not device.scanned

    def test_add_error(self):
        """Test that errors can be added to a Device."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        device.add_error("Test error")
        assert device.errors == ["Test error"]
        device.add_error("Another error")
        assert device.errors == ["Test error", "Another error"]

    def test_reset_services(self):
        """Test that services can be reset."""
        device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            ssh=True,
            snmp=True,
            mysql=True,
            uname="Linux",
        )
        device.reset_services()
        assert not device.ssh
        assert not device.snmp
        assert not device.mysql
        assert device.uname == "unknown"

    def test_to_dict(self):
        """Test that a Device can be converted to a dictionary."""
        device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            snmp_group="private",
            alive=True,
            snmp=True,
            ssh=True,
            mysql=True,
            mysql_user="user",
            mysql_password="password",
            uname="Linux",
            errors=["Error 1", "Error 2"],
            scanned=True,
        )
        device_dict = device.to_dict()
        assert device_dict["id"] == 1
        assert device_dict["host"] == "example.com"
        assert device_dict["ip"] == "192.168.1.1"
        assert device_dict["snmp_group"] == "private"
        assert device_dict["alive"]
        assert device_dict["snmp"]
        assert device_dict["ssh"]
        assert device_dict["mysql"]
        assert device_dict["mysql_user"] == "user"
        assert device_dict["mysql_password"] == "password"
        assert device_dict["uname"] == "Linux"
        assert device_dict["errors"] == ["Error 1", "Error 2"]
        assert device_dict["scanned"]

    def test_from_dict(self):
        """Test that a Device can be created from a dictionary."""
        device_dict = {
            "id": 1,
            "host": "example.com",
            "ip": "192.168.1.1",
            "snmp_group": "private",
            "alive": True,
            "snmp": True,
            "ssh": True,
            "mysql": True,
            "mysql_user": "user",
            "mysql_password": "password",
            "uname": "Linux",
            "errors": ["Error 1", "Error 2"],
            "scanned": True,
        }
        device = Device.from_dict(device_dict)
        assert device.id == 1
        assert device.host == "example.com"
        assert device.ip == "192.168.1.1"
        assert device.snmp_group == "private"
        assert device.alive
        assert device.snmp
        assert device.ssh
        assert device.mysql
        assert device.mysql_user == "user"
        assert device.mysql_password == "password"
        assert device.uname == "Linux"
        assert device.errors == ["Error 1", "Error 2"]
        assert device.scanned

    def test_status(self):
        """Test that a Device's status can be retrieved."""
        device = Device(
            id=1,
            host="example.com",
            ip="192.168.1.1",
            alive=True,
            ssh=True,
            snmp=False,
            mysql=True,
            errors=["Error 1", "Error 2"],
        )
        status = device.status()
        assert "example.com" in status
        assert "alive: True" in status
        assert "ssh: True" in status
        assert "snmp: False" in status
        assert "mysql: True" in status
        assert "Error 1, Error 2" in status

    def test_repr(self):
        """Test that a Device's string representation is correct."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        assert repr(device) == "example.com (192.168.1.1)"

    def test_str(self):
        """Test that a Device's string representation is correct."""
        device = Device(id=1, host="example.com", ip="192.168.1.1")
        assert str(device) == str(device.to_dict())
