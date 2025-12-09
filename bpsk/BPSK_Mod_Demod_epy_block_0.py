import pmt
from gnuradio import gr

class blk(gr.basic_block):
    """
    PDU block that prepends the CCSDS ASM (0x1A CF FC 1D) to each PDU payload.
    Input:  PDU (meta, u8vector)
    Output: PDU (same meta, ASM + payload)
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name="prepend_ccsds_asm_pdu",
            in_sig=None,
            out_sig=None,
        )

        # CCSDS ASM: 0x1A CF FC 1D
        self._asm = bytes([0x1A, 0xCF, 0xFC, 0x1D])

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
        # Split into metadata and data
        meta = pmt.car(msg)
        data = pmt.cdr(msg)

        if not pmt.is_u8vector(data):
            # Not what we expect; ignore
            return

        # Convert u8vector to Python bytes
        in_bytes = bytes(bytearray(pmt.u8vector_elements(data)))

        # Prepend ASM
        out_bytes = self._asm + in_bytes

        # Convert back to u8vector
        out_vec = pmt.init_u8vector(len(out_bytes), list(out_bytes))

        # Preserve metadata (you could also modify meta here if needed)
        out_pdu = pmt.cons(meta, out_vec)

        # Publish on output port
        self.message_port_pub(pmt.intern("out"), out_pdu)
