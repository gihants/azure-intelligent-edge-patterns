# -*- coding: utf-8 -*-
"""App exceptions.
"""

from rest_framework.exceptions import APIException


class ProjectCannotChangeDemoError(APIException):
    """CannotChangeDemoProjectError.
    """

    status_code = 400
    default_detail = "Demo project should not change."
    default_code = "project_cannot_change_demo_project"


class ProjectCustomVisionError(APIException):
    """CannotChangeDemoProjectError.
    """

    status_code = 400
    default_detail = "This project has invalid setting or customvision_id."
    default_code = "project_customvision_error"


class ProjectWithoutSettingError(APIException):
    """ProjectWithoutSettingError.
    """

    status_code = 400
    default_detail = "This project does not have a setting."
    default_code = "project_without_setting_error"


class ProjectResetWithoutNameError(APIException):
    """ProjectWithoutSettingError.
    """

    status_code = 400
    default_detail = "Please provide a name before reset."
    default_code = "project_reset_without_name_error"