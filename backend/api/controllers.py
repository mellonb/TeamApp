#from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import *
from django.contrib.auth import *
# from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
#from django.shortcuts import render_to_response
from django.template import RequestContext
from django_filters.rest_framework import DjangoFilterBackend


from django.shortcuts import *

# Import models
from django.db import models
from django.contrib.auth.models import *
from api.models import *

#REST API
from rest_framework import viewsets, filters
from rest_framework_json_api import parsers, renderers
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import *
from rest_framework.decorators import *
from rest_framework.authentication import *

#filters
#from filters.mixins import *

from api.pagination import *
import json, datetime, pytz
from django.core import serializers
import requests


def home(request):
   """
   Send requests to / to the ember.js clientside app
   """
   return render_to_response('ember/index.html',
               {}, RequestContext(request))

def xss_example(request):
  """
  Send requests to xss-example/ to the insecure client app
  """
  return render_to_response('dumb-test-app/index.html',
              {}, RequestContext(request))

class Register(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # Login
        username = request.POST.get('username') #you need to apply validators to these
        print username
        password = request.POST.get('password') #you need to apply validators to these
        email = request.POST.get('email') #you need to apply validators to these
        gender = request.POST.get('gender') #you need to apply validators to these
        age = request.POST.get('age') #you need to apply validators to these
        educationlevel = request.POST.get('educationlevel') #you need to apply validators to these
        city = request.POST.get('city') #you need to apply validators to these
        state = request.POST.get('state') #you need to apply validators to these

        print request.POST.get('username')
        if User.objects.filter(username=username).exists():
            return Response({'username': 'Username is taken.', 'status': 'error'})
        elif User.objects.filter(email=email).exists():
            return Response({'email': 'Email is taken.', 'status': 'error'})

        #especially before you pass them in here
        newuser = User.objects.create_user(email=email, username=username, password=password)
        newprofile = Profile(user=newuser, gender=gender, age=age, educationlevel=educationlevel, city=city, state=state)
        newprofile.save()

        return Response({'status': 'success', 'userid': newuser.id, 'profile': newprofile.id})

class Session(APIView):
    permission_classes = (AllowAny,)
    def form_response(self, isauthenticated, userid, username, error=""):
        data = {
            'isauthenticated': isauthenticated,
            'userid': userid,
            'username': username
        }
        if error:
            data['message'] = error

        return Response(data)

    def get(self, request, *args, **kwargs):
        # Get the current user
        if request.user.is_authenticated():
            return self.form_response(True, request.user.id, request.user.username)
        return self.form_response(False, None, None)

    def post(self, request, *args, **kwargs):
        # Login
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return self.form_response(True, user.id, user.username)
            return self.form_response(False, None, None, "Account is suspended")
        return self.form_response(False, None, None, "Invalid username or password")

    def delete(self, request, *args, **kwargs):
        # Logout
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

# class Events(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def get(self, request, format=None):
#         events = Event.objects.all()
#         json_data = serializers.serialize('json', events)
#         content = {'events': json_data}
#         return HttpResponse(json_data, content_type='json')
#
#     def post(self, request, *args, **kwargs):
#         print 'REQUEST DATA'
#         print str(request.data)
#
#         eventtype = request.data.get('eventtype')
#         timestamp = int(request.data.get('timestamp'))
#         userid = request.data.get('userid')
#         requestor = request.META['REMOTE_ADDR']
#
#         newEvent = Event(
#             eventtype=eventtype,
#             timestamp=datetime.datetime.fromtimestamp(timestamp/1000, pytz.utc),
#             userid=userid,
#             requestor=requestor
#         )
#
#         try:
#             newEvent.clean_fields()
#         except ValidationError as e:
#             print e
#             return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)
#         newEvent.save()
#         print 'New Event Logged from: ' + requestor
#         return Response({'success': True}, status=status.HTTP_200_OK)

# class DogDetail(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def get(self, request, pk, format=None):
#         dog = Dog.objects.get(id=pk)
#         serializer = DogSerializer(dog)
#         #json_data = serializers.serialize('json', dogdetail)
#         #content = {'dogdetail': json_data}
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         print 'REQUEST DATA'
#         print str(request.data)
#
#         name = request.data.get('name')
#         age = request.data.get('age')
#         breed = Breed.objects.get(id=request.data.get('breed'))
#         gender = request.data.get('gender')
#         color = request.data.get('color')
#         favoritefood = request.data.get('favoritefood')
#         favoritetoy = request.data.get('favoritetoy')
#
#         dog = Dog.objects.get(id=pk)
#         dog.name = name
#         dog.age = age
#         dog.breed = breed
#         dog.gender = gender
#         dog.color = color
#         dog.favoritefood = favoritefood
#         dog.favoritetoy = favoritetoy
#         dog.save()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk, *args, **kwargs):
#         dog =Dog.objects.get(id=pk)
#         dog.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# class DogList(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def get(self, request, format=None):
#         doglist = Dog.objects.all()
#         print doglist
#         serializer = DogSerializer(doglist, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = DogSerializer(data=request.data)
#         print serializer.is_valid(raise_exception=True)
#         print serializer.validated_data
#         serializer.save()
#         return Response(serializer.data)
#
# class BreedDetail(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def get(self, request, pk, format=None):
#         breed = Breed.objects.get(id=pk)
#         serializer = BreedSerializer(breed)
#         print serializer.data
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         print 'REQUEST DATA'
#         print str(request.data)
#
#         name = request.data.get('name')
#         print name
#         size = request.data.get('size')
#         friendliness = request.data.get('friendliness')
#         trainability = request.data.get('trainability')
#         sheddingamount = request.data.get('sheddingamount')
#         exerciseneeds = request.data.get('exerciseneeds')
#
#         breed = Breed.objects.get(id=pk)
#         breed.name = name
#         breed.size = size
#         breed.friendliness = friendliness
#         breed.trainability = trainability
#         breed.sheddingamount = sheddingamount
#         breed.exerciseneeds = exerciseneeds
#         breed.save()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk, *args, **kwargs):
#         breed = Breed.objects.get(id=pk)
#         breed.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
# class BreedList(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def get(self, request, format=None):
#         breedlist = Breed.objects.all()
#         serializer = BreedSerializer(breedlist, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = BreedSerializer(data=request.data)
#         print serializer.is_valid(raise_exception=True)
#         print serializer.validated_data
#         serializer.save()
#         return Response(serializer.data)

class ChildViewSet(viewsets.ModelViewSet):
    serializer_class = ChildSerializer
    queryset = Child.objects.all()
    permission_classes = (AllowAny,)

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    # def list(self, request):
    #     queryset = Child.objects.all()
    #     serializer = ChildSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = Child.objects.all()
    #     child = get_object_or_404(queryset, pk=pk)
    #     serializer = ChildSerializer(child)
    #     return Response(serializer.data)
    #
    # def create(self, request):
    #     serializer = ChildSerializer(data=request.data)
    #     print serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data)
    #
    # def partial_update(self, request, pk=None):
    #     serializer = ChildSerializer(data=request.data, partial=True)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None):
    #     serializer = ChildSerializer(data=request.data)
    #     serializer = ChildSerializer(data=request.data, many=True)
    #     return Response(serializer.data)
    #
    # def destroy(self, request, pk=None):
    #     child = Child.objects.get(id=pk)
    #     child.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class ChildList(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def get(self, request, format=None):
#         childlist = Child.objects.all()
#         serializer = ChildSerializer(childlist, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = ChildSerializer(data=request.data)
#         print serializer.is_valid(raise_exception=True)
#         print serializer.validated_data
#         serializer.save()
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         print 'REQUEST DATA'
#         print str(request.data)
#
#         name = request.data.get('name')
#         parent = request.data.get('parent')
#
#         child = Child.objects.get(id=pk)
#         child.name = name
#         child.parent = parent
#         child.save()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk, *args, **kwargs):
#         child = Child.objects.get(id=pk)
#         child.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class GroupViewSet(viewsets.ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    permission_classes = (AllowAny,)

    # def list(self, request):
    #     queryset = Group.objects.all()
    #     serializer = GroupSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    #     #should be up to date
    #
    # def retrieve(self, request, pk=None):
    #     queryset = Group.objects.all()
    #     group = get_object_or_404(queryset, pk=pk)
    #     serializer = ChildSerializer(group)
    #     return Response(serializer.data)
    #
    # def create(self, request):
    #     serializer = GroupSerializer(data=request.data)
    #     print serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data)
    #
    # def partial_update(self, request, pk=None):
    #     serializer = GroupSerializer(data=request.data, partial=True)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None):
    #     serializer = GroupSerializer(data=request.data, many=True)
    #     return Response(serializer.data)
    #
    # def destroy(self, request, pk=None):
    #     group = Group.objects.get(id=pk)
    #     group.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

# class GroupList(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def get(self, request, format=None):
#         grouplist = Group.objects.all()
#         serializer = GroupSerializer(grouplist, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, *args, **kwargs):
#         serializer = GroupSerializer(data=request.data)
#         print serializer.is_valid(raise_exception=True)
#         print serializer.validated_data
#         serializer.save()
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         print 'REQUEST DATA'
#         print str(request.data)
#
#         name = request.data.get('name')
#         members = request.data.get('members')
#
#         group = Group.objects.get(id=pk)
#         group.name = name
#         group.members = members
#         group.save()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk, *args, **kwargs):
#         group = Group.objects.get(id=pk)
#         group.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ProfileList(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def get(self, request, format=None):
#         profilelist = Profile.objects.all()
#         serializer = ProfileSerializer(profilelist, many=True)
#         return Response(serializer.data)

# class ProfileList(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Profile.objects.all()
#         serializer = ProfileSerializer(queryset, many=True)
#         return Response(serializer.data)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (AllowAny,)
#    def list(self, request):
#        queryset = Profile.objects.all()
#        serializer = ProfileSerializer(queryset, many=True)
#        return Response(serializer.data)

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = (AllowAny,)

    # def list(self, request):
    #     queryset = Event.objects.all()
    #     serializer = EventSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = Event.objects.all()
    #     event = get_object_or_404(queryset, pk=pk)
    #     serializer = ChildSerializer(event)
    #     return Response(serializer.data)
    #
    # def create(self, request):
    #     serializer = EventSerializer(data=request.data)
    #     print serializer.is_valid(raise_exception=True)
    #     return Response(serializer.data)
    #
    # def partial_update(self, request, pk=None):
    #     serializer = EventSerializer(data=request.data, partial=True)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None):
    #     serializer = EventSerializer(data=request.data, many=True)
    #     return Response(serializer.data)
    #
    # def destroy(self, request, pk=None):
    #     event = Event.objects.get(id=pk)
    #     event.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


# class EventList(APIView):
#     permission_classes =(AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def get(self, request, format=None):
#         eventlist = Event.objects.all()
#         serializer = EventSerializer(eventlist, many=True)
#
#     def post(self, request, *args, **kwargs):
#         serializer = EventSerializer(data=request.data)
#         print serializer.is_valid(raise_exception=True)
#         print serializer.validated_data
#         serializer.save()
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         print 'REQUEST DATA'
#         print str(request.data)
#
#         timestamp = request.data.get('timestamp')
#         title = request.data.get('title')
#         info = request.data.get('info')
#         group = request.data.get('group')
#
#         event = Event.objects.get(id=pk)
#         event.timestamp = timestamp
#         event.title = title
#         event.info = info
#         event.group = group
#         event.save()
#         return Response({'success': True}, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk, *args, **kwargs):
#         event = Event.objects.get(id=pk)
#         event.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ActivateIFTTT(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (parsers.JSONParser,parsers.FormParser)
#     renderer_classes = (renderers.JSONRenderer, )
#     def post(self,request):
#         print 'REQUEST DATA'
#         print str(request.data)
#
#         eventtype = request.data.get('eventtype')
#         timestamp = int(request.data.get('timestamp'))
#         requestor = request.META['REMOTE_ADDR']
#         api_key = ApiKey.objects.all().first()
#         event_hook = "test"
#
#         print "Creating New event"
#
#         newEvent = Event(
#             eventtype=eventtype,
#             timestamp=datetime.datetime.fromtimestamp(timestamp/1000, pytz.utc),
#             userid=str(api_key.owner),
#             requestor=requestor
#         )
#
#         print newEvent
#         print "Sending Device Event to IFTTT hook: " + str(event_hook)
#
#         #send the new event to IFTTT and print the result
#         event_req = requests.post('https://maker.ifttt.com/trigger/'+str(event_hook)+'/with/key/'+api_key.key, data= {
#             'value1' : timestamp,
#             'value2':  "\""+str(eventtype)+"\"",
#             'value3' : "\""+str(requestor)+"\""
#         })
#         print event_req.text
#
#         #check that the event is safe to store in the databse
#         try:
#             newEvent.clean_fields()
#         except ValidationError as e:
#             print e
#             return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)
#
#         #log the event in the DB
#         newEvent.save()
#         print 'New Event Logged'
#         return Response({'success': True}, status=status.HTTP_200_OK)
