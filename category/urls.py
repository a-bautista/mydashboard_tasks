from django.urls import path
# import the component task
from .views import (    
                        create_category, 
                        update_category, 
                        retrieve_all
                    )


urlpatterns = [
    path('list/', retrieve_all),
    path('new/', create_category, name='create_category'),
    path('update/<int:id>/', update_category, name='update_category')
]
