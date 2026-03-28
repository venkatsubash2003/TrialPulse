from data.data_loader import load_data
from engine.pipeline import run_pipeline

def main():
    df = load_data()
    print(df.head())
    print(df.columns)

    output_df = run_pipeline(df)

    print(output_df.head())
    output_df.to_csv("data/demo_output.csv", index=False)
    print(output_df.columns)
    output_df.to_csv("data/demo_output.csv", index=False)

if __name__ == "__main__":
    main()