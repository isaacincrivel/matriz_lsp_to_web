# Aplicação Web - Caminhamento de Rede

Aplicação web standalone para coleta de dados de caminhamento de rede elétrica no campo.

## 🚀 Como Usar

### Abrir a Aplicação

1. Abra o arquivo `index.html` em um navegador moderno (Chrome, Firefox, Edge, Safari)
2. A aplicação funciona offline após o primeiro carregamento

### Funcionalidades Principais

#### 1. Importar KML
- Clique no botão **"Importar"** no header
- Selecione um arquivo KML
- Os pontos e linhas serão exibidos no mapa
- Marcadores serão criados automaticamente para cada vértice

#### 2. Adicionar Poste Manualmente
- **Desktop**: Clique no botão **"Adicionar Poste"** na sidebar
- **Mobile**: Toque no botão verde com ícone **"+"** (FAB)
- Clique no mapa para posicionar o poste
- Preencha o formulário com os dados

#### 3. Desenhar Linha
- Clique no botão **"Desenhar"** na toolbar (desktop) ou FAB (mobile)
- Clique no mapa para começar a desenhar
- Clique novamente para adicionar pontos
- Duplo clique para finalizar
- Marcadores serão criados automaticamente nos vértices

#### 4. Editar Poste
- Clique em um marcador no mapa, ou
- Clique em um poste na lista da sidebar
- Preencha os dados nos tabs (Implantar, Existente, Retirar, Deslocar)
- Clique em **"Salvar"**

#### 5. Exportar KML
- Clique no botão **"Exportar"** no header
- O arquivo será baixado automaticamente

#### 6. Gerar CSV
- Clique no botão **"CSV"** no header
- O arquivo `matriz_teste.csv` será gerado no formato compatível
- Formato: separador `;`, decimal `,`

## 📱 Uso no Celular

A aplicação é totalmente responsiva e otimizada para uso em campo:

- **Geolocalização**: A aplicação tenta obter sua localização automaticamente
- **Touch Gestures**: Suporte completo a gestos de toque
- **Menu Lateral**: Deslize da esquerda ou toque no menu para abrir
- **Botões Flutuantes**: Use os botões flutuantes no canto inferior direito
- **Formulários**: Abrem em tela cheia para facilitar o preenchimento

## 📋 Estrutura de Dados

### Status do Poste

Cada poste pode ter até 4 status diferentes:

1. **Implantar**: Dados do poste a ser implantado
2. **Existente**: Dados do poste existente (com número do poste)
3. **Retirar**: Dados do poste a ser retirado
4. **Deslocar**: Dados do poste a ser deslocado

### Campos Principais

- **Sequência**: Número sequencial do poste (gerado automaticamente)
- **Coordenadas**: Latitude e Longitude (obtidas do mapa)
- **Tipo de Poste**: Ex: N3, DT10/300, PDT10/300
- **Estruturas MT**: NV1, NV2, NV3
- **Estruturas BT**: NV1, NV2
- **Base Concreto**: Ex: BC
- **Estai Âncora**: Ex: 1EA
- **Rotação Poste**: Ex: topo1
- **Módulo**: Ex: mt7
- **Município**: Ex: Goiania

## 💾 Armazenamento

Os dados são salvos automaticamente no **localStorage** do navegador:

- Dados persistem entre sessões
- Funciona offline
- Limpe o cache do navegador para resetar os dados

## 🌐 Colocar Online

### Opção 1: Servidor Web Simples
1. Faça upload da pasta `web_app` para seu servidor
2. Acesse via navegador: `http://seuservidor.com/web_app/index.html`

### Opção 2: GitHub Pages
1. Crie um repositório no GitHub
2. Faça upload dos arquivos
3. Ative GitHub Pages nas configurações
4. Acesse: `https://seuusuario.github.io/repositorio/`

### Opção 3: Netlify/Vercel
1. Faça upload da pasta `web_app`
2. Deploy automático
3. URL gerada automaticamente

## 🔧 Tecnologias Utilizadas

- **Leaflet 1.9.4**: Biblioteca de mapas
- **Leaflet.draw**: Desenho no mapa
- **PapaParse**: Parsing de CSV
- **FileSaver.js**: Download de arquivos
- **Bootstrap Icons**: Ícones

## 📝 Formato do CSV Gerado

O CSV gerado é compatível com o formato `matriz_teste.csv`:

```csv
sequencia;status;lat;long;num_poste;tipo_poste;estru_mt_nv1;...
0;Implantar;-17,041935;-49,224541;;;N3;...
0;Existente;;;46464546;DT10/300;N1;...
```

- Separador: `;` (ponto e vírgula)
- Decimal: `,` (vírgula)
- Encoding: UTF-8 com BOM

## 🐛 Solução de Problemas

### Mapa não carrega
- Verifique sua conexão com internet (para carregar tiles)
- Tente recarregar a página

### KML não importa
- Verifique se o arquivo é um KML válido
- Certifique-se de que o arquivo contém coordenadas

### CSV não gera
- Verifique se há pelo menos um poste cadastrado
- Certifique-se de que pelo menos um status está preenchido

### Dados não salvam
- Verifique se o navegador permite localStorage
- Tente usar modo anônimo/privado

## 📞 Suporte

Para problemas ou dúvidas, consulte o código-fonte ou entre em contato com o desenvolvedor.

