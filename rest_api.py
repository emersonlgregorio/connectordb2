from typing import Any, Dict, Optional, Union

import requests
from requests import Response
from requests.auth import HTTPBasicAuth


JsonType = Union[Dict[str, Any], list, str, int, float, bool, None]


def _build_auth(
    basic_auth_username: Optional[str],
    base_auth_password: Optional[str],
    basic_auth_password: Optional[str],
) -> Optional[HTTPBasicAuth]:
    password = basic_auth_password if basic_auth_password is not None else base_auth_password
    if basic_auth_username and password is not None:
        return HTTPBasicAuth(basic_auth_username, password)
    return None


def _request(
    method: str,
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Union[JsonType, bytes, str]] = None,
    basic_auth_username: Optional[str] = None,
    base_auth_password: Optional[str] = None,
    basic_auth_password: Optional[str] = None,
    verify: bool = False,
) -> Response:
    auth = _build_auth(basic_auth_username, base_auth_password, basic_auth_password)

    # If data is a dict/list, send as JSON; otherwise pass through as data
    request_kwargs: Dict[str, Any] = {
        "headers": headers or {},
        "verify": verify,
        "auth": auth,
    }

    if isinstance(data, (dict, list)):
        request_kwargs["json"] = data  # type: ignore[assignment]
    elif data is not None:
        request_kwargs["data"] = data

    return requests.request(method=method.upper(), url=url, **request_kwargs)


def get(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    basic_auth_username: Optional[str] = None,
    base_auth_password: Optional[str] = None,
    basic_auth_password: Optional[str] = None,
    verify: bool = False,
) -> Response:
    return _request(
        "GET",
        url,
        headers=headers,
        data=None,
        basic_auth_username=basic_auth_username,
        base_auth_password=base_auth_password,
        basic_auth_password=basic_auth_password,
        verify=verify,
    )


def post(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Union[JsonType, bytes, str]] = None,
    basic_auth_username: Optional[str] = None,
    base_auth_password: Optional[str] = None,
    basic_auth_password: Optional[str] = None,
    verify: bool = False,
) -> Response:
    return _request(
        "POST",
        url,
        headers=headers,
        data=data,
        basic_auth_username=basic_auth_username,
        base_auth_password=base_auth_password,
        basic_auth_password=basic_auth_password,
        verify=verify,
    )


def patch(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Union[JsonType, bytes, str]] = None,
    basic_auth_username: Optional[str] = None,
    base_auth_password: Optional[str] = None,
    basic_auth_password: Optional[str] = None,
    verify: bool = False,
) -> Response:
    return _request(
        "PATCH",
        url,
        headers=headers,
        data=data,
        basic_auth_username=basic_auth_username,
        base_auth_password=base_auth_password,
        basic_auth_password=basic_auth_password,
        verify=verify,
    )


