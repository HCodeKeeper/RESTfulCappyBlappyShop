from django.contrib import admin
import shop.models as shop_models
import user_profiles.models as user_models

models_to_register = [
    shop_models.Deal, shop_models.Addon, shop_models.Product,
    shop_models.Category, shop_models.Order, shop_models.OrderItem,
    shop_models.Review, shop_models.Telephone,
    user_models.Profile
]

for model in models_to_register:
    admin.site.register(model)
# Register your models here.