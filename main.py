# main.py
from simulate_data import simulate_product_data
from social_buzz import simulate_hashtags
from visualize import plot_style_trend, plot_color_distribution
from trend_model import prepare_training_data, train_model

def main():
    # Step 1: Simulate product data
    df = simulate_product_data()

    # Step 2: Simulate hashtag data
    style_time = simulate_hashtags(df)

    # Step 3: Visualizations
    plot_style_trend(style_time)
    plot_color_distribution(df)

    # Step 4: Train model
    trend_df = prepare_training_data(style_time)
    train_model(trend_df)

if __name__ == '__main__':
    main()
