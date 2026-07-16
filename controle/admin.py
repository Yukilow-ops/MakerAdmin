from django.contrib import admin
from .models import Equipamento, ItemEquipamento, Reserva

# Permite cadastrar e alterar os aparelhos individuais diretamente dentro da página do Grupo
class ItemEquipamentoInline(admin.TabularInline):
    model = ItemEquipamento
    extra = 1  # Deixa uma linha em branco por padrão para adicionar novos facilmente

@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'quantidade_total', 'quantidade_disponivel')
    search_fields = ('nome',)
    inlines = [ItemEquipamentoInline]  # Acopla a lista de itens físicos aqui dentro!

@admin.register(ItemEquipamento)
class ItemEquipamentoAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'equipamento_pai', 'numero_serie', 'status')
    list_filter = ('status', 'equipamento_pai')
    search_fields = ('identificador', 'numero_serie')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('equipamento', 'quantidade_solicitada', 'usuario', 'data_uso', 'aulas', 'status')
    list_filter = ('status', 'data_uso', 'aulas')
    search_fields = ('equipamento__nome', 'usuario__username')