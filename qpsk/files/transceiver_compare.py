import sys

def read_bytes(path):
    with open(path, "rb") as f:
        return list(f.read())

def compare_symbol_streams(tx_file, rx_file, bits_per_symbol=2):
    tx = read_bytes(tx_file)
    rx = read_bytes(rx_file)

    n = min(len(tx), len(rx))
    tx = tx[:n]
    rx = rx[:n]

    if n == 0:
        print("No data to compare.")
        return

    # Symbol errors
    sym_errors = sum(1 for a, b in zip(tx, rx) if a != b)
    sym_err_rate = sym_errors / n

    print(f"Compared {n} symbols.")
    print(f"Symbol errors: {sym_errors}")
    print(f"Symbol error rate: {sym_err_rate:.6e}")

    # Approximate bit errors if Gray-coded QPSK (2 bits per symbol)
    if bits_per_symbol is not None:
        # For a rough estimate: 1 wrong symbol ≈ 1 bit error (Gray) or at most 2
        # Here we'll assume 1 bit error per wrong symbol for a conservative *lower bound*.
        bit_errors_min = sym_errors  # best case (one bit flips per wrong symbol)
        bit_errors_max = sym_errors * bits_per_symbol  # worst case (all bits wrong)

        total_bits = n * bits_per_symbol
        ber_min = bit_errors_min / total_bits
        ber_max = bit_errors_max / total_bits

        print(f"Approx bit errors (min, max): {bit_errors_min}, {bit_errors_max}")
        print(f"Approx BER range       : {ber_min:.6e}  to  {ber_max:.6e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compare_streams.py tx_data.bit rx_data.bit")
        sys.exit(1)

    tx_file = sys.argv[1]
    rx_file = sys.argv[2]
    compare_symbol_streams(tx_file, rx_file, bits_per_symbol=2)  # 2 for QPSK
