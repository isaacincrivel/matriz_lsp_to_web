import random

estados = ['Goiás', 'Pará', 'Piauí', 'Maranhão']
tensoes = ['13,8kV', '34,5kV', '23,1kV', 'BT']
locais = ['Rural', 'Urbano']
tiposRede = ['Construção MT', 'Construção BT', 'Retirada', 'Melhoria Rede MT', 'Melhoria Rede BT', 'Melhoria de Rede MT BT', 'Trifaseamento MT']
fases = ['Monofasico MRT', 'Monofasico', 'Bifasico com Neutro', 'Bifásico sem neutro', 'Trifásico com neutro', 'Trifásico sem neutro']
cabos = ['1/0CAA', '4/0CAA', '4CAA', 'Space 185', 'Space 150', 'Space 50', 'BT35mm', 'BT70mm', 'BT120mm']
posteDerivacao = ['Implantar', 'Existente']
tiposPoste = ['N3', 'DT10/300', 'PDT10/300', 'N1', 'N2']

output = "// Dados da tabela - Array fixo com 150 linhas editáveis\n"
output += "// Edite cada linha individualmente conforme necessário\n\n"
output += "const dadosTabela = [\n"

for i in range(1, 151):
    output += f"    // Linha {i}\n"
    output += "    {\n"
    output += f"        sequencia: {i},\n"
    output += f"        posteDerivacao: '{random.choice(posteDerivacao)}',\n"
    output += f"        estado: '{random.choice(estados)}',\n"
    output += f"        tensao: '{random.choice(tensoes)}',\n"
    output += f"        local: '{random.choice(locais)}',\n"
    output += f"        tipoRede: '{random.choice(tiposRede)}',\n"
    output += f"        quantidadeFases: '{random.choice(fases)}',\n"
    output += f"        cabo: '{random.choice(cabos)}',\n"
    output += f"        numeroModulo: {random.randint(1, 100)},\n"
    mod = random.randint(1, 50)
    output += f"        descricaoModulo: 'Módulo {mod}',\n"
    output += f"        numeroPoste: {random.randint(100000, 999999)},\n"
    output += f"        tipoPoste: '{random.choice(tiposPoste)}',\n"
    lat = f"{-17 + random.random() * 5:.6f}"
    lon = f"{-49 + random.random() * 5:.6f}"
    output += f"        latitude: '{lat}',\n"
    output += f"        longitude: '{lon}',\n"
    output += f"        observacoes: 'Observação {i} - Dados de exemplo'\n"
    if i < 150:
        output += "    },\n\n"
    else:
        output += "    }\n"

output += "];\n"

with open('tabela-data.js', 'w', encoding='utf-8') as f:
    f.write(output)

print("Arquivo gerado com sucesso!")

