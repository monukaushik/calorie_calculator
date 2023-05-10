from django.db import models

class userdetail(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
   
    def __str__(self):
        return self.username + self.useremail


class food_item_gredient(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    date=models.DateField()
    total_cal=models.IntegerField()
    consume_calorie=models.FloatField()
    food_item=models.CharField(max_length=100)
    calories=models.IntegerField()
    protein=models.IntegerField()
    fat=models.IntegerField()
    carbs=models.IntegerField()
    suger=models.IntegerField()
    
    def __str__(self):
        return self.food_item



