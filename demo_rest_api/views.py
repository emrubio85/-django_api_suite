from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

class DemoRestApi(APIView):
    name = "Demo REST API"

    def get(self, request):
      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)


class DemoRestApiItem(APIView):
    """
    Vista para manejar PUT, PATCH y DELETE sobre un elemento identificado por su 'id'
    """

    def put(self, request, id):
        """
        Reemplaza completamente los datos de un elemento, excepto el id.
        """
        for item in data_list:
            if item['id'] == id:
                # El id debe venir en el body y coincidir
                if request.data.get('id') != id:
                    return Response(
                        {"message": "El campo 'id' es obligatorio y debe coincidir."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Reemplazar todos los campos excepto el id
                item.update({
                    'name': request.data.get('name'),
                    'email': request.data.get('email'),
                    'is_active': request.data.get('is_active')
                })
                return Response(
                    {"message": "Elemento reemplazado correctamente.", "data": item},
                    status=status.HTTP_200_OK
                )
        return Response({"message": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        """
        Actualiza parcialmente los campos de un elemento.
        """
        for item in data_list:
            if item['id'] == id:
                # Actualizar solo los campos enviados
                for field in ['name', 'email', 'is_active']:
                    if field in request.data:
                        item[field] = request.data[field]
                return Response(
                    {"message": "Elemento actualizado parcialmente.", "data": item},
                    status=status.HTTP_200_OK
                )
        return Response({"message": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        """
        Elimina lógicamente un elemento (marcar is_active=False).
        """
        for item in data_list:
            if item['id'] == id:
                item['is_active'] = False
                return Response(
                    {"message": "Elemento eliminado lógicamente.", "data": item},
                    status=status.HTTP_200_OK
                )
        return Response({"message": "Elemento no encontrado."}, status=status.HTTP_404_NOT_FOUND)
