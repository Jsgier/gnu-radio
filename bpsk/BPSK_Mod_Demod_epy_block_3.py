import pmt
from gnuradio import gr

class blk(gr.basic_block):
    """
    PDU block that takes a u8vector of bits (0/1 per element)
    and packs them into bytes (MSB-first).

    Input:  PDU (meta, u8vector) length = 2072 bits
    Output: PDU (meta, u8vector) length = 259 bytes (2072 / 8)
    """

    def __init__(self, verbose=False):
        gr.basic_block.__init__(
            self,
            name="bits_to_bytes_pdu",
            in_sig=None,
            out_sig=None,
        )

        self.verbose = verbose

        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)

        self.message_port_register_out(pmt.intern("out"))

    def handle_msg(self, msg):
        meta = pmt.car(msg)
        data = pmt.cdr(msg)

        if not pmt.is_u8vector(data):
            if self.verbose:
                print("[bits_to_bytes_pdu] Non-u8vector PDU, dropping.")
            return

        bits = list(pmt.u8vector_elements(data))
        n_bits = len(bits)

        if n_bits % 8 != 0:
            if self.verbose:
                print(f"[bits_to_bytes_pdu] Bit length {n_bits} not multiple of 8, dropping.")
            return

        n_bytes = n_bits // 8
        out_bytes = []

        # Pack 8 bits (b0..b7) into one byte: b0 = MSB
        idx = 0
        for _ in range(n_bytes):
            byte_val = 0
            for b in range(8):
                bit = bits[idx]
                # Ensure bit is 0/1
                bit = 1 if bit != 0 else 0
                byte_val = (byte_val << 1) | bit
                idx += 1
            out_bytes.append(byte_val)

        out_vec = pmt.init_u8vector(len(out_bytes), out_bytes)
        out_pdu = pmt.cons(meta, out_vec)
        self.message_port_pub(pmt.intern("out"), out_pdu)