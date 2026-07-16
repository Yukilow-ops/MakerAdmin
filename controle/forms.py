from django import forms
from .models import Reserva, Equipamento
from django.core.exceptions import ValidationError
from django.db.models import Sum

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['equipamento', 'data_uso', 'aulas', 'quantidade_solicitada', 'motivo']
        widgets = {
            'data_uso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'aulas': forms.Select(attrs={'class': 'form-control'}),
            'quantidade_solicitada': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        equipamento = cleaned_data.get('equipamento')
        data_uso = cleaned_data.get('data_uso')
        aulas = cleaned_data.get('aulas')
        qtd_solicitada = cleaned_data.get('quantidade_solicitada')

        if equipamento and data_uso and aulas and qtd_solicitada:
            total_disponivel_fisico = equipamento.quantidade_disponivel

            # 1. Verifica se o pedido não supera o estoque ativo de equipamentos funcionando
            if qtd_solicitada > total_disponivel_fisico:
                raise ValidationError(
                    f"Quantidade indisponível. Temos apenas {total_disponivel_fisico} unidades de {equipamento.nome} funcionando atualmente."
                )

            # 2. Soma as quantidades que já estão reservadas para ESSE DIA e ESSA AULA
            reservas_existentes = Reserva.objects.filter(
                equipamento=equipamento,
                data_uso=data_uso,
                aulas=aulas,
                status__in=['pendente', 'em_uso']
            )

            if self.instance and self.instance.pk:
                reservas_existentes = reservas_existentes.exclude(pk=self.instance.pk)

            total_reservado = reservas_existentes.aggregate(Sum('quantidade_solicitada'))['quantidade_solicitada__sum'] or 0
            
            saldo_restante = total_disponivel_fisico - total_reservado

            # 3. Se estourar a capacidade física disponível naquele horário, barra!
            if total_reservado + qtd_solicitada > total_disponivel_fisico:
                raise ValidationError(
                    f"Limite de estoque excedido para esta aula! Restam apenas {saldo_restante} unidades de {equipamento.nome} livres para a data {data_uso.strftime('%d/%m/%Y')}."
                )

        return cleaned_data