import pandas as pd 
import geopandas as gpd



world = gpd.read_file("paises_mundo.geojson")
dic = pd.read_csv(r'Publicacoes\dicionario.csv', sep=';')

dic_data = {
    'África': [
        'Angola', 'Burundi', 'Benin', 'Burkina Faso', 'Cameroon', 'Central African Republic', 
        'Democratic Republic of the Congo', 'Republic of the Congo', 'Ivory Coast', 'Eritrea', 
        'Ethiopia', 'Gabon', 'Ghana', 'Guinea', 'Gambia', 'Guinea Bissau', 'Equatorial Guinea', 
        'Kenya', 'Liberia', 'Libya', 'Madagascar', 'Mali', 'Mauritania', 'Malawi', 'Namibia', 
        'Niger', 'Nigeria', 'Rwanda', 'Senegal', 'Sierra Leone', 'Somalia', 'South Africa', 'Sudan', 
        'South Sudan', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe', 'Botswana', 'Djibouti', 
        'Algeria', 'Egypt', 'Lesotho', 'Morocco', 'Mozambique', 'Western Sahara', 'Somaliland', 'Swaziland',
        'Chad', 'United Republic of Tanzania'
    ],
    'Europa': [
        'Albania', 'Armenia', 'Austria', 'Belgium', 'Bulgaria', 'Bosnia and Herzegovina', 'Belarus', 
        'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 
        'Iceland', 'Ireland', 'Italy', 'Kosovo', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Moldova', 
        'Montenegro', 'Netherlands', 'Norway', 'Poland', 'Portugal', 'Romania', 'Russia', 'Serbia', 'Slovakia', 
        'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Northern Cyprus', 'Cyprus',
        'Croatia', 'Macedonia', 'Republic of Serbia'
    ],
    'Ásia': [
        'Afghanistan', 'United Arab Emirates', 'Armenia', 'Azerbaijan', 'Bangladesh', 'Bhutan', 'Brunei', 
        'Cambodia', 'China', 'Georgia', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Kazakhstan', 
        'Kyrgyzstan', 'Laos', 'Lebanon', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar', 'Nepal', 'North Korea', 
        'Oman', 'Pakistan', 'Philippines', 'Qatar', 'Saudi Arabia', 'South Korea', 'Sri Lanka', 'Syria', 'Taiwan', 
        'Tajikistan', 'Thailand', 'Timor-Leste', 'Turkey', 'Turkmenistan', 'Uzbekistan', 'Vietnam', 
        'Yemen', 'Jordan', 'Kuwait', 'East Timor', 'West Bank'
    ],
    'América do Norte': [
        'Canada', 'United States of America', 'Mexico', 'Greenland','Bermuda', 'The Bahamas', 'Belize'
    ],
    'América do Sul e Central': [
        'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Paraguay', 'Peru',
        'Suriname', 'Uruguay', 'Venezuela', 'French Guiana', 'Guyana','Falkland Islands', 'Cuba',
        'Dominican Republic', 'Guatemala', 'Honduras', 'Jamaica', 'Nicaragua', 'Panama', 'Puerto Rico', 'Trinidad and Tobago', 'Haiti', 'El Salvador', 'Costa Rica'
    ],
    'Oceania': [
        'Australia','Fiji', 'New Zealand', 'Papua New Guinea', 'Solomon Islands', 'Vanuatu', 'New Caledonia'
    ],
    'Antártica': [
        'Antarctica', 'French Southern and Antarctic Lands'
        ]
}

df_africa = pd.DataFrame()
df_africa['País'] = dic_data['África']
df_africa['Região'] = 'África'

df_europa = pd.DataFrame()
df_europa['País'] = dic_data['Europa']
df_europa['Região'] = 'Europa'

df_asia = pd.DataFrame()
df_asia['País'] = dic_data['Ásia']
df_asia['Região'] = 'Ásia'

df_america_do_norte = pd.DataFrame()
df_america_do_norte['País'] = dic_data['América do Norte']
df_america_do_norte['Região'] = 'América do Norte'

df_america_do_sul_e_central = pd.DataFrame()
df_america_do_sul_e_central['País'] = dic_data['América do Sul e Central']
df_america_do_sul_e_central['Região'] = 'América do Sul e Central'

df_oceania = pd.DataFrame()
df_oceania['País'] = dic_data['Oceania']
df_oceania['Região'] = 'Oceania'

df_oceania = pd.DataFrame()
df_oceania['País'] = dic_data['Oceania']
df_oceania['Região'] = 'Oceania'

df_antartica = pd.DataFrame()
df_antartica['País'] = dic_data['Antártica']
df_antartica['Região'] = 'Antártica'


df_regioes = pd.concat([df_africa, df_europa, df_asia, df_america_do_norte, df_america_do_sul_e_central, df_oceania, df_antartica])


def data_countries(world = world, dic=dic, df_regioes=df_regioes):
    world.rename(columns={'name': 'País', 'geometry': 'Geometria', 'id': 'ID'}, inplace=True)
    dic = dic.rename(columns={'name': 'País', 'nome': 'País Traduzido'})




    world = world.merge(df_regioes, how='left', on='País')
    world = world.merge(dic, how='left', on='País')

    return world


# geo = data_countries()

# geo.to_file(r'Contornos\dados_paises.geojson', driver='GeoJSON')  



def data_publications(dic=dic, df_regioes=df_regioes):

    df = pd.read_csv(r'Publicacoes\paises.csv', encoding="ISO-8859-1", sep=';')
    df.rename(columns={'name':'nome'}, inplace=True)
    df['pais_ou_regiao'] = 'País'

    df_1 = pd.read_csv(r'Publicacoes\regioes.csv', encoding="ISO-8859-1", sep=';')
    df_1.rename(columns={'name':'nome'}, inplace=True)
    df_1['pais_ou_regiao'] = 'Região'

    df = pd.concat([df, df_1])

    df = df.merge(dic, how='left', on='nome')
    
    df = df.merge(df_regioes, how='left', left_on='name', right_on='País')
    
    df.loc[df['Região'].isna(), 'Região'] = df.loc[df['Região'].isna(), 'nome']
    return df


# data_publications()