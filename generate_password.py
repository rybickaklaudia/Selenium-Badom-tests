from faker import Faker

# Inicjalizacja obiektu Faker
fake = Faker()

# Generowanie falszywego adresu mailowego
email = fake.email()

# Generowanie fałszywego hasła
password = fake.password(length=12)

# Wyświetlenie fałszywego hasła na konsoli
print("Wygenerowane fałszywe hasło:", email)
print("Wygenerowane fałszywe hasło:", password)
