from django.db import models

class ShowCategory(models.TextChoices):
    INDIAN = 'INDIAN', 'Indian'
    HOLLYWOOD = 'HOLLYWOOD', 'Hollywood'
    OTHER = 'OTHER', 'Other'

class Show(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='shows/', blank=True, null=True)
    category = models.CharField(
        max_length=20,
        choices=ShowCategory.choices,
        default=ShowCategory.OTHER
    )
    duration = models.IntegerField(help_text="Duration in minutes")
    release_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = [
            # Order by category (Indian first, then Hollywood, then others)
            models.Case(
                models.When(category=ShowCategory.INDIAN, then=0),
                models.When(category=ShowCategory.HOLLYWOOD, then=1),
                default=2,
                output_field=models.IntegerField(),
            ),
            '-release_date'  # Then by release date (newest first)
        ]

class ShowTime(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='showtimes')
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"{self.show.title} - {self.date} {self.time}"
    
    class Meta:
        ordering = ['date', 'time']

class Seat(models.Model):
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=2)
    number = models.IntegerField()
    is_reserved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.row}{self.number} - {self.showtime}"
    
    class Meta:
        unique_together = ('showtime', 'row', 'number')
        ordering = ['row', 'number']