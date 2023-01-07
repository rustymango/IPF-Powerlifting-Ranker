from rest_framework import serializers
from .models import Powerlifting

class PowerliftingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Powerlifting
        fields = ["id", "weight", "gender", "age", "squat", "bench", "deadlift", "squat_rank", "bench_rank", "deadlift_rank"]