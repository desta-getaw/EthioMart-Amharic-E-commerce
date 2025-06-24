import re
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager


def plot_channel_distribution(df):
    if "channel_address" not in df.columns:
        raise KeyError("Column 'channel_address' not found in DataFrame.")

    channel_counts = df["channel_address"].value_counts()

    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    colors = sns.color_palette("magma", len(channel_counts))

    # Donut chart
    wedges, texts, autotexts = axes[0].pie(
        channel_counts,
        labels=channel_counts.index,
        autopct="%1.1f%%",
        startangle=140,
        colors=colors,
        wedgeprops={"edgecolor": "white"},
    )
    axes[0].add_artist(plt.Circle((0, 0), 0.5, color="white"))
    axes[0].set_title("Distribution of Messages by Channel (Donut Chart)")

    # Horizontal bar chart
    sns.barplot(
        y=channel_counts.index, x=channel_counts.values, palette="magma", ax=axes[1]
    )
    axes[1].set_xlabel("Message Count")
    axes[1].set_ylabel("Channel Address")
    axes[1].set_title("Messages per Channel (Horizontal Bar Graph)")

    for index, value in enumerate(channel_counts.values):
        axes[1].text(value + 5, index, str(value), va="center", fontsize=13)

    plt.tight_layout()
    plt.show()


def plot_gantt_chart(df):
    if "date" not in df.columns:
        raise KeyError("Column 'date' not found in DataFrame.")

    df["date"] = pd.to_datetime(df["date"])

    if "channel_address" not in df.columns:
        raise KeyError("Column 'channel_address' not found in DataFrame.")

    channel_dates = (
        df.groupby("channel_address")["date"].agg(["min", "max"]).reset_index()
    )
    channel_dates.columns = ["channel_address", "start_date", "end_date"]

    fig, ax = plt.subplots(figsize=(14, 7))

    for _, row in channel_dates.iterrows():
        ax.barh(
            row["channel_address"],
            (row["end_date"] - row["start_date"]).days,
            left=row["start_date"],
            height=0.6,
            color="#C4AD9D",
            edgecolor="grey",
        )

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    plt.xticks(rotation=90)
    ax.grid(True, axis="x", linestyle="--", alpha=0.7)

    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Channel Address", fontsize=12)
    plt.title("Message Start and End Dates for Each Channel", fontsize=14)
    plt.tight_layout()
    plt.show()


def generate_hist_box_plots(df, plot_data):
    num_cols = len(plot_data)
    fig, axes = plt.subplots(
        nrows=2,
        ncols=num_cols,
        figsize=(14, 5),
        sharex="col",
        gridspec_kw={"height_ratios": [7, 0.4]},
    )

    for i, item in enumerate(plot_data):
        col = item["column"]
        if col not in df.columns:
            raise KeyError(f"Column '{col}' not found in DataFrame.")

        sns.histplot(df[col], kde=True, ax=axes[0, i])
        sns.boxplot(x=df[col], ax=axes[1, i], orient="h")
        axes[1, i].set_xlabel(item["label"], fontsize=13)
        axes[0, i].set_title(item["title"], fontsize=13)

    axes[0, 0].set_ylabel("Frequency", fontsize=13)
    fig.tight_layout()
    plt.show()


def plot_word_cloud(df, language=None):
    if "cleaned_message" not in df.columns:
        raise KeyError("Column 'cleaned_message' not found in DataFrame.")

    all_text = " ".join(df["cleaned_message"].dropna())

    if language == "amharic":
        text_to_plot = " ".join(re.findall(r"[\u1200-\u137F]+", all_text))
        font_path = "../assets/fonts/NotoSerifEthiopic_Condensed-Regular.ttf"
    elif language == "english":
        text_to_plot = " ".join(re.findall(r"[A-Za-z]+", all_text))
        font_path = None
    else:
        text_to_plot = all_text
        font_path = "../assets/fonts/NotoSerifEthiopic_Condensed-Regular.ttf"

    wordcloud = WordCloud(
        width=800, height=400, background_color="white", font_path=font_path
    ).generate(text_to_plot)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(
        f"Word Cloud for {'All' if language is None else language.capitalize()} Messages"
    )
    plt.show()


def plot_top_tokens(df, top_n=20):
    if "token" not in df.columns:
        raise KeyError("Column 'token' not found in DataFrame.")

    top_tokens = df["token"].value_counts().head(top_n)

    font_path = "../assets/fonts/NotoSerifEthiopic_Condensed-Regular.ttf"
    prop = font_manager.FontProperties(fname=font_path)

    plt.figure(figsize=(8, 4))
    sns.barplot(x=top_tokens.values, y=top_tokens.index, palette="magma")
    plt.xlabel("Frequency", fontproperties=prop)
    plt.ylabel("Token", fontproperties=prop)
    plt.title(f"Top {top_n} Most Frequent Tokens", fontproperties=prop)
    plt.xticks(fontproperties=prop)
    plt.yticks(fontproperties=prop)
    plt.show()


def plot_label_distribution(df):
    if "label" not in df.columns:
        raise KeyError("Column 'label' not found in DataFrame.")

    label_counts = df["label"].value_counts()
    plt.figure(figsize=(8, 4))
    sns.barplot(x=label_counts.index, y=label_counts.values, palette="magma")
    plt.xlabel("Label")
    plt.ylabel("Count")
    plt.title("Label Distribution")
    plt.show()
