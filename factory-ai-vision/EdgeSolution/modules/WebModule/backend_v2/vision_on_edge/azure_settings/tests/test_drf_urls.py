"""App drf url tests.
"""

from unittest import mock

import pytest
from django.urls import resolve, reverse

from .factories import SettingFactory

pytestmark = pytest.mark.django_db


@pytest.mark.fast
@mock.patch(
    "vision_on_edge.azure_settings.models.Setting.validate",
    mock.MagicMock(return_value=True),
)
@mock.patch(
    "vision_on_edge.azure_settings.models.Setting.get_domain_id",
    mock.MagicMock(return_value="Fake_id"),
)
def test_setting_detail():
    """test_setting_detail.

    Args:
        setting (Setting): setting
    """

    setting = SettingFactory()
    setting.save()
    assert (
        reverse("api:setting-detail", kwargs={"pk": setting.id})
        == f"/api/settings/{setting.id}"
    )
    assert resolve(f"/api/settings/{setting.id}").view_name == "api:setting-detail"


@pytest.mark.fast
def test_setting_list():
    """test_setting_list."""
    assert reverse("api:setting-list") == "/api/settings"
    assert resolve("/api/settings").view_name == "api:setting-list"
