from django.db import models

from usuarios.models import Users

TIPO_CHOICES = [
    ("ABS", "ABS AUTO BOMBA SALVAMENTO"),
    ("ABSR", "ABSR AUTO BOMBA SALVAMENTO E RESGATE"),
    ("ABT", "ABT AUTO BOMBA TANQUE"),
    ("ABTS", "ABTS AUTO BOMBA TANQUE SALVAMENTO"),
    ("ACA", "ACA AUTO COMANDO DE AREA"),
    ("ACE", "ACE AUTO CAÇAMBA ELEVATÓRIA"),
    ("AE", "AE AUTOESCOLA"),
    ("AEM", "AEM AUTO ESCADA MECANICA"),
    ("AJ", "AJ AUTO JAMANTA"),
    ("AMA", "AMA AMBULANCIA ADMINISTRATIVA"),
    ("APE", "APE AUTO PLATAFORMA ESCADA"),
    ("APP", "APP AUTO PRODUTOS PERIGOSOS"),
    ("APV", "APV AUTO PATRULHA DE VISTORIA"),
    ("APV", "APV AUTO PREVENCAO E VISTORIA"),
    ("AR", "AR AUTO REBOQUE"),
    ("ASF", "ASF AUTO SALVAMENTO FLORESTAL"),
    ("ASL", "ASL AUTO SALVAMENTO LEVE"),
    ("ASM", "ASM AUTO SALVAMENTO MEDIO"),
    ("ASP", "ASP AUTO SALVAMENTO PESADO"),
    ("ATB", "ATB AUTO TANQUE BOMBA"),
    ("AUTO", "AUTO ATENDIMENTO DOMICILIAR TERAPEUTICO"),
    ("MB", "MB MOTO DE BOMBEIRO"),
    ("MO", "MO MOTO OPERACIONAL"),
    ("NÃO", "NÃO INFORMADO"),
    ("TAN", "TAN TRANSPORTE DE ANIMAIS"),
    ("TC", "TC TRANSPORTE DE CARGA"),
    ("TCA", "TCA TRANSPORTE DE COMBUSTIVEL DE AVIACAO"),
    ("TCE", "TCE TRANSPORTE DE COORDENACAO ESTRATEGICA"),
    ("TE", "TE TRANSPORTE ESPECIALIZADO"),
    ("TLP", "TLP TRANSPORTE LEVE DE PESSOAL"),
    ("TP", "TP TRANSPORTE DE PESSOAL"),
    ("TPP", "TPP TRANSPORTE PESADO DE PESSOAL"),
    ("TR", "TR TRANSPORTE DE REPRESENTACOES"),
    ("UR", "UR UNIDADE DE RESGATE"),
    ("VA", "VA VIATURAS ADMINISTRATIVAS"),
    ("VRM", "VRM VEICULO DE ROTA DE MANUTENCA")
]

TEMA_CHOICES = [
    ("DA", "DIFICULDADE DE ACESSO"),
    ("NRC", "NAO SEI REALIZAR O CADASTRO"),
    ("ED", "ERRO NOS DADOS"),
    ("NRD", "NÃO RECEBO MAIS DADOS"),
    ("NQD", "NÃO QUERO MAIS RECEBER DADOS"),
    ("TT", "TROQUEI DE TITULAR"),
    ("OT", "OUTRO"),

]


class Categorias(models.Model):
    nome = models.CharField(max_length=80)

    def __str__(self):
        return self.nome


class Titular(models.Model):
    categoria = models.ForeignKey(
        Categorias, on_delete=models.SET_NULL, null=True)
    nome = models.CharField(max_length=100)
    ddd = models.CharField(max_length=2, null=True, blank=True)
    telfnumber = models.CharField(
        max_length=250, null=True, blank=True)
    id_chat_d = models.CharField(
        max_length=30, default="",  null=True, blank=True)
    only_assec = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Assessor(models.Model):

    nome_assessor = models.CharField(max_length=100)
    id_chat_a = models.CharField(max_length=30)
    ddd = models.CharField(max_length=2, null=True, blank=True)
    telfnumber = models.CharField(
        max_length=300, unique=True, null=True, blank=True)
    titular = models.ForeignKey(Titular, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nome_assessor


class Viatura(models.Model):
    tipo = models.CharField(max_length=30,
                            choices=TIPO_CHOICES,
                            default="UR")
    placa = models.CharField(max_length=15)
    titular = models.ForeignKey(Titular, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.placa


class RegistroDisparo(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    disparador = models.CharField(max_length=100, null=True, blank=True)
    titular = models.CharField(max_length=100, null=True, blank=True)
    assessor = models.CharField(max_length=100, null=True, blank=True)
    viatura = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.disparador


class AjudaManager(models.Model):
    nome = models.CharField(max_length=100, blank=True)
    id_user = models.CharField(max_length=30, blank=True)
    categoria = models.CharField(max_length=100, blank=True)
    tema = models.CharField(max_length=50,
                            choices=TEMA_CHOICES)
    telefone = models.CharField(
        max_length=300, unique=True, null=True, blank=True)
    mensagem = models.CharField(max_length=900, blank=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
