"""
Basic drf swagger schema preset
"""

from drf_spectacular.utils import (
    OpenApiResponse, OpenApiExample, inline_serializer
)
from rest_framework import serializers


schema_serializers = {
    400: inline_serializer(
        name='BadRequestSerializer',
        fields={
            'error': serializers.CharField(),
        },
    ),
    401: inline_serializer(
        name='UnauthorizedSerializer',
        fields={
            'error': serializers.CharField(),
        },
    ),
    404: inline_serializer(
        name='NonFoundSerializer',
        fields={
            'error': serializers.CharField(),
        },
    ),
}

descriptions = {
    400: '''
    Bad Request
    ''',
    401:'''
    Unauthoriezd
    ''',
    404: '''
    NotFound
    '''
}

summaries = {
    
}

examples = {
    400: OpenApiExample(
        name='bad request',
        value={
            'error': 'Bad Request',
        },
        status_codes=['400'],
        response_only=True,
    ),
    401: OpenApiExample(
        name='unauthorized',
        value={
            'error': 'Unauthorized',
        },
        status_codes=['401'],
        response_only=True,
    ),
    404: OpenApiExample(
        name='not found',
        value={
            'error': 'Not Found',
        },
        status_codes=['404'],
        response_only=True,
    ),
}

open_api_response = {
    400: OpenApiResponse(
        response=schema_serializers[400],
        description=descriptions[400],
    ),
    401: OpenApiResponse(
        response=schema_serializers[401],
        description=descriptions[401],
    ),
    404: OpenApiResponse(
        response=schema_serializers[404],
        description=descriptions[404],
    ),
}
