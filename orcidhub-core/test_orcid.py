# -*- coding: utf-8 -*-

"""Tests related to ORCID affilation."""

import requests_oauthlib
from models import User, Organisation, UserOrg
from flask_login import login_user
import pytest
from unittest.mock import patch, MagicMock
import time
from flask import url_for


fake_time = time.time()


@patch.object(requests_oauthlib.OAuth2Session, "authorization_url", lambda self, base_url: ("URL_123", None))
def test_link(request_ctx):
    """Test a user affiliation initialization."""
    with request_ctx("/link") as ctx:
        org = Organisation(name="THE ORGANISATION", confirmed=True)
        org.save()
        test_user = User(
            name="TEST USER 123",
            email="test123@test.test.net",
            username="test123",
            organisation=org,
            confirmed=True)
        login_user(test_user, remember=True)

        rv = ctx.app.full_dispatch_request()
        assert b"<!DOCTYPE html>" in rv.data, "Expected HTML content"
        assert b"TEST USER 123" in rv.data, "Expected to have the user name on the page"
        assert b"test123@test.test.net" in rv.data, "Expected to have the user email on the page"
        assert b"URL_123" in rv.data, "Expected to have ORCiD authorization link on the page"


@patch.object(requests_oauthlib.OAuth2Session, "authorization_url", lambda self, base_url: ("URL_123", None))
def test_link_with_unconfirmed_org(request_ctx):
    """Test a user affiliation initialization if the user Organisation isn't registered yet."""
    with request_ctx("/link") as ctx:
        test_user = User(
            name="TEST USER",
            email="test@test.test.net",
            username="test42",
            confirmed=True)
        login_user(test_user, remember=True)

        rv = ctx.app.full_dispatch_request()
        assert b"<!DOCTYPE html>" in rv.data, "Expected HTML content"
        assert b"TEST USER" in rv.data, "Expected to have the user name on the page"
        assert b"test@test.test.net" in rv.data, "Expected to have the user email on the page"
        # TODO: it should fail!!!!
        assert b"URL_123" in rv.data, "Expected to have ORCiD authorization link on the page"


@patch.object(requests_oauthlib.OAuth2Session, "authorization_url", lambda self, base_url: ("URL_123", None))
def test_link_already_affiliated(request_ctx):
    """Test a user affiliation initialization if the uerer is already affilated."""
    with request_ctx("/link") as ctx:
        org = Organisation(name="THE ORGANISATION", confirmed=True)
        org.save()
        test_user = User(
            email="test123@test.test.net",
            name="TEST USER",
            username="test123",
            organisation=org,
            orcid="ABC123",
            confirmed=True)
        test_user.save()
        login_user(test_user, remember=True)
        uo = UserOrg(user=test_user, org=org)
        uo.save()

        rv = ctx.app.full_dispatch_request()
        assert rv.status_code == 302, "If the user is already affiliated, the user should be redirected ..."
        assert "profile" in rv.location, "redirection to 'profile' showing the ORCID"


@pytest.mark.parametrize("name", ["TEST USER", None])
@patch.object(requests_oauthlib.OAuth2Session, "fetch_token", lambda self, *args, **kwargs: dict(
    name="NEW TEST",
    access_token="ABC123",
    orcid="ABC-123-456-789"))
def test_link_orcid_auth_callback(name, request_ctx):
    """Test ORCID callback - the user authorized the organisation access to the ORCID profile."""
    with request_ctx("/auth") as ctx:
        org = Organisation(name="THE ORGANISATION", confirmed=True)
        org.save()
        test_user = User(
            name=name,
            email="test123@test.test.net",
            username="test123",
            organisation=org,
            orcid="ABC123",
            confirmed=True)
        login_user(test_user, remember=True)

        rv = ctx.app.full_dispatch_request()
        assert rv.status_code == 302, "If the user is already affiliated, the user should be redirected ..."
        assert "profile" in rv.location, "redirection to 'profile' showing the ORCID"

        u = User.get(username="test123")
        assert u.orcid == "ABC-123-456-789"
        assert u.access_token == "ABC123"
        if name:
            assert u.name == name, "The user name should be changed"
        else:
            assert u.name == "NEW TEST", "the user name should be set from record coming from ORCID"


def make_fake_response(text, *args, **kwargs):
    """Mock out the response object returned by requests_oauthlib.OAuth2Session.get(...)."""
    mm = MagicMock(name="response")
    mm.text = text
    return mm


@patch.object(requests_oauthlib.OAuth2Session, "get",
              lambda self, *args, **kwargs: make_fake_response('{"test": "TEST1234567890"}'))
def test_profile(request_ctx):
    """Test an affilated user profile and ORCID data retrieval."""
    with request_ctx("/profile") as ctx:
        org = Organisation(name="THE ORGANISATION", confirmed=True)
        org.save()
        test_user = User(
            email="test123@test.test.net",
            username="test123",
            organisation=org,
            orcid="ABC123",
            confirmed=True)
        login_user(test_user, remember=True)

        rv = ctx.app.full_dispatch_request()
        assert rv.status_code == 200
        assert b"TEST1234567890" in rv.data


def test_profile_wo_orcid(request_ctx):
    """Test a user profile that doesn't hava an ORCID."""
    with request_ctx("/profile") as ctx:
        org = Organisation(name="THE ORGANISATION", confirmed=True)
        org.save()
        test_user = User(
            email="test123@test.test.net",
            username="test123",
            organisation=org,
            orcid=None,
            confirmed=True)
        login_user(test_user, remember=True)

        rv = ctx.app.full_dispatch_request()
        assert rv.status_code == 302
        assert rv.location == url_for("link")
