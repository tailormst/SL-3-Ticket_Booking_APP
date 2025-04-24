import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from shows.models import Show, ShowTime
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Adds sample shows and showtimes to the database'

    def handle(self, *args, **kwargs):
        # Check if shows already exist
        if Show.objects.exists():
            self.stdout.write(self.style.WARNING('Shows already exist in the database. Skipping...'))
            return

        # Sample shows data
        shows_data = [
            {
                'title': 'Jawan',
                'description': 'A high-octane action thriller that outlines the emotional journey of a man who is set to rectify the wrongs in society.',
                'category': 'INDIAN',
                'duration': 170,
                'release_date': '2023-09-07',
                'image_url': 'https://m.media-amazon.com/images/M/MV5BOWI5NmU3NTUtOTZiMS00YzA1LThlYTktNDJjYTU5NDFiMDUxXkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg',
            },
            {
                'title': 'Animal',
                'description': 'A son undergoes a remarkable transformation as the bond with his father begins to fracture, and he becomes consumed by a quest for vengeance.',
                'category': 'INDIAN',
                'duration': 201,
                'release_date': '2023-12-01',
                'image_url': 'https://m.media-amazon.com/images/M/MV5BNGViM2M4NmUtMmNkNy00MTQ5LTk5MDYtNmNhODAzODkwOTJlXkEyXkFqcGdeQXVyMTY1NDY4NTIw._V1_FMjpg_UX1000_.jpg',
            },
            {
                'title': 'Oppenheimer',
                'description': 'The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb.',
                'category': 'HOLLYWOOD',
                'duration': 180,
                'release_date': '2023-07-21',
                'image_url': 'https://m.media-amazon.com/images/M/MV5BMDBmYTZjNjUtN2M1MS00MTQ2LTk2ODgtNzc2M2QyZGE5NTVjXkEyXkFqcGdeQXVyNzAwMjU2MTY@._V1_.jpg',
            },
            {
                'title': 'Barbie',
                'description': 'Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.',
                'category': 'HOLLYWOOD',
                'duration': 114,
                'release_date': '2023-07-21',
                'image_url': 'https://m.media-amazon.com/images/M/MV5BNjU3N2QxNzYtMjk1NC00MTc4LTk1NTQtMmUxNTljM2I0NDA5XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_FMjpg_UX1000_.jpg',
            },
            {
                'title': 'Dune: Part Two',
                'description': 'Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.',
                'category': 'HOLLYWOOD',
                'duration': 166,
                'release_date': '2024-03-01',
                'image_url': 'https://m.media-amazon.com/images/M/MV5BODdjMjM3NGQtZDA5OC00NGE4LWIyZDQtZjYwOGZlMTM5ZTQ1XkEyXkFqcGdeQXVyODE5NzE3OTE@._V1_.jpg',
            },
            {
                'title': 'Kalki 2898 AD',
                'description': 'A mythological sci-fi spectacle set in the future, blending futuristic elements with ancient Indian mythology.',
                'category': 'INDIAN',
                'duration': 180,
                'release_date': '2024-06-27',
                'image_url': 'https://m.media-amazon.com/images/M/MV5BN2Q3OWVjODAtMTQ0OS00ZWI5LTliMzktOWNkZWJlOWFhMzU1XkEyXkFqcGdeQXVyMTUzNTgzNzM0._V1_.jpg',
            },
        ]

        # Create shows
        for show_data in shows_data:
            image_url = show_data.pop('image_url')
            show = Show.objects.create(**show_data)
            
            # Download and save image
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_name = f"{show.title.lower().replace(' ', '_')}.jpg"
                    show.image.save(image_name, ContentFile(response.content), save=True)
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'Failed to download image for {show.title}: {e}'))
            
            # Create showtimes for each show
            today = timezone.now().date()
            for i in range(7):  # Create showtimes for the next 7 days
                show_date = today + datetime.timedelta(days=i)
                
                # Morning show
                ShowTime.objects.create(
                    show=show,
                    date=show_date,
                    time=datetime.time(10, 0),  # 10:00 AM
                    price=10.00 if show.category == 'HOLLYWOOD' else 8.00  # Indian shows are cheaper
                )
                
                # Afternoon show
                ShowTime.objects.create(
                    show=show,
                    date=show_date,
                    time=datetime.time(14, 30),  # 2:30 PM
                    price=12.00 if show.category == 'HOLLYWOOD' else 10.00
                )
                
                # Evening show
                ShowTime.objects.create(
                    show=show,
                    date=show_date,
                    time=datetime.time(18, 0),  # 6:00 PM
                    price=15.00 if show.category == 'HOLLYWOOD' else 12.00
                )
                
                # Night show
                ShowTime.objects.create(
                    show=show,
                    date=show_date,
                    time=datetime.time(21, 30),  # 9:30 PM
                    price=15.00 if show.category == 'HOLLYWOOD' else 12.00
                )
            
            self.stdout.write(self.style.SUCCESS(f'Successfully added show: {show.title}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully added all sample shows and showtimes'))