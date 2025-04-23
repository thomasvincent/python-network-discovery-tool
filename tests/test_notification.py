"""Tests for the NotificationService class."""

import pytest
from unittest.mock import patch, MagicMock

from network_discovery.domain.device import Device
from network_discovery.infrastructure.notification import EmailNotificationService


@pytest.fixture
def notification_service():
    """Return a notification service instance."""
    return EmailNotificationService(
        smtp_server="smtp.example.com",
        smtp_port=587,
        username="user@example.com",
        password="password",
        sender="sender@example.com",
        recipients=["recipient1@example.com", "recipient2@example.com"],
    )


@pytest.fixture
def devices():
    """Return a list of devices for testing."""
    return [
        Device(id=1, host="example1.com", ip="192.168.1.1", alive=True, ssh=True, snmp=False, mysql=True),
        Device(id=2, host="example2.com", ip="192.168.1.2", alive=True, ssh=False, snmp=True, mysql=False),
        Device(id=3, host="example3.com", ip="192.168.1.3", alive=False),
    ]


class TestEmailNotificationService:
    """Tests for the EmailNotificationService class."""

    def test_init(self):
        """Test that an EmailNotificationService can be initialized."""
        service = EmailNotificationService(
            smtp_server="smtp.example.com",
            smtp_port=587,
            username="user@example.com",
            password="password",
            sender="sender@example.com",
            recipients=["recipient@example.com"],
        )
        assert service.smtp_server == "smtp.example.com"
        assert service.smtp_port == 587
        assert service.username == "user@example.com"
        assert service.password == "password"
        assert service.sender == "sender@example.com"
        assert service.recipients == ["recipient@example.com"]

    def test_send_notification(self, notification_service, devices):
        """Test that a notification can be sent."""
        # Mock the smtplib.SMTP class
        with patch("smtplib.SMTP") as mock_smtp:
            # Mock the SMTP instance
            mock_instance = MagicMock()
            mock_smtp.return_value = mock_instance
            
            # Send the notification
            notification_service.send_notification(devices)
            
            # Check that the SMTP server was connected to
            mock_smtp.assert_called_once_with(
                notification_service.smtp_server,
                notification_service.smtp_port,
            )
            
            # Check that TLS was started
            mock_instance.starttls.assert_called_once()
            
            # Check that login was called
            mock_instance.login.assert_called_once_with(
                notification_service.username,
                notification_service.password,
            )
            
            # Check that sendmail was called for each recipient
            assert mock_instance.sendmail.call_count == len(notification_service.recipients)
            
            # Check that quit was called
            mock_instance.quit.assert_called_once()

    def test_send_notification_no_devices(self, notification_service):
        """Test that a notification is not sent when there are no devices."""
        # Mock the smtplib.SMTP class
        with patch("smtplib.SMTP") as mock_smtp:
            # Send the notification
            notification_service.send_notification([])
            
            # Check that the SMTP server was not connected to
            mock_smtp.assert_not_called()

    def test_send_notification_smtp_error(self, notification_service, devices):
        """Test that SMTP errors are handled."""
        # Mock the smtplib.SMTP class
        with patch("smtplib.SMTP") as mock_smtp:
            # Mock the SMTP instance to raise an exception
            mock_smtp.side_effect = Exception("SMTP error")
            
            # Send the notification
            notification_service.send_notification(devices)
            
            # Check that the SMTP server was connected to
            mock_smtp.assert_called_once_with(
                notification_service.smtp_server,
                notification_service.smtp_port,
            )

    def test_send_notification_login_error(self, notification_service, devices):
        """Test that login errors are handled."""
        # Mock the smtplib.SMTP class
        with patch("smtplib.SMTP") as mock_smtp:
            # Mock the SMTP instance
            mock_instance = MagicMock()
            mock_smtp.return_value = mock_instance
            
            # Mock the login method to raise an exception
            mock_instance.login.side_effect = Exception("Login error")
            
            # Send the notification
            notification_service.send_notification(devices)
            
            # Check that the SMTP server was connected to
            mock_smtp.assert_called_once_with(
                notification_service.smtp_server,
                notification_service.smtp_port,
            )
            
            # Check that TLS was started
            mock_instance.starttls.assert_called_once()
            
            # Check that login was called
            mock_instance.login.assert_called_once_with(
                notification_service.username,
                notification_service.password,
            )
            
            # Check that sendmail was not called
            mock_instance.sendmail.assert_not_called()
            
            # Check that quit was called
            mock_instance.quit.assert_called_once()

    def test_send_notification_sendmail_error(self, notification_service, devices):
        """Test that sendmail errors are handled."""
        # Mock the smtplib.SMTP class
        with patch("smtplib.SMTP") as mock_smtp:
            # Mock the SMTP instance
            mock_instance = MagicMock()
            mock_smtp.return_value = mock_instance
            
            # Mock the sendmail method to raise an exception
            mock_instance.sendmail.side_effect = Exception("Sendmail error")
            
            # Send the notification
            notification_service.send_notification(devices)
            
            # Check that the SMTP server was connected to
            mock_smtp.assert_called_once_with(
                notification_service.smtp_server,
                notification_service.smtp_port,
            )
            
            # Check that TLS was started
            mock_instance.starttls.assert_called_once()
            
            # Check that login was called
            mock_instance.login.assert_called_once_with(
                notification_service.username,
                notification_service.password,
            )
            
            # Check that sendmail was called
            assert mock_instance.sendmail.call_count > 0
            
            # Check that quit was called
            mock_instance.quit.assert_called_once()

    def test_format_message(self, notification_service, devices):
        """Test that a message can be formatted."""
        # Format the message
        message = notification_service._format_message(devices)
        
        # Check that the message contains the expected content
        assert "Subject: Network Discovery Report" in message
        assert "From: sender@example.com" in message
        assert "To: " in message
        assert "Content-Type: text/html" in message
        assert "<html>" in message
        assert "</html>" in message
        assert "example1.com" in message
        assert "example2.com" in message
        assert "example3.com" in message
        assert "192.168.1.1" in message
        assert "192.168.1.2" in message
        assert "192.168.1.3" in message
