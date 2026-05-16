import requests
from .models import Pet

# 1. Singleton Pattern (Creational)
class APIClientSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.session = requests.Session()
        return cls._instance

    def get(self, url):
        return self.session.get(url)

# 2. Adapter Pattern (Structural)
class PetDataAdapter:
    def fetch_data(self):
        pass

class DogAPIAdapter(PetDataAdapter):
    def fetch_data(self):
        client = APIClientSingleton()
        response = client.get("https://dog.ceo/api/breeds/image/random")
        if response.status_code == 200:
            data = response.json()
            return {
                "name": "Cão Aleatório",
                "species": "Cão",
                "description": "Um garoto/garota muito bom/muito boa vindo da API de Cachorros.",
                "image_url": data.get("message")
            }
        return None

class CatAPIAdapter(PetDataAdapter):
    def fetch_data(self):
        client = APIClientSingleton()
        response = client.get("https://api.thecatapi.com/v1/images/search")
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                return {
                    "name": "Gato Aleatório",
                    "species": "Gato",
                    "description": "Bicho misterioso vindo da API de Gatos.",
                    "image_url": data[0].get("url")
                }
        return None

# 3. Factory Method Pattern (Creational)
class PetFactory:
    @staticmethod
    def create_pet(source="manual", **kwargs):
        if source == "manual":
            return Pet.objects.create(
                name=kwargs.get("name"),
                species=kwargs.get("species"),
                description=kwargs.get("description"),
                image_url=kwargs.get("image_url", ""),
                image_file=kwargs.get("image_file")
            )
        elif source == "api":
            adapter = kwargs.get("adapter")
            if adapter:
                data = adapter.fetch_data()
                if data:
                    return Pet.objects.create(
                        name=data["name"],
                        species=data["species"],
                        description=data["description"],
                        image_url=data["image_url"]
                    )
        return None

# 4. Facade Pattern (Structural)
class CatalogFacade:
    @staticmethod
    def get_available_pets():
        return Pet.objects.filter(is_adopted=False)

    @staticmethod
    def adopt_pet(pet_id):
        try:
            pet = Pet.objects.get(id=pet_id, is_adopted=False)
            pet.is_adopted = True
            pet.save()
            return True
        except Pet.DoesNotExist:
            return False

# 5. Command Pattern (Behavioral)
class AdminCommand:
    def execute(self):
        pass

class AddRandomDogCommand(AdminCommand):
    def execute(self):
        adapter = DogAPIAdapter()
        return PetFactory.create_pet(source="api", adapter=adapter)

class AddRandomCatCommand(AdminCommand):
    def execute(self):
        adapter = CatAPIAdapter()
        return PetFactory.create_pet(source="api", adapter=adapter)

class AdminInvoker:
    def execute_command(self, command: AdminCommand):
        return command.execute()
