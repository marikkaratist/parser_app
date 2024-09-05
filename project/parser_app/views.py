import requests
import json
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import LogEntry
from .serializers import LogEntrySerializer


class LogEntryCreateView(generics.CreateAPIView):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer

    def post(self, request, *args, **kwargs):
        # URL файла на Google Drive
        file_url = "https://drive.google.com/uc?export=download&id=18Ss9afYL8xTeyVd0ZTfFX9dqja4pBGVp"

        # Загрузка файла с помощью requests
        response = requests.get(file_url)

        # Проверка успешности загрузки
        if response.status_code == 200:
            # Предполагаем, что данные в формате JSON
            data = json.loads(response.text)

            # Если данные являются списком, сохраните каждую запись
            if isinstance(data, list):
                for entry in data:
                    serializer = self.get_serializer(data=entry)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "All entries created successfully."}, status=status.HTTP_201_CREATED)

            # Если данные не являются списком, обработайте одну запись
            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Если загрузка не удалась, верните ошибку
        return Response({"error": "Failed to fetch data from the URL."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
