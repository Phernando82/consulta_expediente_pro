import sys
import os
from cx_Freeze import setup, Executable

# Definir o que deve ser incluido na pasta final
arquivos = ['datos.csv', 'buscar.py', 'chave.py','site_url.py']
# Definir a saida de arquivos
configuracao = Executable(
    script='consulta_expediente.py',
    icon='espana.ico'
)
# Configurar o executável
setup(
    name='Consulta Expediente',
    version='1.0',
    description='Busca los expedientes de nacionalidad española',
    author='Tokyme Technologies',
    options={'build_exe':{
        'include_files': arquivos,
        'include_msvcr': True,     # para rodar no Windows sem instalar python

    }},
    executables=[configuracao]
)