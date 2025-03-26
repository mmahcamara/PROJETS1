import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration de la page
st.set_page_config(page_title="Analyse des données Beans & Pods", page_icon="☕", layout="wide")

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("BeansDataSet.csv")
    return df

# Titre de l'application
st.markdown(
    """
    <div style='text-align:center;'>
    <h1 style='color: #6A5ACD;'> ☕ Analyse des données Beans & Pods </h1>
    <p style='font-size: 18px;'>Bienvenue dans l'application d'analyse des ventes de Beans & Pods. Explorez les données pour découvrir des tendances et des recommandations.</p>
    </div>
    """, unsafe_allow_html=True
)

# Chargement des données
df = load_data()

# Fonction pour afficher un aperçu des données
def show_overview(df):
    st.subheader('Chargement des données :')
    st.dataframe(df)

    st.subheader('Affichage des 5 premières ventes :')
    st.dataframe(df.head())

    # Nombre d'éléments par canal
    st.subheader("Nombre d'éléments par canal :")
    channel_count = df['Channel'].value_counts()
    st.write(channel_count)

    # Répartition des ventes par canal
    st.subheader('Répartition des ventes par canal')
    fig, ax_channel = plt.subplots()
    df['Channel'].value_counts().plot(kind='bar', color=['#4CAF50', '#FF5722'], ax=ax_channel)
    ax_channel.set_xlabel("Canal (Store ou Online)")
    ax_channel.set_ylabel("Nombre de ventes")
    st.pyplot(fig)
    plt.close()

    # Statistiques descriptives
    st.subheader('Statistiques descriptives :')
    st.write(df.describe())

# Fonction pour analyser les ventes
def show_sales_analysis(df):
    st.header("Analyse des ventes")
    
    # Ajouter une colonne pour les ventes totales
    product_columns = ['Robusta', 'Arabica', 'Espresso', 'Lungo', 'Latte', 'Cappuccino']
    df['Total_Sales'] = df[product_columns].sum(axis=1)

    # Filtres interactifs
    st.sidebar.header("Filtres")
    selected_channel = st.sidebar.selectbox("Sélectionnez un canal :", df['Channel'].unique())
    selected_region = st.sidebar.selectbox("Sélectionnez une région :", df['Region'].unique())

    # Filtrer les données
    filtered_data = df[(df['Channel'] == selected_channel) & (df['Region'] == selected_region)]

    # Ventes par canal
    st.subheader("Ventes par canal")
    channel_sales = filtered_data.groupby('Channel')['Total_Sales'].sum().reset_index()
    plt.figure(figsize=(6, 4))
    sns.barplot(x='Channel', y='Total_Sales', data=channel_sales, color='blue')  # Utilisation d'une couleur unique
    plt.title('Ventes totales par canal')
    plt.xlabel('Canal')
    plt.ylabel('Ventes totales')
    st.pyplot(plt)
    plt.close()
    
    # Ventes par région
    st.subheader("Ventes par région")
    region_sales = filtered_data.groupby('Region')['Total_Sales'].sum().reset_index()
    plt.figure(figsize=(6, 4))
    sns.barplot(x='Region', y='Total_Sales', data=region_sales, color='orange')  # Utilisation d'une couleur unique
    plt.title('Ventes totales par région')
    plt.xlabel('Région')
    plt.ylabel('Ventes totales')
    st.pyplot(plt)
    plt.close()
    
    # Ventes par produit
    st.subheader("Ventes par produit")
    product_sales = filtered_data[product_columns].sum().reset_index()
    product_sales.columns = ['Product', 'Sales']
    plt.figure(figsize=(6, 4))
    sns.barplot(x='Product', y='Sales', data=product_sales, color='green')  # Utilisation d'une couleur unique
    plt.title('Ventes totales par produit')
    plt.xlabel('Produit')
    plt.ylabel('Ventes totales')
    st.pyplot(plt)
    plt.close()

    # Histogramme des ventes totales
    st.subheader("Histogramme des ventes totales")
    plt.figure(figsize=(8, 5))
    sns.histplot(filtered_data['Total_Sales'], bins=30, kde=True, color='blue')
    plt.title('Distribution des ventes totales')
    plt.xlabel('Ventes totales')
    plt.ylabel('Fréquence')
    st.pyplot(plt)
    plt.close()

    # Matrice de corrélation
    st.subheader("Matrice de Corrélation")
    plt.figure(figsize=(10, 6))
    sns.heatmap(filtered_data[product_columns].corr(), annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Matrice de Corrélation des Ventes')
    st.pyplot(plt)
    plt.close()

    # Boîte à moustaches
    st.subheader('Boîte à moustaches des ventes par produit')
    plt.figure(figsize=(15, 10))
    sns.boxplot(data=filtered_data[product_columns], palette='Set2')
    plt.title('Boîte à moustaches des ventes par produit')
    st.pyplot(plt)
    plt.close()

    # Graphe de densité
    st.subheader('Graphe de densité des ventes par produit')
    plt.figure(figsize=(15, 10))
    for product in product_columns:
        sns.kdeplot(filtered_data[product], label=product, fill=True)
    plt.title('Graphe de densité des ventes par produit')
    plt.xlabel('Ventes')
    plt.ylabel('Densité')
    plt.legend()
    st.pyplot(plt)
    plt.close()

    # Diagramme de paires
    st.subheader('Diagramme de paires')
    fig = sns.pairplot(filtered_data[product_columns])
    st.pyplot(fig)
    plt.close()

# Fonction pour afficher des recommandations
def show_recommendations():
    st.header("Recommandations pour la campagne marketing")
    
    st.markdown("""
    Basé sur l'analyse des données de ventes de Beans & Pods, voici nos recommandations pour maximiser l'efficacité de la nouvelle campagne marketing:
    
    **1. Cibler les canaux les plus rentables**
    - Concentrer les efforts marketing sur le canal qui génère le plus de revenus.
    
    **2. Optimiser l'offre de produits par région**
    - Adapter les promotions en fonction des préférences régionales observées.
    
    **3. Exploiter les corrélations entre produits**
    - Créer des offres groupées pour les produits fortement corrélés.
    
    **4. Stratégie saisonnière**
    - Développer des promotions spécifiques pour les périodes de faibles ventes.
    
    **5. Améliorer l'expérience client**
    - Améliorer l'expérience d'achat en ligne pour augmenter la conversion.
    """)

# Fonction principale
def main():
    st.markdown("""
    Cette application interactive permet d'explorer et d'analyser les données de ventes de Beans & Pods,
    un fournisseur de grains de café et de gousses. L'objectif est d'identifier des tendances dans les données
    et de formuler des recommandations pour une campagne marketing ciblée afin d'augmenter les revenus.
    """)
    
    # Chargement des données
    df = load_data()
    
    # Menu de navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Choisissez une section :", 
                            ["Aperçu des données", 
                             "Analyse des ventes", 
                             "Recommandations"])
    
    # Afficher la page sélectionnée
    if page == "Aperçu des données":
        show_overview(df)
    elif page == "Analyse des ventes":
        show_sales_analysis(df)
    elif page == "Recommandations":
        show_recommendations()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Développé pour le cours 420-IAA-TT, Hiver 2025")
    st.sidebar.markdown("Par : Mmah Camara ")

if __name__ == "__main__":
    main()