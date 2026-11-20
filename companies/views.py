from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from .models import Company
from .forms import CompanyForm
from placements.models import PlacementDrive

def company_list_view(request):
    companies = Company.objects.all().order_by('-is_featured', 'name')

    q = request.GET.get('q', '').strip()
    if q:
        companies = companies.filter(name__icontains=q) | companies.filter(industry__icontains=q) | companies.filter(location__icontains=q)

    company_type = request.GET.get('type', '').strip()
    if company_type:
        companies = companies.filter(company_type=company_type)

    paginator = Paginator(companies, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'companies/company_list.html', {
        'page_obj': page_obj,
        'q': q,
        'selected_type': company_type,
        'total_count': companies.count(),
    })


def company_detail_view(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    open_jobs = company.placement_drives.filter(is_active=True).order_by('-created_at')
    past_drives = company.placement_drives.filter(is_active=False).order_by('-created_at')
    total_selected = company.placement_drives.filter(applications__status__in=['SELECTED', 'PLACED']).count()

    return render(request, 'companies/company_detail.html', {
        'company': company,
        'open_jobs': open_jobs,
        'past_drives': past_drives,
        'total_selected': total_selected,
    })


@login_required
def company_create_view(request):
    if not request.user.is_officer:
        return HttpResponseForbidden("Only placement officers can register companies.")

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            messages.success(request, f"Company '{company.name}' added successfully!")
            return redirect('company_detail', company_id=company.id)
        else:
            messages.error(request, "Please fix errors in the form.")
    else:
        form = CompanyForm()

    return render(request, 'companies/company_form.html', {
        'form': form,
        'title': 'Add Partner Company',
        'is_edit': False,
    })


@login_required
def company_edit_view(request, company_id):
    if not request.user.is_officer:
        return HttpResponseForbidden("Only placement officers can update companies.")

    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, f"Company '{company.name}' updated successfully!")
            return redirect('company_detail', company_id=company.id)
        else:
            messages.error(request, "Please fix errors in the form.")
    else:
        form = CompanyForm(instance=company)

    return render(request, 'companies/company_form.html', {
        'form': form,
        'company': company,
        'title': f'Edit Company: {company.name}',
        'is_edit': True,
    })


@login_required
def company_delete_view(request, company_id):
    if not request.user.is_officer:
        return HttpResponseForbidden("Only placement officers can delete companies.")

    company = get_object_or_404(Company, id=company_id)
    if request.method == 'POST':
        name = company.name
        company.delete()
        messages.info(request, f"Company '{name}' has been deleted.")
        return redirect('company_list')

    return render(request, 'companies/company_confirm_delete.html', {'company': company})
