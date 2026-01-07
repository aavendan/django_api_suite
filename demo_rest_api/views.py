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
    
    def get(self, request, id):
        """
        Obtiene un elemento de data_list según su id
        """

        # Buscar el elemento por id
        for item in data_list:
            if item["id"] == id:
                return Response(item, status=status.HTTP_200_OK)

        # Si no se encuentra el id
        return Response(
            {"error": "Elemento no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    def put(self, request, id):
        """
        Actualiza un elemento de data_list según su id
        """

        # 1. Buscar el elemento por id
        for index, item in enumerate(data_list):
            if item["id"] == id:

                # 2. Reemplazar los valores (PUT = reemplazo completo)
                data_list[index] = {
                    "id": id,  # se mantiene el id original
                    "name": request.data.get("name"),
                    "email": request.data.get("email"),
                    "is_active": request.data.get("is_active", True)
                }

                # 3. Retornar el elemento actualizado
                return Response(
                    data_list[index],
                    status=status.HTTP_200_OK
                )

        # 4. Si no se encuentra el id
        return Response(
            {"error": "Elemento no encontrado"},
            status=status.HTTP_404_NOT_FOUND
        )