from django.contrib import admin
from .models import Oferta, Candidato, Aluno, ProfessorRecrutador

admin.site.register(Oferta)
admin.site.register(Candidato)
admin.site.register(Aluno)
admin.site.register(ProfessorRecrutador)