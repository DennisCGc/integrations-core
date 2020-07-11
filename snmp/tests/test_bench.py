# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

import pytest

from datadog_checks.snmp import SnmpCheck
from .common import BULK_TABULAR_OBJECTS, TABULAR_OBJECTS, create_check, generate_instance_config

pytestmark = pytest.mark.usefixtures("dd_environment")


def test_tabular_enforce(benchmark):
    instance = generate_instance_config(TABULAR_OBJECTS)
    check = create_check(instance)

    benchmark(check.check, instance)


def test_tabular_no_enforce(benchmark):
    instance = generate_instance_config(TABULAR_OBJECTS)
    instance["enforce_mib_constraints"] = False
    check = create_check(instance)

    benchmark(check.check, instance)


def test_tabular_bulk(benchmark):
    instance = generate_instance_config(BULK_TABULAR_OBJECTS)
    instance['bulk_threshold'] = 5
    check = create_check(instance)

    benchmark(check.check, instance)


def test_tabular_no_bulk(benchmark):
    instance = generate_instance_config(BULK_TABULAR_OBJECTS)
    # Don't use bulk requests
    instance['bulk_threshold'] = 100
    check = create_check(instance)

    benchmark(check.check, instance)

instance = generate_instance_config([])
instance['community_string'] = 'f5'
init = {'oid_batch_size': 128}

check = SnmpCheck('snmp', init, [instance])


def test_profile_f5(benchmark):
    benchmark(check.check, instance)
