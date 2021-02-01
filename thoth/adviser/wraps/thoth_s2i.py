#!/usr/bin/env python3
# thoth-adviser
# Copyright(C) 2021 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""A wrap that recommends to use Thoth's s2i if users do not use it."""

from typing import TYPE_CHECKING
from typing import Optional, Dict, Any

from thoth.common import get_justification_link as jl

from ..state import State
from ..wrap import Wrap

if TYPE_CHECKING:
    from ..pipeline_builder import PipelineBuilderContext


class ThothS2IWrap(Wrap):
    """A wrap that notifies about missing observations."""

    _THOTH_S2I_PREFIX = "quay.io/thoth-station/s2i-thoth-"
    _JUSTIFICATION = [
        {
            "type": "INFO",
            "message": "It is recommended to use Thoth's s2i to have recommendations specific to runtime environment",
            "link": jl("thoth_s2i"),
        }
    ]

    @classmethod
    def should_include(cls, builder_context: "PipelineBuilderContext") -> Optional[Dict[Any, Any]]:
        """Include this wrap in adviser if Thoth s2i is not used.."""
        if builder_context.is_included(cls):
            return None

        base_image = builder_context.project.runtime_environment.base_image

        if base_image and not base_image.startswith(cls._THOTH_S2I_PREFIX):
            return {}

        return None

    def run(self, state: State) -> None:
        """Check for no observations made on the given state."""
        self.context.stack_info.extend(self._JUSTIFICATION)
