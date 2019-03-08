# -*- coding: utf-8 -*-

"""
Copyright © 2019-present Lenovo

This file is licensed under both the BSD-3 license for individual/non-commercial use and
EPL-1.0 license for commercial use. Full text of both licenses can be found in
COPYING.BSD and COPYING.EPL files.
"""

from pytest import fixture, mark

from antilles.alarm.models import Policy
from antilles.alarm.scanner.creator_tasks import create_alarm
from antilles.alarm.scanner.datasource import DataSource
from antilles.alarm.scanner.judge import Judge


@fixture
def policy():
    from datetime import timedelta
    return Policy.objects.create(
        metric_policy=Policy.NODE_ACTIVE,
        name='policy_node_active',
        portal='',
        duration=timedelta(seconds=80),
        status=Policy.STATUS_CHOICES[0][0],
        level=Policy.LEVEL_CHOICES[1][0],
        nodes='all',
        creator='hpcadmin',
        wechat=False,
        sound=False,
    )


def query_result(*args, **kwargs):
    from influxdb.resultset import ResultSet
    query_response = {
        "results": [
            {"series": [{"name": "node_active",
                         "tags": {"host": "server01"},
                         "columns": ["time", "val", "host"],
                         "values": [
                             ["2018-01-22T15:51:28.968422294Z",
                              "on",
                              "server01"],
                             ["2018-01-22T15:51:28.968422294Z",
                              "off",
                              "server01"],
                             ["2018-01-22T15:51:28.968422294Z",
                              "on",
                              "server01"]
                         ]},
                        {"name": "node_active",
                         "tags": {"host": "server02"},
                         "columns": ["time", "val", "host"],
                         "values": [
                             ["2018-01-22T15:51:28.968422294Z",
                              "off",
                              "server02"],
                             ["2018-01-22T15:51:28.968422294Z",
                              "off",
                              "server02"],
                             ["2018-01-22T15:51:28.968422294Z",
                              "off",
                              "server02"]
                         ]},
                        {"name": "node_active",
                         "tags": {"host": "server03"},
                         "columns": ["time", "val", "host"],
                         "values": [
                             ["2018-01-22T15:51:28.968422294Z",
                              "off",
                              "server03"],
                             ["2018-01-22T15:51:28.968422294Z",
                              "off",
                              "server03"],
                             ["2018-01-22T15:51:28.968422294Z",
                              "off",
                              "server03"]
                         ]},
                        {"name": "node_active",
                         "tags": {"host": "server04"},
                         "columns": ["time", "val", "host"],
                         "values": [
                             ["2018-01-22T15:51:28.968422294Z",
                              "off",
                              "server04"],
                             ["2018-01-22T15:51:28.968422294Z",
                              "on",
                              "server04"],
                             ["2018-01-22T15:51:28.968422294Z",
                              "off",
                              "server04"]
                         ]},
                        ]
             }
        ]
    }
    return ResultSet(query_response["results"][0])


@mark.django_db
def test_sql_template(policy):
    sql = DataSource(policy)._sql_template
    expect = "select {columns} from " \
             "\"hour\".node_active where time > now() - 80s "
    assert sql == expect


@mark.django_db
def test_get_node_active_data(policy, mocker):
    mock = mocker.patch("django.core.cache.cache.get")
    DataSource(policy)._get_node_active()

    mock.assert_called_with(
        "select host, value as val from "
        "\"hour\".node_active where time > now() - 80s "
        "group by host",
        epoch='s'
    )


@mark.django_db
def test_compare(policy, mocker):
    mocker.patch("django.core.cache.cache.get", side_effect=query_result)
    datas = DataSource(policy).get_data()
    alarms = Judge(datas, policy).compare()

    expect_alarms = [{"node": "server02"},
                     {"node": "server03"}
                     ]

    assert len(alarms) == len(expect_alarms)
    for alarm in alarms:
        assert alarm in expect_alarms


@mark.django_db
def test_create_alarm(policy, mocker):
    mocker.patch("django.core.cache.cache.get", side_effect=query_result)
    mock = mocker.patch("antilles.alarm.models.Alarm.objects.create")
    datas = DataSource(policy).get_data()
    alarms = Judge(datas, policy).compare()

    for alarm in alarms:
        alarm.update({"policy_id": policy.id})
        create_alarm(alarm)

        mock.assert_called_with(**dict({"policy": policy}, **alarm))
