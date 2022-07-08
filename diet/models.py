from django.db import models

from accounts import models as user_model

#해당 날짜 먹은 음식
class DayHistoryDiet(models.Model):
    user_id = models.ForeignKey(user_model.User, 
                            on_delete=models.CASCADE,
                            related_name='day_history_diet_user')
    create_date = models.DateField()
    time = models.CharField(null=True, blank=True, max_length=200)
    food_name = models.CharField(null=True, blank=True, max_length=200)
    food_g = models.IntegerField(null=True, blank=True)
    food_one_meal_g = models.IntegerField(null=True, blank=True)
    food_kcal = models.IntegerField(null=True, blank=True)
    carbohydrate = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    province = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.user_id}_{self.create_date}_{self.food_name}'
