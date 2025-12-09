import pmt
from gnuradio import gr

class blk(gr.basic_block):
    """
    PDU block that strips the CCSDS ASM (0x1A CF FC 1D) from each PDU payload.

    Input:  PDU (meta, u8vector) = [ASM(4) + RS(255)]  => 259 bytes
    Output: PDU (same meta, u8vector) = [RS(255)]      => 255 bytes

    If the ASM does not match or PDU is too short, the PDU is dropped.
    """

    def __init__(self, verbose=False):
        gr.basic_block.__init__(
            self,
            name="strip_ccsds_asm_pdu",
            in_sig=None,
            out_sig=None,
        )

        # CCSDS ASM: 0x1A CF FC 1D
        self._asm = bytes([0x1A, 0xCF, 0xFC, 0x1D])
        self.verbose = verbose

        # Register PDU ports
        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.handle_msg)

        self.message_port_register_out(pmt.intern("out"))

    def handle_msg(self, msg):
        """
        msg is a PDU: (meta, data)
        meta: PMT dictionary (or PMT_NIL)
        data: PMT u8vector
        """
        meta = pmt.car(msg)
        data = pmt.cdr(msg)

        if not pmt.is_u8vector(data):
            if self.verbose:
                print("[strip_ccsds_asm_pdu] Received non-u8vector PDU, dropping.")
            return

        # Convert u8vector to bytes
        in_bytes = bytes(bytearray(pmt.u8vector_elements(data)))
        length = len(in_bytes)

        if length < 4:
            if self.verbose:
                print(f"[strip_ccsds_asm_pdu] PDU too short (len={length}), dropping.")
            return

        # Check ASM
        asm_bytes = in_bytes[:4]
        if asm_bytes != self._asm:
            if self.verbose:
                print(
                    "[strip_ccsds_asm_pdu] ASM mismatch, dropping PDU. "
                    f"Got {asm_bytes.hex()}, expected {self._asm.hex()}"
                )
            return
        else: 
            if self.verbose:
                print(
                    "[strip_ccsds_asm_pdu] ASM match! "
                    f"Got {asm_bytes.hex()}, expected {self._asm.hex()}"
                )
            return

        # Strip ASM, keep remainder (e.g. 255 bytes of RS codeword)
        out_bytes = in_bytes[4:]

        # Convert back to u8vector
        out_vec = pmt.init_u8vector(len(out_bytes), list(out_bytes))

        # Preserve metadata; you could also add a flag here if you want, e.g. asm_ok=True
        out_pdu = pmt.cons(meta, out_vec)

        # Publish on output port
        self.message_port_pub(pmt.intern("out"), out_pdu)
