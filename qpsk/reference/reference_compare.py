import sys

def read_bytes(path):
    with open(path, "rb") as f:
        return list(f.read())

def symbol_error_stats(tx, rx, offset):
    """
    Compare tx and rx with a given offset.
    offset > 0  => rx is delayed; compare tx[offset:] with rx[:]
    offset < 0  => tx is delayed; compare tx[:] with rx[-offset:]
    Returns (n_compared, sym_errors).
    """
    if offset >= 0:
        start_tx = offset
        start_rx = 0
    else:
        start_tx = 0
        start_rx = -offset

    # How many symbols can we compare at this offset?
    n = min(len(tx) - start_tx, len(rx) - start_rx)
    if n <= 0:
        return 0, 0

    sym_errors = 0
    for i in range(n):
        if tx[start_tx + i] != rx[start_rx + i]:
            sym_errors += 1

    return n, sym_errors

def find_best_alignment(tx, rx, max_offset=2000):
    """
    Sweep offsets from -max_offset to +max_offset and find the one
    with the fewest symbol errors (and enough samples).
    Returns (best_offset, n_compared, sym_errors).
    """
    best_offset = None
    best_sym_errors = None
    best_n = 0

    for offset in range(-max_offset, max_offset + 1):
        n, sym_err = symbol_error_stats(tx, rx, offset)
        if n == 0:
            continue

        if best_offset is None:
            best_offset = offset
            best_sym_errors = sym_err
            best_n = n
            continue

        # Choose the alignment with the lowest symbol error rate
        # (ties broken by more compared symbols)
        current_ser = sym_err / n
        best_ser = best_sym_errors / best_n if best_n > 0 else 1.0

        if (current_ser < best_ser) or (current_ser == best_ser and n > best_n):
            best_offset = offset
            best_sym_errors = sym_err
            best_n = n

    return best_offset, best_n, best_sym_errors

def compare_streams_with_alignment(tx_file, rx_file, bits_per_symbol=2, max_offset=2000):
    tx = read_bytes(tx_file)
    rx = read_bytes(rx_file)

    if len(tx) == 0 or len(rx) == 0:
        print("One or both files are empty. Nothing to compare.")
        return

    print(f"Loaded {len(tx)} TX symbols and {len(rx)} RX symbols.")
    print(f"Searching offsets from {-max_offset} to {max_offset}...")

    best_offset, n_compared, sym_errors = find_best_alignment(tx, rx, max_offset=max_offset)

    if best_offset is None or n_compared == 0:
        print("Could not find any overlapping region to compare.")
        return

    sym_err_rate = sym_errors / n_compared

    print("\n=== Best Alignment ===")
    print(f"Best offset (RX relative to TX): {best_offset} symbols")
    print(f"Symbols compared            : {n_compared}")
    print(f"Symbol errors               : {sym_errors}")
    print(f"Symbol error rate (SER)     : {sym_err_rate:.6e}")

    if bits_per_symbol is not None and bits_per_symbol > 0:
        # Approximate bit error range (for Gray-coded constellations like QPSK)
        bit_errors_min = sym_errors                  # at least 1 bit wrong per wrong symbol
        bit_errors_max = sym_errors * bits_per_symbol  # at most all bits wrong per symbol

        total_bits = n_compared * bits_per_symbol
        ber_min = bit_errors_min / total_bits
        ber_max = bit_errors_max / total_bits

        print("\nApproximate bit error stats (for Gray-coded QPSK):")
        print(f"Min possible bit errors     : {bit_errors_min}")
        print(f"Max possible bit errors     : {bit_errors_max}")
        print(f"BER range                   : {ber_min:.6e}  to  {ber_max:.6e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compare_streams.py tx_data.bit rx_data.bit [max_offset] [bits_per_symbol]")
        sys.exit(1)

    tx_file = sys.argv[1]
    rx_file = sys.argv[2]

    max_offset = 2000
    bits_per_symbol = 2  # QPSK default

    if len(sys.argv) >= 4:
        max_offset = int(sys.argv[3])
    if len(sys.argv) >= 5:
        bits_per_symbol = int(sys.argv[4])

    compare_streams_with_alignment(tx_file, rx_file, bits_per_symbol=bits_per_symbol, max_offset=max_offset)
