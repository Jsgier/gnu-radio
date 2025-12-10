import pmt
from gnuradio import gr

class blk(gr.basic_block):
    """
    PDU block that strips the CCSDS ASM (0x1A CF FC 1D) from the END of each PDU.

    Input:  PDU (meta, u8vector) = [payload ... ASM]
    Output: PDU (meta, u8vector) = [payload ...]

    If ASM is not found at the end, the PDU is dropped.
    """

    def __init__(self, verbose=False):
        gr.basic_block.__init__(
            self,
            name="strip_ccsds_asm_pdu_end",
            in_sig=None,
            out_sig=None,
        )

        self._asm = bytes([0x1A, 0xCF, 0xFC, 0x1D])
        self.verbose = verbose

        # Register ports
        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)

        self.message_port_register_out(pmt.intern("out"))

    def handle_msg(self, msg):
        meta = pmt.car(msg)
        data = pmt.cdr(msg)

        if not pmt.is_u8vector(data):
            if self.verbose:
                print("[strip_ccsds_asm_pdu_end] Non-u8vector PDU, dropping.")
            return

        in_bytes = bytes(bytearray(pmt.u8vector_elements(data)))
        length = len(in_bytes)

        if length < 4:
            if self.verbose:
                print(f"[strip_ccsds_asm_pdu_end] PDU too short (len={length}), dropping.")
            return

        # Extract last 4 bytes (expected location of ASM)
        asm_bytes = in_bytes[-4:]

        if asm_bytes != self._asm:
            if self.verbose:
                print(
                    "[strip_ccsds_asm_pdu_end] ASM mismatch, dropping. "
                    f"Got {asm_bytes.hex()}, expected {self._asm.hex()}"
                )
            return

        if self.verbose:
            print(
                "[strip_ccsds_asm_pdu_end] ASM match at END. "
                f"Found {asm_bytes.hex()}"
            )

        # Everything except the last 4 bytes (the ASM)
        out_bytes = in_bytes[:-4]

        # Convert back to u8vector
        out_vec = pmt.init_u8vector(len(out_bytes), list(out_bytes))
        out_pdu = pmt.cons(meta, out_vec)

        # Publish
        self.message_port_pub(pmt.intern("out"), out_pdu)