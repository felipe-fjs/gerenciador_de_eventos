from flask import Blueprint

colab_route = Blueprint('colab', __name__)

"""
    * /nome_evento/colab (get): exibe os colaboradores do evento
    * /nome_evento/colab/novo (get e posto): registra novo colaborador
    * /nome_evento/colab/edit (get e put): edita um colaborador
    * /nome_evento/colab/delete (delete): remove um colaborador

    * /nome_evento/fiscal (get): exibe os fiscais do evento, divididos por área de atuação
    * /nome_evento/fiscal/novo (get e post): registra novo fiscal, que já é um colaborador
    * /nome_evento/fiscal/edit (get e put): edita um fiscal
    * /nome_evento/fiscal/delete (delete): remove um fiscal

    * /nome_evento/sub_evento/colab/area/edit (get e put): edita quais colaboradores da area estarão no subevento
    * /nome_evento/sub_evento/colab/area/delete (delete): remove um colaborador de um subevento 
    
"""