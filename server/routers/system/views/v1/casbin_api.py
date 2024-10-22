from fastapi import APIRouter, Depends
from server.core.response_base import R, ResponseModel
from server.core.security.depends_auth import Auth, auth_support

from ... import schemas
from ... import services

api = APIRouter()
