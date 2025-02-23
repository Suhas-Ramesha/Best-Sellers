# app.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string

# ----------------------------
# Data Loading & Preprocessing
# ----------------------------

@st.cache_data
def load_data():
    # Load the dataset; update the path if needed
    df = pd.read_csv("bestsellers with categories.csv")
    return df

def preprocess_data(df):
    # Rename column for consistency
    df.rename(columns={"User Rating": "User_Rating"}, inplace=True)
    
    # Correct inconsistent author names: change 'J. K. Rowling' to 'J.K. Rowling'
    df.loc[df.Author == 'J. K. Rowling', 'Author'] = 'J.K. Rowling'
    
    # Create a column for the length of the book name (excluding spaces)
    df['name_len'] = df['Name'].apply(lambda x: len(x) - x.count(" "))
    
    # Define function to compute the percentage of punctuation in the book name
    punctuations = string.punctuation
    def count_punc(text):
        count = sum(1 for char in text if char in punctuations)
        return round(count / (len(text) - text.count(" ")) * 100, 3)
    
    df['punc%'] = df['Name'].apply(lambda x: count_punc(x))
    return df

# ----------------------------
# Visualization Functions
# ----------------------------

def plot_genre_distribution(df):
    # Drop duplicate books and count genres
    no_dup = df.drop_duplicates('Name')
    g_count = no_dup['Genre'].value_counts()
    genre_col = ['navy', 'crimson']
    
    # Create a donut pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    
    def make_autopct(values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct * total / 100.0))
            return '{p:.2f}%\n({v:d})'.format(p=pct, v=val)
        return my_autopct

    # Plot pie chart with white circle in the center for donut effect
    wedges, texts, autotexts = ax.pie(
        g_count.values, labels=g_count.index, autopct=make_autopct(g_count.values),
        startangle=90, textprops={'size': 15}, pctdistance=0.5, colors=genre_col
    )
    center_circle = plt.Circle((0, 0), 0.7, color='white')
    ax.add_artist(center_circle)
    ax.set_title('Distribution of Genre for Unique Books (2009-2019)', fontsize=20)
    st.pyplot(fig)

def plot_yearly_genre_distribution(df):
    # Count overall genres (after dropping duplicate books)
    no_dup = df.drop_duplicates('Name')
    g_count = no_dup['Genre'].value_counts()
    genre_col = ['navy', 'crimson']
    
    y1 = np.arange(2009, 2014)
    y2 = np.arange(2014, 2020)
    
    fig, ax = plt.subplots(2, 6, figsize=(12, 6))
    
    # Overall distribution for 2009-2019
    ax[0, 0].pie(
        g_count.values, labels=None, autopct='%1.1f%%',
        startangle=90, textprops={'size': 12, 'color': 'white'},
        pctdistance=0.5, radius=1.3, colors=genre_col
    )
    ax[0, 0].set_title('2009 - 2019\n(Overall)', color='darkgreen', fontdict={'fontsize': 15})
    
    # Distribution for years 2009 to 2013
    for i, year in enumerate(y1):
        counts = df[df['Year'] == year]['Genre'].value_counts()
        ax[0, i + 1].pie(
            counts.values, labels=None, autopct='%1.1f%%',
            startangle=90, textprops={'size': 12, 'color': 'white'},
            pctdistance=0.5, colors=genre_col, radius=1.1
        )
        ax[0, i + 1].set_title(str(year), color='darkred', fontdict={'fontsize': 15})
    
    # Distribution for years 2014 to 2019
    for i, year in enumerate(y2):
        counts = df[df['Year'] == year]['Genre'].value_counts()
        ax[1, i].pie(
            counts.values, labels=None, autopct='%1.1f%%',
            startangle=90, textprops={'size': 12, 'color': 'white'},
            pctdistance=0.5, colors=genre_col, radius=1.1
        )
        ax[1, i].set_title(str(year), color='darkred', fontdict={'fontsize': 15})
    
    fig.legend(g_count.index, loc='center right', fontsize=12)
    st.pyplot(fig)

