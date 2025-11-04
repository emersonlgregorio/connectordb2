import json
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


def _prepare_headers(headers: Optional[Dict[str, str]], data: Optional[Union[JsonType, bytes, str]]) -> Dict[str, str]:
    """Prepara headers com Content-Type apropriado para SpiffWorkflow."""
    prepared_headers = (headers.copy() if headers else {})
    
    # Se dados são dict/list, garantir Content-Type JSON (compatível com SpiffWorkflow)
    if isinstance(data, (dict, list)):
        if "Content-Type" not in prepared_headers:
            prepared_headers["Content-Type"] = "application/json"
        if "Accept" not in prepared_headers:
            prepared_headers["Accept"] = "application/json"
    
    return prepared_headers


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

    # Preparar headers com Content-Type apropriado para SpiffWorkflow
    prepared_headers = _prepare_headers(headers, data)

    # If data is a dict/list, send as JSON; otherwise pass through as data
    request_kwargs: Dict[str, Any] = {
        "headers": prepared_headers,
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
) -> Dict[str, Any]:
    """
    Executa requisição GET e retorna resposta no formato SpiffWorkflow.
    
    Returns:
        Dict com status_code, success, data e error (se houver)
        Formato compatível com SpiffWorkflow Data Objects.
    """
    response = _request(
        "GET",
        url,
        headers=headers,
        data=None,
        basic_auth_username=basic_auth_username,
        base_auth_password=base_auth_password,
        basic_auth_password=basic_auth_password,
        verify=verify,
    )
    return parse_response(response)


def post(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Union[JsonType, bytes, str]] = None,
    basic_auth_username: Optional[str] = None,
    base_auth_password: Optional[str] = None,
    basic_auth_password: Optional[str] = None,
    verify: bool = False,
) -> Dict[str, Any]:
    """
    Executa requisição POST e retorna resposta no formato SpiffWorkflow.
    
    Returns:
        Dict com status_code, success, data e error (se houver)
        Formato compatível com SpiffWorkflow Data Objects.
    """
    response = _request(
        "POST",
        url,
        headers=headers,
        data=data,
        basic_auth_username=basic_auth_username,
        base_auth_password=base_auth_password,
        basic_auth_password=basic_auth_password,
        verify=verify,
    )
    return parse_response(response)


def patch(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Union[JsonType, bytes, str]] = None,
    basic_auth_username: Optional[str] = None,
    base_auth_password: Optional[str] = None,
    basic_auth_password: Optional[str] = None,
    verify: bool = False,
) -> Dict[str, Any]:
    """
    Executa requisição PATCH e retorna resposta no formato SpiffWorkflow.
    
    Returns:
        Dict com status_code, success, data e error (se houver)
        Formato compatível com SpiffWorkflow Data Objects.
    """
    response = _request(
        "PATCH",
        url,
        headers=headers,
        data=data,
        basic_auth_username=basic_auth_username,
        base_auth_password=base_auth_password,
        basic_auth_password=basic_auth_password,
        verify=verify,
    )
    return parse_response(response)


def parse_response(response: Response) -> Dict[str, Any]:
    """
    Converte a resposta HTTP em formato compatível com SpiffWorkflow Data Objects.
    
    Args:
        response: Objeto Response do requests
        
    Returns:
        Dict com status_code, success, data e error (se houver)
        
    Compatível com SpiffWorkflow que espera dados em formato Dict.
    """
    result: Dict[str, Any] = {
        "status_code": response.status_code,
        "success": 200 <= response.status_code < 300,
    }
    
    try:
        # Tentar parsear como JSON primeiro (preferido pelo SpiffWorkflow)
        result["data"] = response.json()
    except (ValueError, json.JSONDecodeError):
        # Se não for JSON, retornar texto
        result["data"] = response.text
    
    if not result["success"]:
        result["error"] = {
            "message": response.reason,
            "status_code": response.status_code,
        }
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                result["error"].update(error_data)
        except (ValueError, json.JSONDecodeError):
            pass
    
    return result


def extract_json_from_response(response: Response) -> Dict[str, Any]:
    """
    Extrai dados JSON da resposta de forma segura para uso no SpiffWorkflow.
    
    Args:
        response: Objeto Response do requests
        
    Returns:
        Dict com os dados da resposta (ou vazio se não for JSON válido)
        
    Útil para extrair variáveis do workflow do SpiffWorkflow.
    """
    try:
        data = response.json()
        if isinstance(data, dict):
            return data
        return {"response": data}
    except (ValueError, json.JSONDecodeError):
        return {"response_text": response.text}


def prepare_spiff_data(data: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
    """
    Prepara dados em formato compatível com SpiffWorkflow Data Objects.
    
    Args:
        data: Dict opcional com dados iniciais
        **kwargs: Variáveis adicionais que serão adicionadas ao dict
        
    Returns:
        Dict combinado com todos os dados
        
    Exemplo:
        >>> prepare_spiff_data({"var1": "value"}, var2="value2")
        {"var1": "value", "var2": "value2"}
    """
    result = data.copy() if data else {}
    result.update(kwargs)
    return result


def validate_json_serializable(data: Any) -> bool:
    """
    Valida se os dados são serializáveis em JSON (requisito do SpiffWorkflow).
    
    Args:
        data: Dados a validar
        
    Returns:
        True se for serializável, False caso contrário
    """
    try:
        json.dumps(data)
        return True
    except (TypeError, ValueError):
        return False


