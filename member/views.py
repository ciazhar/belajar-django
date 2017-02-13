from django.shortcuts import render, redirect
from .forms import UserForm,MemberForm, TopUpForm
from django.views.generic import CreateView, ListView
from member.models import TopUp
# Create your views here.
#ada 2 buah view dlm djangon yaitu class based view atau function based view
#kalo ini pake function based view

def register(request):
    if request.method == 'POST':
        userform = UserForm(request.POST)
        memberform = MemberForm(request.POST)
        if userform.is_valid() * memberform.is_valid():
            user = userform.save(commit=False)
            user.set_password(userform.cleaned_data['password1'])
            user.save()

            member = memberform.save(commit=False)
            member.user = user
            member.save()
            return redirect('login')
    else:
        userform = UserForm()
        memberform = MemberForm()
    return render(request, 'register.html',{'userform':userform,'memberform':memberform})

class TopUpFormView(CreateView):
    form_class = TopUpForm
    template_name = 'topup_form.html'

    def form_valid(self,form):
        topup = form.save(commit=False)
        topup.member = self.request.user
        topup.status = 'p'
        topup.save()
        return redirect('index')

class TopUpListView(ListView):
    template_name = 'topup_list.html'
    model = TopUp

    #fungsi untuk mendampilkan hanya topup history kita
    def get_queryset(self):
        return TopUp.objects.filter(member=self.request.user.member)