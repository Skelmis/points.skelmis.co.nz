from enum import Enum

import arrow
from arrow import Arrow
from piccolo.apps.user.tables import BaseUser
from piccolo.table import Table
from piccolo.columns import Date, ForeignKey, Varchar, Real


class PointTypes(str, Enum):
    NZ_FLIGHT = "NZ_FLIGHT"
    STATUS_BOOST = "STATUS_BOOST"
    A_STAR_FLIGHT = "A*_FLIGHT"
    OTHER = "OTHER"


class Points(Table):
    """A table to track air points"""

    user = ForeignKey(references=BaseUser)
    """The user who owns the points"""
    date_collected = Date()
    """The date you gained the point"""
    point_type = Varchar(choices=PointTypes)
    """The type of point accumulated"""
    value = Real()
    """How many of this point you got"""

    @property
    def is_current(self) -> bool:
        return not self.is_expired

    @property
    def is_expired(self) -> bool:
        """Returns true if the point is older than twelve months.

        Notes
        -----
        We assume points that are a year old are expired.

        Warnings
        --------
        This fails to account for leap years.
        """
        made_at: Arrow = arrow.get(self.date_collected)
        return (made_at - arrow.now()).days >= 365

    @property
    def is_in_future(self) -> bool:
        """Returns true if the points are to be added in the future.

        Warnings
        --------
        Not currently implemented.
        """
        raise NotImplementedError