def plot_top_authors(df):
    # Group data for Non-Fiction and Fiction authors
    try:
        best_nf_authors = df.groupby(['Author', 'Genre']).agg({'Name': 'count'}).unstack()['Name', 'Non Fiction'].sort_values(ascending=False)[:10]
    except Exception as e:
        best_nf_authors = pd.Series([], dtype=int)
    try:
        best_f_authors = df.groupby(['Author', 'Genre']).agg({'Name': 'count'}).unstack()['Name', 'Fiction'].sort_values(ascending=False)[:10]
    except Exception as e:
        best_f_authors = pd.Series([], dtype=int)
        
    genre_col = ['navy', 'crimson']
    
    with plt.style.context('Solarize_Light2'):
        fig, ax = plt.subplots(1, 2, figsize=(10, 8))
        
        # Plot for Non-Fiction authors
        if not best_nf_authors.empty:
            ax[0].barh(y=best_nf_authors.index, width=best_nf_authors.values, color=genre_col[0])
            ax[0].set_xlabel('Number of Appearances')
            ax[0].set_title('Top Non-Fiction Authors')
        else:
            ax[0].text(0.5, 0.5, 'No Non-Fiction data', horizontalalignment='center')
        
        # Plot for Fiction authors
        if not best_f_authors.empty:
            ax[1].barh(y=best_f_authors.index, width=best_f_authors.values, color=genre_col[1])
            ax[1].set_xlabel('Number of Appearances')
            ax[1].set_title('Top Fiction Authors')
        else:
            ax[1].text(0.5, 0.5, 'No Fiction data', horizontalalignment='center')
        
        fig.legend(['Non-Fiction', 'Fiction'], fontsize=12)
        st.pyplot(fig)

def plot_top20_authors(df):
    # Top 20 best selling authors analysis
    n_best = 20
    top_authors = df.Author.value_counts().nlargest(n_best)
    no_dup = df.drop_duplicates('Name')  # remove duplicate books
    color = sns.color_palette("hls", n_best)
    
    fig, ax = plt.subplots(1, 3, figsize=(11, 10), sharey=True)
    
    # Appearances plot
    ax[0].hlines(y=top_authors.index, xmin=0, xmax=top_authors.values, color=color, linestyles='dashed')
    ax[0].plot(top_authors.values, top_authors.index, 'go', markersize=9)
    ax[0].set_xlabel('Number of Appearances')
    ax[0].set_xticks(np.arange(top_authors.values.max()+1))
    ax[0].set_title('Appearances')
    
    # Unique books per author
    book_count = []
    total_reviews = []
    for name in top_authors.index:
        book_count.append(len(no_dup[no_dup.Author == name]['Name']))
        total_reviews.append(no_dup[no_dup.Author == name]['Reviews'].sum() / 1000)
    ax[1].hlines(y=top_authors.index, xmin=0, xmax=book_count, color=color, linestyles='dashed')
    ax[1].plot(book_count, top_authors.index, 'go', markersize=9)
    ax[1].set_xlabel('Number of Unique Books')
    ax[1].set_xticks(np.arange(max(book_count)+1))
    ax[1].set_title('Unique Books')
    
    # Total reviews plot
    ax[2].barh(y=top_authors.index, width=total_reviews, color=color, edgecolor='black', height=0.7)
    for name, val in zip(top_authors.index, total_reviews):
        ax[2].text(val + 2, name, str(val))
    ax[2].set_xlabel("Total Reviews (in 1000's)")
    ax[2].set_title('Total Reviews')
    
    st.pyplot(fig)

# ----------------------------
# Main App Layout
# ----------------------------

def main():
    # Set the title and description
    st.title("Best Selling Books Analysis Dashboard")
    st.markdown("""
    This dashboard analyzes a dataset of best selling books. 
    Use the sidebar to navigate between different visualizations.
    """)
    
    # Load and preprocess data
    df = load_data()
    df = preprocess_data(df)
    
    # Sidebar selection for various analyses
    option = st.sidebar.selectbox(
        "Select Analysis",
        ("Dataset Overview", "Genre Distribution", "Yearly Genre Distribution", "Top Authors (Fiction/Non-Fiction)", "Top 20 Authors Analysis")
    )
    
    if option == "Dataset Overview":
        st.subheader("Dataset Overview")
        st.write(df.head())
        st.write("Dataset shape:", df.shape)
    elif option == "Genre Distribution":
        st.subheader("Genre Distribution for Unique Books (2009-2019)")
        plot_genre_distribution(df)
    elif option == "Yearly Genre Distribution":
        st.subheader("Yearly Genre Distribution")
        plot_yearly_genre_distribution(df)
    elif option == "Top Authors (Fiction/Non-Fiction)":
        st.subheader("Top Authors for Fiction and Non-Fiction")
        plot_top_authors(df)
    elif option == "Top 20 Authors Analysis":
        st.subheader("Top 20 Best Selling Authors Analysis")
        plot_top20_authors(df)

if __name__ == "__main__":
    # Set Seaborn style
    sns.set_style('whitegrid')
    st.write("Seaborn version: " + sns.__version__)
    main()
