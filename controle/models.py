from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 1. O GRUPO / MODELO DO EQUIPAMENTO (O "PAI")
class Equipamento(models.Model):
    nome = models.CharField(max_length=100, unique=True)  # Ex: "Notebook Positivo"

    # Propriedade inteligente que conta quantos aparelhos deste modelo existem no total
    @property
    def quantidade_total(self):
        return self.itens.count()

    # Propriedade inteligente que conta quantos estão realmente disponíveis (fora de manutenção)
    @property
    def quantidade_disponivel(self):
        return self.itens.filter(status='disponivel').count()

    def __str__(self):
        return f"{self.nome} (Disponíveis: {self.quantidade_disponivel}/{self.quantidade_total})"


# 2. O APARELHO FÍSICO INDIVIDUAL (O "FILHO")
class ItemEquipamento(models.Model):
    status_choices = [
        ('disponivel', 'Disponível'),
        ('manutencao', 'Em Manutenção'),
    ]
    
    # Vincula este item físico ao seu respectivo grupo/modelo
    equipamento_pai = models.ForeignKey(Equipamento, on_delete=models.CASCADE, related_name='itens')
    identificador = models.CharField(max_length=50, help_text="Ex: Notebook 01, Projetor A")
    numero_serie = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices, default='disponivel')

    def __str__(self):
        return f"{self.equipamento_pai.nome} - {self.identificador} ({self.get_status_display()})"


# 3. A RESERVA
class Reserva(models.Model): 
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_uso', 'Em Uso'),
        ('cancelada', 'Cancelada'),
        ('concluida', 'Concluída'),
    ]

    AULAS_CHOICES = [
        ('1_aula', '1ª Aula (07:00 - 07:45)'),
        ('2_aula', '2ª Aula (07:45 - 08:30)'),
        ('3_aula', '3ª Aula (08:30 - 09:15)'),
        ('4_aula', '4ª Aula (09:15 - 10:00)'),
        ('5_aula', '5ª Aula (10:15 - 11:00)'),
        ('6_aula', '6ª Aula (11:00 - 11:45)'),
        ('7_aula', '7ª Aula (11:45 - 12:30)'),
        ('8_aula', '8ª Aula (13:30 - 14:15)'),
        ('9_aula', '9ª Aula (14:15 - 15:00)'),
        ('10_aula', '10ª Aula (15:00 - 15:45)'),
        ('1_2_aula', '1ª e 2ª Aula'),
        ('2_3_aula', '2ª e 3ª Aula'),
        ('3_4_aula', '3ª e 4ª Aula'),
        ('4_5_aula', '4ª e 5ª Aula'),
        ('5_6_aula', '5ª e 6ª Aula'),
        ('6_7_aula', '6ª e 7ª Aula'),
        ('7_8_aula', '7ª e 8ª Aula'),
        ('8_9_aula', '8ª e 9ª Aula'),
        ('9_10_aula', '9ª e 10ª Aula'),
    ]

    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_reserva = models.DateTimeField(auto_now_add=True)
    data_uso = models.DateField(default=timezone.now)
    aulas = models.CharField(max_length=50, choices=AULAS_CHOICES, default='1_aula')
    quantidade_solicitada = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    motivo = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quantidade_solicitada}x {self.equipamento.nome} para {self.data_uso} ({self.get_aulas_display()})"