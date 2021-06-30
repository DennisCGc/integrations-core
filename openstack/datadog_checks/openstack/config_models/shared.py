# (C) Datadog, Inc. 2021-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from __future__ import annotations

from typing import Optional, Sequence

from pydantic import BaseModel, root_validator, validator

from datadog_checks.base.utils.functions import identity
from datadog_checks.base.utils.models import validation

from . import defaults, validators


class SharedConfig(BaseModel):
    class Config:
        allow_mutation = False

    exclude_network_ids: Optional[Sequence[str]]
    exclude_server_ids: Optional[Sequence[str]]
    hypervisor_ids: Optional[Sequence[int]]
    keystone_server_url: str
    nova_api_version: Optional[str]
    os_host: Optional[str]
    service: Optional[str]
    ssl_verify: Optional[bool]
    use_agent_proxy: Optional[bool]

    @root_validator(pre=True)
    def _initial_validation(cls, values):
        return validation.core.initialize_config(getattr(validators, 'initialize_shared', identity)(values))

    @validator('*', pre=True, always=True)
    def _ensure_defaults(cls, v, field):
        if v is not None or field.required:
            return v

        return getattr(defaults, f'shared_{field.name}')(field, v)

    @validator('*')
    def _run_validations(cls, v, field):
        if not v:
            return v

        return getattr(validators, f'shared_{field.name}', identity)(v, field=field)

    @root_validator(pre=False)
    def _final_validation(cls, values):
        return validation.core.finalize_config(getattr(validators, 'finalize_shared', identity)(values))