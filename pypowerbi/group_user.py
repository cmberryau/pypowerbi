from enum import Enum


class GroupUserAccessRight(Enum):
    NONE = 'None'
    MEMBER = 'Member'
    ADMIN = 'Admin'
    CONTRIBUTOR = 'Contributor'
    VIEWER = 'Viewer'


class PrincipalType(Enum):
    USER = "User"
    GROUP = "Group"
    APP = "App"


class GroupUser:
    group_user_access_right_key = 'groupUserAccessRight'
    email_address_key = 'emailAddress'
    display_name_key = 'displayName'
    identifier_key = 'identifier'
    principal_type_key = 'principalType'

    def __init__(
        self,
        group_user_access_right,
        email_address="",
        display_name="",
        identifier="",
        principal_type=None
    ):
        """Constructs a GroupUser object

        :param group_user_access_right: Enum GroupUserAccessRight - The access right to assign to the GroupUser
        :param email_address: str - E-mail address of the user if principal type is user
        :param display_name: str - Display name of the principal
        :param identifier: str - Identifier of the principal
        :param principal_type: Enum PrincipalType - The principal type
        """
        self.group_user_access_right = group_user_access_right
        self.email_address = email_address
        self.display_name = display_name
        self.identifier = identifier
        self.principal_type = principal_type

    def as_set_values_dict(self):
        """Convert GroupUser object to dict with only values that are actually set. This dict can be used for
        groups.add_group_user requests.

        :return: Dict with object attributes in camelCase as keys, and attribute values as values.
        """
        group_user_dict = dict()

        if self.group_user_access_right:
            group_user_dict[self.group_user_access_right_key] = self.group_user_access_right.value

        if self.email_address:
            group_user_dict[self.email_address_key] = self.email_address

        if self.display_name:
            group_user_dict[self.display_name_key] = self.display_name

        if self.identifier:
            group_user_dict[self.identifier_key] = self.identifier

        if self.principal_type:
            group_user_dict[self.principal_type_key] = self.principal_type.value

        return group_user_dict
