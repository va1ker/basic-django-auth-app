from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import NewUserForm, LoginForm
from django.contrib.auth import login,authenticate
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def personal(request):
    return render(request, 'personal_account/profile.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("personal")
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'personal_account/login.html', {'form': form})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("personal")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="personal_account/register.html", context={"register_form":form})
