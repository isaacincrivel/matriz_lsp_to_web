// Dados da tabela - Array fixo com 150 linhas editáveis
// Edite cada linha individualmente conforme necessário

const dadosTabela = [
    // Linha 1
    {
        sequencia: 1,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'Space 185',
        numeroModulo: 45,
        descricaoModulo: 'Módulo 5',
        numeroPoste: 313972,
        tipoPoste: 'N2',
        latitude: '-14.609719',
        longitude: '-45.287226',
        observacoes: 'Observação 1 - Dados de exemplo'
    },

    // Linha 2
    {
        sequencia: 2,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '1/0CAA',
        numeroModulo: 75,
        descricaoModulo: 'Módulo 12',
        numeroPoste: 516449,
        tipoPoste: 'N2',
        latitude: '-15.445409',
        longitude: '-44.268857',
        observacoes: 'Observação 2 - Dados de exemplo'
    },

    // Linha 3
    {
        sequencia: 3,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'BT120mm',
        numeroModulo: 29,
        descricaoModulo: 'Módulo 26',
        numeroPoste: 963845,
        tipoPoste: 'N1',
        latitude: '-15.373092',
        longitude: '-44.690608',
        observacoes: 'Observação 3 - Dados de exemplo'
    },

    // Linha 4
    {
        sequencia: 4,
        posteDerivacao: 'ccExistente',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Monofasico',
        cabo: '1/0CAA',
        numeroModulo: 9,
        descricaoModulo: 'Módulo 26',
        numeroPoste: 429531,
        tipoPoste: 'N2',
        latitude: '-14.482075',
        longitude: '-47.087116',
        observacoes: 'Observação 4 - Dados de exemplo'
    },

    // Linha 5
    {
        sequencia: 5,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'Space 185',
        numeroModulo: 9,
        descricaoModulo: 'Módulo 13',
        numeroPoste: 143918,
        tipoPoste: 'DT10/300',
        latitude: '-15.016037',
        longitude: '-47.831320',
        observacoes: 'Observação 5 - Dados de exemplo'
    },

    // Linha 6
    {
        sequencia: 6,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'Space 185',
        numeroModulo: 67,
        descricaoModulo: 'Módulo 22',
        numeroPoste: 145869,
        tipoPoste: 'N2',
        latitude: '-15.762466',
        longitude: '-44.984405',
        observacoes: 'Observação 6 - Dados de exemplo'
    },

    // Linha 7
    {
        sequencia: 7,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT70mm',
        numeroModulo: 81,
        descricaoModulo: 'Módulo 32',
        numeroPoste: 454517,
        tipoPoste: 'DT10/300',
        latitude: '-16.898058',
        longitude: '-44.073602',
        observacoes: 'Observação 7 - Dados de exemplo'
    },

    // Linha 8
    {
        sequencia: 8,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 50',
        numeroModulo: 89,
        descricaoModulo: 'Módulo 37',
        numeroPoste: 833603,
        tipoPoste: 'N2',
        latitude: '-12.571423',
        longitude: '-48.696480',
        observacoes: 'Observação 8 - Dados de exemplo'
    },

    // Linha 9
    {
        sequencia: 9,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'Space 185',
        numeroModulo: 60,
        descricaoModulo: 'Módulo 20',
        numeroPoste: 346841,
        tipoPoste: 'N1',
        latitude: '-12.765928',
        longitude: '-47.947487',
        observacoes: 'Observação 9 - Dados de exemplo'
    },

    // Linha 10
    {
        sequencia: 10,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT120mm',
        numeroModulo: 51,
        descricaoModulo: 'Módulo 13',
        numeroPoste: 529565,
        tipoPoste: 'N3',
        latitude: '-14.198818',
        longitude: '-48.319943',
        observacoes: 'Observação 10 - Dados de exemplo'
    },

    // Linha 11
    {
        sequencia: 11,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT120mm',
        numeroModulo: 53,
        descricaoModulo: 'Módulo 9',
        numeroPoste: 210834,
        tipoPoste: 'PDT10/300',
        latitude: '-15.503418',
        longitude: '-45.402983',
        observacoes: 'Observação 11 - Dados de exemplo'
    },

    // Linha 12
    {
        sequencia: 12,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT70mm',
        numeroModulo: 22,
        descricaoModulo: 'Módulo 46',
        numeroPoste: 822095,
        tipoPoste: 'N1',
        latitude: '-13.728495',
        longitude: '-44.174196',
        observacoes: 'Observação 12 - Dados de exemplo'
    },

    // Linha 13
    {
        sequencia: 13,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT35mm',
        numeroModulo: 96,
        descricaoModulo: 'Módulo 22',
        numeroPoste: 173154,
        tipoPoste: 'PDT10/300',
        latitude: '-16.392526',
        longitude: '-47.806366',
        observacoes: 'Observação 13 - Dados de exemplo'
    },

    // Linha 14
    {
        sequencia: 14,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: '4/0CAA',
        numeroModulo: 12,
        descricaoModulo: 'Módulo 6',
        numeroPoste: 123537,
        tipoPoste: 'N2',
        latitude: '-14.113634',
        longitude: '-48.858616',
        observacoes: 'Observação 14 - Dados de exemplo'
    },

    // Linha 15
    {
        sequencia: 15,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: '1/0CAA',
        numeroModulo: 23,
        descricaoModulo: 'Módulo 11',
        numeroPoste: 556280,
        tipoPoste: 'N2',
        latitude: '-14.591440',
        longitude: '-44.044733',
        observacoes: 'Observação 15 - Dados de exemplo'
    },

    // Linha 16
    {
        sequencia: 16,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Trifásico com neutro',
        cabo: '4/0CAA',
        numeroModulo: 24,
        descricaoModulo: 'Módulo 32',
        numeroPoste: 115516,
        tipoPoste: 'N2',
        latitude: '-12.125149',
        longitude: '-45.472305',
        observacoes: 'Observação 16 - Dados de exemplo'
    },

    // Linha 17
    {
        sequencia: 17,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 150',
        numeroModulo: 8,
        descricaoModulo: 'Módulo 33',
        numeroPoste: 190472,
        tipoPoste: 'N3',
        latitude: '-16.385650',
        longitude: '-44.461164',
        observacoes: 'Observação 17 - Dados de exemplo'
    },

    // Linha 18
    {
        sequencia: 18,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT120mm',
        numeroModulo: 29,
        descricaoModulo: 'Módulo 9',
        numeroPoste: 813358,
        tipoPoste: 'N2',
        latitude: '-16.293436',
        longitude: '-44.625757',
        observacoes: 'Observação 18 - Dados de exemplo'
    },

    // Linha 19
    {
        sequencia: 19,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT120mm',
        numeroModulo: 79,
        descricaoModulo: 'Módulo 33',
        numeroPoste: 375670,
        tipoPoste: 'N3',
        latitude: '-13.280912',
        longitude: '-44.016577',
        observacoes: 'Observação 19 - Dados de exemplo'
    },

    // Linha 20
    {
        sequencia: 20,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'BT70mm',
        numeroModulo: 65,
        descricaoModulo: 'Módulo 31',
        numeroPoste: 883389,
        tipoPoste: 'N2',
        latitude: '-15.218271',
        longitude: '-48.329239',
        observacoes: 'Observação 20 - Dados de exemplo'
    },

    // Linha 21
    {
        sequencia: 21,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT70mm',
        numeroModulo: 71,
        descricaoModulo: 'Módulo 9',
        numeroPoste: 255245,
        tipoPoste: 'N1',
        latitude: '-13.354473',
        longitude: '-46.647655',
        observacoes: 'Observação 21 - Dados de exemplo'
    },

    // Linha 22
    {
        sequencia: 22,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'BT120mm',
        numeroModulo: 38,
        descricaoModulo: 'Módulo 12',
        numeroPoste: 534626,
        tipoPoste: 'N1',
        latitude: '-15.587932',
        longitude: '-44.198018',
        observacoes: 'Observação 22 - Dados de exemplo'
    },

    // Linha 23
    {
        sequencia: 23,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '4/0CAA',
        numeroModulo: 55,
        descricaoModulo: 'Módulo 43',
        numeroPoste: 634176,
        tipoPoste: 'N1',
        latitude: '-14.953558',
        longitude: '-44.561279',
        observacoes: 'Observação 23 - Dados de exemplo'
    },

    // Linha 24
    {
        sequencia: 24,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'Space 150',
        numeroModulo: 17,
        descricaoModulo: 'Módulo 19',
        numeroPoste: 716284,
        tipoPoste: 'PDT10/300',
        latitude: '-16.501888',
        longitude: '-48.315585',
        observacoes: 'Observação 24 - Dados de exemplo'
    },

    // Linha 25
    {
        sequencia: 25,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT70mm',
        numeroModulo: 1,
        descricaoModulo: 'Módulo 16',
        numeroPoste: 461599,
        tipoPoste: 'PDT10/300',
        latitude: '-15.519570',
        longitude: '-48.759959',
        observacoes: 'Observação 25 - Dados de exemplo'
    },

    // Linha 26
    {
        sequencia: 26,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'Space 150',
        numeroModulo: 34,
        descricaoModulo: 'Módulo 12',
        numeroPoste: 363485,
        tipoPoste: 'N2',
        latitude: '-12.578270',
        longitude: '-44.733985',
        observacoes: 'Observação 26 - Dados de exemplo'
    },

    // Linha 27
    {
        sequencia: 27,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'Space 50',
        numeroModulo: 86,
        descricaoModulo: 'Módulo 36',
        numeroPoste: 603989,
        tipoPoste: 'N1',
        latitude: '-14.352993',
        longitude: '-45.922612',
        observacoes: 'Observação 27 - Dados de exemplo'
    },

    // Linha 28
    {
        sequencia: 28,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '1/0CAA',
        numeroModulo: 58,
        descricaoModulo: 'Módulo 5',
        numeroPoste: 603561,
        tipoPoste: 'N2',
        latitude: '-12.682280',
        longitude: '-48.136596',
        observacoes: 'Observação 28 - Dados de exemplo'
    },

    // Linha 29
    {
        sequencia: 29,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '4/0CAA',
        numeroModulo: 14,
        descricaoModulo: 'Módulo 22',
        numeroPoste: 562041,
        tipoPoste: 'DT10/300',
        latitude: '-13.072026',
        longitude: '-44.469739',
        observacoes: 'Observação 29 - Dados de exemplo'
    },

    // Linha 30
    {
        sequencia: 30,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT35mm',
        numeroModulo: 88,
        descricaoModulo: 'Módulo 11',
        numeroPoste: 982479,
        tipoPoste: 'DT10/300',
        latitude: '-15.549191',
        longitude: '-48.867320',
        observacoes: 'Observação 30 - Dados de exemplo'
    },

    // Linha 31
    {
        sequencia: 31,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'Space 50',
        numeroModulo: 97,
        descricaoModulo: 'Módulo 10',
        numeroPoste: 976787,
        tipoPoste: 'DT10/300',
        latitude: '-12.195082',
        longitude: '-44.446377',
        observacoes: 'Observação 31 - Dados de exemplo'
    },

    // Linha 32
    {
        sequencia: 32,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Monofasico',
        cabo: 'BT35mm',
        numeroModulo: 94,
        descricaoModulo: 'Módulo 49',
        numeroPoste: 834438,
        tipoPoste: 'N2',
        latitude: '-13.469545',
        longitude: '-46.513809',
        observacoes: 'Observação 32 - Dados de exemplo'
    },

    // Linha 33
    {
        sequencia: 33,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 150',
        numeroModulo: 17,
        descricaoModulo: 'Módulo 24',
        numeroPoste: 700306,
        tipoPoste: 'PDT10/300',
        latitude: '-14.236323',
        longitude: '-46.997731',
        observacoes: 'Observação 33 - Dados de exemplo'
    },

    // Linha 34
    {
        sequencia: 34,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'BT120mm',
        numeroModulo: 95,
        descricaoModulo: 'Módulo 36',
        numeroPoste: 813776,
        tipoPoste: 'N1',
        latitude: '-13.668780',
        longitude: '-47.147156',
        observacoes: 'Observação 34 - Dados de exemplo'
    },

    // Linha 35
    {
        sequencia: 35,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT70mm',
        numeroModulo: 12,
        descricaoModulo: 'Módulo 23',
        numeroPoste: 620556,
        tipoPoste: 'N2',
        latitude: '-15.156099',
        longitude: '-46.347017',
        observacoes: 'Observação 35 - Dados de exemplo'
    },

    // Linha 36
    {
        sequencia: 36,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: '4CAA',
        numeroModulo: 78,
        descricaoModulo: 'Módulo 47',
        numeroPoste: 657573,
        tipoPoste: 'PDT10/300',
        latitude: '-13.239244',
        longitude: '-45.240887',
        observacoes: 'Observação 36 - Dados de exemplo'
    },

    // Linha 37
    {
        sequencia: 37,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'Space 50',
        numeroModulo: 35,
        descricaoModulo: 'Módulo 26',
        numeroPoste: 336999,
        tipoPoste: 'N1',
        latitude: '-15.612807',
        longitude: '-47.865378',
        observacoes: 'Observação 37 - Dados de exemplo'
    },

    // Linha 38
    {
        sequencia: 38,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Monofasico',
        cabo: '4CAA',
        numeroModulo: 32,
        descricaoModulo: 'Módulo 50',
        numeroPoste: 957800,
        tipoPoste: 'PDT10/300',
        latitude: '-14.428558',
        longitude: '-48.881044',
        observacoes: 'Observação 38 - Dados de exemplo'
    },

    // Linha 39
    {
        sequencia: 39,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'Space 150',
        numeroModulo: 88,
        descricaoModulo: 'Módulo 29',
        numeroPoste: 574990,
        tipoPoste: 'N1',
        latitude: '-16.839643',
        longitude: '-46.219037',
        observacoes: 'Observação 39 - Dados de exemplo'
    },

    // Linha 40
    {
        sequencia: 40,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'Space 150',
        numeroModulo: 14,
        descricaoModulo: 'Módulo 3',
        numeroPoste: 473514,
        tipoPoste: 'N1',
        latitude: '-14.312699',
        longitude: '-45.194073',
        observacoes: 'Observação 40 - Dados de exemplo'
    },

    // Linha 41
    {
        sequencia: 41,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'Space 185',
        numeroModulo: 41,
        descricaoModulo: 'Módulo 43',
        numeroPoste: 403584,
        tipoPoste: 'N3',
        latitude: '-14.596863',
        longitude: '-48.053469',
        observacoes: 'Observação 41 - Dados de exemplo'
    },

    // Linha 42
    {
        sequencia: 42,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: '4/0CAA',
        numeroModulo: 78,
        descricaoModulo: 'Módulo 27',
        numeroPoste: 806722,
        tipoPoste: 'N3',
        latitude: '-14.902993',
        longitude: '-44.276803',
        observacoes: 'Observação 42 - Dados de exemplo'
    },

    // Linha 43
    {
        sequencia: 43,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: '1/0CAA',
        numeroModulo: 28,
        descricaoModulo: 'Módulo 18',
        numeroPoste: 191911,
        tipoPoste: 'DT10/300',
        latitude: '-12.164971',
        longitude: '-46.001347',
        observacoes: 'Observação 43 - Dados de exemplo'
    },

    // Linha 44
    {
        sequencia: 44,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: '4CAA',
        numeroModulo: 2,
        descricaoModulo: 'Módulo 16',
        numeroPoste: 106099,
        tipoPoste: 'N1',
        latitude: '-16.296360',
        longitude: '-47.816365',
        observacoes: 'Observação 44 - Dados de exemplo'
    },

    // Linha 45
    {
        sequencia: 45,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 50',
        numeroModulo: 93,
        descricaoModulo: 'Módulo 36',
        numeroPoste: 833865,
        tipoPoste: 'N3',
        latitude: '-15.908304',
        longitude: '-47.980028',
        observacoes: 'Observação 45 - Dados de exemplo'
    },

    // Linha 46
    {
        sequencia: 46,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 185',
        numeroModulo: 16,
        descricaoModulo: 'Módulo 49',
        numeroPoste: 134018,
        tipoPoste: 'N3',
        latitude: '-14.417839',
        longitude: '-48.185407',
        observacoes: 'Observação 46 - Dados de exemplo'
    },

    // Linha 47
    {
        sequencia: 47,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'Space 150',
        numeroModulo: 77,
        descricaoModulo: 'Módulo 3',
        numeroPoste: 444030,
        tipoPoste: 'N1',
        latitude: '-16.552044',
        longitude: '-48.774284',
        observacoes: 'Observação 47 - Dados de exemplo'
    },

    // Linha 48
    {
        sequencia: 48,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Monofasico MRT',
        cabo: '1/0CAA',
        numeroModulo: 72,
        descricaoModulo: 'Módulo 14',
        numeroPoste: 364981,
        tipoPoste: 'DT10/300',
        latitude: '-13.678524',
        longitude: '-47.906612',
        observacoes: 'Observação 48 - Dados de exemplo'
    },

    // Linha 49
    {
        sequencia: 49,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'Space 50',
        numeroModulo: 49,
        descricaoModulo: 'Módulo 3',
        numeroPoste: 598467,
        tipoPoste: 'PDT10/300',
        latitude: '-14.712401',
        longitude: '-47.405106',
        observacoes: 'Observação 49 - Dados de exemplo'
    },

    // Linha 50
    {
        sequencia: 50,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'Space 50',
        numeroModulo: 36,
        descricaoModulo: 'Módulo 22',
        numeroPoste: 982546,
        tipoPoste: 'N3',
        latitude: '-16.245955',
        longitude: '-46.575645',
        observacoes: 'Observação 50 - Dados de exemplo'
    },

    // Linha 51
    {
        sequencia: 51,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico',
        cabo: '1/0CAA',
        numeroModulo: 51,
        descricaoModulo: 'Módulo 18',
        numeroPoste: 552496,
        tipoPoste: 'N3',
        latitude: '-13.041715',
        longitude: '-48.557839',
        observacoes: 'Observação 51 - Dados de exemplo'
    },

    // Linha 52
    {
        sequencia: 52,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: '1/0CAA',
        numeroModulo: 42,
        descricaoModulo: 'Módulo 35',
        numeroPoste: 857275,
        tipoPoste: 'N3',
        latitude: '-14.048376',
        longitude: '-48.562754',
        observacoes: 'Observação 52 - Dados de exemplo'
    },

    // Linha 53
    {
        sequencia: 53,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'Space 150',
        numeroModulo: 57,
        descricaoModulo: 'Módulo 36',
        numeroPoste: 419478,
        tipoPoste: 'N2',
        latitude: '-12.256374',
        longitude: '-47.455929',
        observacoes: 'Observação 53 - Dados de exemplo'
    },

    // Linha 54
    {
        sequencia: 54,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 185',
        numeroModulo: 43,
        descricaoModulo: 'Módulo 17',
        numeroPoste: 631035,
        tipoPoste: 'PDT10/300',
        latitude: '-16.826619',
        longitude: '-45.935981',
        observacoes: 'Observação 54 - Dados de exemplo'
    },

    // Linha 55
    {
        sequencia: 55,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: '4CAA',
        numeroModulo: 34,
        descricaoModulo: 'Módulo 34',
        numeroPoste: 517002,
        tipoPoste: 'N2',
        latitude: '-12.152681',
        longitude: '-48.727572',
        observacoes: 'Observação 55 - Dados de exemplo'
    },

    // Linha 56
    {
        sequencia: 56,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'Space 150',
        numeroModulo: 31,
        descricaoModulo: 'Módulo 30',
        numeroPoste: 810518,
        tipoPoste: 'PDT10/300',
        latitude: '-14.096719',
        longitude: '-44.867335',
        observacoes: 'Observação 56 - Dados de exemplo'
    },

    // Linha 57
    {
        sequencia: 57,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT120mm',
        numeroModulo: 60,
        descricaoModulo: 'Módulo 35',
        numeroPoste: 460449,
        tipoPoste: 'PDT10/300',
        latitude: '-16.924849',
        longitude: '-47.340318',
        observacoes: 'Observação 57 - Dados de exemplo'
    },

    // Linha 58
    {
        sequencia: 58,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 150',
        numeroModulo: 22,
        descricaoModulo: 'Módulo 32',
        numeroPoste: 563422,
        tipoPoste: 'N3',
        latitude: '-16.587263',
        longitude: '-47.640668',
        observacoes: 'Observação 58 - Dados de exemplo'
    },

    // Linha 59
    {
        sequencia: 59,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'BT120mm',
        numeroModulo: 48,
        descricaoModulo: 'Módulo 9',
        numeroPoste: 827492,
        tipoPoste: 'N2',
        latitude: '-16.386321',
        longitude: '-44.973409',
        observacoes: 'Observação 59 - Dados de exemplo'
    },

    // Linha 60
    {
        sequencia: 60,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: '1/0CAA',
        numeroModulo: 99,
        descricaoModulo: 'Módulo 38',
        numeroPoste: 814523,
        tipoPoste: 'PDT10/300',
        latitude: '-14.061093',
        longitude: '-45.424022',
        observacoes: 'Observação 60 - Dados de exemplo'
    },

    // Linha 61
    {
        sequencia: 61,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: '4/0CAA',
        numeroModulo: 56,
        descricaoModulo: 'Módulo 15',
        numeroPoste: 753154,
        tipoPoste: 'DT10/300',
        latitude: '-13.700105',
        longitude: '-47.800529',
        observacoes: 'Observação 61 - Dados de exemplo'
    },

    // Linha 62
    {
        sequencia: 62,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico',
        cabo: '4/0CAA',
        numeroModulo: 76,
        descricaoModulo: 'Módulo 2',
        numeroPoste: 593366,
        tipoPoste: 'DT10/300',
        latitude: '-14.844803',
        longitude: '-44.799238',
        observacoes: 'Observação 62 - Dados de exemplo'
    },

    // Linha 63
    {
        sequencia: 63,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Trifásico com neutro',
        cabo: '1/0CAA',
        numeroModulo: 52,
        descricaoModulo: 'Módulo 25',
        numeroPoste: 243277,
        tipoPoste: 'N1',
        latitude: '-12.468749',
        longitude: '-45.845752',
        observacoes: 'Observação 63 - Dados de exemplo'
    },

    // Linha 64
    {
        sequencia: 64,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'Space 185',
        numeroModulo: 34,
        descricaoModulo: 'Módulo 35',
        numeroPoste: 950066,
        tipoPoste: 'PDT10/300',
        latitude: '-14.857548',
        longitude: '-48.638737',
        observacoes: 'Observação 64 - Dados de exemplo'
    },

    // Linha 65
    {
        sequencia: 65,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT120mm',
        numeroModulo: 87,
        descricaoModulo: 'Módulo 16',
        numeroPoste: 462126,
        tipoPoste: 'N2',
        latitude: '-15.031541',
        longitude: '-48.884078',
        observacoes: 'Observação 65 - Dados de exemplo'
    },

    // Linha 66
    {
        sequencia: 66,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT120mm',
        numeroModulo: 40,
        descricaoModulo: 'Módulo 13',
        numeroPoste: 161291,
        tipoPoste: 'N2',
        latitude: '-14.685205',
        longitude: '-47.082870',
        observacoes: 'Observação 66 - Dados de exemplo'
    },

    // Linha 67
    {
        sequencia: 67,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 50',
        numeroModulo: 72,
        descricaoModulo: 'Módulo 49',
        numeroPoste: 620546,
        tipoPoste: 'N1',
        latitude: '-13.401479',
        longitude: '-48.642758',
        observacoes: 'Observação 67 - Dados de exemplo'
    },

    // Linha 68
    {
        sequencia: 68,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'Space 185',
        numeroModulo: 34,
        descricaoModulo: 'Módulo 27',
        numeroPoste: 363919,
        tipoPoste: 'PDT10/300',
        latitude: '-15.495430',
        longitude: '-48.645988',
        observacoes: 'Observação 68 - Dados de exemplo'
    },

    // Linha 69
    {
        sequencia: 69,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: '4/0CAA',
        numeroModulo: 68,
        descricaoModulo: 'Módulo 28',
        numeroPoste: 418487,
        tipoPoste: 'N2',
        latitude: '-16.371791',
        longitude: '-44.181335',
        observacoes: 'Observação 69 - Dados de exemplo'
    },

    // Linha 70
    {
        sequencia: 70,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: '4CAA',
        numeroModulo: 43,
        descricaoModulo: 'Módulo 43',
        numeroPoste: 682476,
        tipoPoste: 'PDT10/300',
        latitude: '-12.145419',
        longitude: '-44.939021',
        observacoes: 'Observação 70 - Dados de exemplo'
    },

    // Linha 71
    {
        sequencia: 71,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT70mm',
        numeroModulo: 95,
        descricaoModulo: 'Módulo 37',
        numeroPoste: 795228,
        tipoPoste: 'DT10/300',
        latitude: '-16.222646',
        longitude: '-48.184422',
        observacoes: 'Observação 71 - Dados de exemplo'
    },

    // Linha 72
    {
        sequencia: 72,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'Space 50',
        numeroModulo: 53,
        descricaoModulo: 'Módulo 50',
        numeroPoste: 410397,
        tipoPoste: 'DT10/300',
        latitude: '-15.016084',
        longitude: '-44.763253',
        observacoes: 'Observação 72 - Dados de exemplo'
    },

    // Linha 73
    {
        sequencia: 73,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'Space 185',
        numeroModulo: 47,
        descricaoModulo: 'Módulo 29',
        numeroPoste: 479743,
        tipoPoste: 'DT10/300',
        latitude: '-15.728661',
        longitude: '-44.328844',
        observacoes: 'Observação 73 - Dados de exemplo'
    },

    // Linha 74
    {
        sequencia: 74,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 150',
        numeroModulo: 46,
        descricaoModulo: 'Módulo 10',
        numeroPoste: 672949,
        tipoPoste: 'N1',
        latitude: '-16.478829',
        longitude: '-48.964644',
        observacoes: 'Observação 74 - Dados de exemplo'
    },

    // Linha 75
    {
        sequencia: 75,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: '4/0CAA',
        numeroModulo: 6,
        descricaoModulo: 'Módulo 25',
        numeroPoste: 111734,
        tipoPoste: 'N3',
        latitude: '-13.115856',
        longitude: '-46.015883',
        observacoes: 'Observação 75 - Dados de exemplo'
    },

    // Linha 76
    {
        sequencia: 76,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT120mm',
        numeroModulo: 36,
        descricaoModulo: 'Módulo 45',
        numeroPoste: 827571,
        tipoPoste: 'N3',
        latitude: '-13.242731',
        longitude: '-46.178321',
        observacoes: 'Observação 76 - Dados de exemplo'
    },

    // Linha 77
    {
        sequencia: 77,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT70mm',
        numeroModulo: 25,
        descricaoModulo: 'Módulo 18',
        numeroPoste: 486794,
        tipoPoste: 'PDT10/300',
        latitude: '-15.721311',
        longitude: '-44.555015',
        observacoes: 'Observação 77 - Dados de exemplo'
    },

    // Linha 78
    {
        sequencia: 78,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: '4CAA',
        numeroModulo: 7,
        descricaoModulo: 'Módulo 11',
        numeroPoste: 686668,
        tipoPoste: 'N1',
        latitude: '-12.487358',
        longitude: '-47.504329',
        observacoes: 'Observação 78 - Dados de exemplo'
    },

    // Linha 79
    {
        sequencia: 79,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'Space 185',
        numeroModulo: 45,
        descricaoModulo: 'Módulo 3',
        numeroPoste: 304924,
        tipoPoste: 'DT10/300',
        latitude: '-16.753729',
        longitude: '-48.666771',
        observacoes: 'Observação 79 - Dados de exemplo'
    },

    // Linha 80
    {
        sequencia: 80,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'Space 150',
        numeroModulo: 2,
        descricaoModulo: 'Módulo 25',
        numeroPoste: 507734,
        tipoPoste: 'N2',
        latitude: '-14.656895',
        longitude: '-46.121665',
        observacoes: 'Observação 80 - Dados de exemplo'
    },

    // Linha 81
    {
        sequencia: 81,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'BT120mm',
        numeroModulo: 21,
        descricaoModulo: 'Módulo 23',
        numeroPoste: 451288,
        tipoPoste: 'N1',
        latitude: '-15.409285',
        longitude: '-46.682018',
        observacoes: 'Observação 81 - Dados de exemplo'
    },

    // Linha 82
    {
        sequencia: 82,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'Space 185',
        numeroModulo: 46,
        descricaoModulo: 'Módulo 43',
        numeroPoste: 460017,
        tipoPoste: 'N1',
        latitude: '-15.101200',
        longitude: '-44.961827',
        observacoes: 'Observação 82 - Dados de exemplo'
    },

    // Linha 83
    {
        sequencia: 83,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 150',
        numeroModulo: 71,
        descricaoModulo: 'Módulo 28',
        numeroPoste: 512059,
        tipoPoste: 'N3',
        latitude: '-14.930987',
        longitude: '-46.780653',
        observacoes: 'Observação 83 - Dados de exemplo'
    },

    // Linha 84
    {
        sequencia: 84,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT120mm',
        numeroModulo: 3,
        descricaoModulo: 'Módulo 7',
        numeroPoste: 823476,
        tipoPoste: 'PDT10/300',
        latitude: '-15.319634',
        longitude: '-48.408272',
        observacoes: 'Observação 84 - Dados de exemplo'
    },

    // Linha 85
    {
        sequencia: 85,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'Space 50',
        numeroModulo: 29,
        descricaoModulo: 'Módulo 28',
        numeroPoste: 351350,
        tipoPoste: 'N1',
        latitude: '-16.959303',
        longitude: '-46.475464',
        observacoes: 'Observação 85 - Dados de exemplo'
    },

    // Linha 86
    {
        sequencia: 86,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'BT35mm',
        numeroModulo: 30,
        descricaoModulo: 'Módulo 46',
        numeroPoste: 455245,
        tipoPoste: 'N3',
        latitude: '-14.375063',
        longitude: '-44.048833',
        observacoes: 'Observação 86 - Dados de exemplo'
    },

    // Linha 87
    {
        sequencia: 87,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'Space 50',
        numeroModulo: 9,
        descricaoModulo: 'Módulo 43',
        numeroPoste: 959020,
        tipoPoste: 'N2',
        latitude: '-15.956001',
        longitude: '-45.780377',
        observacoes: 'Observação 87 - Dados de exemplo'
    },

    // Linha 88
    {
        sequencia: 88,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT120mm',
        numeroModulo: 23,
        descricaoModulo: 'Módulo 10',
        numeroPoste: 528538,
        tipoPoste: 'N3',
        latitude: '-15.035976',
        longitude: '-46.726270',
        observacoes: 'Observação 88 - Dados de exemplo'
    },

    // Linha 89
    {
        sequencia: 89,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'BT35mm',
        numeroModulo: 78,
        descricaoModulo: 'Módulo 6',
        numeroPoste: 922295,
        tipoPoste: 'N1',
        latitude: '-16.658939',
        longitude: '-46.529879',
        observacoes: 'Observação 89 - Dados de exemplo'
    },

    // Linha 90
    {
        sequencia: 90,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Monofasico',
        cabo: '1/0CAA',
        numeroModulo: 42,
        descricaoModulo: 'Módulo 23',
        numeroPoste: 914375,
        tipoPoste: 'PDT10/300',
        latitude: '-16.550729',
        longitude: '-46.747251',
        observacoes: 'Observação 90 - Dados de exemplo'
    },

    // Linha 91
    {
        sequencia: 91,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'Space 50',
        numeroModulo: 36,
        descricaoModulo: 'Módulo 6',
        numeroPoste: 865840,
        tipoPoste: 'PDT10/300',
        latitude: '-13.916640',
        longitude: '-47.540962',
        observacoes: 'Observação 91 - Dados de exemplo'
    },

    // Linha 92
    {
        sequencia: 92,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT70mm',
        numeroModulo: 50,
        descricaoModulo: 'Módulo 2',
        numeroPoste: 276884,
        tipoPoste: 'N1',
        latitude: '-14.272032',
        longitude: '-44.556728',
        observacoes: 'Observação 92 - Dados de exemplo'
    },

    // Linha 93
    {
        sequencia: 93,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT35mm',
        numeroModulo: 62,
        descricaoModulo: 'Módulo 14',
        numeroPoste: 667225,
        tipoPoste: 'DT10/300',
        latitude: '-15.756699',
        longitude: '-48.220718',
        observacoes: 'Observação 93 - Dados de exemplo'
    },

    // Linha 94
    {
        sequencia: 94,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '1/0CAA',
        numeroModulo: 31,
        descricaoModulo: 'Módulo 14',
        numeroPoste: 987347,
        tipoPoste: 'DT10/300',
        latitude: '-13.206060',
        longitude: '-45.095459',
        observacoes: 'Observação 94 - Dados de exemplo'
    },

    // Linha 95
    {
        sequencia: 95,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '1/0CAA',
        numeroModulo: 7,
        descricaoModulo: 'Módulo 22',
        numeroPoste: 213835,
        tipoPoste: 'N3',
        latitude: '-15.986724',
        longitude: '-44.806351',
        observacoes: 'Observação 95 - Dados de exemplo'
    },

    // Linha 96
    {
        sequencia: 96,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'Space 50',
        numeroModulo: 80,
        descricaoModulo: 'Módulo 31',
        numeroPoste: 599415,
        tipoPoste: 'PDT10/300',
        latitude: '-14.584893',
        longitude: '-44.900114',
        observacoes: 'Observação 96 - Dados de exemplo'
    },

    // Linha 97
    {
        sequencia: 97,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: '1/0CAA',
        numeroModulo: 40,
        descricaoModulo: 'Módulo 10',
        numeroPoste: 616858,
        tipoPoste: 'DT10/300',
        latitude: '-14.553557',
        longitude: '-47.247112',
        observacoes: 'Observação 97 - Dados de exemplo'
    },

    // Linha 98
    {
        sequencia: 98,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '1/0CAA',
        numeroModulo: 37,
        descricaoModulo: 'Módulo 29',
        numeroPoste: 395745,
        tipoPoste: 'DT10/300',
        latitude: '-14.434959',
        longitude: '-44.207871',
        observacoes: 'Observação 98 - Dados de exemplo'
    },

    // Linha 99
    {
        sequencia: 99,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Monofasico MRT',
        cabo: '1/0CAA',
        numeroModulo: 81,
        descricaoModulo: 'Módulo 4',
        numeroPoste: 103713,
        tipoPoste: 'PDT10/300',
        latitude: '-16.919935',
        longitude: '-48.736906',
        observacoes: 'Observação 99 - Dados de exemplo'
    },

    // Linha 100
    {
        sequencia: 100,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: '4/0CAA',
        numeroModulo: 31,
        descricaoModulo: 'Módulo 24',
        numeroPoste: 536681,
        tipoPoste: 'PDT10/300',
        latitude: '-13.006392',
        longitude: '-46.467140',
        observacoes: 'Observação 100 - Dados de exemplo'
    },

    // Linha 101
    {
        sequencia: 101,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico',
        cabo: '4CAA',
        numeroModulo: 95,
        descricaoModulo: 'Módulo 34',
        numeroPoste: 687840,
        tipoPoste: 'N1',
        latitude: '-13.636895',
        longitude: '-45.220178',
        observacoes: 'Observação 101 - Dados de exemplo'
    },

    // Linha 102
    {
        sequencia: 102,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 185',
        numeroModulo: 48,
        descricaoModulo: 'Módulo 19',
        numeroPoste: 934418,
        tipoPoste: 'PDT10/300',
        latitude: '-13.780856',
        longitude: '-44.746236',
        observacoes: 'Observação 102 - Dados de exemplo'
    },

    // Linha 103
    {
        sequencia: 103,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'Space 50',
        numeroModulo: 49,
        descricaoModulo: 'Módulo 19',
        numeroPoste: 875168,
        tipoPoste: 'N1',
        latitude: '-14.932572',
        longitude: '-47.048692',
        observacoes: 'Observação 103 - Dados de exemplo'
    },

    // Linha 104
    {
        sequencia: 104,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '4/0CAA',
        numeroModulo: 36,
        descricaoModulo: 'Módulo 34',
        numeroPoste: 207819,
        tipoPoste: 'N1',
        latitude: '-16.790227',
        longitude: '-44.665057',
        observacoes: 'Observação 104 - Dados de exemplo'
    },

    // Linha 105
    {
        sequencia: 105,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT35mm',
        numeroModulo: 28,
        descricaoModulo: 'Módulo 10',
        numeroPoste: 652798,
        tipoPoste: 'PDT10/300',
        latitude: '-12.857836',
        longitude: '-45.105135',
        observacoes: 'Observação 105 - Dados de exemplo'
    },

    // Linha 106
    {
        sequencia: 106,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: '4/0CAA',
        numeroModulo: 1,
        descricaoModulo: 'Módulo 31',
        numeroPoste: 411716,
        tipoPoste: 'DT10/300',
        latitude: '-12.237247',
        longitude: '-48.803191',
        observacoes: 'Observação 106 - Dados de exemplo'
    },

    // Linha 107
    {
        sequencia: 107,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Monofasico',
        cabo: '4/0CAA',
        numeroModulo: 38,
        descricaoModulo: 'Módulo 9',
        numeroPoste: 636251,
        tipoPoste: 'N1',
        latitude: '-15.347444',
        longitude: '-44.687990',
        observacoes: 'Observação 107 - Dados de exemplo'
    },

    // Linha 108
    {
        sequencia: 108,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'BT35mm',
        numeroModulo: 55,
        descricaoModulo: 'Módulo 12',
        numeroPoste: 335868,
        tipoPoste: 'N1',
        latitude: '-16.584934',
        longitude: '-45.434580',
        observacoes: 'Observação 108 - Dados de exemplo'
    },

    // Linha 109
    {
        sequencia: 109,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT70mm',
        numeroModulo: 21,
        descricaoModulo: 'Módulo 24',
        numeroPoste: 260928,
        tipoPoste: 'N1',
        latitude: '-12.057885',
        longitude: '-46.661357',
        observacoes: 'Observação 109 - Dados de exemplo'
    },

    // Linha 110
    {
        sequencia: 110,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT35mm',
        numeroModulo: 97,
        descricaoModulo: 'Módulo 28',
        numeroPoste: 844128,
        tipoPoste: 'N1',
        latitude: '-13.164084',
        longitude: '-48.052179',
        observacoes: 'Observação 110 - Dados de exemplo'
    },

    // Linha 111
    {
        sequencia: 111,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: '4/0CAA',
        numeroModulo: 91,
        descricaoModulo: 'Módulo 42',
        numeroPoste: 810358,
        tipoPoste: 'N3',
        latitude: '-15.627741',
        longitude: '-45.722882',
        observacoes: 'Observação 111 - Dados de exemplo'
    },

    // Linha 112
    {
        sequencia: 112,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT70mm',
        numeroModulo: 52,
        descricaoModulo: 'Módulo 49',
        numeroPoste: 988014,
        tipoPoste: 'N2',
        latitude: '-16.481560',
        longitude: '-48.838142',
        observacoes: 'Observação 112 - Dados de exemplo'
    },

    // Linha 113
    {
        sequencia: 113,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'Space 185',
        numeroModulo: 61,
        descricaoModulo: 'Módulo 6',
        numeroPoste: 201424,
        tipoPoste: 'N2',
        latitude: '-12.541942',
        longitude: '-47.707895',
        observacoes: 'Observação 113 - Dados de exemplo'
    },

    // Linha 114
    {
        sequencia: 114,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: '4/0CAA',
        numeroModulo: 32,
        descricaoModulo: 'Módulo 14',
        numeroPoste: 323589,
        tipoPoste: 'N3',
        latitude: '-13.467072',
        longitude: '-45.661419',
        observacoes: 'Observação 114 - Dados de exemplo'
    },

    // Linha 115
    {
        sequencia: 115,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '1/0CAA',
        numeroModulo: 25,
        descricaoModulo: 'Módulo 22',
        numeroPoste: 495345,
        tipoPoste: 'N1',
        latitude: '-16.491918',
        longitude: '-47.549579',
        observacoes: 'Observação 115 - Dados de exemplo'
    },

    // Linha 116
    {
        sequencia: 116,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'Space 50',
        numeroModulo: 92,
        descricaoModulo: 'Módulo 46',
        numeroPoste: 870421,
        tipoPoste: 'N2',
        latitude: '-12.630914',
        longitude: '-45.812782',
        observacoes: 'Observação 116 - Dados de exemplo'
    },

    // Linha 117
    {
        sequencia: 117,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: '1/0CAA',
        numeroModulo: 70,
        descricaoModulo: 'Módulo 25',
        numeroPoste: 452018,
        tipoPoste: 'N3',
        latitude: '-14.491902',
        longitude: '-44.073007',
        observacoes: 'Observação 117 - Dados de exemplo'
    },

    // Linha 118
    {
        sequencia: 118,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'BT120mm',
        numeroModulo: 56,
        descricaoModulo: 'Módulo 40',
        numeroPoste: 254872,
        tipoPoste: 'N2',
        latitude: '-16.829715',
        longitude: '-45.636994',
        observacoes: 'Observação 118 - Dados de exemplo'
    },

    // Linha 119
    {
        sequencia: 119,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: '1/0CAA',
        numeroModulo: 40,
        descricaoModulo: 'Módulo 38',
        numeroPoste: 171940,
        tipoPoste: 'PDT10/300',
        latitude: '-13.597087',
        longitude: '-44.207266',
        observacoes: 'Observação 119 - Dados de exemplo'
    },

    // Linha 120
    {
        sequencia: 120,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'Space 150',
        numeroModulo: 61,
        descricaoModulo: 'Módulo 12',
        numeroPoste: 418337,
        tipoPoste: 'PDT10/300',
        latitude: '-15.787072',
        longitude: '-44.492658',
        observacoes: 'Observação 120 - Dados de exemplo'
    },

    // Linha 121
    {
        sequencia: 121,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT35mm',
        numeroModulo: 60,
        descricaoModulo: 'Módulo 21',
        numeroPoste: 340051,
        tipoPoste: 'N2',
        latitude: '-15.932704',
        longitude: '-46.917899',
        observacoes: 'Observação 121 - Dados de exemplo'
    },

    // Linha 122
    {
        sequencia: 122,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT70mm',
        numeroModulo: 22,
        descricaoModulo: 'Módulo 8',
        numeroPoste: 836215,
        tipoPoste: 'DT10/300',
        latitude: '-15.976061',
        longitude: '-48.480931',
        observacoes: 'Observação 122 - Dados de exemplo'
    },

    // Linha 123
    {
        sequencia: 123,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT35mm',
        numeroModulo: 47,
        descricaoModulo: 'Módulo 25',
        numeroPoste: 364645,
        tipoPoste: 'N2',
        latitude: '-13.692057',
        longitude: '-44.919212',
        observacoes: 'Observação 123 - Dados de exemplo'
    },

    // Linha 124
    {
        sequencia: 124,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '4/0CAA',
        numeroModulo: 9,
        descricaoModulo: 'Módulo 43',
        numeroPoste: 915344,
        tipoPoste: 'DT10/300',
        latitude: '-13.383012',
        longitude: '-48.462198',
        observacoes: 'Observação 124 - Dados de exemplo'
    },

    // Linha 125
    {
        sequencia: 125,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'Space 150',
        numeroModulo: 31,
        descricaoModulo: 'Módulo 42',
        numeroPoste: 992230,
        tipoPoste: 'N3',
        latitude: '-16.311862',
        longitude: '-46.969511',
        observacoes: 'Observação 125 - Dados de exemplo'
    },

    // Linha 126
    {
        sequencia: 126,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico',
        cabo: 'BT120mm',
        numeroModulo: 96,
        descricaoModulo: 'Módulo 12',
        numeroPoste: 638944,
        tipoPoste: 'DT10/300',
        latitude: '-14.407017',
        longitude: '-48.794165',
        observacoes: 'Observação 126 - Dados de exemplo'
    },

    // Linha 127
    {
        sequencia: 127,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT70mm',
        numeroModulo: 36,
        descricaoModulo: 'Módulo 41',
        numeroPoste: 376818,
        tipoPoste: 'N2',
        latitude: '-13.966843',
        longitude: '-46.490681',
        observacoes: 'Observação 127 - Dados de exemplo'
    },

    // Linha 128
    {
        sequencia: 128,
        posteDerivacao: 'Existente',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: '4/0CAA',
        numeroModulo: 40,
        descricaoModulo: 'Módulo 45',
        numeroPoste: 479245,
        tipoPoste: 'DT10/300',
        latitude: '-16.500937',
        longitude: '-47.917121',
        observacoes: 'Observação 128 - Dados de exemplo'
    },

    // Linha 129
    {
        sequencia: 129,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'Space 185',
        numeroModulo: 97,
        descricaoModulo: 'Módulo 20',
        numeroPoste: 789542,
        tipoPoste: 'N1',
        latitude: '-15.484193',
        longitude: '-46.445828',
        observacoes: 'Observação 129 - Dados de exemplo'
    },

    // Linha 130
    {
        sequencia: 130,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 150',
        numeroModulo: 73,
        descricaoModulo: 'Módulo 26',
        numeroPoste: 109871,
        tipoPoste: 'PDT10/300',
        latitude: '-13.917352',
        longitude: '-45.545085',
        observacoes: 'Observação 130 - Dados de exemplo'
    },

    // Linha 131
    {
        sequencia: 131,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Monofasico',
        cabo: '4/0CAA',
        numeroModulo: 34,
        descricaoModulo: 'Módulo 27',
        numeroPoste: 473669,
        tipoPoste: 'DT10/300',
        latitude: '-13.661020',
        longitude: '-46.092258',
        observacoes: 'Observação 131 - Dados de exemplo'
    },

    // Linha 132
    {
        sequencia: 132,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Retirada',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: '4/0CAA',
        numeroModulo: 79,
        descricaoModulo: 'Módulo 42',
        numeroPoste: 138265,
        tipoPoste: 'N3',
        latitude: '-15.389303',
        longitude: '-45.288939',
        observacoes: 'Observação 132 - Dados de exemplo'
    },

    // Linha 133
    {
        sequencia: 133,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Construção MT',
        quantidadeFases: 'Monofasico',
        cabo: 'Space 185',
        numeroModulo: 78,
        descricaoModulo: 'Módulo 21',
        numeroPoste: 315109,
        tipoPoste: 'PDT10/300',
        latitude: '-13.336679',
        longitude: '-48.490501',
        observacoes: 'Observação 133 - Dados de exemplo'
    },

    // Linha 134
    {
        sequencia: 134,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'BT70mm',
        numeroModulo: 78,
        descricaoModulo: 'Módulo 14',
        numeroPoste: 944056,
        tipoPoste: 'N2',
        latitude: '-13.786453',
        longitude: '-46.635196',
        observacoes: 'Observação 134 - Dados de exemplo'
    },

    // Linha 135
    {
        sequencia: 135,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'BT35mm',
        numeroModulo: 49,
        descricaoModulo: 'Módulo 18',
        numeroPoste: 785464,
        tipoPoste: 'N3',
        latitude: '-16.547683',
        longitude: '-48.173870',
        observacoes: 'Observação 135 - Dados de exemplo'
    },

    // Linha 136
    {
        sequencia: 136,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'Space 150',
        numeroModulo: 41,
        descricaoModulo: 'Módulo 5',
        numeroPoste: 883614,
        tipoPoste: 'DT10/300',
        latitude: '-13.821860',
        longitude: '-44.604662',
        observacoes: 'Observação 136 - Dados de exemplo'
    },

    // Linha 137
    {
        sequencia: 137,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'Space 50',
        numeroModulo: 82,
        descricaoModulo: 'Módulo 29',
        numeroPoste: 243242,
        tipoPoste: 'DT10/300',
        latitude: '-15.801342',
        longitude: '-45.308689',
        observacoes: 'Observação 137 - Dados de exemplo'
    },

    // Linha 138
    {
        sequencia: 138,
        posteDerivacao: 'Implantar',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: 'BT70mm',
        numeroModulo: 71,
        descricaoModulo: 'Módulo 22',
        numeroPoste: 313718,
        tipoPoste: 'N2',
        latitude: '-12.900055',
        longitude: '-44.759790',
        observacoes: 'Observação 138 - Dados de exemplo'
    },

    // Linha 139
    {
        sequencia: 139,
        posteDerivacao: 'Implantar',
        estado: 'Maranhão',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT70mm',
        numeroModulo: 66,
        descricaoModulo: 'Módulo 10',
        numeroPoste: 968806,
        tipoPoste: 'N3',
        latitude: '-13.791961',
        longitude: '-48.867459',
        observacoes: 'Observação 139 - Dados de exemplo'
    },

    // Linha 140
    {
        sequencia: 140,
        posteDerivacao: 'Implantar',
        estado: 'Piauí',
        tensao: '34,5kV',
        local: 'Rural',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'BT35mm',
        numeroModulo: 60,
        descricaoModulo: 'Módulo 48',
        numeroPoste: 664053,
        tipoPoste: 'N3',
        latitude: '-16.496864',
        longitude: '-44.932579',
        observacoes: 'Observação 140 - Dados de exemplo'
    },

    // Linha 141
    {
        sequencia: 141,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Trifásico com neutro',
        cabo: '1/0CAA',
        numeroModulo: 64,
        descricaoModulo: 'Módulo 7',
        numeroPoste: 211736,
        tipoPoste: 'PDT10/300',
        latitude: '-15.512379',
        longitude: '-48.531018',
        observacoes: 'Observação 141 - Dados de exemplo'
    },

    // Linha 142
    {
        sequencia: 142,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico',
        cabo: '1/0CAA',
        numeroModulo: 73,
        descricaoModulo: 'Módulo 9',
        numeroPoste: 253419,
        tipoPoste: 'PDT10/300',
        latitude: '-15.448379',
        longitude: '-44.450426',
        observacoes: 'Observação 142 - Dados de exemplo'
    },

    // Linha 143
    {
        sequencia: 143,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '13,8kV',
        local: 'Urbano',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Trifásico sem neutro',
        cabo: 'BT70mm',
        numeroModulo: 62,
        descricaoModulo: 'Módulo 7',
        numeroPoste: 418587,
        tipoPoste: 'N1',
        latitude: '-13.718090',
        longitude: '-45.008136',
        observacoes: 'Observação 143 - Dados de exemplo'
    },

    // Linha 144
    {
        sequencia: 144,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: 'BT',
        local: 'Urbano',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: 'Space 150',
        numeroModulo: 51,
        descricaoModulo: 'Módulo 47',
        numeroPoste: 300926,
        tipoPoste: 'N2',
        latitude: '-15.521658',
        longitude: '-48.663407',
        observacoes: 'Observação 144 - Dados de exemplo'
    },

    // Linha 145
    {
        sequencia: 145,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '23,1kV',
        local: 'Urbano',
        tipoRede: 'Trifaseamento MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'BT120mm',
        numeroModulo: 34,
        descricaoModulo: 'Módulo 4',
        numeroPoste: 451043,
        tipoPoste: 'PDT10/300',
        latitude: '-15.977396',
        longitude: '-44.536866',
        observacoes: 'Observação 145 - Dados de exemplo'
    },

    // Linha 146
    {
        sequencia: 146,
        posteDerivacao: 'Existente',
        estado: 'Pará',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Retirada',
        quantidadeFases: 'Trifásico com neutro',
        cabo: '1/0CAA',
        numeroModulo: 34,
        descricaoModulo: 'Módulo 33',
        numeroPoste: 770532,
        tipoPoste: 'PDT10/300',
        latitude: '-12.017052',
        longitude: '-48.233114',
        observacoes: 'Observação 146 - Dados de exemplo'
    },

    // Linha 147
    {
        sequencia: 147,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: '34,5kV',
        local: 'Urbano',
        tipoRede: 'Melhoria Rede BT',
        quantidadeFases: 'Monofasico',
        cabo: 'BT70mm',
        numeroModulo: 46,
        descricaoModulo: 'Módulo 23',
        numeroPoste: 204217,
        tipoPoste: 'PDT10/300',
        latitude: '-15.162866',
        longitude: '-45.455320',
        observacoes: 'Observação 147 - Dados de exemplo'
    },

    // Linha 148
    {
        sequencia: 148,
        posteDerivacao: 'Existente',
        estado: 'Piauí',
        tensao: '13,8kV',
        local: 'Rural',
        tipoRede: 'Melhoria de Rede MT BT',
        quantidadeFases: 'Bifásico sem neutro',
        cabo: '4/0CAA',
        numeroModulo: 74,
        descricaoModulo: 'Módulo 12',
        numeroPoste: 498765,
        tipoPoste: 'N3',
        latitude: '-12.020525',
        longitude: '-44.200550',
        observacoes: 'Observação 148 - Dados de exemplo'
    },

    // Linha 149
    {
        sequencia: 149,
        posteDerivacao: 'Existente',
        estado: 'Goiás',
        tensao: 'BT',
        local: 'Rural',
        tipoRede: 'Melhoria Rede MT',
        quantidadeFases: 'Monofasico MRT',
        cabo: 'Space 185',
        numeroModulo: 11,
        descricaoModulo: 'Módulo 32',
        numeroPoste: 760147,
        tipoPoste: 'N1',
        latitude: '-12.745479',
        longitude: '-44.445544',
        observacoes: 'Observação 149 - Dados de exemplo'
    },

    // Linha 150
    {
        sequencia: 150,
        posteDerivacao: 'Implantar',
        estado: 'Pará',
        tensao: '23,1kV',
        local: 'Rural',
        tipoRede: 'Construção BT',
        quantidadeFases: 'Bifasico com Neutro',
        cabo: 'Space 150',
        numeroModulo: 37,
        descricaoModulo: 'Módulo 8',
        numeroPoste: 642660,
        tipoPoste: 'N1',
        latitude: '-15.079921',
        longitude: '-48.813048',
        observacoes: 'Observação 150 - Dados de exemplo'
    }
];
