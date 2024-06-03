import matplotlib.pyplot as plt
import pandas as pd


def read_data_from_file(filename):
    data = pd.read_csv(filename, delimiter="|")
    return data


def plot_data(data):
    plt.figure(figsize=(10, 6))

    plt.plot(
        data["l(m)"], data["enc_t"], label="Encryption Time", marker="o", linestyle="-"
    )
    plt.plot(
        data["l(m)"], data["dec_t"], label="Decryption Time", marker="o", linestyle="-"
    )

    plt.xlabel("Message Length l(m)")
    plt.ylabel("Time (ms)")
    plt.title("Encryption and Decryption Times vs Message Length")
    plt.legend()
    plt.grid(True)

    plt.show()


def main():
    # Read the data
    data = read_data_from_file("result_data.txt")

    # Plot the data
    plot_data(data)


if __name__ == "__main__":
    main()
