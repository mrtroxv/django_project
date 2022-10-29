import json
from django.http import HttpRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from song_process.models import Song
from datetime import datetime
from song_process.serializers import SongSerializer
from song_process.pagination import CustomPagination
from rest_framework.generics import ListAPIView
from song_process.process import Completing_data, generator


class SongRoute(APIView):

    #################select song without filter###########################

    def get(self, request: HttpRequest):
        obj = Song.objects.all()
        serializer = SongSerializer(obj, many=True)
        return Response(serializer.data)


###############insert song############################################

    def post(self, request: HttpRequest):
        request_data = Completing_data.complete_data(request.data)
        serializer = SongSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response("ur data is inserted", status.HTTP_200_OK)
        else:
            return Response("ur data is not valid ",
                            status=status.HTTP_400_BAD_REQUEST)


class SongArgumentRoute(APIView):

    ##############select by id ##############################

    def get(self, request: HttpRequest, id):
        try:
            obj = Song.objects.get(id=id)
        except:
            return Response("ur id request  is not founded ",
                            status=status.HTTP_404_NOT_FOUND)
        serializer = SongSerializer(obj)
        return Response(serializer.data)

########################delete######################################

    def delete(self, request: HttpRequest, id):
        try:
            obj = Song.objects.get(id=id)
        except:
            return Response("ur id request is not founded ",
                            status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response("ur data is deleted")


#############################update ####################################

    def put(self, request: HttpRequest, id):
        try:
            obj = Song.objects.get(id=id)
        except:
            return Response("ur id request is not found",
                            status=status.HTTP_404_NOT_FOUND)
        serializer = SongSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("ur data is up to date", status=status.HTTP_200_OK)
        else:
            return Response("Bad request", status=status.HTTP_400_BAD_REQUEST)


class FileInsert(APIView):

    ########################insert file #####################################

    def post(self, request: HttpRequest):
        tag = request.data['tag']
        file_path = (request.FILES['data_file'])
        force_replace = request.data['force_replace']
        file_content = json.load(file_path)
        for i in file_content:
            random_date = generator.date_generoter()
            i['tag'] = tag
            i['time_updated'] = datetime.now()
            i['time_created'] = random_date
            serializer = SongSerializer(data=i)
            if serializer.is_valid():
                serializer.save()
            else:
                if str.lower(force_replace) == 'true':
                    try:
                        obj = Song.objects.get(id=i['id'])
                        serializer = SongSerializer(obj, data=i)
                        if serializer.is_valid():
                            serializer.save()
                    except:
                        continue

        return Response("ur data is inserted", status=status.HTTP_200_OK)


###########################select by filter api###############################


class SelectByFilter(ListAPIView):

    queryset = Song.objects.all()
    serializer_class = SongSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name', '')
        author = self.request.query_params.get('author', '')
        type = self.request.query_params.get('type', '')
        image_url = self.request.query_params.get('image_url', '')
        file_url = self.request.query_params.get('file_url', '')
        rating = self.request.query_params.get('rating', 0.0)
        default_date = datetime.strptime('1/1/1111', '%m/%d/%Y')
        try:
            time_created = datetime.strptime(
                self.request.query_params.get('time_created'), '%m/%d/%Y')
        except:
            time_created = default_date
        try:
            time_updated = datetime.strptime(
                self.request.query_params.get('time_updated'), '%m/%d/%Y')
        except:
            time_updated = default_date

        return queryset.filter(name__contains=name).filter(
            author__contains=author).filter(type__contains=type).filter(
                image_url__contains=image_url).filter(
                    file_url__contains=file_url).filter(
                        rating__gte=rating).filter(
                            time_created__gte=time_created).filter(
                                time_updated__gte=time_updated)


# Create your views here.
