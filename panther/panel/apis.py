from panther import status
from panther.app import API
from panther.configs import config
from panther.request import Request
from panther.response import Response
from panther.exceptions import APIException

from pydantic import ValidationError


@API()
async def models_api():
    result = list()
    for i, m in enumerate(config['models']):
        data = dict()
        data['name'] = m['name']
        data['app'] = '.'.join(a for a in m['app'])
        data['path'] = m['path']
        data['index'] = i
        result.append(data)
    return result


@API()
async def documents_api(request: Request, index: int):
    model = config['models'][index]['class']

    if request.method == 'POST':
        try:
            validated_data = model(**request.pure_data)
        except ValidationError as validation_error:
            error = {e['loc'][0]: e['msg'] for e in validation_error.errors()}
            raise APIException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

        document = model.insert_one(**validated_data.model_dump(exclude=['id']))
        return Response(data=document, status_code=status.HTTP_201_CREATED)

    else:
        result = {
            'fields': {k: getattr(v.annotation, '__name__', str(v.annotation)) for k, v in model.model_fields.items()},
        }
        if data := model.find():
            result['data'] = data
        else:
            result['data'] = []
        return result


@API()
async def single_document_api(request: Request, index: int, id: int | str):
    model = config['models'][index]['class']

    if document := model.find_one(id=id):

        if request.method == 'PUT':
            try:
                validated_data = model(**request.pure_data)
            except ValidationError as validation_error:
                error = {e['loc'][0]: e['msg'] for e in validation_error.errors()}
                raise APIException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

            document.update(**validated_data.model_dump(exclude=['id']))
            return Response(data=document, status_code=status.HTTP_202_ACCEPTED)

        elif request.method == 'DELETE':
            document.delete()
            return Response(status_code=status.HTTP_204_NO_CONTENT)

        else:  # GET
            return document

    else:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

