from django.core.management.base import BaseCommand
from controle.models import atualizar_status_equipamentos_por_horario

class Command(BaseCommand):
    help = 'Atualiza o status dos equipamentos com base no horário das aulas do dia'

    def handle(self, *args, **options):
        atualizar_status_equipamentos_por_horario()
        self.stdout.write(self.style.SUCCESS('Status dos equipamentos atualizados com sucesso!'))