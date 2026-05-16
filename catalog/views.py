from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .patterns import CatalogFacade, AdminInvoker, AddRandomDogCommand, AddRandomCatCommand, PetFactory
from .models import Pet

def catalog_view(request):
    pets = CatalogFacade.get_available_pets()
    return render(request, 'catalog/catalog.html', {'pets': pets})

def adopt_pet_view(request, pet_id):
    if request.method == 'POST':
        success = CatalogFacade.adopt_pet(pet_id)
        # In a real app, we'd show a success message.
    return redirect('catalog')

@login_required
def admin_dashboard_view(request):
    invoker = AdminInvoker()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_dog':
            invoker.execute_command(AddRandomDogCommand())
        elif action == 'add_cat':
            invoker.execute_command(AddRandomCatCommand())
        elif action == 'add_manual':
            name = request.POST.get('name')
            species = request.POST.get('species')
            description = request.POST.get('description')
            image_file = request.FILES.get('image_file')
            if name and species:
                PetFactory.create_pet(
                    source="manual", 
                    name=name, 
                    species=species, 
                    description=description, 
                    image_file=image_file
                )
        elif action == 'mark_adopted':
            pet_id = request.POST.get('pet_id')
            if pet_id:
                CatalogFacade.adopt_pet(pet_id)
        elif action == 'remove_pet':
            pet_id = request.POST.get('pet_id')
            if pet_id:
                Pet.objects.filter(id=pet_id).delete()
        return redirect('custom_admin')

    pets = Pet.objects.all().order_by('-id')
    return render(request, 'catalog/admin_dashboard.html', {'pets': pets})
