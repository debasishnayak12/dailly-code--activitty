from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import Item

@api_view(['POST'])
def createuser(request):
    name=request.data.get('name')
    description = request.data.get('description')
    price = request.data.get('price')
    if name=='' or name==None:
        return Response({"status":False,"message":"Please Enter name"},status=status.HTTP_400_BAD_REQUEST)
    elif description=='' or description==None:
        return Response({"status":False,"message":"Please Enter description"}, status=status.HTTP_400_BAD_REQUEST)
    elif price=='' or price==None:
        return Response({"status":False,"message":"Please Enter price"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            item=Item.objects.create(name=name,description=description,price= price )
            return Response({"status":True,"message":"User created Successfully","id":item.id}, status=status.HTTP_201_CREATED)
             
        except Exception as e:
            return Response({"status":False,"message":"Error","Error":f"{e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def getusers(request):
    try:
        item = Item.objects.all()
        
        for i in item:
            data =[{"id":i.id,"name":i.name,"description":i.description,"price":i.price} for i in item]
        return Response({"status":True,"message":"successfully fetched all data","data":data},status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
            return Response({"status":False,"message":"Unable to fetch data at this moment"},status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"status":False,"Error":f"{e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def getuser(request):
    item_id=request.data.get('id')
    if item_id=='' or item_id == None:
        return Response({"status":True,"message":"Pleas enter id "},status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            item = Item.objects.get(id=item_id)
          
            data={"id":item.id,"name":item.name,"description":item.description,"price":item.price}
            return Response({"status":True,"message":"Successfully fetched data","data":data},status=status.HTTP_200_OK)
        
        except Item.DoesNotExist:
            return Response({"status":False,"message":"Sorry,No data found on this id "},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"status":False,"error":f"{e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def updateuser(request):
    item_id=request.data.get('id')
    name = request.data.get('name')
    description = request.data.get('description')
    price = request.data.get('price')
    if item_id=='' or item_id is None:
        return  Response({"status":False,"message":"Please Enter id"},status=status.HTTP_400_BAD_REQUEST)
    try:
        item  = Item.objects.get(id=item_id)
        if name !='' and name!=None:
            item.name = name
        if description!='' and description != None:
            item.description=description
        if price!= '' and price != None:
            item.price = price

        item.save()   
        return Response({"status":True,"message":"Successfully Updated"},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"status":False,"Error":f"{e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def deleteuser(request):
    item_id = request.data.get('id')
    if item_id == '' or item_id is None:
        return Response({"status":False,"message":"Please Enter id"})
    try:
        item = Item.objects.get(id=item_id)
        item.delete()
        return Response({'status':True,'message':'Data deleted Successfully'},status=status.HTTP_200_OK)
    
    except Item.DoesNotExist:
        return Response({"status":False,"message":"Sorry,No data found on this id "},status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"status":False,"error":f"{e}"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
