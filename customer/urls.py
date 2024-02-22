from django.urls import path, include

from customer.views import customer_home, log_out, crop_prediction, crop_prediction_result, yield_prediction, weather, \
    fertilizer_suggestion

urlpatterns = [
    path('', customer_home, name='customer_home'),
    path('/crop_prediction', crop_prediction, name='customer_crop_prediction'),
    path('/crop_prediction_result/<n>/<p>/<k>/<t>/<h>/<ph>/<r>/', crop_prediction_result, name='customer_crop_prediction_result'),
    path('/yield_prediction', yield_prediction, name='customer_yield_prediction'),
    path('/weather', weather, name='customer_weather'),
    path('/fertilizer', fertilizer_suggestion, name='customer_fertilizer_suggestion'),
    path('/log_out/', log_out, name='log_out'),

]