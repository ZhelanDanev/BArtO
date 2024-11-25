<<<<<<< HEAD
from django.db import models


class WriterGenres(models.TextChoices):
    FANTASY = "Fantasy", "Fantasy"
    SCIENCE_FICTION = "SciFi", "Science Fiction"
    MYSTERY = "Mystery", "Mystery"
    THRILLER = "Thriller", "Thriller"
    ROMANCE = "Romance", "Romance"
    HISTORICAL_FICTION = "HiFi", "Historical fiction"
    HORROR = "Horror", "Horror"
    ADVENTURE = "Adventure", "Adventure"
    BIOGRAPHY = "Biography", "Biography"
    TRUE_CRIME = "True crime", "True crime"
    ESSAY = "Essay", "Essay"
    JOURNALISM = "Journalism", "Journalism"
    LYRIC = "Lyric", "Lyric"
    CHILDREN_LITERATURE = "Children Literature", "Children Literature"
    COMICS = "Comics", "Comics"


class MusicianGenres(models.TextChoices):
    CLASSICAL = "Classical", "Classical"
    BLUES = "Blues", "Blues"
    COUNTRY = "Country", "Country"
    ELECTRONIC = "Electronic", "Electronic"
    FOLK = "Folk", "Folk"
    HIP_HOP = "Hip-Hop", "Hip-Hop"
    JAZZ = "Jazz", "Jazz"
    POP = "Pop", "Pop"
    RNB_AND_SOUL = "R&B and Soul", "R&B and Soul"
    ROCK = "Rock", "Rock"
    METAL = "Metal", "Metal"
    PUNK = "Punk", "Punk"


class ActorGenres(models.TextChoices):
    DRAMA = "Drama", "Drama"
    COMEDY = "Comedy", "Comedy"
    ACTION = "Action", "Action"
    ROMANCE = "Romance", "Romance"
    FANTASY = "Fantasy", "Fantasy"
    HORROR = "Horror", "Horror"
    THRILLER = "Thriller", "Thriller"
    ADVENTURE = "Adventure", "Adventure"
=======
from django.db import models


class WriterGenres(models.TextChoices):
    FANTASY = "Fantasy", "Fantasy"
    SCIENCE_FICTION = "SciFi", "Science Fiction"
    MYSTERY = "Mystery", "Mystery"
    THRILLER = "Thriller", "Thriller"
    ROMANCE = "Romance", "Romance"
    HISTORICAL_FICTION = "HiFi", "Historical fiction"
    HORROR = "Horror", "Horror"
    ADVENTURE = "Adventure", "Adventure"
    BIOGRAPHY = "Biography", "Biography"
    TRUE_CRIME = "True crime", "True crime"
    ESSAY = "Essay", "Essay"
    JOURNALISM = "Journalism", "Journalism"
    LYRIC = "Lyric", "Lyric"
    CHILDREN_LITERATURE = "Children Literature", "Children Literature"
    COMICS = "Comics", "Comics"


class MusicianGenres(models.TextChoices):
    CLASSICAL = "Classical", "Classical"
    BLUES = "Blues", "Blues"
    COUNTRY = "Country", "Country"
    ELECTRONIC = "Electronic", "Electronic"
    FOLK = "Folk", "Folk"
    HIP_HOP = "Hip-Hop", "Hip-Hop"
    JAZZ = "Jazz", "Jazz"
    POP = "Pop", "Pop"
    RNB_AND_SOUL = "R&B and Soul", "R&B and Soul"
    ROCK = "Rock", "Rock"
    METAL = "Metal", "Metal"
    PUNK = "Punk", "Punk"


class ActorGenres(models.TextChoices):
    DRAMA = "Drama", "Drama"
    COMEDY = "Comedy", "Comedy"
    ACTION = "Action", "Action"
    ROMANCE = "Romance", "Romance"
    FANTASY = "Fantasy", "Fantasy"
    HORROR = "Horror", "Horror"
    THRILLER = "Thriller", "Thriller"
    ADVENTURE = "Adventure", "Adventure"
>>>>>>> origin/main
