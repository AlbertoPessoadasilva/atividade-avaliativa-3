import csv
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.db.models import Q
from .models import Funcionario

class FuncionarioCreateView(CreateView):
    model = Funcionario
    fields = "__all__"
    template_name = "form_funcionario.html"
    success_url = reverse_lazy("lista_funcionarios")

class FuncionarioListView(ListView):
    model = Funcionario
    template_name = "lista_funcionarios.html"
    context_object_name = "object_list"

    def get_queryset(self):
        query = self.request.GET.get("q")  
        if query:
            return Funcionario.objects.filter(
                Q(nome__icontains=query) | 
                Q(email__icontains=query)
            )
        return Funcionario.objects.all()
class FuncionarioUpdateView(UpdateView):
    model = Funcionario
    fields = ("nome", "data_nascimento", "email", "remuneracao")
    template_name = "form_funcionario.html"
    success_url = reverse_lazy("lista_funcionarios")

class FuncionarioDetailView(DetailView):
    model = Funcionario
    template_name = "lista_funcionario.html"
    context_object_name = "fun" 

class FuncionarioDeleteView(DeleteView):
    model = Funcionario
    template_name = "remover_funcionario.html"
    success_url = reverse_lazy("lista_funcionarios")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funcionario = get_object_or_404(Funcionario, pk=self.kwargs['pk'])
        
        context['nome'] = funcionario.nome
        context['email'] = funcionario.email
        context['remuneracao'] = funcionario.remuneracao
        return context

def exportar_funcionarios(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=funcionarios.csv'
    
    writer = csv.writer(response)
    
    writer.writerow(['ID', 'Nome', 'Data de Nascimento', 'E-mail', 'Remuneração'])
    funcionarios = Funcionario.objects.all()
    
    for funcionario in funcionarios:
        writer.writerow([funcionario.id, funcionario.nome, funcionario.data_nascimento, funcionario.email, funcionario.remuneracao])
    
    return response
