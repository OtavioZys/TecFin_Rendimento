from django.db import models

class Prorrogacao(models.Model):
    id = models.BigIntegerField(primary_key=True)
    statusDaContratacao = models.CharField(max_length=50, blank=True, null=True)
    cpfCnpj = models.CharField(max_length=14, blank=True, null=True)
    linhaDigitavelSgv = models.CharField(max_length=150, blank=True, null=True)
    nossoNumero = models.BigIntegerField(blank=True, null=True)
    linhaDigitavelProrrogacao = models.CharField(max_length=250, blank=True, null=True)
    dataContratacao = models.DateTimeField(blank=True, null=True)
    dataPrimeiraContratacao = models.DateField(blank=True, null=True)
    clienteIdSgv = models.BigIntegerField(blank=True, null=True)
    clienteDaContratacao = models.CharField(max_length=50, blank=True, null=True)
    scoreCliente = models.IntegerField(blank=True, null=True)
    nomeEmpresa = models.CharField(max_length=50, blank=True, null=True)
    cobrancaId = models.BigIntegerField(blank=True, null=True)
    valorBoletoSgv = models.DecimalField(max_digits=22, decimal_places=2, blank=True, null=True)
    vencimentoBoletoSgv = models.DateField(blank=True, null=True)
    valorBoletoProrrogacao = models.DecimalField(max_digits=22, decimal_places=2, blank=True, null=True)
    valorRepasseGrupoCard = models.DecimalField(max_digits=22, decimal_places=2, blank=True, null=True)
    dataRepasseMoneyGc = models.DateField(blank=True, null=True)
    vencimentoBoletoProrrogacao = models.DateField(blank=True, null=True)
    prazo = models.IntegerField(blank=True, null=True)
    dataPagamentoProrrogacao = models.DateField(blank=True, null=True)
    dia_consulta = models.CharField(max_length=150, blank=True, null=True)
    intervalo_consulta = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tecfin_prorrogacoes'
        verbose_name = 'Prorrogações da TecFin'
        verbose_name_plural = 'Prorrogações da TecFin'

# Create your models here.
